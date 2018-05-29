from django.http import HttpResponseRedirect
from django.urls import reverse

from user.models import Users


def CheckTicket(func):
    def inner(request):
        ticket = request.COOKIES.get('ticket')
        user = Users.objects.filter(ticket=ticket)
        if user:
            return func(request)
        else:
            return HttpResponseRedirect(reverse('user:login'))
    return inner