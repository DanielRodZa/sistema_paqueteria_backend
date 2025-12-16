from django.urls import path
from .views import UserCreateView, UserListView, UserDetailView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
