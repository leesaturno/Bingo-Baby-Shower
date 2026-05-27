#!/usr/bin/env python3
"""
Script para generar cartones de bingo temáticos de baby shower con imágenes.
Genera un PDF con los cartones y las fichas para recortar.
"""

import os
import random
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER
from PIL import Image as PILImage
import io

# Lista de temas/emojis relacionados con bebés y baby showers
BABY_THEMES = [
    "🍼",  # Biberón
    "👶",  # Bebé
    "🧸",  # Osito de peluche
    "🎀",  # Lazo
    "👣",  # Huellas de bebé
    "🛁",  # Bañera
    "🚼",  # Símbolo de bebé
    "🍪",  # Galleta
    "🥄",  # Cuchara
    "🍼",  # Leche
    "🎈",  # Globo
    "🌟",  # Estrella
    "💝",  # Corazón con regalo
    "👕",  # Ropa de bebé
    "🧦",  # Calcetines
    "📦",  # Caja de regalo
    "🎁",  # Regalo
    "🏆",  # Trofeo
    "⭐",  # Estrella brillante
    "🌈",  # Arcoíris
    "🦆",  # Pato de goma
    "🐘",  # Elefante (juguetes comunes)
    "🐻",  # Oso
    "🐰",  # Conejo
    "🐤",  # Polluelo
    "🦋",  # Mariposa
    "🌸",  # Flor
    "🍭",  # Caramelo
    "🍰",  # Pastel
    "🧁",  # Cupcake
]


def generate_bingo_card(size=5):
    """
    Genera un cartón de bingo con imágenes/emojis aleatorios.
    
    Args:
        size: Tamaño del cartón (por defecto 5x5)
    
    Returns:
        Una matriz (lista de listas) con los emojis
    """
    # Seleccionar elementos únicos aleatorios
    num_cells = size * size
    selected_items = random.sample(BABY_THEMES, min(num_cells, len(BABY_THEMES)))
    
    # Si necesitamos más elementos de los disponibles, repetir algunos
    while len(selected_items) < num_cells:
        additional = random.choice(BABY_THEMES)
        if additional not in selected_items or len(BABY_THEMES) <= num_cells:
            selected_items.append(additional)
    
    # Mezclar los elementos
    random.shuffle(selected_items)
    
    # Crear la matriz del cartón
    card = []
    index = 0
    for row in range(size):
        card_row = []
        for col in range(size):
            card_row.append(selected_items[index])
            index += 1
        card.append(card_row)
    
    return card


def create_pdf_with_cards(filename, num_cards=10, cards_per_page=2, size=5):
    """
    Crea un PDF con múltiples cartones de bingo y sus fichas.
    
    Args:
        filename: Nombre del archivo PDF a generar
        num_cards: Número total de cartones a generar
        cards_per_page: Número de cartones por página
        size: Tamaño del cartón (5x5 por defecto)
    """
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Estilo personalizado para el título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.hotpink,
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    # Estilo para subtítulos
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=12,
        textColor=colors.darkblue,
        spaceAfter=6,
        alignment=TA_CENTER
    )
    
    card_count = 0
    
    while card_count < num_cards:
        # Título de la página
        page_num = (card_count // cards_per_page) + 1
        elements.append(Paragraph(f"Baby Shower Bingo - Página {page_num}", title_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Generar cartones para esta página
        for i in range(cards_per_page):
            if card_count >= num_cards:
                break
            
            card_count += 1
            card = generate_bingo_card(size)
            
            # Crear tabla para el cartón
            table_data = []
            
            # Añadir título del cartón
            header_row = [Paragraph(f"Cartón #{card_count}", subtitle_style)] * size
            table_data.append(header_row)
            
            # Añadir filas del cartón
            for row in card:
                table_row = []
                for cell in row:
                    # Convertir emoji a texto grande
                    table_row.append(Paragraph(cell, ParagraphStyle(
                        'EmojiCell',
                        parent=styles['Normal'],
                        fontSize=24,
                        alignment=TA_CENTER
                    )))
                table_data.append(table_row)
            
            # Crear la tabla
            card_table = Table(table_data, colWidths=[1.2*inch] * size)
            
            # Estilo de la tabla
            style = TableStyle([
                # Bordes
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('INNERGRID', (0, 0), (-1, -1), 1, colors.gray),
                
                # Fondo para el encabezado
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightpink),
                
                # Fondo alternado para las celdas
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                
                # Alineación
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                
                # Espaciado
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ])
            
            card_table.setStyle(style)
            elements.append(card_table)
            elements.append(Spacer(1, 0.3*inch))
        
        # Salto de página si hay más cartones
        if card_count < num_cards:
            elements.append(Spacer(1, 2*inch))
            doc.build(elements)
            elements = []
            doc = SimpleDocTemplate(
                filename,
                pagesize=letter,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )
    
    # Construir el documento final
    doc.build(elements)
    print(f"✓ PDF generado exitosamente: {filename}")


def create_fichas_pdf(filename, num_fichas=50):
    """
    Crea un PDF con fichas para marcar los cartones de bingo.
    
    Args:
        filename: Nombre del archivo PDF
        num_fichas: Número de fichas a generar
    """
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Título
    title_style = ParagraphStyle(
        'FichasTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.purple,
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    elements.append(Paragraph("Fichas para Baby Shower Bingo", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Instrucciones
    instructions = ParagraphStyle(
        'Instructions',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=12
    )
    elements.append(Paragraph("Recorta estas fichas para usarlas en los cartones de bingo", instructions))
    elements.append(Spacer(1, 0.2*inch))
    
    # Crear tabla de fichas
    fichas_per_row = 7
    num_rows = (num_fichas + fichas_per_row - 1) // fichas_per_row
    
    table_data = []
    for row in range(num_rows):
        table_row = []
        for col in range(fichas_per_row):
            ficha_num = row * fichas_per_row + col + 1
            if ficha_num <= num_fichas:
                # Crear círculo con emoji
                table_row.append(Paragraph("🔴", ParagraphStyle(
                    'FichaCircle',
                    parent=styles['Normal'],
                    fontSize=20,
                    alignment=TA_CENTER
                )))
            else:
                table_row.append("")
        table_data.append(table_row)
    
    ficha_table = Table(table_data, colWidths=[0.9*inch] * fichas_per_row)
    ficha_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightyellow),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(ficha_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Fichas alternativas con diferentes colores
    elements.append(Paragraph("Fichas adicionales de colores", ParagraphStyle(
        'AltTitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.darkgreen,
        spaceAfter=10,
        alignment=TA_CENTER
    )))
    
    alt_colors = ["🔵", "🟢", "🟡", "🟠", "🟣", "⭐", "💖"]
    alt_data = []
    for i in range(0, len(alt_colors), 7):
        row = []
        for j in range(i, min(i+7, len(alt_colors))):
            row.append(Paragraph(alt_colors[j], ParagraphStyle(
                'AltFicha',
                parent=styles['Normal'],
                fontSize=20,
                alignment=TA_CENTER
            )))
        while len(row) < 7:
            row.append("")
        alt_data.append(row)
    
    alt_table = Table(alt_data, colWidths=[0.9*inch] * 7)
    alt_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    
    elements.append(alt_table)
    
    doc.build(elements)
    print(f"✓ PDF de fichas generado exitosamente: {filename}")


def main():
    """Función principal que interactúa con el usuario."""
    print("=" * 60)
    print("🎉 GENERADOR DE CARTONES DE BINGO PARA BABY SHOWER 🎉")
    print("=" * 60)
    print()
    
    # Solicitar número de cartones
    while True:
        try:
            num_cards = int(input("¿Cuántos cartones de bingo deseas generar? (1-100): "))
            if 1 <= num_cards <= 100:
                break
            else:
                print("Por favor, ingresa un número entre 1 y 100.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número entero.")
    
    # Solicitar tamaño del cartón
    while True:
        try:
            size = int(input("¿Qué tamaño de cartón prefieres? (3, 4 o 5 para 3x3, 4x4 o 5x5): "))
            if size in [3, 4, 5]:
                break
            else:
                print("Por favor, ingresa 3, 4 o 5.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número entero.")
    
    # Solicitar nombre de archivo
    pdf_name = input("\nNombre del archivo PDF para los cartones (por defecto: bingo_cartones.pdf): ").strip()
    if not pdf_name:
        pdf_name = "bingo_cartones.pdf"
    elif not pdf_name.endswith(".pdf"):
        pdf_name += ".pdf"
    
    fichas_name = input("Nombre del archivo PDF para las fichas (por defecto: bingo_fichas.pdf): ").strip()
    if not fichas_name:
        fichas_name = "bingo_fichas.pdf"
    elif not fichas_name.endswith(".pdf"):
        fichas_name += ".pdf"
    
    print("\n" + "=" * 60)
    print("Generando cartones de bingo...")
    print("=" * 60)
    
    # Generar PDF con cartones
    create_pdf_with_cards(pdf_name, num_cards=num_cards, cards_per_page=2, size=size)
    
    # Generar PDF con fichas
    print("\nGenerando fichas...")
    create_fichas_pdf(fichas_name, num_fichas=50)
    
    print("\n" + "=" * 60)
    print("¡GENERACIÓN COMPLETADA!")
    print("=" * 60)
    print(f"\nArchivos generados:")
    print(f"  📄 Cartones: {os.path.abspath(pdf_name)}")
    print(f"  📄 Fichas: {os.path.abspath(fichas_name)}")
    print("\nInstrucciones:")
    print("  1. Imprime ambos archivos PDF")
    print("  2. Recorta los cartones y las fichas")
    print("  3. ¡Disfruta del juego de bingo en tu baby shower! 🎊")
    print()


if __name__ == "__main__":
    main()
