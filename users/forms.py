from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    """Formulaire de création d'utilisateur personnalisé"""
    email = forms.EmailField(required=True, help_text=_('Requis. Entrez une adresse email valide.'))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'telephone', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        # Personnaliser les messages d'erreur de validation de mot de passe
        self.fields['password1'].help_text = _(
            '<ul class="text-muted small">'
            '<li>Votre mot de passe doit contenir au minimum 8 caractères.</li>'
            '<li>Votre mot de passe ne peut pas être trop similaire à vos autres informations personnelles.</li>'
            '<li>Votre mot de passe ne peut pas être un mot de passe couramment utilisé.</li>'
            '<li>Votre mot de passe ne peut pas être entièrement numérique.</li>'
            '</ul>'
        )
        self.fields['password1'].error_messages = {
            'required': _('Ce champ est obligatoire.'),
            'password_too_short': _('Ce mot de passe est trop court. Il doit contenir au minimum 8 caractères.'),
            'password_too_common': _('Ce mot de passe est trop courant.'),
            'password_entirely_numeric': _('Ce mot de passe ne peut pas être entièrement numérique.'),
        }
        
        self.fields['password2'].error_messages = {
            'required': _('Ce champ est obligatoire.'),
            'password_mismatch': _('Les deux mots de passe ne correspondent pas.'),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    """Formulaire de modification d'utilisateur personnalisé"""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'telephone')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class CustomPasswordChangeForm(PasswordChangeForm):
    """Formulaire de changement de mot de passe personnalisé"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        # Personnaliser les messages d'erreur
        self.fields['old_password'].error_messages = {
            'required': _('Ce champ est obligatoire.'),
            'password_incorrect': _('Votre ancien mot de passe est incorrect.'),
        }
        
        self.fields['new_password1'].help_text = _(
            '<ul class="text-muted small">'
            '<li>Votre mot de passe doit contenir au minimum 8 caractères.</li>'
            '<li>Votre mot de passe ne peut pas être trop similaire à vos autres informations personnelles.</li>'
            '<li>Votre mot de passe ne peut pas être un mot de passe couramment utilisé.</li>'
            '<li>Votre mot de passe ne peut pas être entièrement numérique.</li>'
            '</ul>'
        )
        self.fields['new_password1'].error_messages = {
            'required': _('Ce champ est obligatoire.'),
            'password_too_short': _('Ce mot de passe est trop court. Il doit contenir au minimum 8 caractères.'),
            'password_too_common': _('Ce mot de passe est trop courant.'),
            'password_entirely_numeric': _('Ce mot de passe ne peut pas être entièrement numérique.'),
        }
        
        self.fields['new_password2'].error_messages = {
            'required': _('Ce champ est obligatoire.'),
            'password_mismatch': _('Les deux mots de passe ne correspondent pas.'),
        }

class UserProfileForm(forms.ModelForm):
    """Formulaire de profil utilisateur"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'telephone')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    """Formulaire de connexion personnalisé"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': _('Nom d\'utilisateur')
        }),
        label=_('Nom d\'utilisateur')
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': _('Mot de passe')
        }),
        label=_('Mot de passe')
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label=_('Se souvenir de moi')
    )

class PasswordResetRequestForm(forms.Form):
    """Formulaire de demande de réinitialisation de mot de passe"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': _('Adresse email')
        }),
        label=_('Adresse email'),
        error_messages={
            'required': _('Ce champ est obligatoire.'),
            'invalid': _('Entrez une adresse email valide.'),
        }
    )

class CustomSetPasswordForm(SetPasswordForm):
    """Formulaire de définition de nouveau mot de passe personnalisé"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        
        # Personnaliser les messages d'erreur
        self.fields['new_password1'].help_text = _(
            '<ul class="text-muted small">'
            '<li>Votre mot de passe doit contenir au minimum 8 caractères.</li>'
            '<li>Votre mot de passe ne peut pas être trop similaire à vos autres informations personnelles.</li>'
            '<li>Votre mot de passe ne peut pas être un mot de passe couramment utilisé.</li>'
            '<li>Votre mot de passe ne peut pas être entièrement numérique.</li>'
            '</ul>'
        )
        self.fields['new_password1'].error_messages = {
            'required': _('Ce champ est obligatoire.'),
            'password_too_short': _('Ce mot de passe est trop court. Il doit contenir au minimum 8 caractères.'),
            'password_too_common': _('Ce mot de passe est trop courant.'),
            'password_entirely_numeric': _('Ce mot de passe ne peut pas être entièrement numérique.'),
        }
        
        self.fields['new_password2'].error_messages = {
            'required': _('Ce champ est obligatoire.'),
            'password_mismatch': _('Les deux mots de passe ne correspondent pas.'),
        } 