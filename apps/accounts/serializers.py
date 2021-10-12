from django.utils import timezone
from apps.accounts.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
import threading

from apps.companies.models import Company
class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,
                                    max_length=100,
                                    validators=[UniqueValidator(queryset=UserProfile.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    identification = serializers.IntegerField(required=True,validators=[UniqueValidator(queryset=UserProfile.objects.all())])
    username = serializers.CharField(read_only=True,)
    company = serializers.IntegerField()
    class Meta:
        model = UserProfile
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name','identification','company')
        extra_kwargs = {
            'identification': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'company':{'required':True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Contraseñas ingresadas no coinciden"})

        return attrs

    def create(self, validated_data):
        print(validated_data)
        company = Company.objects.get(id=self.initial_data['company'])
        now = timezone.now()
        user = UserProfile.objects.create(
            username=str(validated_data['identification']),
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            identification=validated_data['identification'],
            company=company,
            date_joined=now,
            is_staff=True,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user