from django.urls import URLPattern, path, include
from  . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<str:pk>', views.room, name="room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.updateRoom, name='update-room'),
    path('login/', views.LoginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
]
"""важно чтобы называлось urlpatterns list[URLPattern]
name = url name"""