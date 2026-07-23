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
    const url = `http://localhost:8101/variants/swiss.html`;
    try {
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 20000 });
      await page.waitForSelector('#dlist .ditem', { timeout: 8000 });
      await page.evaluate((i) => {
        const items = document.querySelectorAll('#dlist .ditem');
        if (items[i]) items[i].click();
      }, idx);
      await new Promise(r => setTimeout(r, 900));
      // diagnostics: agent node centers per band + empty-state visibility
      const diag = await page.evaluate(() => {
        const emptyEl = document.getElementById('stage-empty');
        const emptyVisible = emptyEl && !emptyEl.hidden &&
          getComputedStyle(emptyEl).display !== 'none';
        const wrap = document.getElementById('stage-wrap').getBoundingClientRect();
        const rows = {};
        document.querySelectorAll('.node.agent').forEach(a => {
          const r = a.getBoundingClientRect();
          const cy = Math.round(r.top + r.height/2);
          const cx = Math.round(r.left + r.width/2);
          const key = cy; // band ~ same y
          (rows[key] = rows[key] || []).push({
            name: (a.querySelector('.n-name')||{}).textContent, cx
          });
        });
        return { emptyVisible, wrapLeft: Math.round(wrap.left),
          wrapRight: Math.round(wrap.right), wrapCenter: Math.round((wrap.left+wrap.right)/2),
          rows };
      });
      console.log('===', label, '===');
      console.log(JSON.stringify(diag, null, 1));
      const file = path.join(OUT, `swiss-${label}-after.png`);
      await page.screenshot({ path: file });
      console.log('OK', label);
    } catch (e) {
      console.log('ERR', label, e.message);
    }
    await page.close();
  }
  await browser.close();
})();
