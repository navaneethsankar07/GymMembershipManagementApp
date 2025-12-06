from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import OwnerSignupSerializer, GymSerializer, OwnerMemberSerializer
from .models import Gym
from user.models import Membership, Payment
from user.serializers import PaymentHistorySerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from Gym.constants import (
    ROLE_OWNER, FIELD_USERNAME, FIELD_PASSWORD, FIELD_GYM_ID,
    MSG_INVALID_CREDENTIALS, MSG_ONLY_OWNER, MSG_ONLY_OWNER_PAYMENTS,
    MSG_NO_GYMS, MSG_NO_GYMS_ADDED, MSG_PAYMENT_NOT_FOUND,
)

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['POST'])
def owner_signup(request):
    if not request.data.get(FIELD_USERNAME) or not request.data.get(FIELD_PASSWORD):
        return Response({"error": f"{FIELD_USERNAME} and {FIELD_PASSWORD} are required"}, status=400)
    serializer = OwnerSignupSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Owner registered successfully"}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def owner_login(request):
    if not request.data.get(FIELD_USERNAME) or not request.data.get(FIELD_PASSWORD):
        return Response({"error": f"{FIELD_USERNAME} and {FIELD_PASSWORD} are required"}, status=400)

    username = request.data.get(FIELD_USERNAME)
    password = request.data.get(FIELD_PASSWORD)

    user = authenticate(username=username, password=password)

    if user is None or user.role != ROLE_OWNER:
        return Response({"error": MSG_INVALID_CREDENTIALS}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({"message": "Login successful", "refresh": str(refresh), "access": str(refresh.access_token)})


class GymViewSet(ModelViewSet):
    serializer_class = GymSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Gym.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def owner_view_members(request):
    if request.user.role != ROLE_OWNER:
        return Response({"error": MSG_ONLY_OWNER}, status=403)

    gyms = Gym.objects.filter(owner=request.user)
    if not gyms.exists():
        return Response({"error": MSG_NO_GYMS}, status=404)

    memberships = Membership.objects.filter(gym__in=gyms)

    paginator = StandardPagination()
    result = paginator.paginate_queryset(memberships, request)
    serializer = OwnerMemberSerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def owner_payments(request):
    if request.user.role != ROLE_OWNER:
        return Response({"error": MSG_ONLY_OWNER_PAYMENTS}, status=403)

    gyms = request.user.gyms.all()
    if not gyms.exists():
        return Response({"error": MSG_NO_GYMS_ADDED}, status=404)

    payments = Payment.objects.filter(gym__in=gyms).order_by('-date')

    paginator = StandardPagination()
    result = paginator.paginate_queryset(payments, request)
    serializer = PaymentHistorySerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def owner_payment_status(request, payment_id):
    if request.user.role != ROLE_OWNER:
        return Response({"error": MSG_ONLY_OWNER_PAYMENTS}, status=403)

    if payment_id is None:
        return Response({"error": "payment_id is required"}, status=400)

    gyms = request.user.gyms.all()
    if not gyms.exists():
        return Response({"error": MSG_NO_GYMS_ADDED}, status=404)

    try:
        payment = Payment.objects.get(id=payment_id, gym__in=gyms)
    except Payment.DoesNotExist:
        return Response({"message": MSG_PAYMENT_NOT_FOUND}, status=404)

    serializer = PaymentHistorySerializer(payment)
    return Response(serializer.data)
