from rest_framework import serializers
from user.models import User,Membership
from .models import Gym


class OwnerSignupSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']
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
            role="owner"
        )
        return user


class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = ['id','name', 'address', 'description']

class OwnerMemberSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    gym = serializers.CharField(source='gym.name')

    class Meta:
        model = Membership
        fields = ['username', 'email', 'gym', 'start_date', 'end_date', 'is_active']