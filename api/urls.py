from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)



urlpatterns = [
    
    path('authenticate/token/login/', views.CustomUserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('authenticate/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('conversations/create-user-conversation/', views.create_user_conversation, name='create-user-conversation'),
    path('user/signup/', views.create_custom_user, name='create-custom-user'),
    #Message
    path('messages/get-old-message/<str:conversation_id>/', views.get_all_message_in_specific_conversation, name='get-all-message-of-user-in-specific-conversation'),
    
    path('convertdata/', ConvertData.as_view(), name='convertdata'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# dùng endpoint khi initialize model