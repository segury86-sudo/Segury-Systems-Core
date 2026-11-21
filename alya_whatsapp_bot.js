const makeWASocket = require('@whiskeysockets/baileys').default;
const { useMultiFileAuthState } = require('@whiskeysockets/baileys');
const readline = require('readline');

const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
const CLAVE_FIJA = "SEGURYSS";
const MI_NUMERO = "+524531225361";

const ALYA = {
    nombre_largo: "あ ┊⏤͟͟͞͞☆ Alya San ϟ",
    nombre_corto: "Alya",
    moneda: "¥enes",
    prefijos: ["/","#"],
    comandos: 36,
    tipo: "Sub Bot",
    desarrollador: "Profesor Segury SSC",
    numero: MI_NUMERO,
    pais: "🇲🇽 México",
    activo_desde: "28 sep 2026",
    plataforma: "Linux · Termux",
    enlace: "https://api.stellarwa.xyz"
};

function infoAlya(){
return `
ꕤ  ˖⁩   ౼ Información :: *Alya*

ׅ  ׄ  ✤   ׅ り Nombre Largo :: *${ALYA.nombre_largo}*
ׅ  ׄ  ✤   ׅ り Nombre Corto :: *${ALYA.nombre_corto}*
ׅ  ׄ  ✤   ׅ り 𝖬𝗈𝗇𝖾𝖽𝖺 :: *${ALYA.moneda}*
ׅ  ׄ  ✤   ׅ り 𝖯𝗋𝖾𝖿𝗂𝗃𝗈𝗌 :: *${ALYA.prefijos.join(",")}*
ׅ  ׄ  ✤   ׅ り 𝖢𝗆𝖽 𝖤𝗃𝖾𝖼 :: *${ALYA.comandos}*

𖹭᳔ㅤㅤׄㅤㅤ❏ㅤㅤׅㅤㅤゕㅤㅤׄㅤㅤㅤ𑄾𑄾

ׅ  ׄ  ✿   ׅ り Tipo :: *${ALYA.tipo}*
ׅ  ׄ  ✿   ׅ り Propietario :: *${ALYA.desarrollador}*
ׅ  ׄ  ✿   ׅ り País :: *${ALYA.pais}*
ׅ  ׄ  ✿   ׅ り Número :: *${ALYA.numero}*
ׅ  ׄ  ✿   ׅ り Plataforma :: *${ALYA.plataforma}*

𖹭᳔ㅤㅤׄㅤㅤ❀ㅤㅤׅㅤㅤゕㅤㅤׄㅤㅤㅤ𑄾𑄾

> \`Enlace:\` ${ALYA.enlace}
`;
}

async function iniciarBot(){
    console.log("══════════════════════════════════════");
    console.log("🔐 CLAVE: ESCRIBE → SEGURYSS");
    console.log("══════════════════════════════════════");
    
    const clave = await new Promise(res => rl.question("Clave: ", res));
    if(clave.trim() !== CLAVE_FIJA){
        console.log("❌ Incorrecta");
        process.exit(1);
    }
    console.log("✅ Correcta → Conectando...\n");

    const { state, saveCreds } = await useMultiFileAuthState('./auth');
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: false
    });

    sock.ev.on('creds.update', saveCreds);
    
    sock.ev.on('connection.update', async (upd) => {
        const { connection, qr } = upd;
        
        if(qr){
            console.log("══════════════════════════════════════════════");
            console.log("📱 EN TU TELÉFONO HAZ ESTO:");
            console.log("1. WhatsApp → Dispositivos vinculados");
            console.log("2. Toca: ¿No puedes escanear el código?");
            console.log("3. Aparece un CÓDIGO — déjalo visible");
            console.log("══════════════════════════════════════════════");
        }
        
        if(connection === 'open'){
            console.log("\n✅ ALYA CONECTADA 💙✨");
            console.log("👤", MI_NUMERO, "🇲🇽\n");
            rl.close();
        }
        
        if(connection === 'close'){
            console.log("\n❌ No se pudo vincular");
            console.log("💡 Posible solución: cierra y vuelve a abrir WhatsApp");
            console.log("   luego ejecuta: node alya_whatsapp_bot.js");
        }
    });

    sock.ev.on('messages.upsert', async m => {
        const msg = m.messages[0];
        if(!msg.message || msg.key.fromMe) return;
        const texto = msg.message.conversation || msg.message.extendedTextMessage?.text || "";
        const prefijo = ALYA.prefijos.find(p => texto.startsWith(p));
        if(!prefijo) return;
        const cmd = texto.slice(prefijo.length).toLowerCase().trim();
        if(["info","alya","ayuda"].includes(cmd)){
            await sock.sendMessage(msg.key.remoteJid, { text: infoAlya() });
        }
    });
}

iniciarBot();
