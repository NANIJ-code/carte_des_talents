from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login
from .models import UserProfile
from .forms import UserRegistrationForm, UserProfileForm, SearchForm
from django.shortcuts import get_object_or_404
from django.db.models import Q

def home(request):
    """Page d'accueil"""
    return render(request, 'home.html')

def signup(request):
    """
    Affiche et traite le formulaire d'inscription composé de :
    - UserRegistrationForm pour les infos de compte
    - UserProfileForm pour la description des talents/compétences

    Comportement :
    - en POST : valide les deux formulaires, crée l'utilisateur et son profil,
      connecte l'utilisateur et redirige vers la page de détail du profil.
    - en GET : affiche les deux formulaires vides.
    """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            messages.success(request, 'Compte créé et profil enregistré.')
            return redirect('profile_detail', pk=user.id)
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
    """
    Page 'Trouver des collaborateurs'.
    - Affiche un formulaire de recherche.
    - Filtre UserProfile (is_validated=True) par compétences, bio, projets, nom, niveau d'études et langue.
    - Supporte tri par pertinence (q) ou par date de création (newest).
    """
    form = SearchForm(request.GET or None)
    qs = UserProfile.objects.filter(is_validated=True).select_related('user')

    if form.is_valid():
        q = form.cleaned_data.get('q') or ''
        education = form.cleaned_data.get('education_level') or ''
        language = form.cleaned_data.get('language') or ''
        sort_by = form.cleaned_data.get('sort_by') or 'relevance'

        if q:
            # Recherche sur plusieurs champs
            qs = qs.filter(
                Q(skills__icontains=q) |
                Q(bio__icontains=q) |
                Q(projects__icontains=q) |
                Q(user__username__icontains=q) |
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q)
            )

        if education:
            qs = qs.filter(education_level__iexact=education)

        if language:
            qs = qs.filter(languages__icontains=language)

        if sort_by == 'newest':
            qs = qs.order_by('-created_at')
        else:
            # Par défaut pertinence = garder l'ordre existant (ou potentiellement ajouter scoring)
            qs = qs.order_by('-is_validated', '-created_at')

    context = {
        'form': form,
        'results': qs[:200],  # limite simple
    }
    return render(request, 'search/search.html', context)

@login_required
def talent_map(request, pk):
    """Visualisation de la carte de talents"""
    try:
        profile = UserProfile.objects.get(user__id=pk)
    except UserProfile.DoesNotExist:
        messages.error(request, 'Profil non trouvé.')
        return redirect('home')
    
    return render(request, 'talent_map/visualization.html', {'profile': profile})