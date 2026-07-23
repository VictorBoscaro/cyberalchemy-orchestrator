const puppeteer = require('puppeteer-core');
const path = require('path');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const OUT = path.join(__dirname, 'shots');
const PORT = 8106;
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
    const url = `http://localhost:${PORT}/variants/mission.html`;
    try {
      await page.goto(url, { waitUntil: 'networkidle0', timeout: 20000 });
      await page.waitForSelector('#dlist .ditem', { timeout: 8000 });
      await page.evaluate((i) => {
        const items = document.querySelectorAll('#dlist .ditem');
        if (items[i]) items[i].click();
      }, idx);
      await new Promise(r => setTimeout(r, 900));
      // assertions read back to console
      const diag = await page.evaluate(() => {
        const rest = document.getElementById('mc-rest');
        const banner = document.getElementById('mc-banner');
        const empty = document.getElementById('stage-empty');
        const cs = (el) => el ? getComputedStyle(el).display : 'n/a';
        return {
          restDisplay: cs(rest), restHidden: rest.hidden,
          bannerHidden: banner.hidden,
          emptyDisplay: cs(empty), emptyHidden: empty.hidden,
          nodes: document.querySelectorAll('#nodes .node').length,
          edges: document.querySelectorAll('#edges .edge').length
        };
      });
      console.log(label, 'DIAG', JSON.stringify(diag));
      await page.screenshot({ path: path.join(OUT, `mission-${label}-after.png`) });
      console.log('OK', label);
    } catch (e) {
      console.log('ERR', label, e.message);
    }
    await page.close();
  }
  await browser.close();
})();
