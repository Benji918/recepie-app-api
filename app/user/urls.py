"""URL mapping for the user API"""

from django.urls import path

from .views import CreateUserView, CreateTokenView, ManagerUserView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('me/', ManagerUserView.as_view(), name='me'),
]
