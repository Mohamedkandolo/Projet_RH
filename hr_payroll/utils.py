from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
from datetime import datetime

def generate_hr_report_pdf(agents, title="Rapport RH - Agents"):
    """Génère un PDF du rapport RH"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    # Titre
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 20))
    
    # En-tête du tableau
    data = [['Nom', 'Matricule', 'Direction', 'Bureau', 'Grade', 'Statut']]
    
    # Données des agents
    for agent in agents:
        data.append([
            f"{agent.nom} {agent.prenom}",
            agent.matricule,
            agent.direction.nom if agent.direction else 'N/A',
            agent.bureau.nom if agent.bureau else 'N/A',
            agent.grade.nom if agent.grade else 'N/A',
            agent.get_statut_display()
        ])
    
    # Créer le tableau
    table = Table(data, colWidths=[2*inch, 1*inch, 1.5*inch, 1.5*inch, 1.5*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Statistiques
    stats_style = ParagraphStyle(
        'Stats',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=10
    )
    
    total_agents = len(agents)
    actifs = len([a for a in agents if a.statut == 'ACTIF'])
    inactifs = total_agents - actifs
    
    elements.append(Paragraph(f"<b>Statistiques :</b>", stats_style))
    elements.append(Paragraph(f"Total des agents : {total_agents}", stats_style))
    elements.append(Paragraph(f"Agents actifs : {actifs}", stats_style))
    elements.append(Paragraph(f"Agents inactifs : {inactifs}", stats_style))
    
    # Pied de page
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    elements.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} par MiKanda", footer_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_payroll_report_pdf(periode, mouvements, title="Rapport de Paie"):
    """Génère un PDF du rapport de paie"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    
    # Titre
    elements.append(Paragraph(title, title_style))
    elements.append(Spacer(1, 20))
    
    # Informations de la période
    periode_style = ParagraphStyle(
        'Periode',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=20
    )
    elements.append(Paragraph(f"<b>Période :</b> {periode}", periode_style))
    elements.append(Spacer(1, 20))
    
    # En-tête du tableau
    data = [['Agent', 'Élément', 'Type', 'Montant', 'Date']]
    
    # Données des mouvements
    for mouvement in mouvements:
        data.append([
            f"{mouvement.agent.nom} {mouvement.agent.prenom}",
            mouvement.element_paie.nom,
            mouvement.element_paie.get_type_element_display(),
            f"{mouvement.montant:,.0f} FC",
            mouvement.date_mouvement.strftime('%d/%m/%Y')
        ])
    
    # Créer le tableau
    table = Table(data, colWidths=[2*inch, 1.5*inch, 1*inch, 1.2*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20))
    
    # Totaux
    total_gains = sum(m.montant for m in mouvements if m.element_paie.type_element == 'GAIN')
    total_retenues = sum(m.montant for m in mouvements if m.element_paie.type_element == 'RETENUE')
    total_cotisations = sum(m.montant for m in mouvements if m.element_paie.type_element == 'COTISATION')
    
    totals_style = ParagraphStyle(
        'Totals',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=10
    )
    
    elements.append(Paragraph(f"<b>Totaux :</b>", totals_style))
    elements.append(Paragraph(f"Total gains : {total_gains:,.0f} FC", totals_style))
    elements.append(Paragraph(f"Total retenues : {total_retenues:,.0f} FC", totals_style))
    elements.append(Paragraph(f"Total cotisations : {total_cotisations:,.0f} FC", totals_style))
    elements.append(Paragraph(f"Net à payer : {(total_gains - total_retenues - total_cotisations):,.0f} FC", totals_style))
    
    # Pied de page
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        alignment=TA_CENTER,
        textColor=colors.grey
    )
    elements.append(Paragraph(f"Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} par MiKanda", footer_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer 