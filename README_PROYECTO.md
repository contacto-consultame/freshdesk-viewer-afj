# 🎫 Visor de Tickets Freshdesk - AFJ Global V6.0

## 📌 Enlaces Importantes

- **GitHub Pages (Publicado)**: https://contacto-consultame.github.io/freshdesk-viewer-afj/
- **Repositorio GitHub**: https://github.com/contacto-consultame/freshdesk-viewer-afj
- **Servidor Local**: http://localhost:8080

---

## 🚀 Inicio Rápido - Servidor Local

### 1. Iniciar el Servidor
```bash
cd "C:\Users\Srv-LAB\Desktop\AFJ GLOBAL\AFJ Global"
py freshdesk_server.py
```

### 2. Abrir en Navegador
http://localhost:8080

### 3. Detener el Servidor
```bash
taskkill /F /IM py.exe
```

---

## 📁 Archivos Principales

### Servidor Python:
- **freshdesk_server.py** - Servidor Flask V6.0 con API REST

### HTML/Frontend:
- **visor_freshdesk_avanzado.html** - Versión avanzada con 5 pestañas (para localhost)
- **index.html** - Versión publicada en GitHub Pages (actualmente básica)
- **freshdesk_viewer.html** - Versión original básica

### Datos:
- **tickets_data.json** - 613 tickets estáticos para versión offline

---

## 🎯 Versión Actual vs Objetivo

### ❌ GitHub Pages (Actual)
- Visor básico
- Sin pestañas
- Sin gráficos
- Datos estáticos
- Sin selector de año

### ✅ Localhost:8080 (Funcionando)
- 5 pestañas de análisis
- Badge "EN VIVO"
- Gráficos interactivos
- Heatmap 7x24
- Selector de año
- Conexión a Freshdesk API

### 🎯 Objetivo
Hacer que GitHub Pages se vea como la versión local

---

## 🔧 Configuración

### Credenciales Freshdesk (ya configuradas en freshdesk_server.py):
```python
FRESHDESK_DOMAIN = "consultame.freshdesk.com"
FRESHDESK_API_KEY = "6egUChwBAUA2633n18DC"
COMPANY_ID = 63000424434
```

### Python Instalado:
- Python 3.14.2
- flask==3.1.2
- flask-cors==6.0.2
- requests==2.32.5

---

## 📊 Características de la Versión 6.0

### Pestañas:
1. **Todos los Tickets** - Lista completa con filtros
2. **Análisis de Recurrencia** - Top 20 más frecuentes
3. **Análisis por Criticidad** - Distribución por prioridad
4. **Métricas (KPIs)** - Total, cerrados, abiertos, tasa resolución
5. **Tendencias y Carga** - Promedios, heatmap, día pico

### API Endpoints:
- `GET /api/tickets?year=2025`
- `GET /api/kpis?year=2025`
- `GET /api/recurrence?year=2025`
- `GET /api/trends?year=2025`
- `GET /api/refresh`

---

## ⚠️ Problemas Conocidos

1. **GitHub Pages no muestra versión 6.0**
   - Causa: GitHub Pages solo soporta archivos estáticos
   - Solución pendiente: Crear versión estática avanzada o publicar en Render.com

2. **Sin filtro por año en versión publicada**
   - Solo muestra todos los tickets juntos
   - Falta selector de año 2025/2026

3. **Sin conexión en tiempo real en versión publicada**
   - Usa datos estáticos del JSON
   - No se actualiza desde Freshdesk API

---

## 📝 Próximos Pasos

Ver archivo: `C:\Users\Srv-LAB\Desktop\CONTEXTO_COMPLETO_AFJ_GLOBAL.md`

---

**Última actualización**: 19/01/2026
**Contacto**: contacto@solucionpro.cl
