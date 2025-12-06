from rest_framework import serializers
from .models import User, Membership, Payment

class CustomerSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'age']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role="customer",
            age=validated_data.get('age')
        )
        return user


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['start_date', 'end_date', 'is_active']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount']

class PaymentHistorySerializer(serializers.ModelSerializer):
    gym = serializers.CharField(source='gym.name')

    class Meta:
        model = Payment
        fields = ['id', 'gym', 'amount', 'status', 'date']
from rest_framework import serializers
from .models import User, Membership, Payment

class CustomerSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'age']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role="customer",
            age=validated_data.get('age')
        )
        return user


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['start_date', 'end_date', 'is_active']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['amount']

class PaymentHistorySerializer(serializers.ModelSerializer):
    gym = serializers.CharField(source='gym.name')

    class Meta:
        model = Payment
        fields = ['id', 'gym', 'amount', 'status', 'date']
