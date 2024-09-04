from django.urls import include, path
from . import views
from rest_framework.routers import DefaultRouter
from api.views import GetMesages, SendMessages
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )

router = DefaultRouter()
router.register(r'receive', GetMesages, basename='post')


urlpatterns = [
    path('', include(router.urls)),
    path('create-room', views.CreateRoom, name='create-room'),
    #path('<str:room_name>/<str:username>/', views.MessageView, name='room'),
    path('test-room1/<str:room_name>/', views.TestMessageView, name="test-message-view"),
    path('test-room2/', views.TestRoomView, name="test-room")
    
    
    # path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('register/', views.RegisterView.as_view(), name='auth_register'),
    # path('test/', views.testEndPoint, name='test'),
    # path('', views.getRoutes),

    # Todo URLS
    # path("todo/<user_id>/", views.TodoListView.as_view()),
    # path("todo-detail/<user_id>/<todo_id>/", views.TodoDetailView.as_view()),
    # path("todo-mark-as-completed/<user_id>/<todo_id>/", views.TodoMarkAsCompleted.as_view()),

    # # Chat/Text Messaging Functionality
    # path("my-messages/<user_id>/", views.MyInbox.as_view()),
    # path("get-messages/<sender_id>/<reciever_id>/", views.GetMessages.as_view()),
    # path("send-messages/", views.SendMessages.as_view()),

    # # Get profile
    # path("profile/<int:pk>/", views.ProfileDetail.as_view()),
    # path("search/<username>/", views.SearchUser.as_view()),

]

