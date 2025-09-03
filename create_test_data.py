#!/usr/bin/env python
import os
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProjetRH.settings')
django.setup()

from django.contrib.auth import get_user_model

from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def create_test_data():
    print("Création des données de test...")
    
    # Récupérer l'admin
    admin = User.objects.get(username='admin')
    
    # Créer des utilisateurs de test
    users_data = [
        {'username': 'admin1', 'first_name': 'Mohamed', 'last_name': 'Sese', 'email': 'kandolosesetresor@gmail.com', 'role': 'administrateur',},]
        
    
    created_users = []
    for user_data in users_data:
        user, created = User.objects.get_or_create(
            username=user_data['username'],
            defaults={
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'email': user_data['email'],
                'role': user_data['role'],
                
            }
        )
        if created:
            user.set_password('mohkandolo')
            user.save()
            created_users.append(user)
            print(f"Utilisateur créé: {user.get_full_name()}")
    
    print("\nDonnées de test créées avec succès !")
    print("\nComptes de test créés:")
    print("Admin: admin / mohkandolo")
    

if __name__ == '__main__':
    create_test_data() 