from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Collaboration


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Adresse e‑mail valide (obligatoire).")
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Un compte utilise déjà cette adresse e‑mail.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=True,
        help_text="Courte bibliographie : décrivez votre expérience et mentionnez également vos passions (ex : IA, Web, Mobile)."
    )

    class Meta:
        model = UserProfile
        fields = [
            'bio', 'skills', 'education_level', 'languages',
            'passions', 'projects', 'linkedin', 'github', 'website'
        ]
        widgets = {
            'skills': forms.TextInput(attrs={'placeholder': 'Utilisé uniquement en fallback (non visible)'}),
            'languages': forms.TextInput(attrs={'placeholder': 'Ex: Français, Anglais'}),
            'passions': forms.TextInput(attrs={'placeholder': 'Ex: IA, Jeux, Robotique'}),
        }

    def clean_skills(self):
        """
        Récupère toutes les valeurs POST nommées 'skills' (plusieurs inputs possibles)
        puis normalise en chaîne séparée par des virgules stockée en base.
        """
        # self.data est un QueryDict => getlist retourne toutes les valeurs du même nom
        raw_list = []
        try:
            raw_list = self.data.getlist('skills')
        except Exception:
            raw_val = self.cleaned_data.get('skills') or ''
            raw_list = [raw_val]

        cleaned = [s.strip() for s in raw_list if s and s.strip()]
        return ', '.join(cleaned)


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