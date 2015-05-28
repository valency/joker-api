from django.conf.urls import url, include
from rest_framework import routers

import views

router = routers.DefaultRouter()
router.register(r'customers', views.CustomerViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/cust/id', views.get_cust_by_id),
    url(r'^api/cust/assign_pred', views.assign_pred),
    url(r'^api/cust/assign_pred_from_csv', views.assign_pred_from_csv)
]
