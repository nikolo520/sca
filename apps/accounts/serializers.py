from apps.accounts.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True,max_length=100)
    password = serializers.CharField(required=True, min_length=6,max_length=20,write_only=True)
    
    # def validate_password(self):
    #     return make_password(self.cleaned_data['password'])
    class Meta:
        model = UserProfile
        fields = ['identification', 'email','password']