from django.conf.urls import url

import views

urlpatterns = [
    url(r'env/set/$', views.env_set),
    url(r'env/get/$', views.env_get),
    url(r'csv_to_json/$', views.csv_to_json),
    url(r'extract_gzip/$', views.extract_gzip)
]
