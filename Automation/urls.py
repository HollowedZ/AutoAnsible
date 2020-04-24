from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from .views import PostInventoryGroup, PostInventoryHost

urlpatterns = [
    path('', views.home, name='Ansible-home'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('group/', views.addgroup, name='group-create'),
    path('host/', views.addhost, name='host-create'),
    path('playbook/', views.addPlaybook, name='playbook-create'),
    path('about/', views.about, name='Ansible-about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)