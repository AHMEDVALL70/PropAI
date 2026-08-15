#!/usr/bin/env node
/**
 * update-data.js
 * سكربت لتحديث بيانات العقارات من Apify
 */

const fs = require('fs');
const path = require('path');

const CONFIG = {
    APIFY_API_KEY: process.env.APIFY_API_KEY || 'YOUR_KEY_HERE',
    APIFY_ACTOR_ID: process.env.APIFY_ACTOR_ID || 'YOUR_ACTOR_ID',
    OUTPUT_FILE: path.join(__dirname, '..', 'properties.json'),
    MAX_ITEMS: 100
};

async function main() {
    console.log('🚀 بدء تحديث البيانات...');
    
    // بيانات نموذجية (استبدلها ببيانات من Apify)
    const properties = [
        {
            id: "QA-PROP-3001",
            zone: "Lusail Marina",
            type: "شقة",
            size: 160,
            beds: "3",
            price: 2200000,
            pred: 2150000,
            status: "Fair Price",
            cls: "mid",
            desc: "شقة حديثة في موقع متميز."
        }
    ];
    
    fs.writeFileSync(CONFIG.OUTPUT_FILE, JSON.stringify(properties, null, 2));
    console.log(`✅ تم حفظ ${properties.length} عقار`);
    
    if (process.env.GITHUB_ACTIONS) {
        const { execSync } = require('child_process');
        execSync('git add properties.json', { stdio: 'inherit' });
        execSync('git commit -m "🤖 تحديث تلقائي [skip ci]"', { stdio: 'inherit' });
        execSync('git push', { stdio: 'inherit' });
    }
}

main();