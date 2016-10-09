from django.http import HttpResponseRedirect
from django.urls import reverse

import re

class FirstLoginMiddleware:
    def process_request(self, request):
        if request.user.is_authenticated() and \
            not request.user.is_staff and \
            not re.match(r'^/profile/update/?', request.path):

            profile = request.user.employee
            if profile.first_login:
                return HttpResponseRedirect(reverse('update_profile'))
