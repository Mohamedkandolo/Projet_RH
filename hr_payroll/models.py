from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal
import uuid


class Direction(models.Model):
    """Modèle pour gérer les directions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Direction"
        verbose_name_plural = "Directions"
        ordering = ['nom']

    def __str__(self):
        return f"{self.code} - {self.nom}"


class Bureau(models.Model):
    """Modèle pour gérer les bureaux"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=200)
    code = models.CharField(max_length=10)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='bureaux')
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Bureau"
        verbose_name_plural = "Bureaux"
        unique_together = ['code', 'direction']
        ordering = ['direction', 'nom']

    def __str__(self):
        return f"{self.code} - {self.nom} ({self.direction.nom})"


class Grade(models.Model):
    """Modèle pour gérer les grades"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    niveau = models.PositiveIntegerField(help_text="Niveau hiérarchique du grade")
    description = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Grade"
        verbose_name_plural = "Grades"
        ordering = ['niveau', 'nom']

    def __str__(self):
        return f"{self.code} - {self.nom} (Niveau {self.niveau})"


class ElementPaie(models.Model):
    """Modèle pour gérer les éléments de paie"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TYPE_CHOICES = [
        ('GAIN', 'Gain'),
        ('RETENUE', 'Retenue'),
        ('COTISATION', 'Cotisation'),
    ]
    
    nom = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True)
    type_element = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True, null=True)
    calculable = models.BooleanField(default=True, help_text="Si l'élément peut être calculé automatiquement")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Élément de paie"
        verbose_name_plural = "Éléments de paie"
        ordering = ['type_element', 'nom']

    def __str__(self):
        return f"{self.code} - {self.nom} ({self.get_type_element_display()})"


class GrilleSalariale(models.Model):
    """Modèle pour gérer la grille salariale par grade"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='grilles_salariales')
    element_paie = models.ForeignKey(ElementPaie, on_delete=models.CASCADE, related_name='grilles_salariales')
    montant = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Grille salariale"
        verbose_name_plural = "Grilles salariales"
        ordering = ['grade', 'element_paie']

    def __str__(self):
        return f"{self.grade.nom} - {self.element_paie.nom}: {self.montant}"


# ===== NOUVEAUX MODÈLES POUR SIGRH_PAIE =====

class PosteBudgetaire(models.Model):
    """Modèle pour gérer les postes budgétaires (Cadre organique)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TYPE_CHOICES = [
        ('PERMANENT', 'Permanent'),
        ('CONTRACTUEL', 'Contractuel'),
        ('STAGIAIRE', 'Stagiaire'),
    ]
    
    intitule = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    type_poste = models.CharField(max_length=20, choices=TYPE_CHOICES)
    grade_requis = models.ForeignKey(Grade, on_delete=models.PROTECT, related_name='postes_budgetaires')
    bureau = models.ForeignKey(Bureau, on_delete=models.PROTECT, related_name='postes_budgetaires')
    
    # Description du poste
    missions = models.TextField(help_text="Missions et responsabilités du poste")
    competences_requises = models.TextField(help_text="Compétences techniques et managériales requises")
    position_hierarchique = models.CharField(max_length=100, help_text="Position dans l'organigramme")
    
    # Statut du poste
    pourvu = models.BooleanField(default=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Poste budgétaire"
        verbose_name_plural = "Postes budgétaires"
        ordering = ['bureau', 'grade_requis', 'intitule']

    def __str__(self):
        return f"{self.code} - {self.intitule} ({self.get_type_poste_display()})"


class Competence(models.Model):
    """Modèle pour gérer les compétences (Gestion des compétences)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    CATEGORIE_CHOICES = [
        ('TECHNIQUE', 'Technique'),
        ('MANAGERIALE', 'Managériale'),
        ('SPECIFIQUE', 'Spécifique'),
        ('GENERALE', 'Générale'),
    ]
    
    nom = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True)
    categorie = models.CharField(max_length=20, choices=CATEGORIE_CHOICES)
    description = models.TextField(help_text="Description détaillée de la compétence")
    niveau_expertise = models.PositiveIntegerField(choices=[
        (1, 'Débutant'), (2, 'Intermédiaire'), (3, 'Avancé'), (4, 'Expert'), (5, 'Maître')
    ], help_text="Niveau d'expertise requis")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"
        ordering = ['categorie', 'nom']

    def __str__(self):
        return f"{self.code} - {self.nom} ({self.get_categorie_display()})"


class Formation(models.Model):
    """Modèle pour gérer les formations (Renforcement de capacités)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TYPE_CHOICES = [
        ('INTERNE', 'Formation interne'),
        ('EXTERNE', 'Formation externe'),
        ('CERTIFICATION', 'Certification'),
        ('CONFERENCE', 'Conférence/Séminaire'),
    ]
    
    intitule = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    type_formation = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(help_text="Description détaillée de la formation")
    
    # Informations pratiques
    duree_heures = models.PositiveIntegerField(help_text="Durée en heures")
    cout_estime = models.DecimalField(max_digits=10, decimal_places=2, help_text="Coût estimé de la formation")
    lieu = models.CharField(max_length=200, blank=True, null=True)
    
    # Planification
    date_debut = models.DateField()
    date_fin = models.DateField()
    nombre_places = models.PositiveIntegerField(help_text="Nombre de places disponibles")
    
    # Statut
    statut = models.CharField(max_length=20, choices=[
        ('PLANIFIEE', 'Planifiée'),
        ('EN_COURS', 'En cours'),
        ('TERMINEE', 'Terminée'),
        ('ANNULEE', 'Annulée'),
    ], default='PLANIFIEE')
    
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Formation"
        verbose_name_plural = "Formations"
        ordering = ['-date_debut', 'intitule']

    def __str__(self):
        return f"{self.code} - {self.intitule} ({self.get_statut_display()})"


class Agent(models.Model):
    """Modèle pour gérer les agents - VERSION COMPLÈTE SIGRH_PAIE"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUT_CHOICES = [
        ('ACTIF', 'Actif'),
        ('INACTIF', 'Inactif'),
        ('RETRAITE', 'Retraité'),
        ('DEMISSIONNAIRE', 'Démissionnaire'),
    ]
    
    # === IDENTITÉ (ENGAGEMENT) ===
    matricule = models.CharField(max_length=20, unique=True)
    nom = models.CharField(max_length=100)
    prenoms = models.CharField(max_length=200)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=200)
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    nationalite = models.CharField(max_length=100, default="Congolaise")
    photo_identite = models.ImageField(upload_to='photos_agents/', blank=True, null=True)
    numero_identification = models.CharField(max_length=50, blank=True, null=True, help_text="Numéro d'identification national/professionnel")
    
    # === ÉTAT CIVIL ET DÉPENDANTS (ENGAGEMENT) ===
    etat_civil = models.CharField(max_length=20, choices=[
        ('CELIBATAIRE', 'Célibataire'),
        ('MARIE', 'Marié(e)'),
        ('DIVORCE', 'Divorcé(e)'),
        ('VEUF', 'Veuf/Veuve'),
    ], default='CELIBATAIRE')
    nom_conjoint = models.CharField(max_length=100, blank=True, null=True)
    nombre_enfants = models.PositiveIntegerField(default=0)
    numero_securite_sociale = models.CharField(max_length=50, blank=True, null=True)
    
    # === FORMATIONS (ENGAGEMENT) ===
    diplome_principal = models.CharField(max_length=200, blank=True, null=True)
    etablissement_formation = models.CharField(max_length=200, blank=True, null=True)
    annee_obtention = models.PositiveIntegerField(blank=True, null=True)
    specialite = models.CharField(max_length=200, blank=True, null=True)
    
    # === DONNÉES DE SANTÉ (ENGAGEMENT) - CONFIDENTIELLES ===
    visite_medicale_aptitude = models.BooleanField(default=False)
    date_visite_medicale = models.DateField(blank=True, null=True)
    inaptitude_medicale = models.BooleanField(default=False)
    restrictions_medicales = models.TextField(blank=True, null=True, help_text="Mentions confidentielles")
    
    # === ANTÉCÉDENTS JURIDIQUES (ENGAGEMENT) ===
    casier_judiciaire = models.BooleanField(default=False)
    commentaires_juridiques = models.TextField(blank=True, null=True, help_text="Historique des condamnations ou litiges")
    
    # === INFORMATIONS PROFESSIONNELLES ===
    grade = models.ForeignKey(Grade, on_delete=models.PROTECT, related_name='agents')
    bureau = models.ForeignKey(Bureau, on_delete=models.PROTECT, related_name='agents')
    poste_budgetaire = models.ForeignKey(PosteBudgetaire, on_delete=models.PROTECT, related_name='agents', blank=True, null=True)
    date_embauche = models.DateField()
    date_nomination = models.DateField(blank=True, null=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ACTIF')
    
    # === INFORMATIONS DE CONTACT ===
    adresse = models.TextField()
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    # === INFORMATIONS BANCAIRES ===
    banque = models.CharField(max_length=100, blank=True, null=True)
    numero_compte = models.CharField(max_length=50, blank=True, null=True)
    
    # === TRACABILITÉ ===
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='agents_crees')
    actif = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Agent"
        verbose_name_plural = "Agents"
        ordering = ['nom', 'prenoms']

    def __str__(self):
        return f"{self.matricule} - {self.nom} {self.prenoms}"

    @property
    def nom_complet(self):
        return f"{self.nom} {self.prenoms}"
    
    """def save(self, *args, **kwargs):
        if not self.matricule:
            last_matr = Agent.objects.filter(matricule__startswith="M").order_by("-matricule").first()
            
            if last_matr and last_matr.matricule[1:].isdigit():
                last_nbr = int(last_matr.matricule[1:])
                new_nbr = last_nbr + 1
                self.matricule = f"M{new_nbr:04d}"
            else:
                self.matricule = "M0001"
                
        super().save(*args, **kwargs)"""


class Affectation(models.Model):
    """Modèle pour gérer les affectations (Gestion de carrière)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='affectations')
    bureau = models.ForeignKey(Bureau, on_delete=models.PROTECT, related_name='affectations')
    poste_budgetaire = models.ForeignKey(PosteBudgetaire, on_delete=models.PROTECT, related_name='affectations', blank=True, null=True)
    
    # Informations sur l'affectation
    fonctions_exercees = models.TextField(help_text="Description des fonctions exercées")
    date_debut = models.DateField()
    date_fin = models.DateField(blank=True, null=True, help_text="Date de fin si temporaire")
    
    # Statut
    statut = models.CharField(max_length=20, choices=[
        ('ACTIVE', 'Active'),
        ('TERMINEE', 'Terminée'),
        ('SUSPENDUE', 'Suspendue'),
    ], default='ACTIVE')
    
    # Traçabilité
    motif_affectation = models.TextField(blank=True, null=True)
    decision_affectation = models.CharField(max_length=200, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Affectation"
        verbose_name_plural = "Affectations"
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.agent.nom_complet} - {self.bureau.nom} ({self.date_debut})"


class Promotion(models.Model):
    """Modèle pour gérer les promotions et avancements (Gestion de carrière)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='promotions')
    grade_ancien = models.ForeignKey(Grade, on_delete=models.PROTECT, related_name='promotions_ancien', blank=True, null=True)
    grade_nouveau = models.ForeignKey(Grade, on_delete=models.PROTECT, related_name='promotions_nouveau')
    
    # Informations sur la promotion
    type_promotion = models.CharField(max_length=20, choices=[
        ('GRADE', 'Promotion de grade'),
        ('ECHELON', 'Avancement d\'échelon'),
        ('FONCTION', 'Promotion fonctionnelle'),
    ])
    date_promotion = models.DateField()
    motif_promotion = models.TextField(help_text="Justification de la promotion")
    
    # Critères d'éligibilité
    anciennete_requise = models.PositiveIntegerField(help_text="Ancienneté requise en années")
    notation_requise = models.DecimalField(max_digits=4, decimal_places=2, help_text="Note minimale requise")
    
    # Traçabilité
    decision_promotion = models.CharField(max_length=200, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        ordering = ['-date_promotion']

    def __str__(self):
        return f"{self.agent.nom_complet} - {self.grade_nouveau.nom} ({self.date_promotion})"


class Mutation(models.Model):
    """Modèle pour gérer les mutations (Gestion de carrière)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='mutations')
    
    # Informations sur la mutation
    type_mutation = models.CharField(max_length=20, choices=[
        ('SERVICE', 'Changement de service'),
        ('MINISTERE', 'Changement de ministère'),
        ('ZONE_GEO', 'Changement de zone géographique'),
        ('FONCTION', 'Changement de fonction'),
    ])
    
    # Origine et destination
    origine_bureau = models.ForeignKey(Bureau, on_delete=models.PROTECT, related_name='mutations_origine', blank=True, null=True)
    destination_bureau = models.ForeignKey(Bureau, on_delete=models.PROTECT, related_name='mutations_destination')
    
    date_mutation = models.DateField()
    motif_mutation = models.TextField(help_text="Justification de la mutation")
    
    # Traçabilité
    decision_mutation = models.CharField(max_length=200, blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Mutation"
        verbose_name_plural = "Mutations"
        ordering = ['-date_mutation']

    def __str__(self):
        return f"{self.agent.nom_complet} - {self.destination_bureau.nom} ({self.date_mutation})"


class Cotation(models.Model):
    """Modèle pour gérer les cotations (Évaluation des performances)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='cotations')
    periode_evaluation = models.CharField(max_length=20, choices=[
        ('SEMESTRIELLE', 'Semestrielle'),
        ('ANNUELLE', 'Annuelle'),
        ('EXCEPTIONNELLE', 'Exceptionnelle'),
    ])
    
    # Période d'évaluation
    annee = models.PositiveIntegerField()
    semestre = models.PositiveIntegerField(choices=[(1, '1er semestre'), (2, '2ème semestre')], blank=True, null=True)
    
    # Critères d'évaluation (notation sur 20)
    comportement_professionnel = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], help_text="Note sur 20")
    assiduite = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], help_text="Note sur 20")
    resultats_objectifs = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], help_text="Note sur 20")
    qualite_travail = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], help_text="Note sur 20")
    esprit_equipe = models.DecimalField(max_digits=4, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], help_text="Note sur 20")
    
    # Note globale
    note_globale = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    
    # Appréciations
    appreciations = models.TextField(help_text="Commentaires et appréciations générales")
    points_forts = models.TextField(blank=True, null=True)
    points_amelioration = models.TextField(blank=True, null=True)
    
    # Validation
    valide_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='cotations_validees')
    date_validation = models.DateTimeField(blank=True, null=True)
    
    # Traçabilité
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='cotations_crees')

    class Meta:
        verbose_name = "Cotation"
        verbose_name_plural = "Cotations"
        unique_together = ['agent', 'annee', 'semestre', 'periode_evaluation']
        ordering = ['-annee', '-semestre', 'agent']

    def __str__(self):
        return f"Cotation {self.agent.nom_complet} - {self.annee} S{self.semestre or 'A'}"

    def calculer_note_globale(self):
        """Calculer la note globale moyenne"""
        notes = [
            self.comportement_professionnel,
            self.assiduite,
            self.resultats_objectifs,
            self.qualite_travail,
            self.esprit_equipe
        ]
        self.note_globale = sum(notes) / len(notes)
        return self.note_globale


class ActionDisciplinaire(models.Model):
    """Modèle pour gérer les actions disciplinaires"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='actions_disciplinaires')
    
    # Informations sur la faute
    type_faute = models.CharField(max_length=20, choices=[
        ('RETARD', 'Retard'),
        ('ABSENCE', 'Absence injustifiée'),
        ('INDISCIPLINE', 'Indiscipline'),
        ('INSUBORDINATION', 'Insubordination'),
        ('NEGLIGENCE', 'Négligence'),
        ('AUTRE', 'Autre'),
    ])
    
    description_faute = models.TextField(help_text="Description détaillée de la faute")
    date_faute = models.DateField()
    lieu_faute = models.CharField(max_length=200, blank=True, null=True)
    
    # Procédure disciplinaire
    date_notification = models.DateField(blank=True, null=True)
    commission_disciplinaire = models.BooleanField(default=False)
    date_commission = models.DateField(blank=True, null=True)
    
    # Sanction appliquée
    type_sanction = models.CharField(max_length=20, choices=[
        ('AVERTISSEMENT', 'Avertissement'),
        ('BLAME', 'Blâme'),
        ('SUSPENSION', 'Suspension'),
        ('RETROGRADATION', 'Rétrogradation'),
        ('REVOCATION', 'Révocation'),
        ('AUTRE', 'Autre'),
    ], blank=True, null=True)
    
    duree_sanction = models.PositiveIntegerField(blank=True, null=True, help_text="Durée en jours si applicable")
    motif_sanction = models.TextField(blank=True, null=True)
    
    # Statut
    statut = models.CharField(max_length=20, choices=[
        ('EN_COURS', 'En cours'),
        ('NOTIFIEE', 'Notifiée'),
        ('SANCTIONNEE', 'Sanctionnée'),
        ('CLASSEE', 'Classée sans suite'),
    ], default='EN_COURS')
    
    # Traçabilité
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Action disciplinaire"
        verbose_name_plural = "Actions disciplinaires"
        ordering = ['-date_faute']

    def __str__(self):
        return f"Action disciplinaire {self.agent.nom_complet} - {self.get_type_faute_display()} ({self.date_faute})"


class CompetenceAgent(models.Model):
    """Modèle pour gérer les compétences des agents (Gestion des compétences)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='competences')
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE, related_name='agents_competents')
    
    # Niveau de maîtrise de l'agent
    niveau_maitrise = models.PositiveIntegerField(choices=[
        (1, 'Débutant'), (2, 'Intermédiaire'), (3, 'Avancé'), (4, 'Expert'), (5, 'Maître')
    ], help_text="Niveau actuel de maîtrise de l'agent")
    
    # Évaluation de la compétence
    date_evaluation = models.DateField()
    evalue_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='competences_evaluees')
    
    # Commentaires
    commentaires = models.TextField(blank=True, null=True, help_text="Observations sur le niveau de maîtrise")
    
    # Traçabilité
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Compétence d'agent"
        verbose_name_plural = "Compétences d'agents"
        unique_together = ['agent', 'competence']
        ordering = ['agent', 'competence']

    def __str__(self):
        return f"{self.agent.nom_complet} - {self.competence.nom} (Niveau {self.niveau_maitrise})"


class ParticipationFormation(models.Model):
    """Modèle pour gérer les participations aux formations (Renforcement de capacités)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='participations_formations')
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='participants')
    
    # Statut de participation
    statut_participation = models.CharField(max_length=20, choices=[
        ('INSCRIT', 'Inscrit'),
        ('EN_COURS', 'En cours'),
        ('TERMINEE', 'Terminée'),
        ('ABANDON', 'Abandon'),
        ('EXCLU', 'Exclu'),
    ], default='INSCRIT')
    
    # Évaluation post-formation
    note_formation = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True, help_text="Note sur 20")
    appreciation_formation = models.TextField(blank=True, null=True, help_text="Appréciation de la formation")
    impact_formation = models.TextField(blank=True, null=True, help_text="Impact sur les compétences")
    mise_en_pratique = models.TextField(blank=True, null=True, help_text="Comment la formation est mise en pratique")
    
    # Coûts
    cout_participation = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Coût réel de la participation")
    
    # Traçabilité
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    inscrit_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Participation à une formation"
        verbose_name_plural = "Participations aux formations"
        unique_together = ['agent', 'formation']
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.agent.nom_complet} - {self.formation.intitule} ({self.get_statut_participation_display()})"


# ===== MODÈLES EXISTANTS POUR LA PAIE =====

class PeriodePaie(models.Model):
    """Modèle pour gérer les périodes de paie"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUT_CHOICES = [
        ('OUVERTE', 'Ouverte'),
        ('FERMEE', 'Fermée'),
        ('ARCHIVEE', 'Archivée'),
    ]
    
    annee = models.PositiveIntegerField()
    mois = models.PositiveIntegerField(choices=[
        (1, 'Janvier'), (2, 'Février'), (3, 'Mars'), (4, 'Avril'),
        (5, 'Mai'), (6, 'Juin'), (7, 'Juillet'), (8, 'Août'),
        (9, 'Septembre'), (10, 'Octobre'), (11, 'Novembre'), (12, 'Décembre')
    ])
    date_debut = models.DateField()
    date_fin = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='OUVERTE')
    date_ouverture = models.DateTimeField(auto_now_add=True)
    date_fermeture = models.DateTimeField(blank=True, null=True)
    date_archivage = models.DateTimeField(blank=True, null=True)
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Période de paie"
        verbose_name_plural = "Périodes de paie"
        unique_together = ['annee', 'mois']
        ordering = ['-annee', '-mois']

    def __str__(self):
        return f"Paie {self.get_mois_display()} {self.annee} ({self.get_statut_display()})"


class MouvementPaie(models.Model):
    """Modèle pour gérer les mouvements de paie"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    periode = models.ForeignKey(PeriodePaie, on_delete=models.CASCADE, related_name='mouvements')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='mouvements_paie')
    element_paie = models.ForeignKey(ElementPaie, on_delete=models.CASCADE, related_name='mouvements')
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    commentaire = models.TextField(blank=True, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Mouvement de paie"
        verbose_name_plural = "Mouvements de paie"
        unique_together = ['periode', 'agent', 'element_paie']
        ordering = ['periode', 'agent', 'element_paie']

    def __str__(self):
        return f"{self.agent.nom_complet} - {self.element_paie.nom}: {self.montant}"


class BulletinPaie(models.Model):
    """Modèle pour gérer les bulletins de paie"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    periode = models.ForeignKey(PeriodePaie, on_delete=models.CASCADE, related_name='bulletins')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='bulletins')
    
    # Totaux
    total_gains = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_retenues = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cotisations = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_a_payer = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Informations de calcul
    nombre_jours_travailles = models.PositiveIntegerField(default=30)
    nombre_heures_travaillees = models.DecimalField(max_digits=6, decimal_places=2, default=173.33)
    
    date_calcul = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    calcule_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Bulletin de paie"
        verbose_name_plural = "Bulletins de paie"
        unique_together = ['periode', 'agent']
        ordering = ['periode', 'agent']

    def __str__(self):
        return f"Bulletin {self.agent.nom_complet} - {self.periode}"

    def calculer_net_a_payer(self):
        """Calculer le net à payer"""
        self.net_a_payer = self.total_gains - self.total_retenues - self.total_cotisations
        return self.net_a_payer


class HistoriquePaie(models.Model):
    """Modèle pour l'archivage et l'historisation"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    periode = models.ForeignKey(PeriodePaie, on_delete=models.CASCADE, related_name='historique')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='historique_paie')
    bulletin = models.ForeignKey(BulletinPaie, on_delete=models.CASCADE, related_name='historique')
    
    # Données archivées
    donnees_archivees = models.JSONField(help_text="Données complètes du bulletin archivé")
    date_archivage = models.DateTimeField(auto_now_add=True)
    archive_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    commentaire_archivage = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Historique de paie"
        verbose_name_plural = "Historiques de paie"
        ordering = ['-date_archivage']

    def __str__(self):
        return f"Historique {self.agent.nom_complet} - {self.periode} ({self.date_archivage.strftime('%d/%m/%Y')})"


