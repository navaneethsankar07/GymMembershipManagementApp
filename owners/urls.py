from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import owner_signup, owner_login, GymViewSet, owner_view_members, owner_payments, owner_payment_status
router = DefaultRouter()
router.register(r'gyms', GymViewSet, basename='gyms')

urlpatterns = [
    path('signup/', owner_signup),
    path('login/', owner_login),
    path('', include(router.urls)),
    path('members/', owner_view_members),
    path('payments/',owner_payments),
    path('payment/status/<int:payment_id>/', owner_payment_status),

]
