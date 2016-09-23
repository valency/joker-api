from django.conf.urls import url

from joker_summary.views import *

urlpatterns = [
    url(r'retrieve-segment-values/$', retrieve_segment_values),
    url(r'year-on-year-growth/$', year_on_year_growth),
    url(r'month-on-month-growth/$', month_on_month_growth),
    url(r'channel-shares/$', channel_shares),
    url(r'wakeup-rate/$', wakeup_rate),
    url(r'active-rate/$', active_rate),
    url(r'active-rate-new/$', active_rate_new_cust),
    url(r'active-analysis/$', active_analysis),
    url(r'growth-in-detail/$', growth_in_detail)
]
