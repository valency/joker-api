from django.conf.urls import url

import views

urlpatterns = [
    url(r'list-modules/$', views.list_modules),
    url(r'list-profiles/$', views.list_profiles),
    url(r'job-profile/$', views.job_profile)
]
