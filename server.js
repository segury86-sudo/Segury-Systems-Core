const express = require('express');
const fs = require('fs');
const { exec } = require('child_process');
const crypto = require('crypto');
const mqtt = require('mqtt');

const app = express();
const PORT = 8080;

app.use(express.urlencoded({ extended: true }));

// ========== CONFIGURACIÓN DEL BROKER MQTT ==========
const BROKER_URL = 'mqtt://localhost:1883';
const mqttClient = mqtt.connect(BROKER_URL, {
  clientId: 'SeguryFileCloud_' + crypto.randomUUID().slice(0, 8),
  clean: true
});

mqttClient.on('connect', () => {
  console.log('📡 BROKER MQTT — CONECTADO');
});

mqttClient.on('error', () => {
  console.log('⚠️ Broker no disponible — modo local activo');
});

function publicar(topico, datos) {
  if (mqttClient.connected) {
    mqttClient.publish(topico, JSON.stringify(datos));
  }
}
// =====================================================

const USUARIOS = {
  segury: { pass: hashPass('SEGURYSS'), rol: 'admin', nombre: 'Profesor S' },
  kellynanaki: { pass: hashPass('5538:000000'), rol: 'usuario', nombre: 'Comandante Kellynanaki' }
};

const sesiones = {};
const intentos = {};
const MAX_INTENTOS = 5;

function hashPass(pwd) {
  return crypto.createHash('sha256').update(pwd).digest('hex');
}

function log(texto) {
  const fecha = new Date().toISOString().replace('T', ' ').substr(0, 19);
  fs.appendFileSync('sistema_logs.txt', `[${fecha}] ${texto}\n`);
}

function ejecutar(cmd, res) {
  exec(cmd, (err, stdout, stderr) => {
    res.send(stdout + stderr || '✅ Ejecutado');
  });
}

// Página de inicio / Login
app.get('/', (req, res) => {
  const ip = req.ip;
  const restante = MAX_INTENTOS - (intentos[ip] || 0);
  const brokerEstado = mqttClient.connected ? '🟢 BROKER EN LÍNEA' : '🟡 BROKER DESCONECTADO';
  
  res.send(`
  <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>SEGURY FileCloud</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0;font-family:Courier New,monospace}
    body{background:#0a1020;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
    .caja{background:linear-gradient(135deg,#0f1729,#0a1020);border:2px solid #4af;border-radius:20px;padding:40px 30px;width:100%;max-width:450px;box-shadow:0 0 40px rgba(68,170,255,0.25)}
    h1{text-align:center;color:#aef;font-size:26px;margin-bottom:5px;text-shadow:0 0 15px #4af}
    h2{text-align:center;color:#7bd;font-size:14px;margin-bottom:15px;font-weight:normal}
    .broker{text-align:center;padding:8px;border-radius:6px;margin-bottom:20px;font-size:13px;background:rgba(68,170,255,0.1);border:1px solid #4af;color:#adf}
    label{color:#9fdf9f;font-size:16px;margin:18px 0 8px;display:block}
    input{width:100%;background:#050a15;border:2px solid #2a4a7a;border-radius:8px;padding:13px;color:#d0e8ff;font-size:15px}
    button{width:100%;background:linear-gradient(180deg,#1a4a9a,#0f3070);border:2px solid #4af;border-radius:8px;padding:13px;color:#e0f0ff;font-size:17px;cursor:pointer;margin-top:10px}
    button:hover{background:linear-gradient(180deg,#2a6aca,#1a4a9a)}
    .aviso{text-align:center;color:#8ab8e0;font-size:13px;margin-top:20px}
    .pie{text-align:center;color:#ffd066;font-size:11px;margin-top:25px;padding-top:15px;border-top:1px solid #2a4a7a}
  </style></head><body><div class="caja">
    <h1>⚡ SEGURY FileCloud</h1>
    <h2>v5.0 — NODE.JS + MQTT BROKER</h2>
    <div class="broker">${brokerEstado}</div>
    <div style="background:rgba(68,170,255,0.08);border:1px solid #4af;color:#adf;padding:12px;border-radius:8px;text-align:center;font-size:17px;margin-bottom:20px">🔐 INGRESO AL SISTEMA</div>
    <form method="POST" action="/login">
      <label>Usuario:</label>
      <input type="text" name="usuario" required autocomplete="off">
      <label>Contraseña:</label>
      <input type="password" name="clave" required autocomplete="off">
      <button type="submit">🔑 ENTRAR</button>
    </form>
    <p class="aviso">Intentos restantes: ${restante}</p>
    <div class="pie">⚠️ FUNCIONES REALES — DEBIAN EDITION</div>
  </div></body></html>`);
});

// Login POST
app.post('/login', (req, res) => {
  const ip = req.ip;
  const { usuario, clave } = req.body;
  
  console.log('🔍 Intento — Usuario:', usuario, 'Clave recibida:', clave ? '***' : 'VACÍA');
  
  if (!usuario || !clave) {
    return res.send(`<script>alert('⚠️ Completa ambos campos');window.location='/'</script>`);
  }
  
  if (USUARIOS[usuario] && USUARIOS[usuario].pass === hashPass(clave)) {
    intentos[ip] = 0;
    const token = crypto.randomUUID();
    sesiones[token] = usuario;
    log(`✅ INGRESO: ${usuario} desde ${ip}`);
    publicar('segury/usuarios/conectado', { usuario, ip });
    
    res.setHeader('Set-Cookie', `sesion=${token}; Path=/; HttpOnly; SameSite=Lax`);
    return res.redirect('/panel');
  } else {
    intentos[ip] = (intentos[ip] || 0) + 1;
    log(`❌ FALLO: Usuario=${usuario} IP=${ip}`);
    return res.send(`<script>alert('❌ Usuario o contraseña incorrectos');window.location='/'</script>`);
  }
});

// Panel
app.get('/panel', (req, res) => {
  const cookieHeader = req.headers.cookie || '';
  const token = cookieHeader.split(';').find(c => c.trim().startsWith('sesion='));
  const tokenValor = token ? token.split('=')[1].trim() : null;
  const usuario = tokenValor ? sesiones[tokenValor] : null;
  
  if (!usuario) {
    console.log('⚠️ Sin sesión — redirigiendo al login');
    return res.redirect('/');
  }
  
  const datos = USUARIOS[usuario];
  const brokerEstado = mqttClient.connected ? '🟢 CONECTADO' : '🔴 DESCONECTADO';
  
  res.send(`
  <!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Panel — SEGURY FileCloud</title>
  <style>
    *{box-sizing:border-box;margin:0;padding:0;font-family:Courier New,monospace}
    body{background:#0a1020;padding:20px}
    .caja{max-width:700px;margin:0 auto;background:linear-gradient(145deg,#0f1729,#0a1020);border:2px solid #4af;border-radius:20px;padding:30px;box-shadow:0 0 40px rgba(68,170,255,0.2)}
    h1{text-align:center;color:#aef;font-size:24px;margin-bottom:5px}
    h2{text-align:center;color:#7bd;font-size:13px;margin-bottom:15px;font-weight:normal}
    .broker{text-align:center;padding:8px;border-radius:6px;margin-bottom:15px;font-size:13px;background:rgba(68,170,255,0.1);border:1px solid #4af;color:#adf}
    .ok{background:rgba(68,204,102,0.1);border:1px solid #4c6;color:#8f8;padding:12px;border-radius:8px;text-align:center;margin-bottom:20px}
    h3{color:#aef;margin:20px 0 8px 0;font-size:15px;border-bottom:1px solid #2a4a7a;padding-bottom:6px}
    .fila{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:10px;margin:8px 0}
    a.boton{display:block;text-align:center;background:linear-gradient(180deg,#1a4a9a,#0f3070);border:2px solid #4af;border-radius:8px;padding:10px;color:#e0f0ff;text-decoration:none;font-size:14px;cursor:pointer}
    a.boton:hover{background:linear-gradient(180deg,#2a6aca,#1a4a9a)}
    .boton-verde{border-color:#4c6;background:linear-gradient(180deg,#1a6a4a,#0f4a30)}
    .boton-amarillo{border-color:#cc6;background:linear-gradient(180deg,#6a6a1a,#4a4a10)}
    .boton-rojo{border-color:#c44;background:linear-gradient(180deg,#6a2020,#4a1010)}
    .salida{background:#050a15;border:1px solid #4af;padding:15px;margin-top:15px;border-radius:8px;max-height:250px;overflow:auto;display:none}
    pre{color:#cff;font-size:12px;white-space:pre-wrap;margin:0}
    .pie{text-align:center;color:#6ab0d0;font-size:11px;margin-top:25px;padding-top:15px;border-top:1px solid #2a4a7a}
  </style></head><body><div class="caja">
    <h1>⚡ SEGURY FileCloud</h1>
    <h2>Panel de Control — ${datos.nombre} | ${datos.rol.toUpperCase()}</h2>
    <div class="broker">📡 BROKER MQTT: ${brokerEstado}</div>
    <div class="ok">✅ CONECTADO AL NÚCLEO</div>
    
    <h3>📊 SISTEMA</h3>
    <div class="fila">
      <a href="/api/sistema" class="boton" onclick="cargar(this.href);return false">ℹ️ Info</a>
      <a href="/api/hora" class="boton" onclick="cargar(this.href);return false">🕐 Hora</a>
      <a href="/api/red" class="boton" onclick="cargar(this.href);return false">🌐 Red</a>
    </div>
    
    <h3>💾 RECURSOS</h3>
    <div class="fila">
      <a href="/api/memoria" class="boton" onclick="cargar(this.href);return false">🧠 Memoria</a>
      <a href="/api/disco" class="boton" onclick="cargar(this.href);return false">💿 Disco</a>
      <a href="/api/procesos" class="boton" onclick="cargar(this.href);return false">⚡ Procesos</a>
    </div>
    
    <h3>📁 ARCHIVOS</h3>
    <div class="fila">
      <a href="/api/archivos" class="boton" onclick="cargar(this.href);return false">📋 Listar</a>
      <a href="/api/respaldo" class="boton boton-verde" onclick="cargar(this.href);return false">💾 Respaldo</a>
      <a href="/api/limpiar" class="boton boton-amarillo" onclick="cargar(this.href);return false">🧹 Limpiar</a>
    </div>
    
    ${datos.rol === 'admin' ? `<h3>🔧 ADMIN</h3><div class="fila"><a href="/api/logs" class="boton" onclick="cargar(this.href);return false">📝 Registros</a></div>` : ''}
    
    <div class="fila" style="margin-top:25px">
      <a href="/salir" class="boton boton-rojo">🚪 Cerrar Sesión</a>
    </div>
    
    <div class="salida" id="salida"><h4 style="color:#aef;margin:0 0 8px 0">📤 SALIDA REAL:</h4><pre id="salida-texto"></pre></div>
    
    <div class="pie">⚠️ NODE.JS + MQTT — v5.0</div>
  </div>
  <script>
    function cargar(url) {
      fetch(url)
        .then(r => r.text())
        .then(t => {
          document.getElementById('salida-texto').textContent = t;
          document.getElementById('salida').style.display = 'block';
        });
    }
  </script>
  </body></html>`);
});

// Cerrar sesión
app.get('/salir', (req, res) => {
  const cookieHeader = req.headers.cookie || '';
  const token = cookieHeader.split(';').find(c => c.trim().startsWith('sesion='));
  if (token) {
    const tokenValor = token.split('=')[1].trim();
    delete sesiones[tokenValor];
  }
  res.setHeader('Set-Cookie', 'sesion=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT');
  res.redirect('/');
});

// ========== API ENDPOINTS ==========
app.get('/api/sistema', (req, res) => {
  const os = require('os');
  res.send(`Sistema: ${os.type()}\nPlataforma: ${os.platform()}\nVersión: ${os.release()}\nArq: ${os.arch()}\nHost: ${os.hostname()}`);
});

app.get('/api/hora', (req, res) => res.send(`🕐 Hora: ${new Date().toLocaleString()}`));

app.get('/api/red', (req, res) => {
  const os = require('os');
  const ifaces = os.networkInterfaces();
  let ip = 'No disponible';
  for (let i in ifaces) {
    for (let a of ifaces[i]) if (a.family === 'IPv4' && !a.internal) ip = a.address;
  }
  res.send(`Host: ${os.hostname()}\nIP: ${ip}`);
});

app.get('/api/memoria', (req, res) => {
  const os = require('os');
  res.send(`Total: ${(os.totalmem()/1024/1024).toFixed(0)} MB\nLibre: ${(os.freemem()/1024/1024).toFixed(0)} MB`);
});

app.get('/api/disco', (req, res) => ejecutar('df -h', res));
app.get('/api/procesos', (req, res) => ejecutar('ps -ef | head -12', res));
app.get('/api/archivos', (req, res) => ejecutar('ls -la', res));

app.get('/api/respaldo', (req, res) => {
  const nombre = 'backup_' + new Date().toISOString().slice(0,19).replace(/[:T]/g,'-') + '.tar.gz';
  exec(`tar -czf ${nombre} .`, err => {
    if (err) return res.send('❌ Error');
    res.send(`✅ Respaldo: ${nombre}`);
  });
});

app.get('/api/limpiar', (req, res) => ejecutar('rm -f *.pyc', res));

app.get('/api/logs', (req, res) => {
  if (!fs.existsSync('sistema_logs.txt')) return res.send('📭 Sin registros');
  fs.readFile('sistema_logs.txt', 'utf8', (err, d) => {
    res.send(d.split('\n').slice(-30).join('\n'));
  });
});

app.listen(PORT, '0.0.0.0', () => {
  console.log('='.repeat(50));
  console.log('🔒 SEGURY FileCloud — v5.0');
  console.log('📡 WEB: http://localhost:' + PORT);
  console.log('🔑 Admin: segury        | SEGURYSS');
  console.log('🔑 Usuario: kellynanaki | 5538:000000');
  console.log('='.repeat(50));
});
