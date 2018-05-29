from django.utils.deprecation import MiddlewareMixin

from user.models import Users

from django.http import HttpResponseRedirect

from django.urls import reverse


class UserAuthMiddle(MiddlewareMixin):

    def process_request(self,request):

        path = request.path
        s = ['/user/login/','/user/register/']  # 过滤的url
        if path in s :
            return None

        # 验证cookies中的ticket
        # 验证不通过  返回登录
        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return HttpResponseRedirect(reverse('user:login'))

        user = Users.objects.filter(ticket=ticket)
        if not user:
            return HttpResponseRedirect(reverse('user:login'))

        request.user = user