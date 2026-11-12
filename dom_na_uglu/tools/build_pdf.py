#!/usr/bin/env python3
"""90화 원고를 부별·전체 PDF로 만든다. 사용법: python3 tools/build_pdf.py (dom_na_uglu 폴더에서)"""
import glob, html, os, re, subprocess, sys
import markdown

PARTS = [("part1_osen", "Часть первая. ОСЕНЬ", "1부 가을"),
         ("part2_zima", "Часть вторая. ЗИМА", "2부 겨울"),
         ("part3_vesna", "Часть третья. ВЕСНА", "3부 봄"),
         ("part4_leto", "Часть четвёртая. ЛЕТО", "4부 여름"),
         ("part5_novoselye", "Часть пятая. НОВОСЕЛЬЕ", "5부 새 집들이")]
CSS = """
@page { size: A4; margin: 18mm 16mm 18mm 16mm; }
body { font-family: 'DejaVu Serif', 'NanumMyeongjo', serif; font-size: 10.5pt; line-height: 1.55; color: #111; }
h1 { font-size: 20pt; margin: 0 0 4pt; } h2 { font-size: 13pt; margin: 14pt 0 4pt; color: #444; }
h3 { font-size: 15pt; margin: 2pt 0 10pt; }
.ep { page-break-before: always; }
.cover { page-break-after: always; text-align: center; padding-top: 70mm; }
.cover h1 { font-size: 34pt; } .cover p { font-size: 13pt; color: #444; }
.toc { page-break-after: always; } .toc li { margin: 1pt 0; list-style: none; }
.toc h2 { page-break-before: auto; }
blockquote { border-left: 3px solid #999; margin: 6pt 0; padding: 2pt 10pt; color: #333; background: #f6f6f6; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; margin: 6pt 0; page-break-inside: auto; }
th, td { border: 1px solid #bbb; padding: 3pt 5pt; vertical-align: top; } th { background: #eee; }
tr { page-break-inside: avoid; }
p { margin: 3pt 0; } em { color: #444; } hr { border: 0; border-top: 1px solid #ccc; margin: 10pt 0; }
.ko { font-family: 'NanumMyeongjo', 'DejaVu Serif', serif; }
"""
def ep_html(path):
    md = open(path, encoding="utf-8").read()
    body = markdown.markdown(md, extensions=["tables"])
    body = body.replace("<h1>ДОМ НА УГЛУ</h1>", "")
    return f'<section class="ep">{body}</section>'
def title_of(path):
    m = re.search(r"^### (.+)$", open(path, encoding="utf-8").read(), re.M)
    return m.group(1) if m else os.path.basename(path)
def build(name, parts, sub):
    eps = []
    for d, ru, ko in parts:
        eps += [(d, ru, ko, p) for p in sorted(glob.glob(f"{d}/ep*.md"))]
    toc, cur = [], None
    for d, ru, ko, p in eps:
        if d != cur:
            toc.append(f"<h2>{ru} · {ko}</h2>"); cur = d
        toc.append(f"<li>{html.escape(title_of(p))}</li>")
    doc = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="cover"><h1>ДОМ НА УГЛУ</h1><p>Дом на углу — сериал для изучения русского языка</p><p>{sub}</p></div>
<div class="toc"><h1>Содержание · 목차</h1><ul>{''.join(toc)}</ul></div>
{''.join(ep_html(p) for *_, p in eps)}</body></html>"""
    hp = f"pdf/{name}.html"; open(hp, "w", encoding="utf-8").write(doc)
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const pg=await b.newPage();
await pg.goto('file://'+require('path').resolve('{hp}'),{{waitUntil:'load',timeout:0}});
await pg.pdf({{path:'pdf/{name}.pdf',format:'A4',printBackground:true,displayHeaderFooter:true,
headerTemplate:'<div></div>',footerTemplate:'<div style="font-size:8px;width:100%;text-align:center;color:#888"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
margin:{{top:'18mm',bottom:'18mm',left:'16mm',right:'16mm'}},timeout:0}});await b.close();}})();"""
    subprocess.run(["node", "-e", js], check=True)
    os.remove(hp); print("pdf/" + name + ".pdf")
if __name__ == "__main__":
    for i, part in enumerate(PARTS, 1):
        build(f"Дом_на_углу_{i}부", [part], f"{part[1]} · {part[2]} (эпизоды {i*18-17}–{i*18})")
    if "--all" in sys.argv:
        build("Дом_на_углу_전체", PARTS, "Эпизоды 1–90 · 전 90화")
