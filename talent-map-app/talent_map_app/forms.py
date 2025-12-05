from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Collaboration


class UserProfileForm(forms.ModelForm):
    """Formulaire ModelForm pour décrire les talents et informations du profil.

    Contient des widgets adaptés pour une saisie claire et un rendu cohérent
    avec Bootstrap / crispy-forms.
    """
    class Meta:
        model = UserProfile
        fields = [
            'education_level',
            'bio',
            'skills',
            'languages',
            'passions',
            'projects',
            'linkedin',
            'github',
            'youtube',
            'website',
        ]
        widgets = {
            'education_level': forms.Select(attrs={'class': 'form-select'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Courte présentation'}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: Python, Django, JavaScript'}),
            'languages': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ex: Français, Anglais'}),
            'passions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ex: IA, Web, Mobile'}),
            'projects': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Projets réalisés'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://linkedin.com/in/...'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/...'}),
            'youtube': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://youtube.com/...'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://votre-site.com'}),
        }


class CollaborationForm(forms.ModelForm):
    """Formulaire pour créer une demande de collaboration"""

    class Meta:
        model = Collaboration
        fields = ['title', 'description', 'required_skills']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Titre du projet/besoin'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Décrivez votre besoin en collaborateurs'}),
            'required_skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Ex: Python, Django, React'}),
        }


class UserRegistrationForm(forms.ModelForm):
    """Formulaire d'inscription utilisateur avec confirmation de mot de passe.

    Le formulaire expose username, email, first_name, last_name, password et password_confirm.
    """
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mot de passe'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmer le mot de passe'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom d\'utilisateur'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
        }

    def clean(self):
        """
        Validation : vérifie la confirmation du mot de passe.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Les mots de passe ne correspondent pas.")

        return cleaned_data


class SearchForm(forms.Form):
    """
    Formulaire de recherche pour trouver des collaborateurs.
    - q : recherche libre (skills, bio, projets, nom)
    - education_level : filtre par niveau d'études
    - language : filtre par langue (recherche partielle)
    - sort_by : tri simple ('relevance' ou 'newest')
    """
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Ex: Python, Django, IA, UX...'
    }))
    education_level = forms.ChoiceField(required=False, choices=[('', 'Tous niveaux')] + UserProfile.EDUCATION_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))
    language = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Français, Anglais'}))
    sort_by = forms.ChoiceField(required=False, choices=[
        ('relevance', 'Pertinence'),
        ('newest', 'Les plus récents'),
    ], initial='relevance', widget=forms.Select(attrs={'class': 'form-select'}))