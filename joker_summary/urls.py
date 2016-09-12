from django.conf.urls import url

from joker_summary.views import *

urlpatterns = [
    url(r'retrieve-segment-values/$', retrieve_segment_values),
    # url(r'histogram/$', histogram),
    # url(r'update_cache/$', update_cache_by_season),
    url(r'year-on-year-growth/$', year_on_year_growth),
    # url(r'month_on_month_growth/$', month_on_month_growth),
    # url(r'channel_shares/$', channel_shares),
    # url(r'wakeup_rate/$', wakeup_rate),
    # url(r'active_rate/$', active_rate),
    # url(r'active_analysis/$', active_analysis),
    # url(r'growth_in_detail/$', growth_in_detail)
]
