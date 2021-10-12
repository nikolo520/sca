from django.contrib import admin
from django.urls import path,include
from api.views import validate_email,obtain_auth_token
from apps.accounts import views
from apps.access_points.views import AccessPointListView
from apps.accounts.views import Login
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/1.0/',include(('api.urls','api'))),
    path('api_generate_token/', obtain_auth_token.as_view()),
    path('validate_email', validate_email),
    path('', include('django.contrib.auth.urls')),
    path('login/', Login.as_view(), name = 'login'),
    #path('logout/', Logout.as_view(), name = 'logout'),
    path('', AccessPointListView.as_view(),name='list_access_points'),
    path('access_points/',include(('apps.access_points.urls','access_points'))),
    #path('accounts/',include(('apps.accounts.urls','accounts'))),
    #path('companies/',include(('apps.companies.urls','companies'))),
]