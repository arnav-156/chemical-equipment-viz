from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DatasetViewSet, AlertRuleViewSet, AlertHistoryViewSet, login_view, logout_view, register_view

router = DefaultRouter()
router.register(r'datasets', DatasetViewSet)
router.register(r'alert-rules', AlertRuleViewSet)
router.register(r'alert-history', AlertHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/register/', register_view, name='register'),
]
