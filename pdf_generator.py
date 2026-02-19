from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Table
import os

def generate_pdf(filename, content):
    """
    Generates a formatted PDF report from chatbot response.
    """

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    # Title
    elements.append(Paragraph("Science Experiment Report", styles["Title"]))
    elements.append(Spacer(1, 0.5 * inch))

    # Body content
    for line in content.split("\n"):
        elements.append(Paragraph(line, styles["BodyText"]))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)

    return filename
