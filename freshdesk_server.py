#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Flask para Visor de Tickets Freshdesk - AFJ Global
Versión 6.0: Análisis avanzado con Tendencias, KPIs, Criticidad, Recurrencia, Heatmap
"""

from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import requests
from datetime import datetime
from collections import Counter
import os
import time

app = Flask(__name__)
CORS(app)

# ============================================================
# CONFIGURACIÓN
# ============================================================
FRESHDESK_DOMAIN = os.environ.get("FRESHDESK_DOMAIN", "consultame")
FRESHDESK_API_KEY = os.environ.get("FRESHDESK_API_KEY", "6egUChwBAUA2633n18DC")
COMPANY_ID = 63000424434
CLIENTE = "AFJ Global"

# Cache simple
cache = {
    'data': None,
    'timestamp': None,
    'ttl': 300  # 5 minutos
}

# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def classify_priority(subject, description=""):
    """Clasifica la prioridad del ticket basado en keywords"""
    text = f"{subject} {description}".lower()

    # Keywords para prioridad ALTA
    keywords_alta = [
        'aws', 'alarm', 'no enciende', 'no prende', 'escritorio remoto',
        'virus', 'malware', 'error servidor', 'afjlearning',
        'sharepoint lentitud', 'moodle', 'caido', 'down', 'critical', 'urgente'
    ]

    # Keywords para prioridad MEDIA
    keywords_media = [
        'outlook', 'correo', 'fundae', 'limpieza', 'buzon', 'antivirus',
        'pst', 'revisar pc', 'sharepoint', 'spam', 'cambio licencia',
        'acceso carpeta', 'email', 'password', 'licencia'
    ]

    # Clasificar
    for keyword in keywords_alta:
        if keyword in text:
            return 'Alto'

    for keyword in keywords_media:
        if keyword in text:
            return 'Medio'

    return 'Bajo'

def get_tickets_from_api():
    """Obtiene tickets de Freshdesk API con análisis completo"""
    url = f"https://{FRESHDESK_DOMAIN}.freshdesk.com/api/v2/tickets"
    all_tickets = []

    try:
        for page in range(1, 11):  # Obtener hasta 1000 tickets (10 páginas x 100)
            params = {
                'page': page,
                'per_page': 100,
                'include': 'requester,description'
            }

            response = requests.get(
                url,
                auth=(FRESHDESK_API_KEY, 'X'),
                params=params,
                timeout=30
            )

            if response.status_code == 200:
                tickets = response.json()
                if not tickets:
                    break
                all_tickets.extend(tickets)
            else:
                print(f"Error {response.status_code}: {response.text}")
                break

        # Procesar y enriquecer tickets
        processed = []
        status_map = {2: "Abierto", 3: "Pendiente", 4: "Resuelto", 5: "Cerrado"}

        for t in all_tickets:
            subject = t.get('subject', 'Sin asunto')
            description = t.get('description_text', '')
            priority = classify_priority(subject, description)

            # Convertir prioridad a número para compatibilidad
            priority_num = {'Bajo': 1, 'Medio': 2, 'Alto': 3}.get(priority, 1)

            processed.append({
                "id": t.get('id'),
                "subject": subject,
                "description": description[:200] if description else '',
                "priority": priority_num,
                "priority_name": priority,
                "status": t.get('status'),
                "status_name": status_map.get(t.get('status'), "Otro"),
                "created_at": t.get('created_at'),
                "updated_at": t.get('updated_at'),
                "requester_name": t.get('requester', {}).get('name', 'Desconocido'),
                "tags": t.get('tags', [])
            })

        return processed

    except Exception as e:
        print(f"Error obteniendo tickets: {e}")
        return []

def get_cached_tickets():
    """Retorna tickets del cache o hace una nueva petición"""
    now = time.time()

    # Si hay cache válido, retornarlo
    if cache['data'] and cache['timestamp']:
        if now - cache['timestamp'] < cache['ttl']:
            print("Usando datos del cache")
            return cache['data']

    # Si no hay cache o expiró, obtener nuevos datos
    print("Obteniendo datos frescos de Freshdesk...")
    tickets = get_tickets_from_api()

    # Actualizar cache
    cache['data'] = tickets
    cache['timestamp'] = now

    return tickets

def filter_by_year(tickets, year):
    """Filtra tickets por año"""
    if not year or year == 'all':
        return tickets
    return [t for t in tickets if t['created_at'].startswith(year)]

def analyze_trends(tickets):
    """Análisis completo de tendencias temporales con heatmap"""
    # Contadores
    monthly_created = Counter()
    weekday_count = Counter()
    hourly_count = Counter()
    heatmap_data = {}
    date_counter = Counter()

    days_es = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    for ticket in tickets:
        created_str = ticket.get('created_at', '')
        if created_str:
            try:
                created = datetime.fromisoformat(created_str.replace('Z', '+00:00'))

                # Mes/Año
                month_key = created.strftime('%Y-%m')
                monthly_created[month_key] += 1

                # Día de la semana
                weekday = days_es[created.weekday()]
                weekday_count[weekday] += 1

                # Hora del día
                hour = created.hour
                hourly_count[hour] += 1

                # Heatmap (día x hora)
                if weekday not in heatmap_data:
                    heatmap_data[weekday] = {}
                if hour not in heatmap_data[weekday]:
                    heatmap_data[weekday][hour] = 0
                heatmap_data[weekday][hour] += 1

                # Contador de fechas
                date_key = created.strftime('%Y-%m-%d')
                date_counter[date_key] += 1

            except Exception as e:
                print(f"Error procesando fecha: {e}")
                pass

    # Encontrar hora pico
    max_hour = 0
    max_count = 0
    max_day = ''
    for day in heatmap_data:
        for hour in heatmap_data[day]:
            if heatmap_data[day][hour] > max_count:
                max_count = heatmap_data[day][hour]
                max_hour = hour
                max_day = day

    # Calcular promedios
    total_days = len(date_counter) if date_counter else 1
    closed_tickets = sum(1 for t in tickets if t.get('status') in [4, 5])

    avg_daily_created = len(tickets) / total_days
    avg_daily_resolved = closed_tickets / total_days

    # Día con mayor carga
    max_load_date = None
    max_load_count = 0
    if date_counter:
        max_load_date, max_load_count = date_counter.most_common(1)[0]

    return {
        'monthly_created': dict(monthly_created),
        'weekday_distribution': dict(weekday_count),
        'hourly_distribution': dict(hourly_count),
        'heatmap': heatmap_data,
        'peak_hour': {
            'day': max_day,
            'hour': max_hour,
            'count': max_count
        },
        'avg_daily_created': round(avg_daily_created, 2),
        'avg_daily_resolved': round(avg_daily_resolved, 2),
        'max_load_day': {
            'date': max_load_date,
            'count': max_load_count
        }
    }

# ============================================================
# ENDPOINTS DE LA API
# ============================================================

@app.route('/')
def index():
    """Sirve el HTML del visor avanzado"""
    return send_file('index.html')

@app.route('/api/tickets')
def get_tickets():
    """Endpoint: Retorna todos los tickets"""
    year = request.args.get('year')
    tickets = get_cached_tickets()
    filtered = filter_by_year(tickets, year)

    return jsonify({
        "success": True,
        "tickets": filtered,
        "total": len(filtered),
        "cached": True,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/kpis')
def get_kpis():
    """Endpoint: KPIs de rendimiento"""
    year = request.args.get('year')
    tickets = get_cached_tickets()
    filtered = filter_by_year(tickets, year)

    total = len(filtered)
    if total == 0:
        return jsonify({
            "success": True,
            "kpis": {
                "total": 0,
                "closed": 0,
                "open": 0,
                "resolution_rate": 0,
                "by_priority": {"alta": 0, "media": 0, "baja": 0},
                "percentages": {"alta": 0, "media": 0, "baja": 0}
            }
        })

    closed = sum(1 for t in filtered if t.get('status') in [4, 5])
    alta = sum(1 for t in filtered if t.get('priority') == 3)
    media = sum(1 for t in filtered if t.get('priority') == 2)
    baja = sum(1 for t in filtered if t.get('priority') == 1)

    return jsonify({
        "success": True,
        "kpis": {
            "total": total,
            "closed": closed,
            "open": total - closed,
            "resolution_rate": round((closed / total * 100), 2),
            "by_priority": {
                "alta": alta,
                "media": media,
                "baja": baja
            },
            "percentages": {
                "alta": round((alta / total * 100), 1),
                "media": round((media / total * 100), 1),
                "baja": round((baja / total * 100), 1)
            }
        }
    })

@app.route('/api/recurrence')
def get_recurrence():
    """Endpoint: Análisis de tickets recurrentes"""
    year = request.args.get('year')
    tickets = get_cached_tickets()
    filtered = filter_by_year(tickets, year)

    counts = Counter([t['subject'] for t in filtered if t.get('subject')])
    total = len(filtered)

    recurrence = [
        {
            "subject": subject,
            "count": count,
            "percentage": round((count / total * 100), 1) if total > 0 else 0
        }
        for subject, count in counts.most_common(20)
    ]

    return jsonify({
        "success": True,
        "recurrence": recurrence,
        "total": total
    })

@app.route('/api/trends')
def get_trends():
    """Endpoint: Análisis de tendencias y heatmap"""
    year = request.args.get('year')
    tickets = get_cached_tickets()
    filtered = filter_by_year(tickets, year)

    trends = analyze_trends(filtered)

    return jsonify({
        "success": True,
        "trends": trends
    })

@app.route('/api/refresh')
def refresh_cache():
    """Fuerza actualización del cache"""
    cache['data'] = None
    cache['timestamp'] = None
    tickets = get_cached_tickets()

    return jsonify({
        "success": True,
        "message": "Cache actualizado",
        "total_tickets": len(tickets)
    })

# ============================================================
# INICIO DEL SERVIDOR
# ============================================================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    print("\n" + "="*60)
    print("SERVIDOR FRESHDESK V6.0 - ANALISIS AVANZADO")
    print("="*60)
    print(f"Cliente: {CLIENTE}")
    print(f"Company ID: {COMPANY_ID}")
    print(f"Dominio: {FRESHDESK_DOMAIN}.freshdesk.com")
    print(f"\nServidor corriendo en: http://localhost:{port}")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False)
