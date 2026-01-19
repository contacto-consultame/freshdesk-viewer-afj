# 🚀 Guía del Visor de Tickets en Tiempo Real

## ¿Qué es esto?

Un sistema completo que conecta directamente con la API de Freshdesk en TIEMPO REAL para mostrar los tickets de AFJ Global de 2025 y 2026.

## ⚡ Diferencia con la versión anterior

- **Versión Anterior**: Usaba datos estáticos del archivo JSON (se actualizaba manualmente)
- **Versión Nueva (Tiempo Real)**: Se conecta directamente a Freshdesk y obtiene datos frescos cada vez que lo solicitas

## 📁 Archivos del Sistema

1. **freshdesk_server.py** - Servidor backend que se conecta a Freshdesk
2. **freshdesk_viewer_realtime.html** - Página web que se conecta al servidor
3. **freshdesk_report_optimized.py** - Script para generar reportes en Excel (opcional)

## 🎯 Cómo Usar

### Paso 1: Iniciar el Servidor

Abre la terminal y ejecuta:

```bash
cd ~
python3 freshdesk_server.py
```

Deberías ver algo como:

```
============================================================
🚀 SERVIDOR FRESHDESK EN TIEMPO REAL
============================================================
Cliente: AFJ Global
Company ID: 63000424434
Dominio: consultame.freshdesk.com

📡 Servidor corriendo en: http://localhost:8080
============================================================
```

**⚠️ IMPORTANTE**: Deja esta terminal abierta mientras uses la aplicación.

### Paso 2: Abrir la Aplicación Web

**Opción A**: Abrir automáticamente desde el navegador:
- Ve a: http://localhost:8080

**Opción B**: O simplemente espera, el navegador debería abrirse automáticamente.

### Paso 3: Usar la Aplicación

La página se cargará y automáticamente obtendrá los tickets más recientes de Freshdesk.

## ✨ Funcionalidades

### 1. Badge "EN VIVO"
- En la esquina superior derecha verás un badge verde parpadeante
- Indica que estás viendo datos en tiempo real

### 2. Botón "Actualizar"
- Click en "🔄 Actualizar" para obtener los tickets más recientes
- Los datos se cachean por 5 minutos para no saturar la API

### 3. Última Actualización
- Muestra cuándo se obtuvieron los datos por última vez

### 4. Filtros de Prioridad (igual que antes)
- Todos / Baja / Media / Alta / Urgente
- Click en las tarjetas superiores o en los botones

### 5. Búsqueda en Tiempo Real
- Escribe y los resultados se filtran automáticamente

### 6. Selección de Tickets
- Marca los checkboxes para seleccionar múltiples tickets

## 🔄 Actualizar Datos

Para obtener los tickets más recientes:

1. Click en el botón "🔄 Actualizar"
2. Espera unos segundos
3. Los datos se refrescarán automáticamente

**Nota**: El sistema tiene un cache de 5 minutos para evitar hacer demasiadas peticiones a Freshdesk.

## 🛑 Detener el Servidor

Cuando termines de usar la aplicación:

1. Ve a la terminal donde está corriendo el servidor
2. Presiona **Ctrl+C**
3. El servidor se detendrá

## 🔧 Solución de Problemas

### Error: "No se pudo conectar con el servidor"

**Causa**: El servidor Python no está corriendo.

**Solución**:
```bash
python3 freshdesk_server.py
```

### Error: "Address already in use"

**Causa**: Ya hay un servidor corriendo en el puerto 5000.

**Solución**:
```bash
# Detener el servidor anterior
pkill -f freshdesk_server.py

# Iniciar nuevamente
python3 freshdesk_server.py
```

### Los tickets no se actualizan

**Causa**: Cache activo (5 minutos).

**Solución**:
- Espera 5 minutos, O
- Usa el endpoint de refresh: http://localhost:8080/api/refresh

### Error 429 (Rate Limit)

**Causa**: Demasiadas peticiones a Freshdesk.

**Solución**: Espera 1 minuto y vuelve a intentar.

## 🎨 Características de la Interfaz

### Indicadores Visuales
- 🟢 Verde parpadeante = EN VIVO
- Badge activo = Filtro aplicado
- Borde azul en tarjeta = Ticket seleccionado

### Colores de Prioridad
- 🟢 Verde = Prioridad Baja
- 🟡 Amarillo = Prioridad Media
- 🔴 Rojo = Prioridad Alta
- ⚠️ Rojo parpadeante = Prioridad Urgente

### Scroll Personalizado
- La lista de tickets tiene scroll con colores del tema
- Máximo 800px de altura
- Barra de scroll morada

## 📊 Endpoints de la API

El servidor expone 3 endpoints:

1. **GET /** - Sirve la página HTML
   ```
   http://localhost:8080/
   ```

2. **GET /api/tickets** - Obtiene tickets (con cache de 5 min)
   ```
   http://localhost:8080/api/tickets
   ```

3. **GET /api/refresh** - Fuerza actualización inmediata
   ```
   http://localhost:8080/api/refresh
   ```

## 🔐 Seguridad

- El API key está en el servidor Python, NO en el navegador
- El servidor solo es accesible localmente (localhost)
- No se expone a Internet

## 💾 Cache

- **Duración**: 5 minutos
- **Motivo**: Evitar rate limiting de Freshdesk
- **Bypass**: Usa el endpoint `/api/refresh` o espera 5 minutos

## 📈 Ventajas vs Versión Estática

| Característica | Versión Estática | Versión Tiempo Real |
|----------------|------------------|---------------------|
| Datos actualizados | Manual | Automático |
| Click para actualizar | ❌ | ✅ |
| Requiere regenerar JSON | ✅ | ❌ |
| Funciona offline | ✅ | ❌ |
| Datos más frescos | ❌ | ✅ |

## 🚀 Iniciar Rápidamente

Script de 1 línea:

```bash
cd ~ && python3 freshdesk_server.py
```

Luego abre: http://localhost:8080

## 📝 Notas Importantes

1. **Terminal abierta**: Debes mantener la terminal abierta mientras usas la app
2. **Cache de 5 min**: Los datos se cachean para evitar sobrecarga
3. **Solo local**: La aplicación solo funciona en tu computadora
4. **API Key**: Ya está configurada en el servidor

## ⚙️ Personalización

### Cambiar el tiempo de cache

Edita `freshdesk_server.py` línea 18:

```python
'ttl': 300  # Cambia a los segundos que quieras
```

### Cambiar el puerto

Edita `freshdesk_server.py` última línea:

```python
app.run(debug=True, port=5000)  # Cambia 5000 a otro puerto
```

### Filtrar por otro cliente

Edita `freshdesk_server.py` líneas 16-17:

```python
CLIENTE = "AFJ Global"  # Cambia el nombre
COMPANY_ID = 63000424434  # Cambia el ID
```

## 📞 Comandos Útiles

```bash
# Iniciar servidor
python3 freshdesk_server.py

# Detener servidor
Ctrl+C

# Matar servidor si se quedó colgado
pkill -f freshdesk_server.py

# Ver si el servidor está corriendo
curl http://localhost:8080/api/tickets

# Forzar actualización
curl http://localhost:8080/api/refresh
```

## 🎓 Para Desarrolladores

La arquitectura es simple:

```
[Navegador] <--> [Flask Server] <--> [Freshdesk API]
              (Python)            (REST API)
```

- Frontend: HTML + JavaScript (Vanilla)
- Backend: Flask (Python)
- API: Freshdesk REST API v2

---

**Generado el**: 18 de Enero 2026
**Cliente**: AFJ Global
**Período**: 2025 - 2026
