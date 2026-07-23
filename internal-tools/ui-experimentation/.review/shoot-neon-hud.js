const puppeteer = require('puppeteer-core');
const path = require('path');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const OUT = path.join(__dirname, 'shots');
const PORT = 8112;
// rich = richest dispatch (index 0), small = 1-group/2-agent (index 5)
const CASES = { rich: 0, small: 5 };

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox', '--window-size=1400,900']
  });
  for (const [label, idx] of Object.entries(CASES)) {
    const page = await browser.newPage();
    await page.setViewport({ width: 1400, height: 900, deviceScaleFactor: 1 });
    const url = `http://localhost:${PORT}/variants/neon-hud.html`;
    try {
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 20000 });
      await page.waitForSelector('#dlist .ditem', { timeout: 8000 });
      await page.evaluate((i) => {
        const items = document.querySelectorAll('#dlist .ditem');
        if (items[i]) items[i].click();
      }, idx);
      await new Promise(r => setTimeout(r, 900));
      const diag = await page.evaluate(() => {
        const empty = document.getElementById('stage-empty');
        const cs = (el) => el ? getComputedStyle(el).display : 'n/a';
        return {
          emptyDisplay: cs(empty), emptyHidden: empty.hidden,
          nodes: document.querySelectorAll('#nodes .node').length,
          agents: document.querySelectorAll('#nodes .node.agent').length,
          edges: document.querySelectorAll('#edges .edge').length,
          revNodes: document.querySelectorAll('#nodes .node.rev').length
        };
      });
      console.log(label, 'DIAG', JSON.stringify(diag));
      await page.screenshot({ path: path.join(OUT, `neon-hud-${label}.png`) });
      console.log('OK', label);
    } catch (e) {
      console.log('ERR', label, e.message);
    }
    await page.close();
  }
  await browser.close();
})();
