from django.urls import path
from .views import RecepcionistaCreateView, UserListView, UserDetailView

urlpatterns = [
    path('add-recepcionista/', RecepcionistaCreateView.as_view(), name='add-recepcionista'),
    path('', UserListView.as_view(), name='user-list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]


