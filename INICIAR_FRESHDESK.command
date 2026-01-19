#!/bin/bash

echo "============================================================"
echo "🚀 INICIANDO VISOR DE TICKETS FRESHDESK"
echo "============================================================"
echo ""

cd ~

# Detener servidor anterior si existe
pkill -f freshdesk_server.py 2>/dev/null

echo "📡 Iniciando servidor..."
python3 freshdesk_server.py > /tmp/freshdesk_server.log 2>&1 &
SERVER_PID=$!
echo $SERVER_PID > /tmp/freshdesk_server.pid

echo "⏳ Esperando que el servidor inicie..."
sleep 5

# Verificar si el servidor está corriendo
if curl -s http://localhost:8080 > /dev/null; then
    echo "✅ Servidor corriendo correctamente en puerto 8080"
    echo ""
    echo "🌐 Abriendo navegador..."
    open http://localhost:8080
    echo ""
    echo "============================================================"
    echo "✨ ¡LISTO! La aplicación se abrió en tu navegador"
    echo "============================================================"
    echo ""
    echo "📋 Información:"
    echo "   URL: http://localhost:8080"
    echo "   PID del servidor: $SERVER_PID"
    echo ""
    echo "🛑 Para detener el servidor:"
    echo "   Ejecuta: kill $SERVER_PID"
    echo "   O presiona Ctrl+C en esta ventana"
    echo ""
    echo "============================================================"
    echo ""

    # Mantener la terminal abierta
    echo "Presiona Ctrl+C para detener el servidor..."
    wait $SERVER_PID
else
    echo "❌ Error: El servidor no pudo iniciarse"
    echo "Revisa el log en: /tmp/freshdesk_server.log"
    exit 1
fi
