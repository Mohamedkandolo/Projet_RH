from django import forms
from django.forms import ModelForm, inlineformset_factory
from .models import (
    Direction, Bureau, Grade, ElementPaie, GrilleSalariale, Agent,
    PeriodePaie, MouvementPaie, BulletinPaie, PosteBudgetaire, Competence,
    Formation, Affectation, Promotion, Mutation, Cotation, ActionDisciplinaire,
    CompetenceAgent, ParticipationFormation
)
from django.contrib.auth.models import User
from decimal import Decimal


class DirectionForm(ModelForm):
    class Meta:
        model = Direction
        fields = ['nom', 'code', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class BureauForm(ModelForm):
    class Meta:
        model = Bureau
        fields = ['nom', 'code', 'direction', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'direction': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class GradeForm(ModelForm):
    class Meta:
        model = Grade
        fields = ['nom', 'code', 'niveau', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'niveau': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ElementPaieForm(ModelForm):
    class Meta:
        model = ElementPaie
        fields = ['nom', 'code', 'type_element', 'description', 'calculable']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'type_element': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'calculable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class GrilleSalarialeForm(ModelForm):
    class Meta:
        model = GrilleSalariale
        fields = ['grade', 'element_paie', 'montant']
        widgets = {
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'element_paie': forms.Select(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

        def __init__(self, *args,**kwargs):
            super().__init__(self, **args, **kwargs)
            self.fields['element_paie'].queryset = ElementPaie.objects.filter(actif=True)


# ===== NOUVEAUX FORMULAIRES POUR SIGRH_PAIE =====

class PosteBudgetaireForm(ModelForm):
    """Formulaire pour la gestion du cadre organique"""
    class Meta:
        model = PosteBudgetaire
        fields = ['intitule', 'code', 'type_poste', 'grade_requis', 'bureau', 
                 'missions', 'competences_requises', 'position_hierarchique']
        widgets = {
            'intitule': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'type_poste': forms.Select(attrs={'class': 'form-control'}),
            'grade_requis': forms.Select(attrs={'class': 'form-control'}),
            'bureau': forms.Select(attrs={'class': 'form-control'}),
            'missions': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'competences_requises': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'position_hierarchique': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CompetenceForm(ModelForm):
    """Formulaire pour la gestion des compétences"""
    class Meta:
        model = Competence
        fields = ['nom', 'code', 'categorie', 'description', 'niveau_expertise']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'categorie': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'niveau_expertise': forms.Select(attrs={'class': 'form-control'}),
        }


class FormationForm(ModelForm):
    """Formulaire pour la gestion des formations (renforcement de capacités)"""
    class Meta:
        model = Formation
        fields = ['intitule', 'code', 'type_formation', 'description', 'duree_heures',
                 'cout_estime', 'lieu', 'date_debut', 'date_fin', 'nombre_places']
        widgets = {
            'intitule': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'type_formation': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'duree_heures': forms.NumberInput(attrs={'class': 'form-control'}),
            'cout_estime': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'lieu': forms.TextInput(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'nombre_places': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class AgentForm(ModelForm):
    """Formulaire complet pour l'engagement des agents"""
    class Meta:
        model = Agent
        fields = [
            # Identité
            'matricule','nom', 'prenoms', 'date_naissance', 'lieu_naissance', 'sexe',
            'nationalite', 'photo_identite', 'numero_identification',
            
            # État civil et dépendants
            'etat_civil', 'nom_conjoint', 'nombre_enfants', 'numero_securite_sociale',
            
            # Formations
            'diplome_principal', 'etablissement_formation', 'annee_obtention', 'specialite',
            
            # Données de santé (confidentielles)
            'visite_medicale_aptitude', 'date_visite_medicale', 'inaptitude_medicale', 'restrictions_medicales',
            
            # Antécédents juridiques
            'casier_judiciaire', 'commentaires_juridiques',
            
            # Informations professionnelles
            'grade', 'bureau', 'poste_budgetaire', 'date_embauche', 'date_nomination', 'statut',
            
            # Informations de contact
            'adresse', 'telephone', 'email',
            
            # Informations bancaires
            'banque', 'numero_compte'
        ]
        
        
        widgets = {

            'matricule' : forms.TextInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenoms': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lieu_naissance': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-control'}),
            'nationalite': forms.TextInput(attrs={'class': 'form-control'}),
            'photo_identite': forms.FileInput(attrs={'class': 'form-control'}),
            'numero_identification': forms.TextInput(attrs={'class': 'form-control'}),
            
            'etat_civil': forms.Select(attrs={'class': 'form-control'}),
            'nom_conjoint': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_enfants': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_securite_sociale': forms.TextInput(attrs={'class': 'form-control'}),
            
            'diplome_principal': forms.TextInput(attrs={'class': 'form-control'}),
            'etablissement_formation': forms.TextInput(attrs={'class': 'form-control'}),
            'annee_obtention': forms.NumberInput(attrs={'class': 'form-control'}),
            'specialite': forms.TextInput(attrs={'class': 'form-control'}),
            
            'visite_medicale_aptitude': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_visite_medicale': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'inaptitude_medicale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'restrictions_medicales': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            'casier_judiciaire': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'commentaires_juridiques': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            
            'grade': forms.Select(attrs={'class': 'form-control'}),
            'bureau': forms.Select(attrs={'class': 'form-control'}),
            'poste_budgetaire': forms.Select(attrs={'class': 'form-control'}),
            'date_embauche': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_nomination': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
            
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            
            'banque': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_compte': forms.TextInput(attrs={'class': 'form-control'}),
        }
        exclude = ('cree_par',)


class AffectationForm(ModelForm):
    """Formulaire pour la gestion des affectations (carrière)"""
    class Meta:
        model = Affectation
        fields = ['agent', 'bureau', 'poste_budgetaire', 'fonctions_exercees', 
                 'date_debut', 'date_fin', 'motif_affectation', 'decision_affectation']
        widgets = {
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'bureau': forms.Select(attrs={'class': 'form-control'}),
            'poste_budgetaire': forms.Select(attrs={'class': 'form-control'}),
            'fonctions_exercees': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motif_affectation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'decision_affectation': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PromotionForm(ModelForm):
    """Formulaire pour la gestion des promotions (carrière)"""
    class Meta:
        model = Promotion
        fields = ['agent', 'grade_ancien', 'grade_nouveau', 'type_promotion', 
                 'date_promotion', 'motif_promotion', 'anciennete_requise', 
                 'notation_requise', 'decision_promotion']
        widgets = {
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'grade_ancien': forms.Select(attrs={'class': 'form-control'}),
            'grade_nouveau': forms.Select(attrs={'class': 'form-control'}),
            'type_promotion': forms.Select(attrs={'class': 'form-control'}),
            'date_promotion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motif_promotion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'anciennete_requise': forms.NumberInput(attrs={'class': 'form-control'}),
            'notation_requise': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'decision_promotion': forms.TextInput(attrs={'class': 'form-control'}),
        }


class MutationForm(ModelForm):
    """Formulaire pour la gestion des mutations (carrière)"""
    class Meta:
        model = Mutation
        fields = ['agent', 'type_mutation', 'origine_bureau', 'destination_bureau', 
                 'date_mutation', 'motif_mutation', 'decision_mutation']
        widgets = {
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'type_mutation': forms.Select(attrs={'class': 'form-control'}),
            'origine_bureau': forms.Select(attrs={'class': 'form-control'}),
            'destination_bureau': forms.Select(attrs={'class': 'form-control'}),
            'date_mutation': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'motif_mutation': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'decision_mutation': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CotationForm(ModelForm):
    """Formulaire pour la cotation (évaluation des performances)"""
    class Meta:
        model = Cotation
        fields = ['agent', 'periode_evaluation', 'annee', 'semestre',
                 'comportement_professionnel', 'assiduite', 'resultats_objectifs',
                 'qualite_travail', 'esprit_equipe', 'appreciations', 
                 'points_forts', 'points_amelioration']
        widgets = {
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'periode_evaluation': forms.Select(attrs={'class': 'form-control'}),
            'annee': forms.NumberInput(attrs={'class': 'form-control'}),
            'semestre': forms.Select(attrs={'class': 'form-control'}),
            'comportement_professionnel': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '20'}),
            'assiduite': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '20'}),
            'resultats_objectifs': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '20'}),
            'qualite_travail': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '20'}),
            'esprit_equipe': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '20'}),
            'appreciations': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'points_forts': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'points_amelioration': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        


class ActionDisciplinaireForm(ModelForm):
    """Formulaire pour la gestion des actions disciplinaires"""
    class Meta:
        model = ActionDisciplinaire
        fields = ['agent', 'type_faute', 'description_faute', 'date_faute', 'lieu_faute',
                 'date_notification', 'commission_disciplinaire', 'date_commission',
                 'type_sanction', 'duree_sanction', 'motif_sanction']
        widgets = {
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'type_faute': forms.Select(attrs={'class': 'form-control'}),
            'description_faute': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'date_faute': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lieu_faute': forms.TextInput(attrs={'class': 'form-control'}),
            'date_notification': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'commission_disciplinaire': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'date_commission': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'type_sanction': forms.Select(attrs={'class': 'form-control'}),
            'duree_sanction': forms.NumberInput(attrs={'class': 'form-control'}),
            'motif_sanction': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CompetenceAgentForm(ModelForm):
    """Formulaire pour la gestion des compétences des agents"""
    class Meta:
        model = CompetenceAgent
        fields = ['agent', 'competence', 'niveau_maitrise', 'date_evaluation', 'commentaires']
        widgets = {
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'competence': forms.Select(attrs={'class': 'form-control'}),
            'niveau_maitrise': forms.Select(attrs={'class': 'form-control'}),
            'date_evaluation': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'commentaires': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class ParticipationFormationForm(ModelForm):
    """Formulaire pour la gestion des participations aux formations"""
    class Meta:
        model = ParticipationFormation
        fields = ['agent', 'formation', 'statut_participation', 'note_formation',
                 'appreciation_formation', 'impact_formation', 'mise_en_pratique', 'cout_participation']
        widgets = {
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'formation': forms.Select(attrs={'class': 'form-control'}),
            'statut_participation': forms.Select(attrs={'class': 'form-control'}),
            'note_formation': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0', 'max': '20'}),
            'appreciation_formation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'impact_formation': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'mise_en_pratique': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'cout_participation': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }


# ===== FORMULAIRES EXISTANTS POUR LA PAIE =====

class PeriodePaieForm(ModelForm):
    class Meta:
        model = PeriodePaie
        fields = ['annee', 'mois', 'date_debut', 'date_fin', 'commentaire']
        widgets = {
            'annee': forms.NumberInput(attrs={'class': 'form-control'}),
            'mois': forms.Select(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class MouvementPaieForm(ModelForm):
    class Meta:
        model = MouvementPaie
        fields = ['periode', 'agent', 'element_paie', 'montant', 'commentaire']
        widgets = {
            'periode': forms.Select(attrs={'class': 'form-control'}),
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'element_paie': forms.Select(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        periode = kwargs.pop('periode', None)
        super().__init__(*args, **kwargs)
        if periode:
            # Filtrer les agents actifs pour cette période
            self.fields['agent'].queryset = Agent.objects.filter(actif=True, statut='ACTIF')


class BulletinPaieForm(ModelForm):
    class Meta:
        model = BulletinPaie
        fields = ['agent', 'nombre_jours_travailles', 'nombre_heures_travaillees', 'commentaire']
        widgets = {
            'agent': forms.Select(attrs={'class': 'form-control'}),
            'nombre_jours_travailles': forms.NumberInput(attrs={'class': 'form-control'}),
            'nombre_heures_travaillees': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        periode = kwargs.pop('periode', None)
        super().__init__(*args, **kwargs)
        if periode:
            # Filtrer les agents actifs pour cette période
            self.fields['agent'].queryset = Agent.objects.filter(actif=True, statut='ACTIF')


# ===== FORMULAIRES DE RECHERCHE ET FILTRES ÉTENDUS =====

class RechercheAgentForm(forms.Form):
    nom = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}))
    matricule = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Matricule'}))
    grade = forms.ModelChoiceField(queryset=Grade.objects.filter(actif=True), required=False, 
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    bureau = forms.ModelChoiceField(queryset=Bureau.objects.filter(actif=True), required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    statut = forms.ChoiceField(choices=[('', 'Tous')] + Agent.STATUT_CHOICES, required=False,
                             widget=forms.Select(attrs={'class': 'form-control'}))
    etat_civil = forms.ChoiceField(choices=[('', 'Tous')] + [
        ('CELIBATAIRE', 'Célibataire'),
        ('MARIE', 'Marié(e)'),
        ('DIVORCE', 'Divorcé(e)'),
        ('VEUF', 'Veuf/Veuve'),
    ], required=False, widget=forms.Select(attrs={'class': 'form-control'}))


class RechercheCotationForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.filter(actif=True), required=False,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    annee = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Année'}))
    semestre = forms.ChoiceField(choices=[('', 'Tous'), (1, '1er semestre'), (2, '2ème semestre')], 
                               required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    note_min = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Note min'}))
    note_max = forms.DecimalField(required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Note max'}))


class RechercheFormationForm(forms.Form):
    intitule = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Intitulé'}))
    type_formation = forms.ChoiceField(choices=[('', 'Tous')] + Formation.TYPE_CHOICES, 
                                     required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    statut = forms.ChoiceField(choices=[('', 'Tous')] + [
        ('PLANIFIEE', 'Planifiée'),
        ('EN_COURS', 'En cours'),
        ('TERMINEE', 'Terminée'),
        ('ANNULEE', 'Annulée'),
    ], required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    date_debut = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))


class RechercheActionDisciplinaireForm(forms.Form):
    agent = forms.ModelChoiceField(queryset=Agent.objects.filter(actif=True), required=False,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    type_faute = forms.ChoiceField(choices=[('', 'Tous')] + ActionDisciplinaire.type_faute.field.choices, 
                                 required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    statut = forms.ChoiceField(choices=[('', 'Tous')] + ActionDisciplinaire.statut.field.choices, 
                             required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    date_debut = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_fin = forms.DateField(required=False, widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))


# ===== FORMULAIRES POUR LES RAPPORTS ÉTENDUS =====

class RapportCotationForm(forms.Form):
    TYPE_RAPPORT_CHOICES = [
        ('individuel', 'Cotation individuelle'),
        ('collectif', 'Cotation collective'),
        ('comparatif', 'Comparatif des performances'),
        ('evolution', 'Évolution des performances'),
    ]
    
    type_rapport = forms.ChoiceField(choices=TYPE_RAPPORT_CHOICES, 
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    annee = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    semestre = forms.ChoiceField(choices=[(1, '1er semestre'), (2, '2ème semestre')], 
                               required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    direction = forms.ModelChoiceField(queryset=Direction.objects.filter(actif=True), required=False,
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    bureau = forms.ModelChoiceField(queryset=Bureau.objects.filter(actif=True), required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    grade = forms.ModelChoiceField(queryset=Grade.objects.filter(actif=True), required=False,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    format_export = forms.ChoiceField(choices=[('pdf', 'PDF'), ('excel', 'Excel'), ('csv', 'CSV')],
                                    widget=forms.Select(attrs={'class': 'form-control'}))


class RapportFormationForm(forms.Form):
    TYPE_RAPPORT_CHOICES = [
        ('planification', 'Planification des formations'),
        ('participation', 'Taux de participation'),
        ('evaluation', 'Évaluation des formations'),
        ('cout', 'Analyse des coûts'),
    ]
    
    type_rapport = forms.ChoiceField(choices=TYPE_RAPPORT_CHOICES, 
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    periode_debut = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    periode_fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    type_formation = forms.ChoiceField(choices=[('', 'Tous')] + Formation.TYPE_CHOICES, 
                                     required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    format_export = forms.ChoiceField(choices=[('pdf', 'PDF'), ('excel', 'Excel'), ('csv', 'CSV')],
                                    widget=forms.Select(attrs={'class': 'form-control'}))


class RapportCarriereForm(forms.Form):
    TYPE_RAPPORT_CHOICES = [
        ('affectations', 'Historique des affectations'),
        ('promotions', 'Historique des promotions'),
        ('mutations', 'Historique des mutations'),
        ('evolution', 'Évolution de carrière'),
    ]
    
    type_rapport = forms.ChoiceField(choices=TYPE_RAPPORT_CHOICES, 
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    agent = forms.ModelChoiceField(queryset=Agent.objects.filter(actif=True), required=False,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    date_debut = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    date_fin = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    direction = forms.ModelChoiceField(queryset=Direction.objects.filter(actif=True), required=False,
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    format_export = forms.ChoiceField(choices=[('pdf', 'PDF'), ('excel', 'Excel'), ('csv', 'CSV')],
                                    widget=forms.Select(attrs={'class': 'form-control'}))


# ===== FORMULAIRES EXISTANTS POUR LA PAIE =====

class RechercheMouvementForm(forms.Form):
    periode = forms.ModelChoiceField(queryset=PeriodePaie.objects.all(), required=False,
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    agent = forms.ModelChoiceField(queryset=Agent.objects.filter(actif=True), required=False,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    element_paie = forms.ModelChoiceField(queryset=ElementPaie.objects.filter(actif=True), required=False,
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    type_element = forms.ChoiceField(choices=[('', 'Tous')] + ElementPaie.TYPE_CHOICES, required=False,
                                   widget=forms.Select(attrs={'class': 'form-control'}))


class CalculPaieForm(forms.Form):
    periode = forms.ModelChoiceField(queryset=PeriodePaie.objects.filter(statut='OUVERTE'), 
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    agent = forms.ModelChoiceField(queryset=Agent.objects.filter(actif=True, statut='ACTIF'), required=False,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    calculer_tous = forms.BooleanField(required=False, initial=True,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    forcer_recalcul = forms.BooleanField(required=False, initial=False,
                                       widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def clean(self):
        cleaned_data = super().clean()
        agent = cleaned_data.get('agent')
        calculer_tous = cleaned_data.get('calculer_tous')
        if not calculer_tous and not agent:
            self.add_error('agent', "Veuillez sélectionner un agent ou cocher 'Calculer tous'.")
        return cleaned_data


# Formulaires pour les rapports
class RapportPaieForm(forms.Form):
    TYPE_RAPPORT_CHOICES = [
        ('bulletin', 'Bulletins de paie'),
        ('mouvements', 'Mouvements de paie'),
        ('statistiques', 'Statistiques'),
        ('comparatif', 'Comparatif mensuel'),
    ]
    
    type_rapport = forms.ChoiceField(choices=TYPE_RAPPORT_CHOICES, 
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    periode_debut = forms.ModelChoiceField(queryset=PeriodePaie.objects.all(), required=False,
                                         widget=forms.Select(attrs={'class': 'form-control'}))
    periode_fin = forms.ModelChoiceField(queryset=PeriodePaie.objects.all(), required=False,
                                       widget=forms.Select(attrs={'class': 'form-control'}))
    direction = forms.ModelChoiceField(queryset=Direction.objects.filter(actif=True), required=False,
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    bureau = forms.ModelChoiceField(queryset=Bureau.objects.filter(actif=True), required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}))
    grade = forms.ModelChoiceField(queryset=Grade.objects.filter(actif=True), required=False,
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    format_export = forms.ChoiceField(choices=[('pdf', 'PDF'), ('excel', 'Excel'), ('csv', 'CSV')],
                                    widget=forms.Select(attrs={'class': 'form-control'}))


# Formulaires pour l'archivage
class ArchivageForm(forms.Form):
    periode = forms.ModelChoiceField(queryset=PeriodePaie.objects.filter(statut='FERMEE'), 
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    commentaire = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}))
    confirmer_archivage = forms.BooleanField(required=True,
                                           widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


# Formulaires pour les imports/exports
class ImportAgentsForm(forms.Form):
    fichier = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    format_fichier = forms.ChoiceField(choices=[('excel', 'Excel'), ('csv', 'CSV')],
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    ecraser_existants = forms.BooleanField(required=False, initial=False,
                                         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))


class ImportMouvementsForm(forms.Form):
    fichier = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    periode = forms.ModelChoiceField(queryset=PeriodePaie.objects.filter(statut='OUVERTE'),
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    format_fichier = forms.ChoiceField(choices=[('excel', 'Excel'), ('csv', 'CSV')],
                                     widget=forms.Select(attrs={'class': 'form-control'}))
    ecraser_existants = forms.BooleanField(required=False, initial=False,
                                         widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})) 