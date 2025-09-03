from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Sum, Count
from .models import (
    Direction, Bureau, Grade, ElementPaie, GrilleSalariale, Agent,
    PeriodePaie, MouvementPaie, BulletinPaie, HistoriquePaie,
    PosteBudgetaire, Competence, Formation, Affectation, Promotion, 
    Mutation, Cotation, ActionDisciplinaire, CompetenceAgent, ParticipationFormation
)


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'actif', 'date_creation']
    list_filter = ['actif', 'date_creation']
    search_fields = ['nom', 'code']
    ordering = ['nom']


@admin.register(Bureau)
class BureauAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'direction', 'actif', 'date_creation']
    list_filter = ['actif', 'direction', 'date_creation']
    search_fields = ['nom', 'code', 'direction__nom']
    ordering = ['direction__nom', 'nom']


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'niveau', 'actif', 'date_creation']
    list_filter = ['actif', 'niveau', 'date_creation']
    search_fields = ['nom', 'code']
    ordering = ['niveau', 'nom']


@admin.register(ElementPaie)
class ElementPaieAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'type_element', 'calculable', 'actif', 'date_creation']
    list_filter = ['actif', 'type_element', 'calculable', 'date_creation']
    search_fields = ['nom', 'code']
    ordering = ['type_element', 'nom']


@admin.register(GrilleSalariale)
class GrilleSalarialeAdmin(admin.ModelAdmin):
    list_display = ['grade', 'element_paie', 'montant', 'actif', 'date_creation']
    list_filter = ['actif', 'grade', 'element_paie__type_element', 'date_creation']
    search_fields = ['grade__nom', 'element_paie__nom']
    ordering = ['grade__niveau', 'element_paie__type_element']


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['matricule', 'nom', 'prenoms', 'grade', 'bureau', 'statut', 'actif', 'date_creation']
    list_filter = ['actif', 'statut', 'grade', 'bureau', 'sexe', 'etat_civil', 'date_creation']
    search_fields = ['matricule', 'nom', 'prenoms', 'email']
    ordering = ['nom', 'prenoms']
    readonly_fields = ['date_creation', 'date_modification']
    
    fieldsets = (
        ('Identité', {
            'fields': ('matricule', 'nom', 'prenoms', 'date_naissance', 'lieu_naissance', 'sexe', 'nationalite', 'photo_identite', 'numero_identification')
        }),
        ('État civil et dépendants', {
            'fields': ('etat_civil', 'nom_conjoint', 'nombre_enfants', 'numero_securite_sociale')
        }),
        ('Formations', {
            'fields': ('diplome_principal', 'etablissement_formation', 'annee_obtention', 'specialite')
        }),
        ('Données de santé', {
            'fields': ('visite_medicale_aptitude', 'date_visite_medicale', 'inaptitude_medicale', 'restrictions_medicales'),
            'classes': ('collapse',)
        }),
        ('Antécédents juridiques', {
            'fields': ('casier_judiciaire', 'commentaires_juridiques'),
            'classes': ('collapse',)
        }),
        ('Informations professionnelles', {
            'fields': ('grade', 'bureau', 'poste_budgetaire', 'date_embauche', 'date_nomination', 'statut')
        }),
        ('Informations de contact', {
            'fields': ('adresse', 'telephone', 'email')
        }),
        ('Informations bancaires', {
            'fields': ('banque', 'numero_compte')
        }),
        ('Traçabilité', {
            'fields': ('cree_par', 'actif'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PeriodePaie)
class PeriodePaieAdmin(admin.ModelAdmin):
    list_display = ['annee', 'mois', 'date_debut', 'date_fin', 'statut', 'date_ouverture']
    list_filter = ['statut', 'annee', 'mois', 'date_ouverture']
    search_fields = ['annee', 'mois']
    ordering = ['-annee', '-mois']


@admin.register(MouvementPaie)
class MouvementPaieAdmin(admin.ModelAdmin):
    list_display = ['periode', 'agent', 'element_paie', 'montant', 'date_creation']
    list_filter = ['periode', 'element_paie__type_element', 'date_creation']
    search_fields = ['agent__nom', 'agent__prenoms', 'element_paie__nom']
    ordering = ['-date_creation']


@admin.register(BulletinPaie)
class BulletinPaieAdmin(admin.ModelAdmin):
    list_display = ['periode', 'agent', 'total_gains', 'total_retenues', 'net_a_payer', 'date_calcul']
    list_filter = ['periode', 'date_calcul']
    search_fields = ['agent__nom', 'agent__prenoms']
    ordering = ['-periode__annee', '-periode__mois']


@admin.register(HistoriquePaie)
class HistoriquePaieAdmin(admin.ModelAdmin):
    list_display = ['periode', 'agent', 'date_archivage', 'archive_par']
    list_filter = ['date_archivage', 'periode']
    search_fields = ['agent__nom', 'agent__prenoms']
    ordering = ['-date_archivage']


# ===== NOUVEAUX MODÈLES SIGRH_PAIE ====

@admin.register(PosteBudgetaire)
class PosteBudgetaireAdmin(admin.ModelAdmin):
    list_display = ['code', 'intitule', 'type_poste', 'grade_requis', 'bureau', 'pourvu', 'actif', 'date_creation']
    list_filter = ['actif', 'type_poste', 'grade_requis', 'bureau', 'pourvu', 'date_creation']
    search_fields = ['intitule', 'code', 'bureau__nom']
    ordering = ['bureau__nom', 'grade_requis__niveau']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('intitule', 'code', 'type_poste', 'grade_requis', 'bureau')
        }),
        ('Description du poste', {
            'fields': ('missions', 'competences_requises', 'position_hierarchique')
        }),
        ('Statut', {
            'fields': ('pourvu', 'actif')
        }),
    )


@admin.register(Competence)
class CompetenceAdmin(admin.ModelAdmin):
    list_display = ['code', 'nom', 'categorie', 'niveau_expertise', 'actif', 'date_creation']
    list_filter = ['actif', 'categorie', 'niveau_expertise', 'date_creation']
    search_fields = ['nom', 'code']
    ordering = ['categorie', 'nom']


@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ['code', 'intitule', 'type_formation', 'date_debut', 'date_fin', 'statut', 'actif', 'date_creation']
    list_filter = ['actif', 'type_formation', 'statut', 'date_creation']
    search_fields = ['intitule', 'code']
    ordering = ['-date_debut']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('intitule', 'code', 'type_formation', 'description')
        }),
        ('Informations pratiques', {
            'fields': ('duree_heures', 'cout_estime', 'lieu')
        }),
        ('Planification', {
            'fields': ('date_debut', 'date_fin', 'nombre_places')
        }),
        ('Statut', {
            'fields': ('statut', 'actif')
        }),
    )


@admin.register(Affectation)
class AffectationAdmin(admin.ModelAdmin):
    list_display = ['agent', 'bureau', 'poste_budgetaire', 'date_debut', 'date_fin', 'statut', 'date_creation']
    list_filter = ['statut', 'bureau', 'date_creation']
    search_fields = ['agent__nom', 'agent__prenoms', 'bureau__nom']
    ordering = ['-date_debut']
    
    fieldsets = (
        ('Agent et affectation', {
            'fields': ('agent', 'bureau', 'poste_budgetaire')
        }),
        ('Informations sur l\'affectation', {
            'fields': ('fonctions_exercees', 'date_debut', 'date_fin')
        }),
        ('Statut et traçabilité', {
            'fields': ('statut', 'motif_affectation', 'decision_affectation', 'cree_par')
        }),
    )


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['agent', 'type_promotion', 'grade_ancien', 'grade_nouveau', 'date_promotion', 'date_creation']
    list_filter = ['type_promotion', 'date_promotion', 'date_creation']
    search_fields = ['agent__nom', 'agent__prenoms']
    ordering = ['-date_promotion']
    
    fieldsets = (
        ('Agent et promotion', {
            'fields': ('agent', 'type_promotion', 'grade_ancien', 'grade_nouveau')
        }),
        ('Informations sur la promotion', {
            'fields': ('date_promotion', 'motif_promotion')
        }),
        ('Critères d\'éligibilité', {
            'fields': ('anciennete_requise', 'notation_requise')
        }),
        ('Traçabilité', {
            'fields': ('decision_promotion', 'cree_par')
        }),
    )


@admin.register(Mutation)
class MutationAdmin(admin.ModelAdmin):
    list_display = ['agent', 'type_mutation', 'origine_bureau', 'destination_bureau', 'date_mutation', 'date_creation']
    list_filter = ['type_mutation', 'date_mutation', 'date_creation']
    search_fields = ['agent__nom', 'agent__prenoms']
    ordering = ['-date_mutation']
    
    fieldsets = (
        ('Agent et mutation', {
            'fields': ('agent', 'type_mutation')
        }),
        ('Origine et destination', {
            'fields': ('origine_bureau', 'destination_bureau')
        }),
        ('Informations sur la mutation', {
            'fields': ('date_mutation', 'motif_mutation')
        }),
        ('Traçabilité', {
            'fields': ('decision_mutation', 'cree_par')
        }),
    )


@admin.register(Cotation)
class CotationAdmin(admin.ModelAdmin):
    list_display = ['agent', 'periode_evaluation', 'annee', 'semestre', 'note_globale', 'valide_par', 'date_creation']
    list_filter = ['periode_evaluation', 'annee', 'semestre', 'date_creation']
    search_fields = ['agent__nom', 'agent__prenoms']
    ordering = ['-annee', '-semestre']
    
    fieldsets = (
        ('Agent et période', {
            'fields': ('agent', 'periode_evaluation', 'annee', 'semestre')
        }),
        ('Critères d\'évaluation', {
            'fields': ('comportement_professionnel', 'assiduite', 'resultats_objectifs', 'qualite_travail', 'esprit_equipe')
        }),
        ('Note globale', {
            'fields': ('note_globale',)
        }),
        ('Appréciations', {
            'fields': ('appreciations', 'points_forts', 'points_amelioration')
        }),
        ('Validation', {
            'fields': ('valide_par', 'date_validation')
        }),
        ('Traçabilité', {
            'fields': ('cree_par',)
        }),
    )
    
    readonly_fields = ['note_globale']


@admin.register(ActionDisciplinaire)
class ActionDisciplinaireAdmin(admin.ModelAdmin):
    list_display = ['agent', 'type_faute', 'date_faute', 'type_sanction', 'statut', 'date_creation']
    list_filter = ['type_faute', 'type_sanction', 'statut', 'date_creation']
    search_fields = ['agent__nom', 'agent__prenoms']
    ordering = ['-date_faute']
    
    fieldsets = (
        ('Agent et faute', {
            'fields': ('agent', 'type_faute', 'description_faute', 'date_faute', 'lieu_faute')
        }),
        ('Procédure disciplinaire', {
            'fields': ('date_notification', 'commission_disciplinaire', 'date_commission')
        }),
        ('Sanction', {
            'fields': ('type_sanction', 'duree_sanction', 'motif_sanction')
        }),
        ('Statut et traçabilité', {
            'fields': ('statut', 'cree_par')
        }),
    )


@admin.register(CompetenceAgent)
class CompetenceAgentAdmin(admin.ModelAdmin):
    list_display = ['agent', 'competence', 'niveau_maitrise', 'date_evaluation', 'evalue_par', 'date_creation']
    list_filter = ['niveau_maitrise', 'date_evaluation', 'date_creation']
    search_fields = ['agent__nom', 'agent__prenoms', 'competence__nom']
    ordering = ['agent__nom', 'competence__nom']
    
    fieldsets = (
        ('Agent et compétence', {
            'fields': ('agent', 'competence', 'niveau_maitrise')
        }),
        ('Évaluation', {
            'fields': ('date_evaluation', 'evalue_par', 'commentaires')
        }),
    )


@admin.register(ParticipationFormation)
class ParticipationFormationAdmin(admin.ModelAdmin):
    list_display = ['agent', 'formation', 'statut_participation', 'note_formation', 'date_inscription']
    list_filter = ['statut_participation', 'date_inscription']
    search_fields = ['agent__nom', 'agent__prenoms', 'formation__intitule']
    ordering = ['-date_inscription']
    
    fieldsets = (
        ('Agent et formation', {
            'fields': ('agent', 'formation', 'statut_participation')
        }),
        ('Évaluation post-formation', {
            'fields': ('note_formation', 'appreciation_formation', 'impact_formation', 'mise_en_pratique')
        }),
        ('Coûts et traçabilité', {
            'fields': ('cout_participation', 'inscrit_par')
        }),
    )


# Configuration de l'admin
admin.site.site_header = "Administration RH et Paie"
admin.site.site_title = "RH et Paie"
admin.site.index_title = "Gestion des Ressources Humaines et de la Paie"
