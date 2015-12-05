from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^joker/auth/', include('joker_auth.urls')),
    url(r'^joker/model/1/', include('joker_model_1.urls')),
    url(r'^joker/model/2/', include('joker_model_2.urls')),
    url(r'^joker/model/4/', include('joker_model_4.urls')),
    url(r'^joker/tool/', include('joker_tools.urls')),
    url(r'^joker/connector/', include('joker_connector.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
