from django.contrib import admin
from django.urls import path, include
from talent_map_app import views as talent_views

urlpatterns = [
    path('accounts/profile/', talent_views.redirect_to_profile, name='accounts_profile'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('talent_map_app.urls')),
]
