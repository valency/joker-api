from django.conf.urls import url

import views

urlpatterns = [
    url(r'list-modules/$', views.list_modules),
    url(r'list-profiles/$', views.list_profiles),
    url(r'job-profile/$', views.job_profile),
    url(r'job-profile-push/$', views.job_profile_push),
    url(r'job-profile-remove/$', views.job_profile_remove),
    url(r'job-status/$', views.job_status),
    url(r'job-kill/$', views.job_kill),
    url(r'job-clear/$', views.job_clear),
    url(r'job-set-num-slots/$', views.job_set_num_slots),
    url(r'job-submit/$', views.job_submit),
    url(r'job-remove/$', views.job_remove),
    url(r'job-top/$', views.job_top),
    url(r'job-reset/$', views.job_reset)
]
