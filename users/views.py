from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from .forms import (
    CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm,
    UserProfileForm, LoginForm, PasswordResetRequestForm, CustomSetPasswordForm,
)
from .models import Customer
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone


User = get_user_model()

def login_view(request):
    """Vue de connexion personnalisée"""
    if request.user.is_authenticated:
        return redirect('hr_payroll:home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(0)
                messages.success(request, _('Connexion réussie !'))
                return redirect('hr_payroll:home')
            else:
                messages.error(request, _('Nom d\'utilisateur ou mot de passe incorrect.'))
    else:
        form = LoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.info(request, _('Vous avez été déconnecté.'))
    return redirect('users:login')



@login_required
def profile_view(request):
    """Vue du profil utilisateur"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profil mis à jour avec succès !'))
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
        'user': request.user,
    }
    return render(request, 'users/profile.html', context)

class CustomPasswordChangeView(PasswordChangeView):
    """Vue de changement de mot de passe personnalisée"""
    template_name = 'users/password_change.html'
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('users:profile')
    
    def form_valid(self, form):
        messages.success(self.request, _('Mot de passe modifié avec succès !'))
        return super().form_valid(form)

@login_required
def user_list_view(request):
    """Vue de liste des utilisateurs (admin seulement)"""
    if not request.user.is_admin:
        messages.error(request, _('Accès non autorisé.'))
        return redirect('hr_payroll:tableau_bord')
    
    users = Customer.objects.all().order_by('username')
    context = {
        'users': users,
    }
    return render(request, 'users/user_list.html', context)

@login_required
def user_detail_view(request, user_id):
    """Vue de détail d'un utilisateur (admin seulement)"""
    if not request.user.is_admin:
        messages.error(request, _('Accès non autorisé.'))
        return redirect('hr_payroll:tableau_bord')
    
    user = get_object_or_404(Customer, id=user_id)
    context = {
        'user_detail': user,
    }
    return render(request, 'users/user_detail.html', context)

class UserCreateView(LoginRequiredMixin, CreateView):
    """Vue de création d'utilisateur (admin seulement)"""
    model = Customer
    form_class = CustomUserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, _('Accès non autorisé.'))
            return redirect('hr_payroll:tableau_bord')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, _('Utilisateur créé avec succès !'))
        return super().form_valid(form)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    """Vue de modification d'utilisateur (admin seulement)"""
    model = Customer
    form_class = CustomUserChangeForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, _('Accès non autorisé.'))
            return redirect('hr_payroll:tableau_bord')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        messages.success(self.request, _('Utilisateur modifié avec succès !'))
        return super().form_valid(form)

def password_reset_request_view(request):
    """Vue de demande de réinitialisation de mot de passe améliorée"""
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = Customer.objects.get(email=email, is_active=True)
                
                # Vérifier que l'utilisateur a un mot de passe utilisable
                if not user.has_usable_password():
                    messages.error(request, _('Ce compte utilise une méthode d\'authentification externe. Contactez votre administrateur.'))
                    return render(request, 'users/password_reset_request.html', {'form': form})
                
                # Générer le token et l'URL de réinitialisation
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                
                # Construire l'URL de réinitialisation
                reset_url = request.build_absolute_uri(
                    reverse_lazy('users:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
                )
                
                # Envoyer l'email
                if settings.DEBUG:
                    # En développement, afficher l'URL dans la console
                    print(f"\n{'='*60}")
                    print(f"URL de réinitialisation pour {email}:")
                    print(f"{reset_url}")
                    print(f"{'='*60}\n")
                    messages.info(request, f'URL de réinitialisation (développement): {reset_url}')
                else:
                    # En production, envoyer l'email
                    try:
                        subject = _('Réinitialisation de votre mot de passe - Système d\'Archivage')
                        html_message = render_to_string('users/password_reset_email.html', {
                            'user': user,
                            'reset_url': reset_url,
                        })
                        plain_message = f"""
                        Bonjour {user.get_full_name() or user.username},
                        
                        Vous recevez cet email car vous avez demandé la réinitialisation du mot de passe de votre compte sur le Système d'Archivage.
                        
                        Pour réinitialiser votre mot de passe, veuillez cliquer sur le lien suivant :
                        {reset_url}
                        
                        Ce lien expirera dans 24 heures.
                        
                        Si vous n'avez pas demandé cette réinitialisation, vous pouvez ignorer cet email en toute sécurité.
                        
                        Cordialement,
                        L'équipe du Système d'Archivage
                        """
                        
                        send_mail(
                            subject=subject,
                            message=plain_message,
                            from_email=settings.DEFAULT_FROM_EMAIL,
                            recipient_list=[email],
                            html_message=html_message,
                            fail_silently=False,
                        )
                        
                        messages.success(request, _('Un email de réinitialisation a été envoyé à votre adresse. Vérifiez votre boîte de réception et votre dossier spam.'))
                        
                    except Exception as e:
                        messages.error(request, _('Erreur lors de l\'envoi de l\'email. Veuillez réessayer ou contactez votre administrateur.'))
                        if settings.DEBUG:
                            print(f"Erreur d'envoi d'email: {e}")
                        return render(request, 'users/password_reset_request.html', {'form': form})
                
                return redirect('users:password_reset_done')
                
            except Customer.DoesNotExist:
                # Pour des raisons de sécurité, ne pas révéler si l'email existe ou non
                messages.success(request, _('Si cette adresse email existe dans notre système, vous recevrez un email de réinitialisation.'))
                return redirect('users:password_reset_done')
            except Exception as e:
                messages.error(request, _('Une erreur inattendue s\'est produite. Veuillez réessayer.'))
                if settings.DEBUG:
                    print(f"Erreur inattendue: {e}")
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'users/password_reset_request.html', {'form': form})

class CustomPasswordResetView(PasswordResetView):
    """Vue de réinitialisation de mot de passe personnalisée"""
    template_name = 'users/password_reset_request.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('users:password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    """Vue de confirmation d'envoi d'email de réinitialisation"""
    template_name = 'users/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    """Vue de confirmation de réinitialisation de mot de passe"""
    template_name = 'users/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('users:password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    """Vue de confirmation de réinitialisation terminée"""
    template_name = 'users/password_reset_complete.html'

def profil(request, id_user):
    """Vue de profil utilisateur spécifique"""
    user_detail = get_object_or_404(Customer, id=id_user)
    
    # Vérifier les permissions
    if request.user != user_detail and not request.user.is_admin:
        messages.error(request, _('Accès non autorisé.'))
        return redirect('hr_payroll:tableau_bord')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_detail)
        if form.is_valid():
            form.save()
            messages.success(request, _('Profil mis à jour avec succès !'))
            return redirect('users:prof', id_user=id_user)
    else:
        form = UserProfileForm(instance=user_detail)
    
    context = {
        'form': form,
        'user_detail': user_detail,
    }
    return render(request, 'users/profile_user.html', context)

def is_admin(user):
    """Vérifie si l'utilisateur est administrateur"""
    return user.is_authenticated and user.role == 'admin'

def is_manager(user):
    """Vérifie si l'utilisateur est gestionnaire ou admin"""
    return user.is_authenticated and user.role in ['admin', 'manager']
