from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from owners.models import Gym
from rest_framework.pagination import PageNumberPagination
from .serializers import CustomerSerializer, MembershipSerializer, PaymentSerializer, PaymentHistorySerializer
from .models import Membership, Payment
from datetime import date, timedelta
from Gym.constants import (
    FIELD_USERNAME, FIELD_PASSWORD, FIELD_GYM_ID,
    MSG_INVALID_CREDENTIALS, MSG_GYM_NOT_FOUND,
    MSG_PAYMENT_NOT_FOUND, MEMBERSHIP_DURATION_DAYS,
    PAYMENT_SUCCESS
)

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


@api_view(['POST'])
def UserSignupView(request):
    if not request.data.get(FIELD_USERNAME) or not request.data.get(FIELD_PASSWORD):
        return Response({"error": f"{FIELD_USERNAME} and {FIELD_PASSWORD} are required"}, status=400)
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "user created successfully"}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def UserLoginView(request):
    if not request.data.get(FIELD_USERNAME) or not request.data.get(FIELD_PASSWORD):
        return Response({"error": f"{FIELD_USERNAME} and {FIELD_PASSWORD} are required"}, status=400)

    username = request.data.get(FIELD_USERNAME)
    password = request.data.get(FIELD_PASSWORD)

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": MSG_INVALID_CREDENTIALS}, status=400)

    refresh = RefreshToken.for_user(user)
    return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def membership_status(request):
    memberships = Membership.objects.filter(user=request.user)
    if not memberships.exists():
        return Response({"message": "No memberships found"}, status=404)

    data = [
        {
            "gym": m.gym.name,
            "start_date": m.start_date,
            "end_date": m.end_date,
            "is_active": m.is_active
        }
        for m in memberships
    ]
    return Response(data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def make_payment(request):
    gym_id = request.data.get(FIELD_GYM_ID)
    if gym_id is None:
        return Response({"error": f"{FIELD_GYM_ID} is required"}, status=400)

    try:
        gym = Gym.objects.get(id=gym_id)
    except Gym.DoesNotExist:
        return Response({"error": MSG_GYM_NOT_FOUND}, status=404)

    serializer = PaymentSerializer(data=request.data)
    if serializer.is_valid():
        amount = serializer.validated_data['amount']

        payment = Payment.objects.create(
            user=request.user,
            gym=gym,
            amount=amount,
            status=PAYMENT_SUCCESS
        )

        duration = MEMBERSHIP_DURATION_DAYS

        try:
            membership = Membership.objects.get(user=request.user, gym=gym)
            membership.end_date += timedelta(days=duration)
            membership.is_active = True
            membership.save()
        except Membership.DoesNotExist:
            membership = Membership.objects.create(
                user=request.user,
                gym=gym,
                start_date=date.today(),
                end_date=date.today() + timedelta(days=duration),
                is_active=True
            )

        return Response({
            "payment_id": payment.id,
            "gym": gym.name,
            "status": payment.status,
            "amount": payment.amount,
            "next_renewal_date": membership.end_date
        })

    return Response(serializer.errors, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by('-date')
    paginator = StandardPagination()
    result = paginator.paginate_queryset(payments, request)
    serializer = PaymentHistorySerializer(result, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_status(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id, user=request.user)
    except Payment.DoesNotExist:
        return Response({"message": MSG_PAYMENT_NOT_FOUND}, status=404)
    serializer = PaymentHistorySerializer(payment)
    return Response(serializer.data)


@api_view(['GET'])
def gym_list(request):
    gyms = Gym.objects.all()
    paginator = StandardPagination()
    result = paginator.paginate_queryset(gyms, request)
    data = [{"id": g.id, "name": g.name, "address": g.address} for g in result]
    return paginator.get_paginated_response(data)
