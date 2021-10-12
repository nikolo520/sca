from django.contrib import admin
from django.urls import path,include
from api.views import Login,Logout,validate_email,obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/1.0/',include(('api.urls','api'))),
    path('api_generate_token/', obtain_auth_token.as_view()),
    path('validate_email', validate_email),
    path('login/',Login.as_view(), name = 'login'),
    path('logout/', Logout.as_view()),
]