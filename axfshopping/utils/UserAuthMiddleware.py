from datetime import datetime, timedelta

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from user.models import UserTicketModel


class UserAuthMiddle(MiddlewareMixin):

    def process_request(self,request):
        path = request.path

        need_login = ['/axf/mine/', '/axf/cart/', '/axf/generateOrder/','/axf/allSelect/',
                      '/axf/changeOrderStatus/','/axf/waitPay/','/axf/payed/', '/axf/getTotalPrice/']
        can_pass = ['/axf/addcart/', '/axf/subcart/']
        if (path in need_login) or (path in can_pass):

            ticket = request.COOKIES.get('ticket')

            if not ticket:
                if path in can_pass:
                    return None
                return HttpResponseRedirect(reverse('user:login'))
            user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
            if not user_ticket:
                if path in can_pass:
                    return None
                return HttpResponseRedirect(reverse('user:login'))
            out_time = user_ticket.out_time.replace(tzinfo=None)+timedelta(hours=8)
            if datetime.now() > out_time:
                UserTicketModel.objects.filter(user=user_ticket.user).delete()
                if path in can_pass:
                    return None
                return HttpResponseRedirect(reverse('user:login'))
            request.user = user_ticket.user
            UserTicketModel.objects.filter(Q(user=user_ticket.user) & ~Q(ticket=ticket)).delete()