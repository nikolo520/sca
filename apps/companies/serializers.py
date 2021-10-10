from enum import unique

from django.db.models.fields import AutoField
from rest_framework.fields import ReadOnlyField
from apps.companies.models import Company
from rest_framework import serializers

class CompanySerializer(serializers.Serializer):

    id = serializers.IntegerField(read_only=True)
    nit = serializers.IntegerField(required=True)
    business_name = serializers.CharField(required=True, max_length=100)
    trade_name = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(max_length=50)
    email_is_valid = serializers.BooleanField(default=False,read_only=True)
    phone = serializers.CharField(max_length=10)
    phone_indicator = serializers.CharField(max_length=4, default='57')
    country = serializers.CharField(max_length=100,)
    state = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    web_page = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField(default=True)
    
    class Meta:
        model = Company
        fields = ('id', 
                    'business_name',
                    'is_active',
                    'email',
                    'email_is_valid',
                    'phone',
                    'phone_indicator',
                    'country',
                    'state',
                    'city',
                    )