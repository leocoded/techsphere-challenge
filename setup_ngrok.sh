#!/bin/bash

# Script de configuración rápida para Ngrok con TechSphere API

echo "🔧 Configuración rápida de Ngrok para TechSphere API"
echo "=================================================="

# Verificar si Ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    echo "❌ Ngrok no está instalado en el sistema"
    echo ""
    echo "💡 Para instalar Ngrok:"
    echo "   1. Visita: https://ngrok.com/download"
    echo "   2. Descarga e instala para macOS"
    echo "   3. O usando Homebrew: brew install ngrok/ngrok/ngrok"
    echo ""
    read -p "¿Quieres continuar sin Ngrok instalado? (y/n): " continue_without
    if [[ $continue_without != "y" && $continue_without != "Y" ]]; then
        echo "❌ Instalación cancelada"
        exit 1
    fi
fi

# Verificar token de autenticación
echo ""
echo "🔑 Configuración del token de autenticación de Ngrok"
echo "   Para obtener un token gratuito:"
echo "   1. Visita: https://dashboard.ngrok.com/get-started/your-authtoken"
echo "   2. Crea una cuenta gratuita si no tienes una"
echo "   3. Copia tu token de autenticación"
echo ""

read -p "¿Tienes un token de Ngrok? (y/n): " has_token

if [[ $has_token == "y" || $has_token == "Y" ]]; then
    read -p "Introduce tu token de Ngrok: " ngrok_token
    
    # Configurar token en Ngrok
    if command -v ngrok &> /dev/null; then
        ngrok config add-authtoken $ngrok_token
        echo "✅ Token configurado en Ngrok"
    fi
    
    # Guardar token como variable de entorno (opcional)
    echo "export NGROK_AUTH_TOKEN='$ngrok_token'" >> ~/.zshrc
    echo "✅ Token guardado en ~/.zshrc"
    
else
    echo "⚠️  Sin token, Ngrok tendrá limitaciones (sesiones de 2 horas)"
fi

echo ""
echo "🚀 Configuración completada!"
echo ""
echo "📋 Comandos disponibles:"
echo "   • Solo local:    python run_api.py"
echo "   • Con Ngrok:     python run_api.py --ngrok"
echo "   • Con token:     python run_api.py --ngrok --ngrok-token TU_TOKEN"
echo "   • Puerto custom: python run_api.py --ngrok --port 8080"
echo ""
echo "📖 Para más información, consulta: USAGE_GUIDE.md"
