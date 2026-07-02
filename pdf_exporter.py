from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from datetime import datetime

def export_logistics_pdf(results: dict, ai_insight: str):
    filename = "data/logistics_report.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=12
    )

    story.append(Paragraph("Logistics Performance Report", title_style))
    story.append(Paragraph(
        f"Generated: {datetime.now().strftime('%B %d, %Y')}",
        styles['Normal']
    ))
    story.append(Spacer(1, 0.3*inch))

    # Summary Table
    table_data = [
        ['Metric', 'Value'],
        ['Overall Delivery Rate', f"{results['overall_delivery_rate']}%"],
        ['Total Fuel Cost', f"KES {results['total_fuel_cost']:,}"],
        ['Total Distance', f"{results['total_distance']:,} km"],
        ['Average Delay', f"{results['avg_delay_minutes']} mins"],
        ['Best Route', results['best_route']],
        ['Worst Route', results['worst_route']],
        ['Best Driver', results['best_driver']],
        ['Most Delayed Driver', results['most_delayed_driver']],
        ['Most Efficient Vehicle', results['most_efficient_vehicle']],
    ]

    table = Table(table_data, colWidths=[3*inch, 2.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 12),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 11),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))

    story.append(table)
    story.append(Spacer(1, 0.4*inch))

    # Route Performance Table
    route_title = ParagraphStyle(
        'RouteTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1a1a2e'),
        spaceAfter=8
    )

    story.append(Paragraph("Route Performance Breakdown", route_title))

    route_df = results['route_performance'].reset_index()
    route_table_data = [['Route', 'Delivery Rate %', 'Fuel Cost KES', 'Avg Delay mins']]
    for _, row in route_df.iterrows():
        route_table_data.append([
            row['route'],
            f"{row['avg_delivery_rate']}%",
            f"{row['total_fuel_cost']:,}",
            f"{row['avg_delay']}"
        ])

    route_table = Table(route_table_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
    route_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#16213e')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))

    story.append(route_table)
    story.append(Spacer(1, 0.4*inch))

    # AI Insight
    story.append(Paragraph("AI Executive Insight", route_title))
    story.append(Paragraph(ai_insight, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))

    # Footer
    story.append(Paragraph(
        "This report was generated automatically by the Logistics Insight Engine.",
        styles['Italic']
    ))

    doc.build(story)
    print(f"  PDF exported to {filename}")
    return filename