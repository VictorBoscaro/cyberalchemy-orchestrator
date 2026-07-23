const puppeteer = require('puppeteer-core');
const path = require('path');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const VARIANTS = ['blueprint','editorial','terminal','brutalist','glass','orbital','swiss','mission','sketch','mono'];
const OUT = path.join(__dirname, 'shots');
// index 0 = richest (5 grp/6 ag/4 edge), index 5 = small (1 grp/2 ag)
const CASES = { rich: 0, small: 5 };

(async () => {
  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    args: ['--no-sandbox','--window-size=1400,900']
  });
  for (const v of VARIANTS) {
    for (const [label, idx] of Object.entries(CASES)) {
      const page = await browser.newPage();
      await page.setViewport({ width: 1400, height: 900, deviceScaleFactor: 1 });
      const url = `http://localhost:8099/variants/${v}.html`;
      try {
        await page.goto(url, { waitUntil: 'networkidle0', timeout: 20000 });
        // wait for dispatch list to populate
        await page.waitForSelector('#dlist .ditem', { timeout: 8000 });
        // click the target dispatch item
        await page.evaluate((i) => {
          const items = document.querySelectorAll('#dlist .ditem');
          if (items[i]) items[i].click();
        }, idx);
        await new Promise(r => setTimeout(r, 900));
        const file = path.join(OUT, `${v}-${label}.png`);
        await page.screenshot({ path: file });
        console.log('OK', v, label);
      } catch (e) {
        console.log('ERR', v, label, e.message);
      }
      await page.close();
    }
  }
  await browser.close();
})();
