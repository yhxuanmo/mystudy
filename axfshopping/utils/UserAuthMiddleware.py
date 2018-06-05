from datetime import datetime, timedelta

from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from user.models import UserTicketModel


class UserAuthMiddle(MiddlewareMixin):

    def process_request(self,request):
        path = request.path

        pass_paths = ['/user/login/', '/user/register/', '/axf/home/']
        if path in pass_paths:
            return None

        ticket = request.COOKIES.get('ticket')

        if not ticket:
            return HttpResponseRedirect(reverse('user:login'))
        user_ticket = UserTicketModel.objects.filter(ticket=ticket).first()
        if not user_ticket:
            return HttpResponseRedirect(reverse('user:login'))
        out_time = user_ticket.out_time.replace(tzinfo=None)+timedelta(hours=8)
        if datetime.now() > out_time:
            UserTicketModel.objects.filter(user=user_ticket.user).delete()
            return HttpResponseRedirect(reverse('user:login'))
        request.user = user_ticket.user
        UserTicketModel.objects.filter(Q(user=user_ticket.user) & ~Q(ticket=ticket)).delete()