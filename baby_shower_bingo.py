#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Baby Shower Bingo Generator
Genera cartones de bingo temáticos de baby shower con imágenes descargadas de internet
y sus respectivas fichas para imprimir.
"""

import random
import os
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import urllib.request
import tempfile
import ssl

# Lista de URLs de imágenes temáticas de baby shower (imágenes gratuitas de Flaticon)
BABY_IMAGES = [
    "https://cdn-icons-png.flaticon.com/512/2921/2921226.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921229.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921230.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921232.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921235.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921237.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921240.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921242.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921245.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921248.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921250.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921252.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921255.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921258.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921260.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921262.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921265.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921268.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921270.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921272.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921275.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921278.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921280.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921282.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921285.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921288.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921290.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921292.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921295.png",
    "https://cdn-icons-png.flaticon.com/512/2921/2921298.png",
]

def download_image(url, temp_dir):
    """Descarga una imagen de internet"""
    try:
        filename = url.split('/')[-1]
        filepath = os.path.join(temp_dir, filename)
        
        if os.path.exists(filepath):
            return filepath
        
        # Configurar SSL para evitar errores de certificado
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, timeout=15, context=ssl_context) as response:
            with open(filepath, 'wb') as out_file:
                out_file.write(response.read())
        
        return filepath
    except Exception as e:
        print(f"Error descargando {url}: {e}")
        return None

def create_placeholder_image(temp_dir, index, text=""):
    """Crea una imagen placeholder con colores pastel"""
    placeholder_path = os.path.join(temp_dir, f"placeholder_{index}.png")
    
    pastel_colors = [
        (255, 182, 193), (255, 218, 185), (255, 255, 185),
        (185, 255, 185), (185, 255, 255), (185, 185, 255),
        (255, 185, 255), (255, 218, 218), (218, 255, 218)
    ]
    
    color = pastel_colors[index % len(pastel_colors)]
    
    c = canvas.Canvas(placeholder_path, pagesize=(2*inch, 2*inch))
    c.setFillColorRGB(color[0]/255, color[1]/255, color[2]/255)
    c.rect(0, 0, 2*inch, 2*inch, fill=True, stroke=False)
    c.setStrokeColor(colors.black)
    c.setLineWidth(2)
    c.rect(0, 0, 2*inch, 2*inch, fill=False, stroke=True)
    c.save()
    
    return placeholder_path

def load_images(image_urls, temp_dir):
    """Carga todas las imágenes desde internet"""
    print("\n📥 Descargando imágenes de internet...")
    loaded_images = []
    
    for i, url in enumerate(image_urls):
        filepath = download_image(url, temp_dir)
        if filepath and os.path.exists(filepath):
            loaded_images.append(filepath)
            print(f"   ✓ [{i+1}/{len(image_urls)}] Imagen descargada")
        else:
            print(f"   ✗ [{i+1}/{len(image_urls)}] Error, se usará placeholder")
            loaded_images.append(None)
    
    return loaded_images

def generate_bingo_card(images_data, grid_size, temp_dir):
    """Genera un cartón de bingo con imágenes"""
    available_indices = list(range(len(images_data)))
    selected_indices = random.sample(available_indices, min(grid_size * grid_size, len(available_indices)))
    
    card_data = []
    for row in range(grid_size):
        row_data = []
        for col in range(grid_size):
            idx = row * grid_size + col
            if idx < len(selected_indices):
                image_idx = selected_indices[idx]
                image_path = images_data[image_idx]
                
                if image_path is None or not os.path.exists(image_path):
                    image_path = create_placeholder_image(temp_dir, image_idx)
                
                try:
                    img = Image(image_path, width=1.6*inch, height=1.6*inch)
                    row_data.append(img)
                except Exception as e:
                    image_path = create_placeholder_image(temp_dir, image_idx)
                    img = Image(image_path, width=1.6*inch, height=1.6*inch)
                    row_data.append(img)
            else:
                row_data.append("")
        card_data.append(row_data)
    
    return card_data

def create_bingo_pdf(num_cards, grid_size, output_filename, temp_dir):
    """Crea el PDF con los cartones de bingo"""
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                           rightMargin=0.3*inch, leftMargin=0.3*inch,
                           topMargin=0.3*inch, bottomMargin=0.3*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HotPink,
        alignment=1,
        spaceAfter=15
    )
    
    title = Paragraph("🍼 Baby Shower Bingo 🧸", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.2*inch))
    
    images_data = load_images(BABY_IMAGES, temp_dir)
    
    cards_per_page = 2 if grid_size >= 4 else 4
    
    for card_num in range(num_cards):
        if card_num > 0 and card_num % cards_per_page == 0:
            elements.append(Spacer(1, 0.3*inch))
        
        card_data = generate_bingo_card(images_data, grid_size, temp_dir)
        
        table = Table(card_data, colWidths=[1.7*inch]*grid_size, rowHeights=[1.7*inch]*grid_size)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 2, colors.HotPink),
            ('BOX', (0, 0), (-1, -1), 3, colors.DeepPink),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.3*inch))
    
    doc.build(elements)
    print(f"\n✓ Cartones guardados en: {output_filename}")

def create_tokens_pdf(num_cards, output_filename, temp_dir):
    """Crea el PDF con las fichas para marcar"""
    doc = SimpleDocTemplate(output_filename, pagesize=letter,
                           rightMargin=0.5*inch, leftMargin=0.5*inch,
                           topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    elements = []
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.BlueViolet,
        alignment=1,
        spaceAfter=20
    )
    
    title = Paragraph("🎀 Fichas para Bingo 🎀", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    token_colors = [
        colors.HotPink, colors.DeepSkyBlue, colors.Gold,
        colors.MediumPurple, colors.LimeGreen, colors.OrangeRed,
        colors.Magenta, colors.Cyan, colors.YellowGreen
    ]
    
    tokens_per_row = 8
    rows_needed = (num_cards * 4 + tokens_per_row - 1) // tokens_per_row
    
    for row in range(rows_needed):
        row_data = []
        for col in range(tokens_per_row):
            token_idx = row * tokens_per_row + col
            if token_idx < num_cards * 4:
                color = token_colors[token_idx % len(token_colors)]
                
                token_path = os.path.join(temp_dir, f"token_{token_idx}.png")
                c = canvas.Canvas(token_path, pagesize=(1*inch, 1*inch))
                c.setFillColor(color)
                c.setStrokeColor(colors.white)
                c.setLineWidth(2)
                c.circle(0.5*inch, 0.5*inch, 0.45*inch, fill=True, stroke=True)
                c.save()
                
                try:
                    img = Image(token_path, width=0.9*inch, height=0.9*inch)
                    row_data.append(img)
                except:
                    row_data.append("")
            else:
                row_data.append("")
        
        if any(row_data):
            table = Table([row_data], colWidths=[1*inch]*tokens_per_row, rowHeights=[1*inch])
            table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.2*inch))
    
    doc.build(elements)
    print(f"✓ Fichas guardadas en: {output_filename}")

def main():
    print("=" * 60)
    print("       🍼 GENERADOR DE BINGO BABY SHOWER 🧸")
    print("=" * 60)
    
    while True:
        try:
            num_cards = int(input("\n¿Cuántos cartones deseas generar? (1-100): "))
            if 1 <= num_cards <= 100:
                break
            else:
                print("Por favor, ingresa un número entre 1 y 100.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número.")
    
    while True:
        try:
            grid_size = int(input("¿Tamaño de la cuadrícula? (3, 4 o 5): "))
            if grid_size in [3, 4, 5]:
                break
            else:
                print("Por favor, ingresa 3, 4 o 5.")
        except ValueError:
            print("Entrada inválida. Por favor, ingresa 3, 4 o 5.")
    
    temp_dir = tempfile.mkdtemp(prefix="baby_bingo_")
    print(f"\n📁 Directorio temporal: {temp_dir}")
    
    try:
        timestamp = f"{num_cards}cartones_{grid_size}x{grid_size}"
        cards_filename = f"baby_shower_bingo_cartones_{timestamp}.pdf"
        tokens_filename = f"baby_shower_bingo_fichas_{timestamp}.pdf"
        
        print(f"\n🎯 Generando {num_cards} cartones de {grid_size}x{grid_size}...")
        
        create_bingo_pdf(num_cards, grid_size, cards_filename, temp_dir)
        create_tokens_pdf(num_cards, tokens_filename, temp_dir)
        
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
        
    finally:
        print(f"\n🗂️  Las imágenes temporales se guardaron en: {temp_dir}")

if __name__ == "__main__":
    main()
