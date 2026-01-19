#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Flask para Visor de Tickets Freshdesk - AFJ Global
Versión con análisis avanzado: Tendencias, KPIs, Criticidad, Recurrencia
"""

from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
import requests
from datetime import datetime, timedelta
from collections import Counter
import json
import time

app = Flask(__name__)
CORS(app)

# ============================================================
# CONFIGURACIÓN - REEMPLAZAR CON TUS CREDENCIALES
# ============================================================
FRESHDESK_DOMAIN = "consultame.freshdesk.com"
FRESHDESK_API_KEY = "6egUChwBAUA2633n18DC"
COMPANY_ID = 63000424434  # AFJ Global
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

def get_freshdesk_tickets():
    """Obtiene tickets de Freshdesk API"""
    url = f"https://{FRESHDESK_DOMAIN}/api/v2/tickets"
    headers = {"Content-Type": "application/json"}

    all_tickets = []
    page = 1

    try:
        while True:
            params = {
                'page': page,
                'per_page': 100,
                'order_by': 'created_at',
                'order_type': 'desc'
            }

            response = requests.get(
                url,
                auth=(FRESHDESK_API_KEY, 'X'),
                headers=headers,
                params=params,
                timeout=30
            )

            if response.status_code == 200:
                tickets = response.json()
                if not tickets:
                    break
                all_tickets.extend(tickets)
                page += 1

                # Limitar a 1000 tickets para evitar timeouts
                if len(all_tickets) >= 1000:
                    break
            else:
                print(f"Error {response.status_code}: {response.text}")
                break

        return all_tickets
    except Exception as e:
        print(f"Error obteniendo tickets: {e}")
        return []

def classify_priority(ticket):
    """Clasifica la criticidad del ticket basado en keywords"""
    subject = ticket.get('subject', '').lower()
    description = ticket.get('description_text', '').lower()
    text = f"{subject} {description}"

    # Keywords para criticidad ALTA
    keywords_alta = [
        'aws', 'alarm', 'no enciende', 'no prende', 'escritorio remoto',
        'virus', 'malware', 'error servidor', 'afjlearning',
        'sharepoint lentitud', 'moodle', 'caído', 'down', 'critical'
    ]

    # Keywords para criticidad MEDIA
    keywords_media = [
        'outlook', 'correo', 'fundae', 'limpieza', 'buzón', 'antivirus',
        'pst', 'revisar pc', 'sharepoint', 'spam', 'cambio licencia',
        'acceso carpeta', 'email', 'password'
    ]

    # Clasificar
    for keyword in keywords_alta:
        if keyword in text:
            return 'Alto'

    for keyword in keywords_media:
        if keyword in text:
            return 'Medio'

    return 'Bajo'

def get_cached_tickets():
    """Retorna tickets del cache o hace una nueva petición"""
    now = time.time()

    # Si hay cache válido, retornarlo
    if cache['data'] and cache['timestamp']:
        if now - cache['timestamp'] < cache['ttl']:
            return cache['data']

    # Si no hay cache o expiró, obtener nuevos datos
    tickets = get_freshdesk_tickets()

    # Procesar y enriquecer tickets
    processed_tickets = []
    for ticket in tickets:
        processed = {
            'id': ticket.get('id'),
            'subject': ticket.get('subject', 'Sin asunto'),
            'description': ticket.get('description_text', ''),
            'status': ticket.get('status'),
            'priority': classify_priority(ticket),
            'created_at': ticket.get('created_at'),
            'updated_at': ticket.get('updated_at'),
            'tags': ', '.join(ticket.get('tags', []))
        }
        processed_tickets.append(processed)

    # Actualizar cache
    cache['data'] = processed_tickets
    cache['timestamp'] = now

    return processed_tickets

def analyze_recurrence(tickets):
    """Analiza tickets recurrentes"""
    subjects = [t['subject'] for t in tickets if t.get('subject')]
    counter = Counter(subjects)

    # Top 20 más recurrentes
    top_20 = [
        {'subject': subject, 'count': count}
        for subject, count in counter.most_common(20)
    ]

    return top_20

def analyze_trends(tickets):
    """Análisis de tendencias temporales"""
    # Tickets por mes
    monthly_created = Counter()
    monthly_resolved = Counter()

    # Tickets por día de la semana
    weekday_count = Counter()

    # Tickets por hora del día
    hourly_count = Counter()

    # Mapa de calor (día x hora)
    heatmap_data = {}

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

                # Heatmap
                if weekday not in heatmap_data:
                    heatmap_data[weekday] = {}
                if hour not in heatmap_data[weekday]:
                    heatmap_data[weekday][hour] = 0
                heatmap_data[weekday][hour] += 1

            except:
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

    # Calcular promedios diarios
    if len(monthly_created) > 0:
        total_days = len(set(t.get('created_at', '')[:10] for t in tickets if t.get('created_at')))
        avg_daily_created = len(tickets) / max(total_days, 1)
        avg_daily_resolved = sum(1 for t in tickets if t.get('status') in [4, 5]) / max(total_days, 1)
    else:
        avg_daily_created = 0
        avg_daily_resolved = 0

    # Día con mayor carga
    max_load_count = 0
    max_load_date = None
    date_counter = Counter(t.get('created_at', '')[:10] for t in tickets if t.get('created_at'))
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

def calculate_kpis(tickets):
    """Calcula KPIs de rendimiento"""
    total = len(tickets)
    if total == 0:
        return {}

    # Estados
    closed = sum(1 for t in tickets if t.get('status') in [4, 5])
    open_tickets = total - closed

    # Por criticidad
    alta = sum(1 for t in tickets if t.get('priority') == 'Alto')
    media = sum(1 for t in tickets if t.get('priority') == 'Medio')
    baja = sum(1 for t in tickets if t.get('priority') == 'Bajo')

    # Tasa de resolución
    resolution_rate = (closed / total * 100) if total > 0 else 0

    return {
        'total_tickets': total,
        'tickets_closed': closed,
        'tickets_open': open_tickets,
        'resolution_rate': round(resolution_rate, 2),
        'criticality': {
            'alta': alta,
            'media': media,
            'baja': baja
        },
        'percentages': {
            'alta': round(alta / total * 100, 1) if total > 0 else 0,
            'media': round(media / total * 100, 1) if total > 0 else 0,
            'baja': round(baja / total * 100, 1) if total > 0 else 0
        }
    }

# ============================================================
# ENDPOINTS DE LA API
# ============================================================

@app.route('/')
def index():
    """Sirve el HTML del visor"""
    return send_file('visor_freshdesk_avanzado.html')

@app.route('/api/tickets')
def get_tickets():
    """Endpoint principal: Retorna todos los tickets con análisis"""
    tickets = get_cached_tickets()

    return jsonify({
        'success': True,
        'tickets': tickets,
        'total': len(tickets),
        'cached': True,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/recurrence')
def get_recurrence():
    """Endpoint: Análisis de recurrencia"""
    tickets = get_cached_tickets()
    recurrence = analyze_recurrence(tickets)

    return jsonify({
        'success': True,
        'top_20': recurrence
    })

@app.route('/api/trends')
def get_trends():
    """Endpoint: Análisis de tendencias"""
    tickets = get_cached_tickets()
    trends = analyze_trends(tickets)

    return jsonify({
        'success': True,
        'trends': trends
    })

@app.route('/api/kpis')
def get_kpis():
    """Endpoint: KPIs de rendimiento"""
    tickets = get_cached_tickets()
    kpis = calculate_kpis(tickets)

    return jsonify({
        'success': True,
        'kpis': kpis
    })

@app.route('/api/refresh')
def refresh_cache():
    """Fuerza actualización del cache"""
    cache['data'] = None
    cache['timestamp'] = None
    tickets = get_cached_tickets()

    return jsonify({
        'success': True,
        'message': 'Cache actualizado',
        'total_tickets': len(tickets)
    })

# ============================================================
# INICIO DEL SERVIDOR
# ============================================================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("SERVIDOR FRESHDESK EN TIEMPO REAL")
    print("="*60)
    print(f"Cliente: {CLIENTE}")
    print(f"Company ID: {COMPANY_ID}")
    print(f"Dominio: {FRESHDESK_DOMAIN}")
    print(f"\nServidor corriendo en: http://localhost:8080")
    print("="*60 + "\n")

    app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
