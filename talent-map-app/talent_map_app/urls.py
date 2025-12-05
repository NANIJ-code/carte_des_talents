from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Page d'accueil
    path('', views.home, name='home'),
    
    # Authentification
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    
    # Profil
    path('profile/create/', views.profile_create, name='profile_create'),
    path('profile/<int:pk>/', views.profile_detail, name='profile_detail'),
    path('profile/<int:pk>/edit/', views.profile_edit, name='profile_edit'),
    
    # Recherche
    path('search/', views.search_profiles, name='search'),
    path('profile/<int:pk>/map/', views.talent_map, name='talent_map'),
]