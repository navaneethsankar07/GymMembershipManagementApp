from django.urls import path
from .views import UserSignupView,UserLoginView,membership_status,make_payment,payment_history,payment_status,gym_list

urlpatterns = [
    path('auth/user/signup/',UserSignupView),
    path('auth/user/login/',UserLoginView),
    path('membership/status/',membership_status),
    path('membership/pay/',make_payment),
    path('membership/history/',payment_history),
    path('payment/status/<int:payment_id>/', payment_status),
    path('gyms/', gym_list),


]
