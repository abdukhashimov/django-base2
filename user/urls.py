from django.urls import path
from user.views import CreateUserView, ManageUserView
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token
app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('me/', ManageUserView.as_view(), name='me'),
    path('auth-token/', obtain_jwt_token, name='auth_token'),
    path('auth-token-verify/', verify_jwt_token, name='auth_token_verify')
]
