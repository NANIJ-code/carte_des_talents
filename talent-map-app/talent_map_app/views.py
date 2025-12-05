from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import UserProfile
from .forms import UserRegistrationForm, UserProfileForm, SearchForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db import IntegrityError, transaction
from django.contrib.auth.models import User
import re

def home(request):
    """Page d'accueil"""
    return render(request, 'home.html')

def signup(request):
    """
    Inscription : crée l'utilisateur + son profile si les deux formulaires sont valides.
    Protection contre doublons de username (unique constraint).
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            username = user_form.cleaned_data.get('username')
            email = user_form.cleaned_data.get('email', '')
            # double-check existence avant tentative d'insertion
            if User.objects.filter(username__iexact=username).exists():
                messages.error(request, "Le nom d'utilisateur est déjà utilisé. Choisissez-en un autre.")
            else:
                try:
                    with transaction.atomic():
                        user = user_form.save(commit=False)
                        user.email = email
                        user.save()  # création user
                        profile = profile_form.save(commit=False)
                        profile.user = user
                        profile.save()
                        login(request, user)
                        messages.success(request, "Compte créé et profil enregistré.")
                        return redirect('profile_detail', pk=user.profile.pk)
                except IntegrityError:
                    # protège contre race condition ou insertion concurrente
                    messages.error(request, "Erreur lors de la création du compte : nom d'utilisateur déjà utilisé.")
        else:
            messages.error(request, "Corrigez les erreurs du formulaire.")
    else:
        user_form = UserRegistrationForm()
        profile_form = UserProfileForm()

    return render(request, 'auth/signup.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def profile_create(request):
    """
    Affiche et traite le formulaire de création / édition du profil utilisateur.
    - Si l'utilisateur a déjà un profil, ouvre en édition.
    - En POST : valide et enregistre (associe profile.user = request.user).
    """
    # récupérer ou créer un profil pour l'utilisateur courant
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Profil sauvegardé.')
            return redirect('profile_detail', pk=request.user.id)
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile/create.html', {'form': form, 'profile': profile})

@login_required
def profile_detail(request, pk):
    """Détail du profil"""
    try:
        profile = UserProfile.objects.get(user__id=pk)
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil non trouvé.')
        return redirect('home')
    
    return render(request, 'profile/detail.html', {'profile': profile})

@login_required
def profile_edit(request, pk):
    """Édition du profil"""
    try:
        profile = UserProfile.objects.get(user__id=pk)
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil non trouvé.')
        return redirect('home')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil mis à jour !')
            return redirect('profile_detail', pk=pk)
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile/edit.html', {'form': form, 'profile': profile})

@login_required
def search_profiles(request):
    """Affiche tous les profils (sauf l'utilisateur connecté) et applique les filtres du SearchForm."""
    form = SearchForm(request.GET or None)
    qs = UserProfile.objects.all()
    if request.user.is_authenticated:
        qs = qs.exclude(user=request.user)

    if form.is_valid():
        q = (form.cleaned_data.get('q') or '').strip()
        education = form.cleaned_data.get('education_level')
        language = form.cleaned_data.get('language')
        sort_by = form.cleaned_data.get('sort_by')

        if q:
            terms = [t for t in re.split(r'[,;]\s*|\s+', q) if t]
            q_filter = Q()
            for term in terms:
                q_filter |= (
                    Q(skills__icontains=term) |
                    Q(bio__icontains=term) |
                    Q(user__username__icontains=term) |
                    Q(user__first_name__icontains=term) |
                    Q(user__last_name__icontains=term)
                )
            qs = qs.filter(q_filter)

        if education:
            qs = qs.filter(education_level=education)

        if language:
            qs = qs.filter(languages__icontains=language)

        if sort_by == 'newest':
            qs = qs.order_by('-user__date_joined')
        elif sort_by == 'oldest':
            qs = qs.order_by('user__date_joined')

    return render(request, 'search/search.html', {'form': form, 'results': qs})

# exposer la même vue sous le nom attendu par les URLs
search = search_profiles

@login_required
def redirect_to_profile(request):
    """Redirige /accounts/profile/ vers le détail du profil de l'utilisateur connecté."""
    return redirect('profile_detail', pk=request.user.id)

@login_required
def talent_map(request, pk):
    """
    Affiche la visualisation / carte d'un profil donné.
    URL attendue : profile/<int:pk>/map/
    """
    profile = get_object_or_404(UserProfile, user__id=pk)
    
    # Préparer les données pour la visualisation JavaScript
    talent_data = {
        'skills': profile.skills_list,
        'passions': [p.strip() for p in (profile.passions or '').split(',') if p.strip()],
    }
    
    return render(request, 'talent_map/visualization.html', {'profile': profile, 'talent_data': talent_data})