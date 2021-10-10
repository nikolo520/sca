
from apps.access_points.models import AccessPoint
from apps.companies.models import Company
from rest_framework import  viewsets
from rest_framework import permissions
from apps.companies.serializers import CompanySerializer
from rest_framework import generics, status
from rest_framework import  status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer
from apps.accounts.serializers import UserProfileSerializer
from rest_framework import permissions
from rest_framework import generics
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from apps.access_points.serializers import AccessPointsSerializer
from rest_framework.pagination import PageNumberPagination

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

class Login(FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy('api:list_access_points')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,*kwargs)

    def form_valid(self,form):
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)
        if token:
            login(self.request, form.get_user())
            return super(Login,self).form_valid(form)

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
            print(serializer_company.data)
            data['company'] = serializer_company.data['id']
            serializers_user = UserProfileSerializer(data=data)
            if serializers_user.is_valid():
                serializers_user.save()
                return JsonResponse({"status":True,"message":"El registro fue exitoso"}, status=201)
            company = Company.objects.get(id=serializer_company.data['id'])
            company.delete()
            return JsonResponse(serializers_user.errors, status=400)
        return JsonResponse(serializer_company.errors, status=400)
    else:
        return Response([{"error_code":"1","message":"BAD REQUEST"}], status=status.HTTP_400_BAD_REQUEST)