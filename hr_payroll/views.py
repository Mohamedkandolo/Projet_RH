from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum, Count, Q
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime, date
import json

from .models import (
    Direction, Bureau, Grade, ElementPaie, GrilleSalariale, Agent,
    PeriodePaie, MouvementPaie, BulletinPaie, HistoriquePaie,
    PosteBudgetaire, Competence, Formation, Affectation, Promotion, Mutation, Cotation, ActionDisciplinaire, CompetenceAgent, ParticipationFormation
)
from .forms import (
    DirectionForm, BureauForm, GradeForm, ElementPaieForm, GrilleSalarialeForm,
    AgentForm, PeriodePaieForm, MouvementPaieForm, BulletinPaieForm,
    RechercheAgentForm, RechercheMouvementForm, CalculPaieForm, RapportPaieForm,
    ArchivageForm, ImportAgentsForm, ImportMouvementsForm,
    PosteBudgetaireForm, CompetenceForm, FormationForm, AffectationForm, PromotionForm, MutationForm, CotationForm, ActionDisciplinaireForm, CompetenceAgentForm, ParticipationFormationForm, RapportCotationForm, RapportFormationForm, RapportCarriereForm
)
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from xhtml2pdf import pisa

User = get_user_model()


# Accueil
@login_required
def home(request):
    return render(request, 'hr_payroll/home.html')




# Vues pour les directions
@login_required
def direction_list(request):
    directions = Direction.objects.filter(actif=True).order_by('nom')
    return render(request, 'hr_payroll/direction_list.html', {'directions': directions})


@login_required
def direction_detail(request, pk):
    direction = get_object_or_404(Direction, pk=pk)
    bureaux = direction.bureaux.filter(actif=True)
    return render(request, 'hr_payroll/direction_detail.html', {
        'direction': direction,
        'bureaux': bureaux
    })


@login_required
def direction_create(request):
    if request.method == 'POST':
        form = DirectionForm(request.POST)
        if form.is_valid():
            direction = form.save()
            messages.success(request, 'Direction créée avec succès.')
            return redirect('hr_payroll:direction_detail', pk=direction.pk)
    else:
        form = DirectionForm()
    
    return render(request, 'hr_payroll/direction_form.html', {'form': form, 'title': 'Nouvelle Direction'})


@login_required
def direction_update(request, pk):
    direction = get_object_or_404(Direction, pk=pk)
    if request.method == 'POST':
        form = DirectionForm(request.POST, instance=direction)
        if form.is_valid():
            form.save()
            messages.success(request, 'Direction mise à jour avec succès.')
            return redirect('hr_payroll:direction_detail', pk=direction.pk)
    else:
        form = DirectionForm(instance=direction)
    
    return render(request, 'hr_payroll/direction_form.html', {
        'form': form, 
        'direction': direction,
        'title': 'Modifier la Direction'
    })


@login_required
def direction_delete(request, pk):
    direction = get_object_or_404(Direction, pk=pk)
    if request.method == 'POST':
        direction.actif = False
        direction.save()
        messages.success(request, 'Direction supprimée avec succès.')
        return redirect('hr_payroll:direction_list')
    
    return render(request, 'payroll/direction_confirm_delete.html', {'direction': direction})


# Vues pour les bureaux
@login_required
def bureau_list(request):
    bureaux = Bureau.objects.filter(actif=True).select_related('direction').order_by('direction__nom', 'nom')
    return render(request, 'hr_payroll/bureau_list.html', {'bureaux': bureaux})


@login_required
def bureau_detail(request, pk):
    bureau = get_object_or_404(Bureau, pk=pk)
    agents = bureau.agents.filter(actif=True).select_related('grade')
    agents_actifs_count = agents.filter(statut='ACTIF').count()
    return render(request, 'hr_payroll/bureau_detail.html', {
        'bureau': bureau,
        'agents': agents,
        'agents_actifs_count': agents_actifs_count
    })


@login_required
def bureau_create(request):
    if request.method == 'POST':
        form = BureauForm(request.POST)
        if form.is_valid():
            bureau = form.save()
            messages.success(request, 'Bureau créé avec succès.')
            return redirect('hr_payroll:bureau_detail', pk=bureau.pk)
    else:
        form = BureauForm()
    
    return render(request, 'hr_payroll/bureau_form.html', {'form': form, 'title': 'Nouveau Bureau'})


@login_required
def bureau_update(request, pk):
    bureau = get_object_or_404(Bureau, pk=pk)
    if request.method == 'POST':
        form = BureauForm(request.POST, instance=bureau)
        if form.is_valid():
            form.save()
            messages.success(request, 'Bureau mis à jour avec succès.')
            return redirect('hr_payroll:bureau_detail', pk=bureau.pk)
    else:
        form = BureauForm(instance=bureau)
    
    return render(request, 'hr_payroll/bureau_form.html', {
        'form': form, 
        'bureau': bureau,
        'title': 'Modifier le Bureau'
    })


@login_required
def bureau_delete(request, pk):
    bureau = get_object_or_404(Bureau, pk=pk)
    if request.method == 'POST':
        bureau.actif = False
        bureau.save()
        messages.success(request, 'Bureau supprimé avec succès.')
        return redirect('hr_payroll:bureau_list')
    
    return render(request, 'hr_payroll/bureau_confirm_delete.html', {'bureau': bureau})


# Vues pour les grades
@login_required
def grade_list(request):
    grades = Grade.objects.filter(actif=True).order_by('niveau', 'nom')
    return render(request, 'hr_payroll/grade_list.html', {'grades': grades})


@login_required
def grade_detail(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    agents = grade.agents.filter(actif=True).select_related('bureau')
    grilles = grade.grilles_salariales.filter(actif=True).select_related('element_paie')
    return render(request, 'hr_payroll/grade_detail.html', {
        'grade': grade,
        'agents': agents,
        'grilles': grilles
    })


@login_required
def grade_create(request):
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save()
            messages.success(request, 'Grade créé avec succès.')
            return redirect('hr_payroll:grade_detail', pk=grade.pk)
    else:
        form = GradeForm()
    
    return render(request, 'hr_payroll/grade_form.html', {'form': form, 'title': 'Nouveau Grade'})


@login_required
def grade_update(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=grade)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grade mis à jour avec succès.')
            return redirect('hr_payroll:grade_detail', pk=grade.pk)
    else:
        form = GradeForm(instance=grade)
    
    return render(request, 'hr_payroll/grade_form.html', {
        'form': form, 
        'grade': grade,
        'title': 'Modifier le Grade'
    })


@login_required
def grade_delete(request, pk):
    grade = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        grade.actif = False
        grade.save()
        messages.success(request, 'Grade supprimé avec succès.')
        return redirect('hr_payroll:grade_list')
    
    return render(request, 'hr_payroll/grade_confirm_delete.html', {'grade': grade})


# Vues pour les éléments de paie
@login_required
def element_paie_list(request):
    elements_paie = ElementPaie.objects.filter(actif=True).order_by('type_element', 'nom')
    return render(request, 'hr_payroll/element_paie_list.html', {'elements_paie': elements_paie})


@login_required
def element_paie_detail(request, pk):
    element = get_object_or_404(ElementPaie, pk=pk)
    grilles = element.grilles_salariales.all().select_related('grade')
    return render(request, 'hr_payroll/element_paie_detail.html', {
        'element': element,
        'grilles': grilles
    })


@login_required
def element_paie_create(request):
    if request.method == 'POST':
        form = ElementPaieForm(request.POST)
        if form.is_valid():
            element = form.save()
            messages.success(request, 'Élément de paie créé avec succès.')
            return redirect('hr_payroll:element_paie_detail', pk=element.pk)
    else:
        form = ElementPaieForm()
    
    return render(request, 'hr_payroll/element_paie_form.html', {'form': form, 'title': 'Nouvel Élément de Paie'})


@login_required
def element_paie_update(request, pk):
    element = get_object_or_404(ElementPaie, pk=pk)
    if request.method == 'POST':
        form = ElementPaieForm(request.POST, instance=element)
        if form.is_valid():
            form.save()
            messages.success(request, 'Élément de paie mis à jour avec succès.')
            return redirect('hr_payroll:element_paie_detail', pk=element.pk)
    else:
        form = ElementPaieForm(instance=element)
    
    return render(request, 'hr_payroll/element_paie_form.html', {
        'form': form, 
        'element': element,
        'title': 'Modifier l\'Élément de Paie'
    })


@login_required
def element_paie_delete(request, pk):
    element = get_object_or_404(ElementPaie, pk=pk)
    if request.method == 'POST':
       element.actif = False
       element.save()
       messages.success(request, 'Élément de paie supprimé avec succès.')
       return redirect('hr_payroll:element_paie_list')
        
    return render(request, 'hr_payroll/element_paie_confirm_delete.html', {'element': element})


# Vues pour les grilles salariales
@login_required
def grille_salariale_list(request):
    grilles = GrilleSalariale.objects.all().select_related(
        'grade', 'element_paie'
    ).order_by('grade__niveau', 'element_paie__type_element', 'element_paie__nom')
    
    paginator = Paginator(grilles, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'hr_payroll/grille_salariale_list.html', {
        'page_obj': page_obj
    })


@login_required
def grille_salariale_detail(request, pk):
    grille = get_object_or_404(GrilleSalariale, pk=pk)
    return render(request, 'hr_payroll/grille_salariale_detail.html', {
        'grille': grille
    })


@login_required
def grille_salariale_create(request):
    if request.method == 'POST':
        form = GrilleSalarialeForm(request.POST)
        if form.is_valid():
            grille = form.save(commit=False)
            grille.save()
            messages.success(request, 'Grille salariale créée avec succès.')
            return redirect('hr_payroll:grille_salariale_list')
    else:
        form = GrilleSalarialeForm()
    
    return render(request, 'hr_payroll/grille_salariale_form.html', {
        'form': form, 
        'title': 'Nouvelle Grille Salariale'
    })


@login_required
def grille_salariale_update(request, pk):
    grille = get_object_or_404(GrilleSalariale, pk=pk)
    if request.method == 'POST':
        form = GrilleSalarialeForm(request.POST, instance=grille)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grille salariale mise à jour avec succès.')
            return redirect('hr_payroll:grille_salariale_list')
    else:
        form = GrilleSalarialeForm(instance=grille)
    
    return render(request, 'hr_payroll/grille_salariale_form.html', {
        'form': form, 
        'grille': grille,
        'title': 'Modifier la Grille Salariale'
    })


@login_required
def grille_salariale_delete(request, pk):
    grille = get_object_or_404(GrilleSalariale, pk=pk)
    if request.method == 'POST':
        grille.delete()
        messages.success(request, 'Grille salariale supprimée avec succès.')
        return redirect('hr_payroll:grille_salariale_list')
    
    return render(request, 'hr_payroll/grille_salariale_confirm_delete.html', {'grille': grille})


# Vues pour les agents
@login_required
def agent_list(request):
    form = RechercheAgentForm(request.GET)
    agents = Agent.objects.filter(actif=True).select_related('grade', 'bureau', 'bureau__direction')
    
    if form.is_valid():
        if form.cleaned_data['nom']:
            agents = agents.filter(nom__icontains=form.cleaned_data['nom'])
        if form.cleaned_data['matricule']:
            agents = agents.filter(matricule__icontains=form.cleaned_data['matricule'])
        if form.cleaned_data['grade']:
            agents = agents.filter(grade=form.cleaned_data['grade'])
        if form.cleaned_data['bureau']:
            agents = agents.filter(bureau=form.cleaned_data['bureau'])
        if form.cleaned_data['statut']:
            agents = agents.filter(statut=form.cleaned_data['statut'])
    
    paginator = Paginator(agents, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'form': form
    }

    return render(request, 'hr_payroll/agent_list.html', context)




# Génération d'un fichier pdf pour la liste des agent
def agent_list_pdf(request):

    agents = Agent.objects.filter(actif=True).select_related('grade', 'bureau', 'bureau__direction')
    
    

    context = {
        'agents': agents,
    }

    template_path = 'hr_payroll/agent_list_pdf.html'
    template = get_template(template_path)
    html = template.render(context)

    reponse = HttpResponse(content_type = 'hr_payroll/pdf')
    reponse['content-display']= "attachemnt; filename = 'agent.pdf'"
    pisa_status = pisa.CreatePDF(html, dest=reponse)
    if pisa_status.err:
        return HttpResponse('Erreur lors de la génération de PDF', status = 500)
    return reponse






#@login_required
def agent_detail(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    grille_ag = GrilleSalariale.objects.filter(grade = agent.grade)
    bulletins = agent.bulletins.all().order_by('-periode__annee', '-periode__mois')[:12]
    return render(request, 'hr_payroll/agent_detail.html', {
        'agent': agent,
        'bulletins': bulletins, 
        'grille' : grille_ag
    })


@login_required
def agent_create(request):
    
    if request.method == 'POST':
        form = AgentForm(request.POST, request.FILES)
        if form.is_valid():
            agent = form.save(commit=False)
            agent.cree_par = request.user
            agent.save()
            messages.success(request, 'Agent créé avec succès.')
            return redirect('hr_payroll:agent_detail', pk=agent.pk)
    else:
        form = AgentForm()
    
    return render(request, 'hr_payroll/agent_form.html', {'form': form, 'title': 'Nouvel Agent'})


@login_required
def agent_update(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        form = AgentForm(request.POST, instance=agent)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agent mis à jour avec succès.')
            return redirect('hr_payroll:agent_detail', pk=agent.pk)
    else:
        form = AgentForm(instance=agent)
    
    return render(request, 'hr_payroll/agent_form.html', {
        'form': form, 
        'agent': agent,
        'title': 'Modifier l\'Agent'
    })


@login_required
def agent_delete(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        agent.actif = False
        agent.save()
        messages.success(request, 'Agent supprimé avec succès.')
        return redirect('hr_payroll:agent_list')
    
    return render(request, 'hr_payroll/agent_confirm_delete.html', {'agent': agent})


# Vues pour les périodes de paie
@login_required
def periode_paie_list(request):
    periodes = PeriodePaie.objects.all().order_by('-annee', '-mois')
    
    # Calculer les statistiques
    periodes_ouvertes_count = periodes.filter(statut='OUVERTE').count()
    periodes_fermees_count = periodes.filter(statut='FERMEE').count()
    periodes_archivees_count = periodes.filter(statut='ARCHIVEE').count()
    
    return render(request, 'hr_payroll/periode_paie_list.html', {
        'periodes': periodes,
        'periodes_ouvertes_count': periodes_ouvertes_count,
        'periodes_fermees_count': periodes_fermees_count,
        'periodes_archivees_count': periodes_archivees_count,
    })


@login_required
def periode_paie_detail(request, pk):
    periode = get_object_or_404(PeriodePaie, pk=pk)
    bulletins = periode.bulletins.all().select_related('agent', 'agent__grade', 'agent__bureau')
    mouvements = periode.mouvements.all().select_related('agent', 'element_paie')
    
    # Statistiques
    total_gains = bulletins.aggregate(total=Sum('total_gains'))['total'] or 0
    total_retenues = bulletins.aggregate(total=Sum('total_retenues'))['total'] or 0
    total_cotisations = bulletins.aggregate(total=Sum('total_cotisations'))['total'] or 0
    net_total = bulletins.aggregate(total=Sum('net_a_payer'))['total'] or 0
    
    return render(request, 'hr_payroll/periode_paie_detail.html', {
        'periode': periode,
        'bulletins': bulletins,
        'mouvements': mouvements,
        'total_gains': total_gains,
        'total_retenues': total_retenues,
        'total_cotisations': total_cotisations,
        'net_total': net_total
    })


@login_required
def periode_paie_create(request):
    if request.method == 'POST':
        form = PeriodePaieForm(request.POST)
        if form.is_valid():
            periode = form.save()
            messages.success(request, 'Période de paie créée avec succès.')
            return redirect('hr_payroll:periode_paie_detail', pk=periode.pk)
    else:
        form = PeriodePaieForm()
    
    return render(request, 'hr_payroll/periode_paie_form.html', {'form': form, 'title': 'Nouvelle Période de Paie'})


@login_required
def periode_paie_fermer(request, pk):
    periode = get_object_or_404(PeriodePaie, pk=pk)
    if request.method == 'POST':
        if periode.statut == 'OUVERTE':
            periode.statut = 'FERMEE'
            periode.date_fermeture = timezone.now()
            periode.save()
            messages.success(request, 'Période de paie fermée avec succès.')
        else:
            messages.error(request, 'Cette période ne peut pas être fermée.')
        return redirect('hr_payroll:periode_paie_detail', pk=periode.pk)
    
    return render(request, 'hr_payroll/periode_paie_confirm_fermer.html', {'periode': periode})


@login_required
def periode_paie_update(request, pk):
    periode = get_object_or_404(PeriodePaie, pk=pk)
    if request.method == 'POST':
        form = PeriodePaieForm(request.POST, instance=periode)
        if form.is_valid():
            form.save()
            messages.success(request, 'Période de paie mise à jour avec succès.')
            return redirect('hr_payroll:periode_paie_detail', pk=periode.pk)
    else:
        form = PeriodePaieForm(instance=periode)
    
    return render(request, 'hr_payroll/periode_paie_form.html', {
        'form': form, 
        'periode': periode,
        'title': 'Modifier la Période de Paie'
    })


@login_required
def periode_paie_delete(request, pk):
    periode = get_object_or_404(PeriodePaie, pk=pk)
    if request.method == 'POST':
        periode.delete()
        messages.success(request, 'Période de paie supprimée avec succès.')
        return redirect('hr_payroll:periode_paie_list')
    
    return render(request, 'hr_payroll/periode_paie_confirm_delete.html', {'periode': periode})


# Vues pour les mouvements de paie
@login_required
def mouvement_paie_list(request):
    form = RechercheMouvementForm(request.GET)
    mouvements = MouvementPaie.objects.all().select_related(
        'periode', 'agent', 'agent__grade', 'element_paie'
    )
    
    if form.is_valid():
        if form.cleaned_data['periode']:
            mouvements = mouvements.filter(periode=form.cleaned_data['periode'])
        if form.cleaned_data['agent']:
            mouvements = mouvements.filter(agent=form.cleaned_data['agent'])
        if form.cleaned_data['element_paie']:
            mouvements = mouvements.filter(element_paie=form.cleaned_data['element_paie'])
        if form.cleaned_data['type_element']:
            mouvements = mouvements.filter(element_paie__type_element=form.cleaned_data['type_element'])
    
    paginator = Paginator(mouvements, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'hr_payroll/mouvement_paie_list.html', {
        'page_obj': page_obj,
        'form': form
    })


@login_required
def mouvement_paie_detail(request, pk):
    mouvement = get_object_or_404(MouvementPaie, pk=pk)
    return render(request, 'hr_payroll/mouvement_paie_detail.html', {
        'mouvement': mouvement
    })


@login_required
def mouvement_paie_create(request):
    if request.method == 'POST':
        form = MouvementPaieForm(request.POST)
        if form.is_valid():
            mouvement = form.save(commit=False)
            mouvement.cree_par = request.user
            mouvement.save()
            messages.success(request, 'Mouvement de paie créé avec succès.')
            return redirect('hr_payroll:mouvement_paie_list')
    else:
        form = MouvementPaieForm()
    
    return render(request, 'hr_payroll/mouvement_paie_form.html', {'form': form, 'title': 'Nouveau Mouvement'})


@login_required
def mouvement_paie_update(request, pk):
    mouvement = get_object_or_404(MouvementPaie, pk=pk)
    if request.method == 'POST':
        form = MouvementPaieForm(request.POST, instance=mouvement)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mouvement de paie mis à jour avec succès.')
            return redirect('hr_payroll:mouvement_paie_list')
    else:
        form = MouvementPaieForm(instance=mouvement)
    
    return render(request, 'hr_payroll/mouvement_paie_form.html', {
        'form': form, 
        'mouvement': mouvement,
        'title': 'Modifier le Mouvement'
    })


@login_required
def mouvement_paie_delete(request, pk):
    mouvement = get_object_or_404(MouvementPaie, pk=pk)
    if request.method == 'POST':
        mouvement.delete()
        messages.success(request, 'Mouvement de paie supprimé avec succès.')
        return redirect('hr_payroll:mouvement_paie_list')
    
    return render(request, 'hr_payroll/mouvement_paie_confirm_delete.html', {'mouvement': mouvement})


# Vues pour le calcul de paie
@login_required
def calcul_paie(request):
    if request.method == 'POST':
        form = CalculPaieForm(request.POST)
        if form.is_valid():
            periode = form.cleaned_data['periode']
            agent = form.cleaned_data['agent']
            calculer_tous = form.cleaned_data['calculer_tous']
            forcer_recalcul = form.cleaned_data['forcer_recalcul']

            if calculer_tous:
                agents = Agent.objects.filter(actif=True, statut='ACTIF')
            else:
                agents = [agent] if agent else []

            bulletins_calcules = []
            for agent in agents:
                # Générer automatiquement les mouvements de paie selon la grille salariale
                grilles = GrilleSalariale.objects.filter(grade=agent.grade, actif=True)
                for grille in grilles:
                    montant = grille.montant
                    # Si pourcentage, appliquer sur la base (ex: salaire de base ou autre)
                    if grille.montant == 'salaire_base' and hasattr(agent, 'salaire_base'):
                            base = agent.salaire_base
                    else:
                        base = montant
                    MouvementPaie.objects.update_or_create(
                        periode=periode,
                        agent=agent,
                        element_paie=grille.element_paie,
                        defaults={
                            'montant': montant,
                            'cree_par': request.user
                        }
                    )

                bulletin, created = BulletinPaie.objects.get_or_create(
                    periode=periode,
                    agent=agent,
                    defaults={'calcule_par': request.user}
                )

                if created or forcer_recalcul:
                    mouvements_gains = MouvementPaie.objects.filter(
                        periode=periode,
                        agent=agent,
                        element_paie__type_element='GAIN'
                    ).aggregate(total=Sum('montant'))['total'] or 0

                    mouvements_retenues = MouvementPaie.objects.filter(
                        periode=periode,
                        agent=agent,
                        element_paie__type_element='RETENUE'
                    ).aggregate(total=Sum('montant'))['total'] or 0

                    mouvements_cotisations = MouvementPaie.objects.filter(
                        periode=periode,
                        agent=agent,
                        element_paie__type_element='COTISATION'
                    ).aggregate(total=Sum('montant'))['total'] or 0

                    bulletin.total_gains = mouvements_gains
                    bulletin.total_retenues = mouvements_retenues
                    bulletin.total_cotisations = mouvements_cotisations
                    bulletin.calculer_net_a_payer()
                    bulletin.calcule_par = request.user
                    bulletin.save()

                bulletins_calcules.append(bulletin)

            messages.success(request, f'{len(bulletins_calcules)} bulletins calculés avec succès.')
            return redirect('hr_payroll:periode_paie_detail', pk=periode.pk)
    else:
        form = CalculPaieForm()

    return render(request, 'hr_payroll/calcul_paie.html', {'form': form})


# Vues pour les rapports
@login_required
def rapports(request):
    if request.method == 'POST':
        form = RapportPaieForm(request.POST)
        if form.is_valid():
            # Logique de génération des rapports
            type_rapport = form.cleaned_data['type_rapport']
            periode_debut = form.cleaned_data['periode_debut']
            periode_fin = form.cleaned_data['periode_fin']
            direction = form.cleaned_data['direction']
            bureau = form.cleaned_data['bureau']
            grade = form.cleaned_data['grade']
            format_export = form.cleaned_data['format_export']
            
            # Ici vous pouvez implémenter la logique de génération des rapports
            messages.success(request, f'Rapport {type_rapport} généré avec succès.')
            return redirect('hr_payroll:rapports')
    else:
        form = RapportPaieForm()
    
    return render(request, 'hr_payroll/rapports.html', {'form': form})


# Vues pour l'archivage
@login_required
def archivage(request):
    if request.method == 'POST':
        form = ArchivageForm(request.POST)
        if form.is_valid():
            periode = form.cleaned_data['periode']
            commentaire = form.cleaned_data['commentaire']
            
            # Archiver tous les bulletins de la période
            bulletins = periode.bulletins.all()
            for bulletin in bulletins:
                donnees_archivees = {
                    'periode': {
                        'annee': bulletin.periode.annee,
                        'mois': bulletin.periode.mois,
                        'date_debut': bulletin.periode.date_debut.isoformat(),
                        'date_fin': bulletin.periode.date_fin.isoformat(),
                    },
                    'agent': {
                        'matricule': bulletin.agent.matricule,
                        'nom': bulletin.agent.nom,
                        'prenoms': bulletin.agent.prenoms,
                        'grade': bulletin.agent.grade.nom,
                        'bureau': bulletin.agent.bureau.nom,
                    },
                    'totaux': {
                        'total_gains': float(bulletin.total_gains),
                        'total_retenues': float(bulletin.total_retenues),
                        'total_cotisations': float(bulletin.total_cotisations),
                        'net_a_payer': float(bulletin.net_a_payer),
                    },
                    'mouvements': []
                }
                
                # Ajouter les mouvements
                mouvements = MouvementPaie.objects.filter(periode=periode, agent=bulletin.agent)
                for mouvement in mouvements:
                    donnees_archivees['mouvements'].append({
                        'element_paie': mouvement.element_paie.nom,
                        'type_element': mouvement.element_paie.type_element,
                        'montant': float(mouvement.montant),
                        'base_calcul': float(mouvement.montant) if mouvement.montant else None,
                    
                    })
                
                HistoriquePaie.objects.create(
                    periode=periode,
                    agent=bulletin.agent,
                    bulletin=bulletin,
                    donnees_archivees=donnees_archivees,
                    archive_par=request.user,
                    commentaire_archivage=commentaire
                )
            
            # Marquer la période comme archivée
            periode.statut = 'ARCHIVEE'
            periode.date_archivage = timezone.now()
            periode.save()
            
            messages.success(request, f'Période {periode} archivée avec succès.')
            return redirect('hr_payroll:periode_paie_list')
    else:
        form = ArchivageForm()
    
    return render(request, 'hr_payroll/archivage.html', {'form': form})


# Vue tableau de bord
@login_required
def tableau_bord(request):
    # Statistiques générales
    total_agents = Agent.objects.filter(actif=True).count()
    agents_actifs = Agent.objects.filter(actif=True, statut='ACTIF').count()
    total_directions = Direction.objects.filter(actif=True).count()
    total_bureaux = Bureau.objects.filter(actif=True).count()
    total_grades = Grade.objects.filter(actif=True).count()
    total_grilles_salariales = GrilleSalariale.objects.filter(actif=True).count()
    total_periodes = PeriodePaie.objects.count()
    total_mouvements = MouvementPaie.objects.count()
    
    # Périodes récentes
    periodes_recentes = PeriodePaie.objects.all().order_by('-annee', '-mois')[:5]
    
    # Mouvements récents
    mouvements_recents = MouvementPaie.objects.all().select_related(
        'periode', 'agent', 'element_paie'
    ).order_by('-date_creation')[:10]
    
    # Agents récents
    agents_recents = Agent.objects.filter(actif=True).select_related(
        'grade', 'bureau'
    ).order_by('-date_creation')[:10]
    
    context = {
        'total_agents': total_agents,
        'agents_actifs': agents_actifs,
        'total_directions': total_directions,
        'total_bureaux': total_bureaux,
        'total_grades': total_grades,
        'total_grilles_salariales': total_grilles_salariales,
        'total_periodes': total_periodes,
        'total_mouvements': total_mouvements,
        'periodes_recentes': periodes_recentes,
        'mouvements_recents': mouvements_recents,
        'agents_recents': agents_recents,
    }
    
    return render(request, 'hr_payroll/tableau_bord.html', context)


# ===== NOUVELLES VUES POUR SIGRH_PAIE =====

# === GESTION DU CADRE ORGANIQUE (Postes budgétaires) ===

@login_required
def poste_budgetaire_list(request):
    """Liste des postes budgétaires"""
    postes = PosteBudgetaire.objects.filter(actif=True).select_related('grade_requis', 'bureau').order_by('bureau__nom', 'grade_requis__niveau')
    return render(request, 'hr_payroll/poste_budgetaire_list.html', {'postes': postes})


@login_required
def poste_budgetaire_detail(request, pk):
    """Détail d'un poste budgétaire"""
    poste = get_object_or_404(PosteBudgetaire, pk=pk)
    agents_occupants = poste.agents.filter(actif=True).select_related('grade')
    affectations = poste.affectations.filter(statut='ACTIVE').select_related('agent', 'bureau')
    
    context = {
        'poste': poste,
        'agents_occupants': agents_occupants,
        'affectations': affectations,
    }
    return render(request, 'hr_payroll/poste_budgetaire_detail.html', context)


@login_required
def poste_budgetaire_create(request):
    """Créer un nouveau poste budgétaire"""
    if request.method == 'POST':
        form = PosteBudgetaireForm(request.POST)
        if form.is_valid():
            poste = form.save()
            messages.success(request, 'Poste budgétaire créé avec succès.')
            return redirect('hr_payroll:poste_budgetaire_detail', pk=poste.pk)
    else:
        form = PosteBudgetaireForm()
    
    return render(request, 'hr_payroll/poste_budgetaire_form.html', {
        'form': form, 
        'title': 'Nouveau Poste Budgétaire'
    })


@login_required
def poste_budgetaire_update(request, pk):
    """Modifier un poste budgétaire"""
    poste = get_object_or_404(PosteBudgetaire, pk=pk)
    if request.method == 'POST':
        form = PosteBudgetaireForm(request.POST, instance=poste)
        if form.is_valid():
            form.save()
            messages.success(request, 'Poste budgétaire mis à jour avec succès.')
            return redirect('hr_payroll:poste_budgetaire_detail', pk=poste.pk)
    else:
        form = PosteBudgetaireForm(instance=poste)
    
    return render(request, 'hr_payroll/poste_budgetaire_form.html', {
        'form': form, 
        'poste': poste,
        'title': 'Modifier le Poste Budgétaire'
    })


@login_required
def poste_budgetaire_delete(request, pk):
    """Supprimer un poste budgétaire"""
    poste = get_object_or_404(PosteBudgetaire, pk=pk)
    if request.method == 'POST':
        poste.actif = False
        poste.save()
        messages.success(request, 'Poste budgétaire supprimé avec succès.')
        return redirect('hr_payroll:poste_budgetaire_list')
    
    return render(request, 'hr_payroll/poste_budgetaire_confirm_delete.html', {'poste': poste})


# === GESTION DES COMPÉTENCES ===

@login_required
def competence_list(request):
    """Liste des compétences"""
    competences = Competence.objects.filter(actif=True).order_by('categorie', 'nom')
    return render(request, 'hr_payroll/competence_list.html', {'competences': competences})


@login_required
def competence_detail(request, pk):
    """Détail d'une compétence"""
    competence = get_object_or_404(Competence, pk=pk)
    agents_competents = competence.agents_competents.select_related('agent', 'agent__grade', 'agent__bureau')
    
    context = {
        'competence': competence,
        'agents_competents': agents_competents,
    }
    return render(request, 'hr_payroll/competence_detail.html', context)


@login_required
def competence_create(request):
    """Créer une nouvelle compétence"""
    if request.method == 'POST':
        form = CompetenceForm(request.POST)
        if form.is_valid():
            competence = form.save()
            messages.success(request, 'Compétence créée avec succès.')
            return redirect('hr_payroll:competence_detail', pk=competence.pk)
    else:
        form = CompetenceForm()
    
    return render(request, 'hr_payroll/competence_form.html', {
        'form': form, 
        'title': 'Nouvelle Compétence'
    })


@login_required
def competence_update(request, pk):
    """Modifier une compétence"""
    competence = get_object_or_404(Competence, pk=pk)
    if request.method == 'POST':
        form = CompetenceForm(request.POST, instance=competence)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compétence mise à jour avec succès.')
            return redirect('hr_payroll:competence_detail', pk=competence.pk)
    else:
        form = CompetenceForm(instance=competence)
    
    return render(request, 'hr_payroll/competence_form.html', {
        'form': form, 
        'competence': competence,
        'title': 'Modifier la Compétence'
    })


@login_required
def competence_delete(request, pk):
    """Supprimer une compétence"""
    competence = get_object_or_404(Competence, pk=pk)
    if request.method == 'POST':
        competence.actif = False
        competence.save()
        messages.success(request, 'Compétence supprimée avec succès.')
        return redirect('hr_payroll:competence_list')
    
    return render(request, 'hr_payroll/competence_confirm_delete.html', {'competence': competence})


# === RENFORCEMENT DE CAPACITÉS (Formations) ===

@login_required
def formation_list(request):
    """Liste des formations"""
    formations = Formation.objects.filter(actif=True).order_by('-date_debut', 'intitule')
    return render(request, 'hr_payroll/formation_list.html', {'formations': formations})


@login_required
def formation_detail(request, pk):
    """Détail d'une formation"""
    formation = get_object_or_404(Formation, pk=pk)
    participants = formation.participants.select_related('agent', 'agent__grade', 'agent__bureau')
    
    context = {
        'formation': formation,
        'participants': participants,
    }
    return render(request, 'hr_payroll/formation_detail.html', context)


@login_required
def formation_create(request):
    """Créer une nouvelle formation"""
    if request.method == 'POST':
        form = FormationForm(request.POST)
        if form.is_valid():
            formation = form.save()
            messages.success(request, 'Formation créée avec succès.')
            return redirect('hr_payroll:formation_detail', pk=formation.pk)
    else:
        form = FormationForm()
    
    return render(request, 'hr_payroll/formation_form.html', {
        'form': form, 
        'title': 'Nouvelle Formation'
    })


@login_required
def formation_update(request, pk):
    """Modifier une formation"""
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        form = FormationForm(request.POST, instance=formation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Formation mise à jour avec succès.')
            return redirect('hr_payroll:formation_detail', pk=formation.pk)
    else:
        form = FormationForm(instance=formation)
    
    return render(request, 'hr_payroll/formation_form.html', {
        'form': form, 
        'formation': formation,
        'title': 'Modifier la Formation'
    })


@login_required
def formation_delete(request, pk):
    """Supprimer une formation"""
    formation = get_object_or_404(Formation, pk=pk)
    if request.method == 'POST':
        formation.actif = False
        formation.save()
        messages.success(request, 'Formation supprimée avec succès.')
        return redirect('hr_payroll:formation_list')
    
    return render(request, 'hr_payroll/formation_confirm_delete.html', {'formation': formation})


# === GESTION DE CARRIÈRE (Affectations) ===

@login_required
def affectation_list(request):
    """Liste des affectations"""
    affectations = Affectation.objects.filter(statut='ACTIVE').select_related(
        'agent', 'bureau', 'poste_budgetaire'
    ).order_by('-date_debut')
    return render(request, 'hr_payroll/affectation_list.html', {'affectations': affectations})


@login_required
def affectation_detail(request, pk):
    """Détail d'une affectation"""
    affectation = get_object_or_404(Affectation, pk=pk)
    return render(request, 'hr_payroll/affectation_detail.html', {'affectation': affectation})


@login_required
def affectation_create(request):
    """Créer une nouvelle affectation"""
    if request.method == 'POST':
        form = AffectationForm(request.POST)
        if form.is_valid():
            affectation = form.save(commit=False)
            affectation.cree_par = request.user
            affectation.save()
            messages.success(request, 'Affectation créée avec succès.')
            return redirect('hr_payroll:affectation_detail', pk=affectation.pk)
    else:
        form = AffectationForm()
    
    return render(request, 'hr_payroll/affectation_form.html', {
        'form': form, 
        'title': 'Nouvelle Affectation'
    })


@login_required
def affectation_update(request, pk):
    """Modifier une affectation"""
    affectation = get_object_or_404(Affectation, pk=pk)
    if request.method == 'POST':
        form = AffectationForm(request.POST, instance=affectation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Affectation mise à jour avec succès.')
            return redirect('hr_payroll:affectation_detail', pk=affectation.pk)
    else:
        form = AffectationForm(instance=affectation)
    
    return render(request, 'hr_payroll/affectation_form.html', {
        'form': form, 
        'affectation': affectation,
        'title': 'Modifier l\'Affectation'
    })


@login_required
def affectation_delete(request, pk):
    """Supprimer une affectation"""
    affectation = get_object_or_404(Affectation, pk=pk)
    if request.method == 'POST':
        affectation.statut = 'TERMINEE'
        affectation.save()
        messages.success(request, 'Affectation terminée avec succès.')
        return redirect('hr_payroll:affectation_list')
    
    return render(request, 'hr_payroll/affectation_confirm_delete.html', {'affectation': affectation})


# === GESTION DE CARRIÈRE (Promotions) ===

@login_required
def promotion_list(request):
    """Liste des promotions"""
    promotions = Promotion.objects.all().select_related(
        'agent', 'grade_ancien', 'grade_nouveau'
    ).order_by('-date_promotion')
    return render(request, 'hr_payroll/promotion_list.html', {'promotions': promotions})


@login_required
def promotion_detail(request, pk):
    """Détail d'une promotion"""
    promotion = get_object_or_404(Promotion, pk=pk)
    return render(request, 'hr_payroll/promotion_detail.html', {'promotion': promotion})


@login_required
def promotion_create(request):
    """Créer une nouvelle promotion"""
    if request.method == 'POST':
        form = PromotionForm(request.POST)
        if form.is_valid():
            promotion = form.save(commit=False)
            promotion.cree_par = request.user
            promotion.save()
            messages.success(request, 'Promotion créée avec succès.')
            return redirect('hr_payroll:promotion_detail', pk=promotion.pk)
    else:
        form = PromotionForm()
    
    return render(request, 'hr_payroll/promotion_form.html', {
        'form': form, 
        'title': 'Nouvelle Promotion'
    })


@login_required
def promotion_update(request, pk):
    """Modifier une promotion"""
    promotion = get_object_or_404(Promotion, pk=pk)
    if request.method == 'POST':
        form = PromotionForm(request.POST, instance=promotion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Promotion mise à jour avec succès.')
            return redirect('hr_payroll:promotion_detail', pk=promotion.pk)
    else:
        form = PromotionForm(instance=promotion)
    
    return render(request, 'hr_payroll/promotion_form.html', {
        'form': form, 
        'promotion': promotion,
        'title': 'Modifier la Promotion'
    })


@login_required
def promotion_delete(request, pk):
    """Supprimer une promotion"""
    promotion = get_object_or_404(Promotion, pk=pk)
    if request.method == 'POST':
        promotion.delete()
        messages.success(request, 'Promotion supprimée avec succès.')
        return redirect('hr_payroll:promotion_list')
    
    return render(request, 'hr_payroll/promotion_confirm_delete.html', {'promotion': promotion})


# === GESTION DE CARRIÈRE (Mutations) ===

@login_required
def mutation_list(request):
    """Liste des mutations"""
    mutations = Mutation.objects.all().select_related(
        'agent', 'origine_bureau', 'destination_bureau'
    ).order_by('-date_mutation')
    return render(request, 'hr_payroll/mutation_list.html', {'mutations': mutations})


@login_required
def mutation_detail(request, pk):
    """Détail d'une mutation"""
    mutation = get_object_or_404(Mutation, pk=pk)
    return render(request, 'hr_payroll/mutation_detail.html', {'mutation': mutation})


@login_required
def mutation_create(request):
    """Créer une nouvelle mutation"""
    if request.method == 'POST':
        form = MutationForm(request.POST)
        if form.is_valid():
            mutation = form.save(commit=False)
            mutation.cree_par = request.user
            mutation.save()
            messages.success(request, 'Mutation créée avec succès.')
            return redirect('hr_payroll:mutation_detail', pk=mutation.pk)
    else:
        form = MutationForm()
    
    return render(request, 'hr_payroll/mutation_form.html', {
        'form': form, 
        'title': 'Nouvelle Mutation'
    })


@login_required
def mutation_update(request, pk):
    """Modifier une mutation"""
    mutation = get_object_or_404(Mutation, pk=pk)
    if request.method == 'POST':
        form = MutationForm(request.POST, instance=mutation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mutation mise à jour avec succès.')
            return redirect('hr_payroll:mutation_detail', pk=mutation.pk)
    else:
        form = MutationForm(instance=mutation)
    
    return render(request, 'hr_payroll/mutation_form.html', {
        'form': form, 
        'mutation': mutation,
        'title': 'Modifier la Mutation'
    })


@login_required
def mutation_delete(request, pk):
    """Supprimer une mutation"""
    mutation = get_object_or_404(Mutation, pk=pk)
    if request.method == 'POST':
        mutation.delete()
        messages.success(request, 'Mutation supprimée avec succès.')
        return redirect('hr_payroll:mutation_list')
    
    return render(request, 'hr_payroll/mutation_confirm_delete.html', {'mutation': mutation})


# === COTATION (Évaluation des performances) ===

@login_required
def cotation_list(request):
    """Liste des cotations"""
    cotations = Cotation.objects.all().select_related(
        'agent', 'agent__grade', 'agent__bureau'
    ).order_by('-annee', '-semestre', 'agent__nom')
    return render(request, 'hr_payroll/cotation_list.html', {'cotations': cotations})


@login_required
def cotation_detail(request, pk):
    """Détail d'une cotation"""
    cotation = get_object_or_404(Cotation, pk=pk)
    return render(request, 'hr_payroll/cotation_detail.html', {'cotation': cotation})


@login_required
def cotation_create(request):
    """Créer une nouvelle cotation"""
    if request.method == 'POST':
        form = CotationForm(request.POST)
        if form.is_valid():
            cotation = form.save(commit=False)
            cotation.cree_par = request.user
            cotation.calculer_note_globale()
            cotation.save()
            messages.success(request, 'Cotation créée avec succès.')
            return redirect('hr_payroll:cotation_detail', pk=cotation.pk)
    else:
        form = CotationForm()
    
    return render(request, 'hr_payroll/cotation_form.html', {
        'form': form, 
        'title': 'Nouvelle Cotation'
    })


@login_required
def cotation_update(request, pk):
    """Modifier une cotation"""
    cotation = get_object_or_404(Cotation, pk=pk)
    if request.method == 'POST':
        form = CotationForm(request.POST, instance=cotation)
        if form.is_valid():
            cotation = form.save(commit=False)
            cotation.calculer_note_globale()
            cotation.save()
            messages.success(request, 'Cotation mise à jour avec succès.')
            return redirect('hr_payroll:cotation_detail', pk=cotation.pk)
    else:
        form = CotationForm(instance=cotation)
    
    return render(request, 'hr_payroll/cotation_form.html', {
        'form': form, 
        'cotation': cotation,
        'title': 'Modifier la Cotation'
    })


@login_required
def cotation_delete(request, pk):
    """Supprimer une cotation"""
    cotation = get_object_or_404(Cotation, pk=pk)
    if request.method == 'POST':
        cotation.delete()
        messages.success(request, 'Cotation supprimée avec succès.')
        return redirect('hr_payroll:cotation_list')
    
    return render(request, 'hr_payroll/cotation_confirm_delete.html', {'cotation': cotation})


@login_required
def cotation_valider(request, pk):
    """Valider une cotation"""
    cotation = get_object_or_404(Cotation, pk=pk)
    if request.method == 'POST':
        cotation.valide_par = request.user
        cotation.date_validation = timezone.now()
        cotation.save()
        messages.success(request, 'Cotation validée avec succès.')
        return redirect('hr_payroll:cotation_detail', pk=cotation.pk)
    
    return render(request, 'hr_payroll/cotation_confirm_validation.html', {'cotation': cotation})


# === ACTIONS DISCIPLINAIRES ===

@login_required
def action_disciplinaire_list(request):
    """Liste des actions disciplinaires"""
    actions = ActionDisciplinaire.objects.all().select_related(
        'agent', 'agent__grade', 'agent__bureau'
    ).order_by('-date_faute')
    return render(request, 'hr_payroll/action_disciplinaire_list.html', {'actions': actions})


@login_required
def action_disciplinaire_detail(request, pk):
    """Détail d'une action disciplinaire"""
    action = get_object_or_404(ActionDisciplinaire, pk=pk)
    return render(request, 'hr_payroll/action_disciplinaire_detail.html', {'action': action})


@login_required
def action_disciplinaire_create(request):
    """Créer une nouvelle action disciplinaire"""
    if request.method == 'POST':
        form = ActionDisciplinaireForm(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.cree_par = request.user
            action.save()
            messages.success(request, 'Action disciplinaire créée avec succès.')
            return redirect('hr_payroll:action_disciplinaire_detail', pk=action.pk)
    else:
        form = ActionDisciplinaireForm()
    
    return render(request, 'hr_payroll/action_disciplinaire_form.html', {
        'form': form, 
        'title': 'Nouvelle Action Disciplinaire'
    })


@login_required
def action_disciplinaire_update(request, pk):
    """Modifier une action disciplinaire"""
    action = get_object_or_404(ActionDisciplinaire, pk=pk)
    if request.method == 'POST':
        form = ActionDisciplinaireForm(request.POST, instance=action)
        if form.is_valid():
            form.save()
            messages.success(request, 'Action disciplinaire mise à jour avec succès.')
            return redirect('hr_payroll:action_disciplinaire_detail', pk=action.pk)
    else:
        form = ActionDisciplinaireForm(instance=action)
    
    return render(request, 'hr_payroll/action_disciplinaire_form.html', {
        'form': form, 
        'action': action,
        'title': 'Modifier l\'Action Disciplinaire'
    })


@login_required
def action_disciplinaire_delete(request, pk):
    """Supprimer une action disciplinaire"""
    action = get_object_or_404(ActionDisciplinaire, pk=pk)
    if request.method == 'POST':
        action.delete()
        messages.success(request, 'Action disciplinaire supprimée avec succès.')
        return redirect('hr_payroll:action_disciplinaire_list')
    
    return render(request, 'hr_payroll/action_disciplinaire_confirm_delete.html', {'action': action})


# === GESTION DES COMPÉTENCES DES AGENTS ===

@login_required
def competence_agent_list(request):
    """Liste des compétences des agents"""
    competences_agents = CompetenceAgent.objects.all().select_related(
        'agent', 'agent__grade', 'agent__bureau', 'competence'
    ).order_by('agent__nom', 'competence__nom')
    return render(request, 'hr_payroll/competence_agent_list.html', {'competences_agents': competences_agents})


@login_required
def competence_agent_detail(request, pk):
    """Détail d'une compétence d'agent"""
    competence_agent = get_object_or_404(CompetenceAgent, pk=pk)
    return render(request, 'hr_payroll/competence_agent_detail.html', {'competence_agent': competence_agent})


@login_required
def competence_agent_create(request):
    """Créer une nouvelle compétence d'agent"""
    if request.method == 'POST':
        form = CompetenceAgentForm(request.POST)
        if form.is_valid():
            competence_agent = form.save(commit=False)
            competence_agent.evalue_par = request.user
            competence_agent.save()
            messages.success(request, 'Compétence d\'agent créée avec succès.')
            return redirect('hr_payroll:competence_agent_detail', pk=competence_agent.pk)
    else:
        form = CompetenceAgentForm()
    
    return render(request, 'hr_payroll/competence_agent_form.html', {
        'form': form, 
        'title': 'Nouvelle Compétence d\'Agent'
    })


@login_required
def competence_agent_update(request, pk):
    """Modifier une compétence d'agent"""
    competence_agent = get_object_or_404(CompetenceAgent, pk=pk)
    if request.method == 'POST':
        form = CompetenceAgentForm(request.POST, instance=competence_agent)
        if form.is_valid():
            form.save()
            messages.success(request, 'Compétence d\'agent mise à jour avec succès.')
            return redirect('hr_payroll:competence_agent_detail', pk=competence_agent.pk)
    else:
        form = CompetenceAgentForm(instance=competence_agent)
    
    return render(request, 'hr_payroll/competence_agent_form.html', {
        'form': form, 
        'competence_agent': competence_agent,
        'title': 'Modifier la Compétence d\'Agent'
    })


@login_required
def competence_agent_delete(request, pk):
    """Supprimer une compétence d'agent"""
    competence_agent = get_object_or_404(CompetenceAgent, pk=pk)
    if request.method == 'POST':
        competence_agent.delete()
        messages.success(request, 'Compétence d\'agent supprimée avec succès.')
        return redirect('hr_payroll:competence_agent_list')
    
    return render(request, 'hr_payroll/competence_agent_confirm_delete.html', {'competence_agent': competence_agent})


# === PARTICIPATION AUX FORMATIONS ===

@login_required
def participation_formation_list(request):
    """Liste des participations aux formations"""
    participations = ParticipationFormation.objects.all().select_related(
        'agent', 'agent__grade', 'agent__bureau', 'formation'
    ).order_by('-date_inscription')
    return render(request, 'hr_payroll/participation_formation_list.html', {'participations': participations})


@login_required
def participation_formation_detail(request, pk):
    """Détail d'une participation à une formation"""
    participation = get_object_or_404(ParticipationFormation, pk=pk)
    return render(request, 'hr_payroll/participation_formation_detail.html', {'participation': participation})


@login_required
def participation_formation_create(request):
    """Créer une nouvelle participation à une formation"""
    if request.method == 'POST':
        form = ParticipationFormationForm(request.POST)
        if form.is_valid():
            participation = form.save(commit=False)
            participation.inscrit_par = request.user
            participation.save()
            messages.success(request, 'Participation à la formation créée avec succès.')
            return redirect('hr_payroll:participation_formation_detail', pk=participation.pk)
    else:
        form = ParticipationFormationForm()
    
    return render(request, 'hr_payroll/participation_formation_form.html', {
        'form': form, 
        'title': 'Nouvelle Participation à une Formation'
    })


@login_required
def participation_formation_update(request, pk):
    """Modifier une participation à une formation"""
    participation = get_object_or_404(ParticipationFormation, pk=pk)
    if request.method == 'POST':
        form = ParticipationFormationForm(request.POST, instance=participation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participation à la formation mise à jour avec succès.')
            return redirect('hr_payroll:participation_formation_detail', pk=participation.pk)
    else:
        form = ParticipationFormationForm(instance=participation)
    
    return render(request, 'hr_payroll/participation_formation_form.html', {
        'form': form, 
        'participation': participation,
        'title': 'Modifier la Participation à la Formation'
    })


@login_required
def participation_formation_delete(request, pk):
    """Supprimer une participation à une formation"""
    participation = get_object_or_404(ParticipationFormation, pk=pk)
    if request.method == 'POST':
        participation.delete()
        messages.success(request, 'Participation à la formation supprimée avec succès.')
        return redirect('hr_payroll:participation_formation_list')
    
    return render(request, 'hr_payroll/participation_formation_confirm_delete.html', {'participation': participation})


# === RAPPORTS ÉTENDUS ===

@login_required
def rapport_cotation(request):
    """Rapport des cotations"""
    if request.method == 'POST':
        form = RapportCotationForm(request.POST)
        if form.is_valid():
            # Logique de génération du rapport
            messages.success(request, 'Rapport de cotation généré avec succès.')
            return redirect('hr_payroll:rapport_cotation')
    else:
        form = RapportCotationForm()
    
    return render(request, 'hr_payroll/rapport_cotation.html', {'form': form})


@login_required
def rapport_formation(request):
    """Rapport des formations"""
    if request.method == 'POST':
        form = RapportFormationForm(request.POST)
        if form.is_valid():
            # Logique de génération du rapport
            messages.success(request, 'Rapport de formation généré avec succès.')
            return redirect('hr_payroll:rapport_formation')
    else:
        form = RapportFormationForm()
    
    return render(request, 'hr_payroll/rapport_formation.html', {'form': form})


@login_required
def rapport_carriere(request):
    """Rapport de carrière"""
    if request.method == 'POST':
        form = RapportCarriereForm(request.POST)
        if form.is_valid():
            # Logique de génération du rapport
            messages.success(request, 'Rapport de carrière généré avec succès.')
            return redirect('hr_payroll:rapport_carriere')
    else:
        form = RapportCarriereForm()
    
    return render(request, 'hr_payroll/rapport_carriere.html', {'form': form})


# === PORTAL AGENT (Accès aux informations personnelles) ===

@login_required
def portal_agent(request):
    """Portail de l'agent pour accéder à ses informations"""
    try:
        # Récupérer l'agent connecté par son email
        if request.user.email:
            agent = Agent.objects.get(email=request.user.email, actif=True)
        else:
            messages.error(request, 'Votre compte utilisateur n\'a pas d\'email associé.')
            return redirect('hr_payroll:tableau_bord')
    except Agent.DoesNotExist:
        messages.error(request, 'Aucun agent associé à votre compte utilisateur.')
        return redirect('hr_payroll:tableau_bord')
    
    # Récupérer les informations de l'agent
    affectations = agent.affectations.filter(statut='ACTIVE').select_related('bureau', 'poste_budgetaire')
    promotions = agent.promotions.all().select_related('grade_ancien', 'grade_nouveau')
    mutations = agent.mutations.all().select_related('origine_bureau', 'destination_bureau')
    cotations = agent.cotations.all().order_by('-annee', '-semestre')
    actions_disciplinaires = agent.actions_disciplinaires.all().order_by('-date_faute')
    competences = agent.competences.all().select_related('competence')
    participations_formations = agent.participations_formations.all().select_related('formation')
    bulletins = agent.bulletins.all().select_related('periode').order_by('-periode__annee', '-periode__mois')
    
    context = {
        'agent': agent,
        'affectations': affectations,
        'promotions': promotions,
        'mutations': mutations,
        'cotations': cotations,
        'actions_disciplinaires': actions_disciplinaires,
        'competences': competences,
        'participations_formations': participations_formations,
        'bulletins': bulletins,
    }
    
    return render(request, 'hr_payroll/portal_agent.html', context)


# === TABLEAU DE BORD ÉTENDU ===

@login_required
def tableau_bord_etendu(request):
    """Tableau de bord étendu avec toutes les fonctionnalités SIGRH_PAIE"""
    # Statistiques générales
    total_agents = Agent.objects.filter(actif=True).count()
    agents_actifs = Agent.objects.filter(actif=True, statut='ACTIF').count()
    total_directions = Direction.objects.filter(actif=True).count()
    total_bureaux = Bureau.objects.filter(actif=True).count()
    total_grades = Grade.objects.filter(actif=True).count()
    total_postes_budgetaires = PosteBudgetaire.objects.filter(actif=True).count()
    total_competences = Competence.objects.filter(actif=True).count()
    total_formations = Formation.objects.filter(actif=True).count()
    
    # Statistiques de carrière
    total_affectations = Affectation.objects.filter(statut='ACTIVE').count()
    total_promotions = Promotion.objects.count()
    total_mutations = Mutation.objects.count()
    
    # Statistiques de cotation
    total_cotations = Cotation.objects.count()
    cotations_validees = Cotation.objects.filter(valide_par__isnull=False).count()
    
    # Statistiques disciplinaires
    total_actions_disciplinaires = ActionDisciplinaire.objects.count()
    actions_en_cours = ActionDisciplinaire.objects.filter(statut='EN_COURS').count()
    
    # Statistiques de formation
    total_participations = ParticipationFormation.objects.count()
    formations_en_cours = Formation.objects.filter(statut='EN_COURS').count()
    
    # Données récentes
    agents_recents = Agent.objects.filter(actif=True).select_related('grade', 'bureau').order_by('-date_creation')[:5]
    cotations_recentes = Cotation.objects.all().select_related('agent', 'agent__grade').order_by('-date_creation')[:5]
    formations_recentes = Formation.objects.filter(actif=True).order_by('-date_creation')[:5]
    actions_recentes = ActionDisciplinaire.objects.all().select_related('agent').order_by('-date_creation')[:5]
    
    context = {
        # Statistiques générales
        'total_agents': total_agents,
        'agents_actifs': agents_actifs,
        'total_directions': total_directions,
        'total_bureaux': total_bureaux,
        'total_grades': total_grades,
        'total_postes_budgetaires': total_postes_budgetaires,
        'total_competences': total_competences,
        'total_formations': total_formations,
        
        # Statistiques de carrière
        'total_affectations': total_affectations,
        'total_promotions': total_promotions,
        'total_mutations': total_mutations,
        
        # Statistiques de cotation
        'total_cotations': total_cotations,
        'cotations_validees': cotations_validees,
        
        # Statistiques disciplinaires
        'total_actions_disciplinaires': total_actions_disciplinaires,
        'actions_en_cours': actions_en_cours,
        
        # Statistiques de formation
        'total_participations': total_participations,
        'formations_en_cours': formations_en_cours,
        
        # Données récentes
        'agents_recents': agents_recents,
        'cotations_recentes': cotations_recentes,
        'formations_recentes': formations_recentes,
        'actions_recentes': actions_recentes,
    }
    
    return render(request, 'hr_payroll/home.html', context)
