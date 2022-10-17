from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from discordAuth import views
from Dashboard.views import panel_manager, panel, logout_Discord_user

from src import settings



urlpatterns = [
    path('admin/', views.logout),
    path('admin/connexion', admin.site.urls),
    path('panel/', panel, name='panel'),
    path('panel/<int:slug>/', panel_manager, name='panel_manager'),
    path('logout', logout_Discord_user, name="logout"),

    #tailwind
    path("__reload__/", include("django_browser_reload.urls")),
    # oauth2
    path('auth/user', views.get_authenticated_user, name='get_authenticated_user'),
    path('oauth2/login/', views.discord_login, name='oauth_login'),
    path('oauth2/login/redirect/', views.discord_login_redirect, name='oauth_login_redirect')
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
