from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from api.views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenObtainPairView
)

router = DefaultRouter()
router.register(r'receive', GetMesages, basename='post')


urlpatterns = [
    # path('', include(router.urls)),
    # path('rooms/create-room', views.createRoom, name='create-room'),
    path('room/<str:room_name>/<str:username>/', views.MessageView, name='room'),
    path('test-room1/<str:room_name>/', views.TestMessageView, name="test-message-view"),
    path('test-room2/', views.TestRoomView.as_view(), name="test-room"),
    path('test-room3/', views.TestRoomView2, name='test-room3'),
    
    path('authenticate/token/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('authenticate/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/register/', views.RegisterView.as_view(), name='auth_register'),
    path('user/signup/', views.create_custom_guest2, name='create-custom-guest2'),
    path('rooms/create-guest2-room/', views.create_guest2_room, name='create-guest2-room'),
    # path('test/', views.testEndPoint, name='test'),
    # path('', views.getRoutes),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair2'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh2'),
    path('guest/login/', views.guest_login, name='guest-login'),
    #path('rooms/create-guest-room/', views.create_guest_room, name='create-guest-room'),

    #Message
    path('messages/get-old-message/<str:room_name>/', views.get_all_message_in_specific_room, name='get-all-message-of-guest-in-specific-room'),

    #Profile
    path('profile/', views.getProfile, name='profile'),
    path('profile/update/', views.updateProfile, name='update-profile'),
    # path('users/<int:pk>/rooms', views.getUserRooms, name='user-room')

    # # Get profile
    # path("profile/<int:pk>/", views.ProfileDetail.as_view()),
    # path("search/<username>/", views.SearchUser.as_view()),

    # Todo URLS
    # path("todo/<user_id>/", views.TodoListView.as_view()),
    # path("todo-detail/<user_id>/<todo_id>/", views.TodoDetailView.as_view()),
    # path("todo-mark-as-completed/<user_id>/<todo_id>/", views.TodoMarkAsCompleted.as_view()),

    # # Chat/Text Messaging Functionality
    # path("my-messages/<user_id>/", views.MyInbox.as_view()),
    # path("get-messages/<sender_id>/<reciever_id>/", views.GetMessages.as_view()),
    # path("send-messages/", views.SendMessages.as_view()),

    

]

urlpatterns = format_suffix_patterns(urlpatterns)
