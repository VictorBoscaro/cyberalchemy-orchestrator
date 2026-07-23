const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

function findChrome() {
  const candidates = [
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
  ];
  for (const c of candidates) if (fs.existsSync(c)) return c;
  const base = path.join(process.env.USERPROFILE || process.env.HOME, '.cache', 'puppeteer', 'chrome');
  if (fs.existsSync(base)) {
    for (const d of fs.readdirSync(base)) {
      const p = path.join(base, d, 'chrome-win64', 'chrome.exe');
      if (fs.existsSync(p)) return p;
    }
  }
  throw new Error('no chrome found');
}

const CHROME = findChrome();
const OUT = path.join(__dirname, 'shots');
const CASES = { rich: 0, small: 5 };

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox','--window-size=1400,900']
  });
  for (const [label, idx] of Object.entries(CASES)) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1400, height: 900, deviceScaleFactor: 1 });
    const url = `http://localhost:8115/variants/holo.html`;
    try {
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 20000 });
      await page.waitForSelector('#dlist .ditem', { timeout: 8000 });
      await page.evaluate((i) => {
        const items = document.querySelectorAll('#dlist .ditem');
        if (items[i]) items[i].click();
      }, idx);
      await new Promise(r => setTimeout(r, 900));
      const diag = await page.evaluate(() => {
        const emptyEl = document.getElementById('stage-empty');
        const emptyVisible = emptyEl && getComputedStyle(emptyEl).display !== 'none';
        const idleEl = document.getElementById('sh-idle');
        const idleVisible = idleEl && getComputedStyle(idleEl).display !== 'none';
        const agents = [];
        document.querySelectorAll('.node.agent .n-name').forEach(nm => {
          const clipped = nm.scrollWidth > nm.clientWidth + 1 || nm.scrollHeight > nm.clientHeight + 1;
          agents.push({ text: nm.textContent, clipped });
        });
        const groups = [];
        document.querySelectorAll('.node.group').forEach(g => {
          const lbl = g.querySelector('.g-label');
          const clipped = lbl && (lbl.scrollWidth > lbl.clientWidth + 1);
          groups.push({ label: g.textContent.trim(), clipped });
        });
        const edges = document.querySelectorAll('.edge').length;
        return { emptyVisible, idleVisible, edges,
          anyAgentClipped: agents.some(a => a.clipped),
          anyGroupClipped: groups.some(g => g.clipped),
          agentCount: agents.length, agents, groups };
      });
      console.log('===', label, '===');
      console.log(JSON.stringify(diag, null, 1));
      const file = path.join(OUT, `holo-${label}.png`);
      await page.screenshot({ path: file });
      console.log('OK', label, '->', file);
    } catch (e) {
      console.log('ERR', label, e.message);
    }
    await page.close();
  }
  await browser.close();
})();
