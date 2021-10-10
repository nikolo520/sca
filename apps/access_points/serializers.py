from django.db import models
from rest_framework import serializers

from apps.access_points.models import AccessPoint


class AccessPointsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True,max_length=150)
    address = serializers.CharField(required=True,max_length=50)
    email = serializers.EmailField(required=True,max_length=50)
    latitude = serializers.DecimalField(decimal_places=4,max_digits=4,required=False)
    longitude = serializers.DecimalField(decimal_places=4,max_digits=4,required=False)
    company = serializers.HyperlinkedRelatedField(many=False,read_only=True,view_name='api:setget_company')
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = AccessPoint
        fields = ('id','name','address','email','company','latitude','longitude','is_active',)
