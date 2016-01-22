# -*- coding: UTF-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import Summary, MessisInfo
from django.contrib.auth.decorators import permission_required

urlpatterns = patterns('',
    url(r'^reg_sum/(?P<slug>[a-zA-Z0-9-]+)$', permission_required('is_staff')(Summary.as_view(template_name='hhlregistrations/summary.html')), name='summary'),
    url(r'^reg_sum/$', permission_required('is_staff')(Summary.as_view())),
  
    url(r'^messis_info/$', permission_required('is_staff')(MessisInfo.as_view())),

)
