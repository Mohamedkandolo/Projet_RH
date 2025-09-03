from django.urls import path
from . import views

app_name = 'users'


urlpatterns = [
    # URLs d'authentification
    
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # URLs de gestion des mots de passe
    path('password/change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/reset/', views.password_reset_request_view, name='password_reset_request'),
    path('password/reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # URLs de gestion des utilisateurs
    path('profile/', views.profile_view, name='profile'),
    path('list/', views.user_list_view, name='user_list'),
    path('create/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:user_id>/', views.user_detail_view, name='user_detail'),
    path('<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('prof/<int:id_user>/', views.profil, name='prof'),
    
    # URLs de configuration d'entreprise (nouvelles vues)
] 