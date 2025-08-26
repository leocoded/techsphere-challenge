# 🌐 Guía de Configuración de Ngrok para TechSphere API

Esta guía te ayudará a configurar Ngrok para exponer tu TechSphere API al público de forma segura.

## ¿Qué es Ngrok?

Ngrok es un servicio que crea un túnel seguro desde internet hacia tu aplicación local, permitiendo que otros accedan a tu API sin necesidad de configurar puertos o DNS.

## 🚀 Configuración Rápida

### Paso 1: Ejecutar el Script de Configuración

```bash
./setup_ngrok.sh
```

### Paso 2: Ejecutar la API con Ngrok

```bash
# Activar entorno virtual
source techsphere-env/bin/activate

# Ejecutar con Ngrok
python run_api.py --ngrok
```

## 🔧 Configuración Manual

### 1. Instalar Ngrok

**macOS (Homebrew):**

```bash
brew install ngrok/ngrok/ngrok
```

**Descarga Manual:**

- Visita: https://ngrok.com/download
- Descarga para tu sistema operativo
- Descomprime y coloca el ejecutable en tu PATH

### 2. Crear Cuenta y Obtener Token (Recomendado)

1. Visita: https://dashboard.ngrok.com/signup
2. Crea una cuenta gratuita
3. Ve a: https://dashboard.ngrok.com/get-started/your-authtoken
4. Copia tu token de autenticación

### 3. Configurar Token

```bash
# Configurar token en Ngrok
ngrok config add-authtoken TU_TOKEN_AQUI

# O configurar como variable de entorno
export NGROK_AUTH_TOKEN="TU_TOKEN_AQUI"
```

## 💻 Comandos Disponibles

```bash
# Solo local (sin Ngrok)
python run_api.py

# Con Ngrok usando token configurado
python run_api.py --ngrok

# Con Ngrok y token específico
python run_api.py --ngrok --ngrok-token TU_TOKEN

# Puerto personalizado
python run_api.py --ngrok --port 8080

# Host personalizado
python run_api.py --ngrok --host 127.0.0.1 --port 8080
```

## 🌍 Acceso Público

Cuando ejecutes con `--ngrok`, obtendrás:

```
🌐 Ngrok túnel creado: https://abc123.ngrok-free.app

🚀 TechSphere API está disponible públicamente en:
   📡 URL pública: https://abc123.ngrok-free.app
   📖 Documentación: https://abc123.ngrok-free.app/api/v1/docs
   🔍 Redoc: https://abc123.ngrok-free.app/api/v1/redoc
   💡 Health check: https://abc123.ngrok-free.app/api/v1/health

🔧 Panel de Ngrok: http://localhost:4040
   (Para ver estadísticas y logs del túnel)
```

## 🔒 Seguridad

### Limitaciones de la Cuenta Gratuita

- **Sesiones de 2 horas**: Sin token, las sesiones expiran
- **Dominios aleatorios**: URLs cambian en cada ejecución
- **Límite de túneles**: 1 túnel simultáneo

### Con Cuenta Autenticada (Gratis)

- **Sin límite de tiempo**: Sesiones permanentes
- **Dominios persistentes**: Posibilidad de URLs fijas (plan pago)
- **Múltiples túneles**: Hasta 3 túneles simultáneos
- **Estadísticas**: Panel de control completo

### Consejos de Seguridad

1. **No compartas URLs públicas** con datos sensibles
2. **Usa tokens de autenticación** para mayor estabilidad
3. **Monitorea el panel** en `http://localhost:4040`
4. **Cierra túneles** cuando no los uses (`Ctrl+C`)

## 🛠️ Troubleshooting

### Error: "ngrok: command not found"

```bash
# Instalar Ngrok
brew install ngrok/ngrok/ngrok
# O descargar de https://ngrok.com/download
```

### Error: "Failed to complete tunnel connection"

```bash
# Verificar token
ngrok config add-authtoken TU_TOKEN

# O configurar variable de entorno
export NGROK_AUTH_TOKEN="TU_TOKEN"
```

### Error: "Port already in use"

```bash
# Usar puerto diferente
python run_api.py --ngrok --port 8001
```

### Error: "Tunnel session failed: Your account is limited"

- Crea cuenta gratuita en https://ngrok.com/
- Configura tu token de autenticación

## 📊 Monitoreo

### Panel Local de Ngrok

Accede a `http://localhost:4040` para ver:

- **Solicitudes HTTP**: Logs en tiempo real
- **Estadísticas**: Ancho de banda, latencia
- **Configuración**: Detalles del túnel activo

### Logs de la API

La API mostrará logs de todas las solicitudes, incluyendo las que vienen a través de Ngrok.

## 🔄 Cierre Seguro

Para cerrar correctamente:

1. Presiona `Ctrl+C` en la terminal
2. El sistema cerrará automáticamente los túneles de Ngrok
3. Liberará el puerto local

## ⚡ Ejemplo de Uso Completo

```bash
# 1. Activar entorno virtual
source techsphere-env/bin/activate

# 2. Ejecutar con Ngrok
python run_api.py --ngrok

# 3. Usar la API públicamente
curl -X POST "https://abc123.ngrok-free.app/api/v1/ml/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "Cardiac study results show improved outcomes."}'

# 4. Cerrar con Ctrl+C
```

## 📞 Soporte

- **Documentación Ngrok**: https://ngrok.com/docs
- **Panel de Control**: https://dashboard.ngrok.com/
- **Soporte Ngrok**: https://ngrok.com/support

¡Ya tienes tu TechSphere API disponible globalmente! 🎉
