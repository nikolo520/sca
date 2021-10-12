
from apps.access_points.models import AccessPoint
from apps.accounts.models import UserProfile
from apps.companies.models import Company
from rest_framework import  viewsets
from rest_framework import permissions
from apps.companies.serializers import CompanySerializer
from rest_framework import generics, status
from rest_framework import  status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer
from apps.accounts.serializers import UserProfileSerializer
from rest_framework import permissions
from rest_framework import generics
from django.contrib.auth import logout, tokens
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from apps.access_points.serializers import AccessPointsSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken import views
class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    authentication_class = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class CompanyListCreate(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        company_current_user = request.user.company
        self.pagination_class = StandardResultsPagination
        self.queryset = Company.objects.all()
        self.serializer_class = CompanySerializer
        self.permission_classes = (IsAuthenticated,)
        self.authentication_class = (TokenAuthentication,)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.serializer_class = CompanySerializer
        self.permission_classes = (IsAuthenticated,)
        self.authentication_class = (TokenAuthentication,)
        company_current_user = request.user.company
        request.cleaned_data['company'] = company_current_user.id
        return super().post(request, *args, **kwargs)

class StandardResultsPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 9000


class AccessPointsViewSet(viewsets.ModelViewSet):
    queryset = AccessPoint.objects.all()
    serializer_class = AccessPointsSerializer
    authentication_class = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

class AccessPointsListCreate(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        company_current_user = request.user.company
        self.pagination_class = StandardResultsPagination
        self.queryset = AccessPoint.objects.filter(company = company_current_user)
        self.serializer_class = AccessPointsSerializer
        self.permission_classes = (IsAuthenticated,)
        self.authentication_class = (TokenAuthentication,)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        company_current_user = request.user.company
        self.serializer_class = AccessPointsSerializer
        self.permission_classes = (IsAuthenticated,)
        self.authentication_class = (TokenAuthentication,)
        kwargs['company'] = company_current_user.id
        return super().post(request, *args, **kwargs)
class Logout(APIView):
    def get(self,request, format = None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status = status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def get_access_points(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = AccessPointsSerializer(data=data)



@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer_company = CompanySerializer(data=data)
        if serializer_company.is_valid():
            serializer_company.save()
            data['company'] = serializer_company.data['id']
            serializers_user = UserProfileSerializer(data=data)
            if serializers_user.is_valid():
                serializers_user.save()
                return JsonResponse({"status":True,"message":"El registro fue exitoso"}, status=status.HTTP_201_CREATED)
            return JsonResponse(serializers_user.errors, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse(serializer_company.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response({"status":False,"message":"Bad request"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def validate_email(request):
    token=request.GET.get('token',False)
    id=request.GET.get('ut',False)
    if token and id:
        token_generator = tokens.PasswordResetTokenGenerator()
        user_check = UserProfile.objects.get(id=id)
        is_valid = token_generator.check_token(user=user_check,token=token)
        if is_valid:
            user_check.email_is_valid = True
            user_check.save()
            JsonResponse({"status":True, "message":"Se activo el usuario exitosamente"}, status=status.HTTP_200_OK)
        return JsonResponse({"status":False, "message":"Error al intentar activar el usuario"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response([{"error_code":"1","message":"BAD REQUEST"}], status=status.HTTP_400_BAD_REQUEST)

class obtain_auth_token(views.ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        data = JSONParser().parse(request.data)
        username = data['username']
        if username:
            user = UserProfile.objects.filter(username=username,email_is_valid=True)
            if user:
                print("paso")
                return super().post(request, *args, **kwargs)
            else:
                return JsonResponse({"status":False, "message":"El usuario ha activado su cuenta, por favor valide su correo electrónico."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response([{"error_code":"1","message":"BAD REQUEST"}], status=status.HTTP_400_BAD_REQUEST)



class UserProfileListCreate(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous():
            if request.user.is_staff:
                company_current_user = request.user.company
                self.pagination_class = StandardResultsPagination
                self.queryset = UserProfile.objects.filter(company = company_current_user)
                self.serializer_class = UserProfileSerializer
                self.permission_classes = (IsAuthenticated,)
                self.authentication_class = (TokenAuthentication,)
                return super().get(request, *args, **kwargs)
            else:
                return Response([{"error_code":"1","message":"No tiene permisos"}], status=status.HTTP_403_FORBIDDEN)
        else:
            return Response([{"error_code":"1","message":"No tiene permisos"}], status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        if not request.user.is_anonymous():
            company_current_user = request.user.company
            self.serializer_class = UserProfileSerializer
            self.permission_classes = (IsAuthenticated,)
            self.authentication_class = (TokenAuthentication,)
            kwargs['company'] = company_current_user.id
            return super().post(request, *args, **kwargs)
        else:
            return Response([{"error_code":"1","message":"No tiene permisos"}], status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
@authentication_classes((TokenAuthentication,))
def invite(request):
    if request.method == 'GET':
        email=request.GET.get('email',False)
        id=request.GET.get('ic',False)
    else:
        return Response([{"error_code":"1","message":"BAD REQUEST"}], status=status.HTTP_400_BAD_REQUEST)