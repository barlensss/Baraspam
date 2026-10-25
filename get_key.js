// get_key.js
const fs = require('fs');

try {
    // Baca isi apikey.js
    let content = fs.readFileSync('apikey.js', 'utf8');
    
    // Eksekusi kodenya di dalam sandbox
    let validKeys = [];
    eval(content); // Ini bakal ngejalanin obfuscator lo dan ngisi validKeys
    
    // Print ke JSON biar bisa dibaca Python
    console.log(JSON.stringify(validKeys));
} catch (e) {
    console.error("Error:", e.message);
    process.exit(1);
}
