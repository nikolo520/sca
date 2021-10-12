from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import AccessPointsListCreate,AccessPointsViewSet, signup, CompanyListCreate,CompanyViewSet,UserProfileListCreate

urlpatterns = [
    path('signup/', signup),
    path('access_points/', AccessPointsListCreate.as_view(),name='list_access_points'),
    path('users/', UserProfileListCreate.as_view(),name='list_users'),
    path('access_points/<int:pk>', AccessPointsViewSet.as_view({'get':'retrieve','post':'update','delte':'destroy'}), name="setget_access_points"),
    path('companies/', CompanyListCreate.as_view(),name='list_companies'),
    path('company/<int:pk>', CompanyViewSet.as_view({'get':'retrieve','post':'update','delte':'destroy'}), name="setget_company"),
]

urlpatterns = format_suffix_patterns(urlpatterns)