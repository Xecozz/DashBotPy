from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from discordAuth import views
from Dashboard.views import accueil, panel, logout_Discord_user, manage_members, logs, index

from src import settings



urlpatterns = [
    path('admin/', views.logout),
    path('admin/connexion', admin.site.urls),

    path('', index, name='index'),
    path('panel/', panel, name='panel'),

    path('panel_manager/<int:slug>/', accueil, name='panel_manager_accueil'),
    path('panel_manager/manage_members/<int:slug>/', manage_members, name='panel_manager_manage_members'),
    path('panel_manager/logs/<int:slug>/', logs, name='panel_manager_logs'),

    path('logout', logout_Discord_user, name="logout"),

    #tailwind
    path("__reload__/", include("django_browser_reload.urls")),
    # oauth2
    path('auth/user', views.get_authenticated_user, name='get_authenticated_user'),
    path('oauth2/login/', views.discord_login, name='oauth_login'),
    path('oauth2/login/redirect/', views.discord_login_redirect, name='oauth_login_redirect')
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
