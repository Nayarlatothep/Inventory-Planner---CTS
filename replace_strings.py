import os
import glob

replacements = {
    "Reportes y KPIs": "Indicadores y Reportes",
    "VER DASHBOARD DE KPIs": "VER PANEL DE INDICADORES",
    "Ver dashboard de KPIs": "Ver Panel de Indicadores",
    "Ingreso Material": "Registrar Entrada de Material",
    "Ingreso de Material": "Registrar Entrada de Material",
    "Ingreso de Nuevo Material": "Registrar Entrada de Material",
    "Recepción del material": "Confirmar Recepción",
    "Recepción": "Confirmar Recepción",
    "Recepcion": "Confirmar Recepción",
    "Solicitud de Orden de Trabajo": "Crear orden de trabajo",
    "Solicitud Ordenes de Trabajo": "Crear orden de trabajo",
    "Todas las Solicitudes de Ordenes de Trabajo": "Historial de órdenes de trabajo",
    "Todas las Solicitudes": "Historial de órdenes de trabajo",
    "Despacho Ordenes de Trabajo": "Entrega de material a trabajo",
    "Despacho de Ordenes de Trabajo": "Entrega de material a trabajo",
    "Despacho de Ordenes": "Entrega de material a trabajo",
}

html_files = glob.glob("*.html")
for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We apply replacements in a safe order (longer strings first if they overlap)
    for old, new in sorted(replacements.items(), key=lambda x: len(x[0]), reverse=True):
        content = content.replace(old, new)
        
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Replacements done!")
