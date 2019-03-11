from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions
from django.urls import path, include
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static

from apps.users.urls import router as users_router

admin.site.site_header = 'Listen2ME'
admin.site.site_title = 'Listen2ME'
admin.site.index_title = 'Welcome to Listen2ME Administration!'


class DefaultRouter(routers.DefaultRouter):

    def extend(self, app_router):
        self.registry.extend(app_router.registry)


router = DefaultRouter()
router.extend(users_router)


schema_view = get_schema_view(
    openapi.Info(
        title='Listen2ME API',
        default_version='v1',
        description='listen2me api endpoints',
    ),
    validators=['flex', 'ssv'],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include('apps.users.urls')),
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + (static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) if settings.DEBUG else [])
