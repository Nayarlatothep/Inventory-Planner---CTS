import os
import glob

replacements = {
    "btnNuevaConfirmar Recepción": "btnNuevaRecepcion",
    "inputCantConfirmar Recepciónada": "inputCantRecepcionada",
    "Confirmar Confirmar Recepción": "Confirmar Recepción",
    "KPI Confirmar Recepción": "KPI Recepción",
    "Nueva Confirmar Recepción": "Nueva Recepción",
    "Confirmar Recepciónes Hoy": "Recepciones Hoy",
    "Confirmar Recepciónista": "Recepcionista",
    "Confirmar Confirmar Recepciónada": "Confirmar Recepcionada",
    "Resumen de Confirmar Recepción (OC)": "Resumen de Recepción (OC)",
    "Confirmar Recepción guardada con éxito": "Recepción guardada con éxito",
}

html_files = glob.glob("*.html")
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    for old, new in replacements.items():
        content = content.replace(old, new)
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Fixes applied!")
