const fs = require('fs');
try {
    let content = fs.readFileSync('apikey.js', 'utf8');

    const validKeys = eval(content + '; validKeys;');
    console.log(JSON.stringify(validKeys));
} catch (e) {
    process.exit(1);
}
