from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('joker_auth.urls')),
    url(r'^model/1/', include('joker_model_1.urls')),
    url(r'^model/2/', include('joker_model_2.urls')),
    url(r'^model/4/', include('joker_model_4.urls')),
    url(r'^tool/', include('joker_tools.urls')),
    url(r'^connector/', include('joker_connector.urls'))
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
