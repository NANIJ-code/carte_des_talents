from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Modèle pour stocker les profils utilisateur avec leurs talents et compétences"""
    
    EDUCATION_CHOICES = [
        ('bac', 'Baccalauréat'),
        ('licence', 'Licence'),
        ('master', 'Master'),
        ('doctorat', 'Doctorat'),
        ('autre', 'Autre'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    education_level = models.CharField(max_length=20, choices=EDUCATION_CHOICES, default='licence')
    bio = models.TextField(blank=True, null=True, help_text="Courte biographie")
    
    # Compétences (texte libre, séparées par des virgules)
    skills = models.TextField(blank=True, null=True, help_text="Ex: Python, Django, JavaScript")
    
    # Langues
    languages = models.TextField(blank=True, null=True, help_text="Ex: Français, Anglais, Espagnol")
    
    # Domaines d'intérêt / Passions
    passions = models.TextField(blank=True, null=True, help_text="Ex: IA, Web, Mobile")
    
    # Projets réalisés
    projects = models.TextField(blank=True, null=True, help_text="Ex: Projet 1 - Description, Projet 2 - Description")
    
    # Liens professionnels
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Validation
    is_validated = models.BooleanField(default=False, help_text="Profil validé par un responsable")
    validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name='validated_profiles', 
                                      help_text="Responsable qui a validé le profil")
    validated_at = models.DateTimeField(null=True, blank=True)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profil Utilisateur"
        verbose_name_plural = "Profils Utilisateurs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Profil de {self.user.username}"


class Collaboration(models.Model):
    """Modèle pour les demandes de collaboration entre utilisateurs"""
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('rejected', 'Rejetée'),
    ]
    
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collaborations_sent')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collaborations_received')
    
    title = models.CharField(max_length=200, help_text="Titre du besoin / du projet")
    description = models.TextField(help_text="Description du besoin en collaborateurs")
    required_skills = models.TextField(blank=True, null=True, help_text="Ex: Python, Django")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Collaboration"
        verbose_name_plural = "Collaborations"
        ordering = ['-created_at']
        unique_together = ('requester', 'receiver')  # Évite les doublons
    
    def __str__(self):
        return f"Collaboration: {self.requester.username} -> {self.receiver.username}"