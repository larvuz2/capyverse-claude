// node render.js in.svg out.png [width] [bg]  — render an SVG to PNG with the preinstalled Chromium.
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const [inp, out, width = '2000', bg = 'transparent'] = process.argv.slice(2);
  const svg = fs.readFileSync(inp, 'utf8');
  const vb = svg.match(/viewBox="([\d.\- ]+)"/)[1].split(/\s+/).map(Number);
  const w = parseInt(width), h = Math.round(w * vb[3] / vb[2]);
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: w, height: h } });
  await p.setContent(`<html><body style="margin:0;background:${bg}">${svg.replace('<svg', `<svg width="${w}" height="${h}"`)}</body></html>`);
  await p.screenshot({ path: out, omitBackground: bg === 'transparent' });
  await b.close();
})();
