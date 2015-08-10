from django.conf.urls import include, url

from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^joker-auth/', include('joker-auth.urls')),
    url(r'^joker-model-1/', include('joker-model-1.urls')),
    url(r'^joker-model-2/', include('joker-model-2.urls'))
]
