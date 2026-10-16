const { chromium } = require('playwright');
(async () => {
  const [,, inp, out] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + inp, { waitUntil: 'load', timeout: 300000 });
  await p.pdf({ path: out, format: 'A4', printBackground: true, preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: '<div style="font-size:7pt;width:100%;text-align:center;color:#888;font-family:DejaVu Serif">' + (process.argv[4] || 'СМОЛЕНСКАЯ ПЛОЩАДЬ') + '</div>',
    footerTemplate: '<div style="font-size:8pt;width:100%;text-align:center;color:#666;font-family:DejaVu Serif"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
    timeout: 0, outline: true, tagged: true });
  await b.close();
})();
