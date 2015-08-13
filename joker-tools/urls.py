from django.conf.urls import url

import views

urlpatterns = [
    url(r'^joker/env/set/$', views.env_set),
    url(r'^joker/env/get/$', views.env_get),
    url(r'^joker/tool/csv_to_json/$', views.csv_to_json),
    url(r'^joker/tool/extract_gzip/$', views.extract_gzip)
]
