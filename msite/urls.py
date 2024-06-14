from django.urls import path, re_path
from msite import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from CustomizedOpenAPISchemaGenerator import CustomizedOpenAPISchemaGenerator

schema_view = get_schema_view(
    openapi.Info(
      title="My API",
      default_version='v1',
      description="Test description",
      license=openapi.License(name="MIT License"),
    ),
   public=True,
   permission_classes=(permissions.AllowAny,),
   generator_class=CustomizedOpenAPISchemaGenerator
)

urlpatterns = [


    path('api/Dailybind', views.DailybindView.as_view()),
    path('api/Cardtyperef', views.CardtyperefView.as_view()),
    path('api/RegisterCard', views.RegisterCardView.as_view()),
    path('api/RegisterCard/batch', views.RegisterCardBatchView.as_view()),
    path('api/RutenCompare', views.RutenCompare.as_view()),

]

urlpatterns += [
   re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]