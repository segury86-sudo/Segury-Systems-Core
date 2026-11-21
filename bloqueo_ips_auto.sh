#!/data/data/com.termux/files/usr/bin/bash

# ==============================================
# SISTEMA DE DETECCIÓN Y BLOQUEO DE IPS
# Alertas automáticas en RUSO
# ==============================================

ARCHIVO_LOGS="logs_mosquitto.txt"
ARCHIVO_BLOQUEADAS="ips_bloqueadas.txt"
UMBRAL_INTENTOS=5
TIEMPO_MONITOREO=60

# Crear archivos si no existen
mkdir -p logs
touch "$ARCHIVO_BLOQUEADAS"

echo "=================================================="
echo "🛡️  SISTEMA DE BLOQUEO AUTOMÁTICO ACTIVADO"
echo "Umbral: $UMBRAL_INTENTOS intentos | Tiempo: $TIEMPO_MONITOREO seg"
echo "=================================================="

# Función: Enviar alerta en RUSO
alerta_ruso() {
    local ip=$1
    local razon=$2
    local mensaje="
⚠️  ВНИМАНИЕ! ПОДОЗРИТЕЛЬНАЯ АКТИВНОСТЬ
=========================================
🔒 IP-АДРЕС ЗАБЛОКИРОВАН: $ip
📋 ПРИЧИНА: $razon
⏰ ВРЕМЯ: $(date '+%d.%m.%Y %H:%M:%S')
⚠️  ДОСТУП ЗАПРЕЩЕН. ПОВТОРНЫЙ ВХОД ЗАПРЕЩЕН.
========================================="
    echo -e "$mensaje"
    
    # Enviar por MQTT al sistema
    mosquitto_pub -t "segury/alerta/ip" -m "$mensaje" 2>/dev/null
    
    # Guardar en registro
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] BLOQUEADA: $ip — $razon" >> logs/registro_bloqueos.log
    echo "$ip" >> "$ARCHIVO_BLOQUEADAS"
}

# Función: Bloquear IP
bloquear_ip() {
    local ip=$1
    local razon=$2
    
    # Verificar si ya está bloqueada
    if grep -q "^$ip$" "$ARCHIVO_BLOQUEADAS" 2>/dev/null; then
        echo "ℹ️  IP $ip ya estaba bloqueada"
        return
    fi
    
    echo "🚨 DETECTADA IP SOSPECHOSA: $ip — $razon"
    
    # Bloquear en Termux/hosts (bloqueo local)
    if ! grep -q "^$ip" /data/data/com.termux/files/usr/etc/hosts 2>/dev/null; then
        echo "127.0.0.1   $ip" >> /data/data/com.termux/files/usr/etc/hosts
    fi
    
    # Enviar alerta en ruso
    alerta_ruso "$ip" "$razon"
}

# ==============================================
# MOTOR DE ESCANEO Y DETECCIÓN
# ==============================================
echo "🔍 Escaneando conexiones al puerto 1883..."

while true; do
    # Revisar conexiones activas al broker MQTT
    CONEXIONES=$(netstat -tn 2>/dev/null | grep ":1883" | grep "ESTABLISHED" | awk '{print $5}' | cut -d: -f1 | sort | uniq -c)
    
    if [ -n "$CONEXIONES" ]; then
        echo "$CONEXIONES" | while read -r cantidad ip; do
            if [ "$cantidad" -gt "$UMBRAL_INTENTOS" ]; then
                bloquear_ip "$ip" "Demasiadas conexiones ($cantidad intentos)"
            fi
        done
    fi
    
    # Detectar escaneo de puertos
    ESCANEO=$(ss -tuln 2>/dev/null | grep -E ":(22|80|443|1883|8080)" | awk '{print $5}' | grep -v "0.0.0.0" | grep -v ":::" | cut -d: -f1 | sort | uniq -c | sort -rn | head -5)
    
    if echo "$ESCANEO" | grep -qE "^[[:space:]]*[6-9][0-9]|^[[:space:]]*[0-9]{2,}"; then
        ip_sospechosa=$(echo "$ESCANEO" | head -1 | awk '{print $2}')
        bloquear_ip "$ip_sospechosa" "Escaneo de puertos detectado"
    fi
    
    sleep $TIEMPO_MONITOREO
done
