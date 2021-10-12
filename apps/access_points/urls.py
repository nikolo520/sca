from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from apps.access_points import views

urlpatterns = [
    path('', views.AccessPointListView.as_view(),name='index'),
    #path('/<int:pk>', AccessPointsViewSet.as_view({'get':'retrieve','post':'update','delte':'destroy'}), name="setget_access_points"),
]
