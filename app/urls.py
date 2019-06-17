from django.urls import path, include
from django.contrib.auth.views import logout_then_login
from .views import signup, loginview, profile, logoutview
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', loginview, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logoutview, name='logout' )
]