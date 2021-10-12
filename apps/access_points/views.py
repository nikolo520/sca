from django.shortcuts import render
from django.views import generic
from apps.access_points.models import AccessPoint
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseNotAllowed
class AccessPointListView(LoginRequiredMixin,generic.ListView):
    def get(self, request, *args, **kwargs):
        if request.user:
            if request.user.id:
                self.model = AccessPoint
                self.queryset = AccessPoint.objects.filter(company=request.user.company)
                self.redirect_field_name = 'redirect_to'
                return super().get(self, request, *args, **kwargs)
        return HttpResponseNotAllowed()