from django.urls import path
from . import views

app_name = 'hr_payroll'

urlpatterns = [

    # Tableau de 
    
    path('', views.home, name='home'),
    path('tableau-de-bord/', views.tableau_bord, name='tableau_bord'),
    path('tableau-bord-etendu/', views.tableau_bord_etendu, name='tableau_bord_etendu'),
    
    # Directions
    path('directions/', views.direction_list, name='direction_list'),
    path('directions/<uuid:pk>/', views.direction_detail, name='direction_detail'),
    path('directions/create/', views.direction_create, name='direction_create'),
    path('directions/<uuid:pk>/update/', views.direction_update, name='direction_update'),
    path('directions/<uuid:pk>/delete/', views.direction_delete, name='direction_delete'),
    
    # Bureaux
    path('bureaux/', views.bureau_list, name='bureau_list'),
    path('bureaux/<uuid:pk>/', views.bureau_detail, name='bureau_detail'),
    path('bureaux/create/', views.bureau_create, name='bureau_create'),
    path('bureaux/<uuid:pk>/update/', views.bureau_update, name='bureau_update'),
    path('bureaux/<uuid:pk>/delete/', views.bureau_delete, name='bureau_delete'),
    
    # Grades
    path('grades/', views.grade_list, name='grade_list'),
    path('grades/<uuid:pk>/', views.grade_detail, name='grade_detail'),
    path('grades/create/', views.grade_create, name='grade_create'),
    path('grades/<uuid:pk>/update/', views.grade_update, name='grade_update'),
    path('grades/<uuid:pk>/delete/', views.grade_delete, name='grade_delete'),
    
    # Éléments de paie
    path('elements-paie/', views.element_paie_list, name='element_paie_list'),
    path('elements-paie/<uuid:pk>/', views.element_paie_detail, name='element_paie_detail'),
    path('elements-paie/create/', views.element_paie_create, name='element_paie_create'),
    path('elements-paie/<uuid:pk>/update/', views.element_paie_update, name='element_paie_update'),
    path('elements-paie/<uuid:pk>/delete/', views.element_paie_delete, name='element_paie_delete'),
    
    # Grilles salariales
    path('grilles-salariales/', views.grille_salariale_list, name='grille_salariale_list'),
    path('grilles-salariales/<uuid:pk>/', views.grille_salariale_detail, name='grille_salariale_detail'),
    path('grilles-salariales/create/', views.grille_salariale_create, name='grille_salariale_create'),
    path('grilles-salariales/<uuid:pk>/update/', views.grille_salariale_update, name='grille_salariale_update'),
    path('grilles-salariales/<uuid:pk>/delete/', views.grille_salariale_delete, name='grille_salariale_delete'),
    
    # Agents
    path('agents/', views.agent_list, name='agent_list'),
    path('agents/<uuid:pk>/', views.agent_detail, name='agent_detail'),
    path('agents/create/', views.agent_create, name='agent_create'),
    path('agents/<uuid:pk>/update/', views.agent_update, name='agent_update'),
    path('agents/<uuid:pk>/delete/', views.agent_delete, name='agent_delete'),
    
    # Périodes de paie
    path('periodes/', views.periode_paie_list, name='periode_paie_list'),
    path('periodes/<uuid:pk>/', views.periode_paie_detail, name='periode_paie_detail'),
    path('periodes/create/', views.periode_paie_create, name='periode_paie_create'),
    path('periodes/<uuid:pk>/update/', views.periode_paie_update, name='periode_paie_update'),
    path('periodes/<uuid:pk>/delete/', views.periode_paie_delete, name='periode_paie_delete'),
    path('periodes/<uuid:pk>/fermer/', views.periode_paie_fermer, name='periode_paie_fermer'),
    
    # Mouvements de paie
    path('mouvements/', views.mouvement_paie_list, name='mouvement_paie_list'),
    path('mouvements/<uuid:pk>/', views.mouvement_paie_detail, name='mouvement_paie_detail'),
    path('mouvements/create/', views.mouvement_paie_create, name='mouvement_paie_create'),
    path('mouvements/<uuid:pk>/update/', views.mouvement_paie_update, name='mouvement_paie_update'),
    path('mouvements/<uuid:pk>/delete/', views.mouvement_paie_delete, name='mouvement_paie_delete'),
    
    # Calcul de paie
    path('calcul-paie/', views.calcul_paie, name='calcul_paie'),
    
    # Rapports
    path('rapports/', views.rapports, name='rapports'),
    
    # Archivage
    path('archivage/', views.archivage, name='archivage'),
    
    # ===== NOUVELLES URLS POUR SIGRH_PAIE =====
    
    # === GESTION DU CADRE ORGANIQUE (Postes budgétaires) ===
    path('postes-budgetaires/', views.poste_budgetaire_list, name='poste_budgetaire_list'),
    path('postes-budgetaires/<uuid:pk>/', views.poste_budgetaire_detail, name='poste_budgetaire_detail'),
    path('postes-budgetaires/create/', views.poste_budgetaire_create, name='poste_budgetaire_create'),
    path('postes-budgetaires/<uuid:pk>/update/', views.poste_budgetaire_update, name='poste_budgetaire_update'),
    path('postes-budgetaires/<uuid:pk>/delete/', views.poste_budgetaire_delete, name='poste_budgetaire_delete'),
    
    # === GESTION DES COMPÉTENCES ===
    path('competences/', views.competence_list, name='competence_list'),
    path('competences/<uuid:pk>/', views.competence_detail, name='competence_detail'),
    path('competences/create/', views.competence_create, name='competence_create'),
    path('competences/<uuid:pk>/update/', views.competence_update, name='competence_update'),
    path('competences/<uuid:pk>/delete/', views.competence_delete, name='competence_delete'),
    
    # === RENFORCEMENT DE CAPACITÉS (Formations) ===
    path('formations/', views.formation_list, name='formation_list'),
    path('formations/<uuid:pk>/', views.formation_detail, name='formation_detail'),
    path('formations/create/', views.formation_create, name='formation_create'),
    path('formations/<uuid:pk>/update/', views.formation_update, name='formation_update'),
    path('formations/<uuid:pk>/delete/', views.formation_delete, name='formation_delete'),
    
    # === GESTION DE CARRIÈRE (Affectations) ===
    path('affectations/', views.affectation_list, name='affectation_list'),
    path('affectations/<uuid:pk>/', views.affectation_detail, name='affectation_detail'),
    path('affectations/create/', views.affectation_create, name='affectation_create'),
    path('affectations/<uuid:pk>/update/', views.affectation_update, name='affectation_update'),
    path('affectations/<uuid:pk>/delete/', views.affectation_delete, name='affectation_delete'),
    
    # === GESTION DE CARRIÈRE (Promotions) ===
    path('promotions/', views.promotion_list, name='promotion_list'),
    path('promotions/<uuid:pk>/', views.promotion_detail, name='promotion_detail'),
    path('promotions/create/', views.promotion_create, name='promotion_create'),
    path('promotions/<uuid:pk>/update/', views.promotion_update, name='promotion_update'),
    path('promotions/<uuid:pk>/delete/', views.promotion_delete, name='promotion_delete'),
    
    # === GESTION DE CARRIÈRE (Mutations) ===
    path('mutations/', views.mutation_list, name='mutation_list'),
    path('mutations/<uuid:pk>/', views.mutation_detail, name='mutation_detail'),
    path('mutations/create/', views.mutation_create, name='mutation_create'),
    path('mutations/<uuid:pk>/update/', views.mutation_update, name='mutation_update'),
    path('mutations/<uuid:pk>/delete/', views.mutation_delete, name='mutation_delete'),
    
    # === COTATION (Évaluation des performances) ===
    path('cotations/', views.cotation_list, name='cotation_list'),
    path('cotations/<uuid:pk>/', views.cotation_detail, name='cotation_detail'),
    path('cotations/create/', views.cotation_create, name='cotation_create'),
    path('cotations/<uuid:pk>/update/', views.cotation_update, name='cotation_update'),
    path('cotations/<uuid:pk>/delete/', views.cotation_delete, name='cotation_delete'),
    path('cotations/<uuid:pk>/valider/', views.cotation_valider, name='cotation_valider'),
    
    # === ACTIONS DISCIPLINAIRES ===
    path('actions-disciplinaires/', views.action_disciplinaire_list, name='action_disciplinaire_list'),
    path('actions-disciplinaires/<uuid:pk>/', views.action_disciplinaire_detail, name='action_disciplinaire_detail'),
    path('actions-disciplinaires/create/', views.action_disciplinaire_create, name='action_disciplinaire_create'),
    path('actions-disciplinaires/<uuid:pk>/update/', views.action_disciplinaire_update, name='action_disciplinaire_update'),
    path('actions-disciplinaires/<uuid:pk>/delete/', views.action_disciplinaire_delete, name='action_disciplinaire_delete'),
    
    # === GESTION DES COMPÉTENCES DES AGENTS ===
    path('competences-agents/', views.competence_agent_list, name='competence_agent_list'),
    path('competences-agents/<uuid:pk>/', views.competence_agent_detail, name='competence_agent_detail'),
    path('competences-agents/create/', views.competence_agent_create, name='competence_agent_create'),
    path('competences-agents/<uuid:pk>/update/', views.competence_agent_update, name='competence_agent_update'),
    path('competences-agents/<uuid:pk>/delete/', views.competence_agent_delete, name='competence_agent_delete'),
    
    # === PARTICIPATION AUX FORMATIONS ===
    path('participations-formations/', views.participation_formation_list, name='participation_formation_list'),
    path('participations-formations/<uuid:pk>/', views.participation_formation_detail, name='participation_formation_detail'),
    path('participations-formations/create/', views.participation_formation_create, name='participation_formation_create'),
    path('participations-formations/<uuid:pk>/update/', views.participation_formation_update, name='participation_formation_update'),
    path('participations-formations/<uuid:pk>/delete/', views.participation_formation_delete, name='participation_formation_delete'),
    
    # === RAPPORTS ÉTENDUS ===
    path('rapports/cotations/', views.rapport_cotation, name='rapport_cotation'),
    path('rapports/formations/', views.rapport_formation, name='rapport_formation'),
    path('rapports/carriere/', views.rapport_carriere, name='rapport_carriere'),
    
    # === PORTAL AGENT ===
    path('portal-agent/', views.portal_agent, name='portal_agent'),


    # Pdf
    path('list_agent_pdf/', views.agent_list_pdf, name = "agent_list_pdf")
] 