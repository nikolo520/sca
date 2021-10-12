from apps.companies.models import Company
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

class CompanySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    nit = serializers.CharField(required=True)
    business_name = serializers.CharField(required=True, max_length=100)
    trade_name = serializers.CharField(required=True, max_length=100)
    email = serializers.EmailField(max_length=50)
    phone = serializers.CharField(max_length=10)
    phone_indicator = serializers.CharField(max_length=4, default='57')
    country = serializers.CharField(max_length=100,)
    state = serializers.CharField(max_length=100)
    city = serializers.CharField(max_length=100)
    web_page = serializers.CharField(max_length=100)
    is_active = serializers.BooleanField(default=True)
    
    class Meta:
        model = Company
        fields = (
            'id',
            'nit',
            'business_name',
            'trade_name',
            'email',
            'phone',
            'phone_indicator',
            'country',
            'state',
            'city',
            'web_page',
            'is_active',
        )

    def create(self, validated_data):
        company = Company.objects.create(
            nit = validated_data['nit'],
            business_name = validated_data['business_name'],
            trade_name = validated_data['trade_name'],
            phone = validated_data['phone'],
            phone_indicator = validated_data['phone_indicator'],
            country = validated_data['country'],
            state = validated_data['state'],
            city = validated_data['city'],
            web_page = validated_data['web_page']
        )
        company.save()
        return company