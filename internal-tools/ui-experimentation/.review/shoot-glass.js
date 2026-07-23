const puppeteer = require('puppeteer-core');
const path = require('path');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
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
    const url = `http://localhost:8103/variants/glass.html`;
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
        const emptyVisible = emptyEl && !emptyEl.hidden &&
          getComputedStyle(emptyEl).display !== 'none';
        const groups = [];
        document.querySelectorAll('.node.group').forEach(g => {
          const r = g.getBoundingClientRect();
          groups.push({ label: g.textContent.trim(),
            cx: Math.round(r.left + r.width/2), cy: Math.round(r.top + r.height/2) });
        });
        return { emptyVisible, emptyDisplay: getComputedStyle(emptyEl).display, groups };
      });
      console.log('===', label, '===');
      console.log(JSON.stringify(diag, null, 1));
      const file = path.join(OUT, `glass-${label}-after.png`);
      await page.screenshot({ path: file });
      console.log('OK', label);
    } catch (e) {
      console.log('ERR', label, e.message);
    }
    await page.close();
  }
  await browser.close();
})();
