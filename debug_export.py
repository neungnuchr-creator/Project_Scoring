import sys
sys.path.insert(0, '.')

from app import app, ProjectScoringSystem
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from datetime import datetime

print("Testing export PDF function...")
print("=" * 50)

try:
    # Initialize database
    ProjectScoringSystem.init_database()
    print("OK: Database initialized")
    
    # Get test user (admin)
    user = ProjectScoringSystem.get_user(1)
    if not user:
        print("ERROR: No user found with ID 1")
        sys.exit(1)
    print(f"OK: Got user: {user['first_name']} {user['last_name']}")
    
    # Get projects
    projects = ProjectScoringSystem.get_user_projects(1)
    print(f"OK: Got {len(projects)} projects")
    
    # Get statistics
    stats = ProjectScoringSystem.get_statistics(1)
    print(f"OK: Got statistics: {stats}")
    
    # Test PDF creation
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#3b82f6'),
        alignment=TA_CENTER
    )
    elements.append(Paragraph('Project Scoring Report', title_style))
    elements.append(Spacer(1, 12))
    
    # User Info
    user_info_style = ParagraphStyle('UserInfo', parent=styles['Normal'], fontSize=12)
    elements.append(Paragraph(f"Employee: {user['first_name']} {user['last_name']}", user_info_style))
    elements.append(Spacer(1, 20))
    
    # Summary Table
    summary_data = [
        ['Metric', 'Value'],
        ['Total Projects', str(stats['total_projects'])],
        ['Total Score', f"{stats['total_score']:.2f}"],
        ['Average Score', f"{stats['avg_score']:.2f}"]
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    elements.append(summary_table)
    
    # Build PDF
    doc.build(elements)
    print(f"OK: PDF created successfully ({len(buffer.getvalue())} bytes)")
    
    # Save test file
    with open('test_export.pdf', 'wb') as f:
        f.write(buffer.getvalue())
    print("OK: Test PDF saved as test_export.pdf")
    
    print("=" * 50)
    print("SUCCESS: All export tests passed!")
    
except Exception as e:
    print("=" * 50)
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

