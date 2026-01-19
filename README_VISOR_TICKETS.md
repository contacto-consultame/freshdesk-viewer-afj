# 🎫 Visor de Tickets Freshdesk - AFJ Global

## ¿Qué es esto?

Una aplicación web interactiva que te permite buscar, filtrar y visualizar los tickets de Freshdesk del cliente AFJ Global de forma fácil y rápida.

## 📁 Archivos Generados

En tu **Escritorio** encontrarás:

1. **freshdesk_viewer.html** - La página web principal
2. **tickets_data.json** - Los datos de los 613 tickets
3. **reporte_freshdesk_AFJ_Global.xlsx** - El Excel original
4. **resumen_reporte_AFJ_Global.txt** - Resumen en texto

## 🚀 Cómo Usar

### Opción 1: Abrir Directamente (Recomendado)
1. Ve a tu **Escritorio**
2. Haz doble clic en **freshdesk_viewer.html**
3. Se abrirá en tu navegador predeterminado

### Opción 2: Desde el Navegador
1. Abre tu navegador (Chrome, Safari, Firefox)
2. Arrastra el archivo **freshdesk_viewer.html** a la ventana del navegador

## ✨ Funcionalidades

### 1. Dashboard de Estadísticas
En la parte superior verás:
- Total de tickets (613)
- Tickets por prioridad (Baja, Media, Alta, Urgente)

### 2. Búsqueda Inteligente
- **Búsqueda en tiempo real**: Escribe en el campo de búsqueda y los resultados se filtran automáticamente
- Busca por:
  - Asunto del ticket
  - Descripción
  - ID del ticket

### 3. Filtros
- **Filtro por prioridad**: Selecciona una prioridad específica o ve todas
- **Botón Limpiar**: Resetea todos los filtros y la búsqueda

### 4. Selector de Tickets
- **Checkbox**: Cada ticket tiene un checkbox para seleccionarlo
- **Click en la tarjeta**: También puedes hacer click en la tarjeta completa para seleccionar
- **Contador**: Ve cuántos tickets has seleccionado en tiempo real

### 5. Tarjetas de Tickets
Cada ticket muestra:
- ID del ticket
- Asunto completo
- Descripción (primeros 200 caracteres)
- Badge de prioridad con color:
  - 🟢 Verde: Prioridad Baja
  - 🟡 Amarillo: Prioridad Media
  - 🔴 Rojo: Prioridad Alta
  - ⚠️ Rojo parpadeante: Prioridad Urgente
- Fecha de creación
- Etiquetas (si las tiene)

### 6. Interactividad
- **Hover**: Al pasar el mouse sobre un ticket, se resalta
- **Selección**: Los tickets seleccionados se destacan con fondo azul
- **Responsive**: Funciona en computadoras, tablets y móviles

## 💡 Ejemplos de Uso

### Buscar tickets de Windows
1. Escribe "Windows" en el campo de búsqueda
2. Verás todos los tickets relacionados con Windows

### Ver solo tickets urgentes
1. Selecciona "Urgente" en el filtro de prioridad
2. Se mostrarán solo los tickets urgentes

### Buscar un ticket específico por ID
1. Escribe el número del ticket (ej: "12345")
2. Encontrará el ticket exacto

### Seleccionar múltiples tickets
1. Busca o filtra los tickets que necesitas
2. Haz click en los checkboxes de los tickets que quieres seleccionar
3. El contador te dirá cuántos has seleccionado

## 🔄 Actualizar los Datos

Si necesitas actualizar los datos con tickets nuevos:

1. Ejecuta el script de Python:
   ```bash
   python3 freshdesk_report_optimized.py
   ```

2. Convierte el nuevo Excel a JSON:
   ```bash
   python3 convert_excel_to_json.py
   ```

3. Refresca la página web (F5 o Cmd+R)

## 🛠️ Scripts Disponibles

En tu carpeta de usuario (`/Users/ladydayanaradarobertis/`):

1. **freshdesk_report_optimized.py** - Obtiene tickets de Freshdesk y genera Excel
2. **convert_excel_to_json.py** - Convierte el Excel a JSON para la web
3. **test_freshdesk_api.py** - Prueba la conexión con la API de Freshdesk

## 📊 Tecnologías Usadas

- **HTML5**: Estructura de la página
- **CSS3**: Diseño moderno y responsive
- **JavaScript (Vanilla)**: Funcionalidad sin dependencias externas
- **Python**: Scripts para obtener y procesar datos

## 🎨 Características de Diseño

- Gradiente morado moderno
- Tarjetas con sombras y animaciones suaves
- Diseño responsive (se adapta a cualquier pantalla)
- Colores de prioridad intuitivos
- Animación de "pulso" para tickets urgentes
- Efectos hover para mejor UX

## ⚡ Rendimiento

- Carga instantánea de 613 tickets
- Búsqueda en tiempo real sin retrasos
- Sin dependencias externas (funciona offline)
- Tamaño ligero del archivo JSON (~200KB)

## 🔒 Seguridad

- Los datos están completamente offline en tu computadora
- No se envía información a ningún servidor externo
- La API key está solo en los scripts Python, no en la web

## 🆘 Problemas Comunes

### La página está en blanco
- Asegúrate de que **tickets_data.json** está en la misma carpeta que **freshdesk_viewer.html**
- Ambos archivos deben estar en el Escritorio

### No se ven los tickets
- Abre la consola del navegador (F12) y revisa si hay errores
- Verifica que el archivo JSON se haya generado correctamente

### Los datos están desactualizados
- Ejecuta nuevamente el script de Python para obtener datos frescos
- Convierte el nuevo Excel a JSON

## 📞 Próximos Pasos

Puedes mejorar la aplicación agregando:
- Exportar tickets seleccionados a Excel
- Gráficas de estadísticas con Chart.js
- Conexión directa con la API de Freshdesk
- Filtros por fecha
- Ordenamiento personalizado

## 📄 Licencia

Uso interno para AFJ Global

---

**Generado el:** 18 de Enero 2026
**Total de tickets:** 613
**Período:** 2025 - 2026
