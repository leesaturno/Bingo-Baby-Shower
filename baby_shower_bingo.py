#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baby Shower Bingo Generator - Versión simplificada
Genera cartones de bingo con íconos dibujados directamente en el PDF
"""

import os
import sys
import random
import tempfile
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.graphics.shapes import Drawing, Circle, Rect, Line, PolyLine
from reportlab.graphics import renderPDF
import math

BABY_THEMES = [
    "biberon", "osito", "regalo", "chupete", "patitos", 
    "estrella", "corazon", "flor", "mariposa", "globo",
    "zapatos", "gorrito", "mordedor", "sonaja", "cuna",
    "leche", "galleta", "pajaro", "nube", "luna",
    "arbol", "coche", "pelota", "libro", "camara",
    "peine", "botella", "panal", "babero", "calcetin"
]

COLOR_MAP = {
    "biberon": (0.6, 0.8, 1.0), "osito": (0.8, 0.6, 0.4),
    "regalo": (1.0, 0.6, 0.8), "chupete": (0.6, 1.0, 0.7),
    "patitos": (1.0, 0.9, 0.4), "estrella": (1.0, 0.85, 0.2),
    "corazon": (1.0, 0.4, 0.6), "flor": (1.0, 0.4, 0.8),
    "mariposa": (1.0, 0.6, 0.3), "globo": (0.4, 0.8, 1.0),
    "zapatos": (0.7, 0.4, 1.0), "gorrito": (1.0, 0.6, 0.6),
    "mordedor": (0.3, 0.9, 0.9), "sonaja": (0.9, 0.7, 0.5),
    "cuna": (0.4, 0.4, 0.8), "leche": (0.95, 0.95, 0.9),
    "galleta": (0.9, 0.75, 0.5), "pajaro": (0.4, 0.7, 1.0),
    "nube": (0.9, 0.9, 0.95), "luna": (1.0, 0.95, 0.6),
    "arbol": (0.3, 0.8, 0.4), "coche": (1.0, 0.4, 0.4),
    "pelota": (0.6, 1.0, 0.4), "libro": (0.5, 0.4, 0.9),
    "camara": (0.6, 0.6, 0.6), "peine": (0.8, 0.4, 0.9),
    "botella": (0.3, 0.7, 0.7), "panal": (0.9, 0.85, 0.9),
    "babero": (1.0, 0.5, 0.5), "calcetin": (0.9, 0.5, 0.7)
}

def draw_icon(c, theme, x, y, size):
    """Dibuja un ícono en el canvas"""
    cx, cy = x + size/2, y + size/2
    r = size/2 - 3
    color = COLOR_MAP.get(theme, (0.7, 0.7, 0.8))
    
    # Fondo circular
    c.setFillColor(colors.Color(0.97, 0.97, 0.97))
    c.setStrokeColor(colors.Color(*color))
    c.setLineWidth(2)
    c.circle(cx, cy, r, fill=True, stroke=True)
    c.setFillColor(colors.Color(*color))
    
    if theme == "biberon":
        c.rect(cx-size*0.15, cy-size*0.25, size*0.3, size*0.5, fill=True, stroke=True)
        c.setFillColor(colors.white)
        c.circle(cx, cy+size*0.35, size*0.08, fill=True, stroke=True)
        c.setFillColor(colors.Color(*color))
        c.rect(cx-size*0.1, cy+size*0.25, size*0.2, size*0.1, fill=True, stroke=True)
    elif theme == "osito":
        c.circle(cx, cy+size*0.05, size*0.18, fill=True, stroke=True)
        c.circle(cx-size*0.15, cy+size*0.2, size*0.06, fill=True, stroke=True)
        c.circle(cx+size*0.15, cy+size*0.2, size*0.06, fill=True, stroke=True)
        c.setFillColor(colors.black)
        c.circle(cx-size*0.05, cy+size*0.08, size*0.02, fill=True, stroke=False)
        c.circle(cx+size*0.05, cy+size*0.08, size*0.02, fill=True, stroke=False)
        c.circle(cx, cy+size*0.02, size*0.03, fill=True, stroke=False)
    elif theme == "regalo":
        c.rect(cx-size*0.2, cy-size*0.2, size*0.4, size*0.4, fill=True, stroke=True)
        c.setFillColor(colors.Color(1.0, 0.9, 0.2))
        c.rect(cx-size*0.05, cy-size*0.2, size*0.1, size*0.4, fill=True, stroke=False)
        c.rect(cx-size*0.2, cy-size*0.05, size*0.4, size*0.1, fill=True, stroke=False)
        c.circle(cx-size*0.08, cy+size*0.25, size*0.06, fill=True, stroke=False)
        c.circle(cx+size*0.08, cy+size*0.25, size*0.06, fill=True, stroke=False)
    elif theme == "chupete":
        c.setFillColor(colors.Color(*color))
        c.circle(cx, cy, size*0.2, fill=True, stroke=True)
        c.setFillColor(colors.white)
        c.circle(cx, cy, size*0.1, fill=True, stroke=True)
        c.setFillColor(colors.Color(0.7, 0.7, 0.7))
        c.setStrokeColor(colors.Color(0.5, 0.5, 0.5))
        c.setLineWidth(2)
        c.circle(cx, cy-size*0.25, size*0.05, fill=True, stroke=True)
    elif theme == "patitos":
        c.setFillColor(colors.Color(*color))
        c.circle(cx, cy+size*0.05, size*0.15, fill=True, stroke=True)
        c.circle(cx+size*0.12, cy+size*0.2, size*0.09, fill=True, stroke=True)
        c.setFillColor(colors.orange)
        c.circle(cx+size*0.2, cy+size*0.18, size*0.03, fill=True, stroke=False)
        c.setFillColor(colors.black)
        c.circle(cx+size*0.14, cy+size*0.22, size*0.015, fill=True, stroke=False)
    elif theme == "estrella":
        points = []
        for i in range(10):
            angle = (i * 36 - 90) * math.pi / 180
            rad = size*0.2 if i % 2 == 0 else size*0.09
            points.extend([cx + rad * math.cos(angle), cy + rad * math.sin(angle)])
        p = c.beginPath()
        p.moveTo(points[0], points[1])
        for j in range(2, len(points), 2):
            p.lineTo(points[j], points[j+1])
        p.close()
        c.drawPath(p, fill=True, stroke=True)
    elif theme == "corazon":
        c.circle(cx-size*0.08, cy+size*0.05, size*0.1, fill=True, stroke=True)
        c.circle(cx+size*0.08, cy+size*0.05, size*0.1, fill=True, stroke=True)
        p = c.beginPath()
        p.moveTo(cx-size*0.18, cy+size*0.05)
        p.lineTo(cx, cy-size*0.15)
        p.lineTo(cx+size*0.18, cy+size*0.05)
        p.close()
        c.drawPath(p, fill=True, stroke=True)
    elif theme == "globo":
        c.circle(cx, cy+size*0.05, size*0.18, fill=True, stroke=True)
        c.setStrokeColor(colors.gray)
        c.setLineWidth(2)
        c.line(cx, cy-size*0.13, cx, cy-size*0.3)
        c.setFillColor(colors.Color(*color))
        c.circle(cx, cy-size*0.13, size*0.03, fill=True, stroke=False)
    elif theme == "flor":
        for i in range(6):
            angle = i * 60 * math.pi / 180
            px = cx + size*0.12 * math.cos(angle)
            py = cy + size*0.12 * math.sin(angle)
            c.circle(px, py, size*0.07, fill=True, stroke=True)
        c.setFillColor(colors.yellow)
        c.setStrokeColor(colors.orange)
        c.setLineWidth(1)
        c.circle(cx, cy, size*0.08, fill=True, stroke=True)
    elif theme == "nube":
        c.circle(cx-size*0.12, cy, size*0.1, fill=True, stroke=True)
        c.circle(cx+size*0.12, cy, size*0.1, fill=True, stroke=True)
        c.circle(cx, cy+size*0.05, size*0.12, fill=True, stroke=True)
        c.rect(cx-size*0.22, cy-size*0.08, size*0.44, size*0.15, fill=True, stroke=True)
    elif theme == "luna":
        c.circle(cx, cy, size*0.18, fill=True, stroke=True)
        c.setFillColor(colors.Color(0.97, 0.97, 0.97))
        c.circle(cx+size*0.08, cy, size*0.16, fill=True, stroke=False)
    elif theme == "arbol":
        c.setFillColor(colors.brown)
        c.setStrokeColor(colors.brown)
        c.rect(cx-size*0.05, cy-size*0.2, size*0.1, size*0.25, fill=True, stroke=True)
        c.setFillColor(colors.Color(*color))
        c.setStrokeColor(colors.Color(*color))
        p = c.beginPath()
        p.moveTo(cx, cy+size*0.25)
        p.lineTo(cx-size*0.18, cy-size*0.05)
        p.lineTo(cx+size*0.18, cy-size*0.05)
        p.close()
        c.drawPath(p, fill=True, stroke=True)
    elif theme == "pelota":
        c.circle(cx, cy, size*0.18, fill=True, stroke=True)
        c.setStrokeColor(colors.white)
        c.setLineWidth(2)
        c.line(cx-size*0.18, cy, cx+size*0.18, cy)
        c.line(cx, cy-size*0.18, cx, cy+size*0.18)
    else:
        c.setFillColor(colors.Color(*color))
        c.setStrokeColor(colors.Color(*color))
        c.setLineWidth(2)
        c.circle(cx, cy, size*0.18, fill=True, stroke=True)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", size*0.25)
        c.drawCentredString(cx, cy-size*0.1, theme[0].upper())

class IconCell:
    def __init__(self, theme):
        self.theme = theme
        self.width = 1.7*inch
        self.height = 1.7*inch
    
    def wrap(self, availWidth, availHeight):
        return self.width, self.height
    
    def drawOn(self, canv, x, y, _sW=0):
        draw_icon(canv, self.theme, x, y, self.width)

def generate_bingo_card(grid_size):
    selected = random.sample(BABY_THEMES, min(grid_size * grid_size, len(BABY_THEMES)))
    card_data = []
    for row in range(grid_size):
        row_data = []
        for col in range(grid_size):
            idx = row * grid_size + col
            if idx < len(selected):
                row_data.append(IconCell(selected[idx]))
            else:
                row_data.append("")
        card_data.append(row_data)
    return card_data

def create_bingo_pdf(num_cards, grid_size, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=letter, rightMargin=0.3*inch, leftMargin=0.3*inch, topMargin=0.3*inch, bottomMargin=0.3*inch)
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=22, textColor=colors.hotpink, alignment=1, spaceAfter=15)
    elements.append(Paragraph("🍼 Baby Shower Bingo 🧸", title_style))
    elements.append(Spacer(1, 0.2*inch))
    cards_per_page = 2 if grid_size >= 4 else 4
    for card_num in range(num_cards):
        if card_num > 0 and card_num % cards_per_page == 0:
            elements.append(Spacer(1, 0.3*inch))
        card_data = generate_bingo_card(grid_size)
        table = Table(card_data, colWidths=[1.7*inch]*grid_size, rowHeights=[1.7*inch]*grid_size)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), colors.white), ('GRID', (0, 0), (-1, -1), 2, colors.hotpink), ('BOX', (0, 0), (-1, -1), 3, colors.deeppink), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'), ('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
    doc.build(elements)
    print(f"\n✓ Cartones guardados en: {output_filename}")

def create_tokens_pdf(num_cards, output_filename):
    doc = SimpleDocTemplate(output_filename, pagesize=letter, rightMargin=0.5*inch, leftMargin=0.5*inch, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.blueviolet, alignment=1, spaceAfter=20)
    elements.append(Paragraph("🎀 Fichas para Bingo 🎀", title_style))
    elements.append(Spacer(1, 0.3*inch))
    token_colors = [colors.hotpink, colors.deepskyblue, colors.gold, colors.mediumpurple, colors.limegreen, colors.orangered, colors.magenta, colors.cyan, colors.yellowgreen]
    tokens_per_row = 8
    rows_needed = (num_cards * 4 + tokens_per_row - 1) // tokens_per_row
    for row in range(rows_needed):
        row_data = []
        for col in range(tokens_per_row):
            token_idx = row * tokens_per_row + col
            if token_idx < num_cards * 4:
                color = token_colors[token_idx % len(token_colors)]
                cell = TokenCell(color)
                row_data.append(cell)
            else:
                row_data.append("")
        if any(row_data):
            table = Table([row_data], colWidths=[1*inch]*tokens_per_row, rowHeights=[1*inch])
            table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
            elements.append(table)
            elements.append(Spacer(1, 0.2*inch))
    doc.build(elements)
    print(f"✓ Fichas guardadas en: {output_filename}")

class TokenCell:
    def __init__(self, color):
        self.color = color
        self.width = 1*inch
        self.height = 1*inch
    
    def wrap(self, availWidth, availHeight):
        return self.width, self.height
    
    def drawOn(self, canv, x, y, _sW=0):
        cx, cy = x + self.width/2, y + self.height/2
        canv.setFillColor(self.color)
        canv.setStrokeColor(colors.white)
        canv.setLineWidth(2)
        canv.circle(cx, cy, 0.45*inch, fill=True, stroke=True)

def main():
    print("=" * 60)
    print("       🍼 GENERADOR DE BINGO BABY SHOWER 🧸")
    print("=" * 60)
    while True:
        try:
            num_cards = int(input("\n¿Cuántos cartones deseas generar? (1-100): "))
            if 1 <= num_cards <= 100:
                break
            print("Por favor, ingresa un número entre 1 y 100.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número.")
    while True:
        try:
            grid_size = int(input("¿Tamaño de la cuadrícula? (3, 4 o 5): "))
            if grid_size in [3, 4, 5]:
                break
            print("Por favor, ingresa 3, 4 o 5.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa 3, 4 o 5.")
    timestamp = f"{num_cards}cartones_{grid_size}x{grid_size}"
    cards_filename = f"baby_shower_bingo_cartones_{timestamp}.pdf"
    tokens_filename = f"baby_shower_bingo_fichas_{timestamp}.pdf"
    print(f"\n🎯 Generando {num_cards} cartones de {grid_size}x{grid_size}...")
    create_bingo_pdf(num_cards, grid_size, cards_filename)
    create_tokens_pdf(num_cards, tokens_filename)
    print("\n" + "=" * 60)
    print("¡GENERACIÓN COMPLETADA!")
    print("=" * 60)
    print(f"\n📄 Archivos generados:")
    print(f"   • Cartones: {cards_filename}")
    print(f"   • Fichas: {tokens_filename}")
    print(f"\n💡 Instrucciones:")
    print(f"   1. Imprime ambos archivos en papel grueso o cartulina")
    print(f"   2. Recorta los cartones por las líneas marcadas")
    print(f"   3. Recorta las fichas y úsalas para marcar")
    print(f"   4. ¡Disfruta del juego en tu Baby Shower!")

if __name__ == "__main__":
    main()
