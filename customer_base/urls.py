from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from core.views import CustomerViewSet, ProfessionViewSet, DataSheetViewSet, DocumentViewSet

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet, basename="customer")
router.register(r'professions', ProfessionViewSet)
router.register(r'data-sheets', DataSheetViewSet)
router.register(r'documents', DocumentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('api/', include(router.urls))
]
