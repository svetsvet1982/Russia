"""부별 PDF와 문서(기획서·바이블) PDF를 pdf/에 만든다. 사용: python3 tools/pdf/build_all.py [parts] [docs] [smol]"""
import subprocess, sys
from pathlib import Path
R=Path(__file__).resolve().parents[2]; S=Path('/tmp/vlast_pdf_build'); S.mkdir(exist_ok=True)
OUT=R/'pdf'; V=R/'chetvyortaya_vlast'
def render(md, pdf, title):
    html=md.with_suffix('.html')
    subprocess.run(['pandoc',str(md),'-f','markdown-yaml_metadata_block','-t','html5','-s','--toc','--toc-depth=2',f'--css={R}/tools/pdf/style.css','--metadata',f'title={title}','--metadata','lang=ru','-o',str(html)],check=True)
    subprocess.run(['node',str(R/'tools/pdf/print.js'),str(html),str(pdf),title],check=True,capture_output=True)
    print(pdf.name, flush=True)
def cover(t,sub,meta):
    return f'<div class="cover"><div class="cover-title">{t}</div><div class="cover-sub">{sub}</div><div class="cover-meta">{meta}</div></div>\n'
def episode_md(e):
    lines=e.read_text(encoding='utf-8').splitlines(); body=[]; inc=False
    for l in lines[2:]:
        if l.startswith('## Комментарий'):
            inc=True; l='<div class="pb"></div>\n\n### '+l[3:]+' {.commentary}'
        elif l.startswith('### '):
            l=('#### ' if inc else '## ')+l[4:]
        body.append(l)
    return '\n\n<div class="pb"></div>\n\n'+'\n'.join(body)
parts=["part1_obrushenie","part2_bely_khalat","part3_tenevoy_flot","part4_dvoynoe_naznachenie","part5_krot","part6_prachechnaya","part7_zakaz","part8_istochnik"]
which=sys.argv[1:] or ['parts','docs']
if 'parts' in which:
  for i,p in enumerate(parts,1):
    eps=sorted((V/p).glob('ep*.md'))
    pt=eps[0].read_text(encoding='utf-8').splitlines()[1].lstrip('# ').strip()
    n1=int(eps[0].name[2:5]); n2=int(eps[-1].name[2:5])
    md=S/f'vlast_part{i}.md'
    md.write_text(cover('ЧЕТВЁРТАЯ ВЛАСТЬ',pt,f'Эпизоды {n1}–{n2}')+''.join(episode_md(e) for e in eps)+'\n',encoding='utf-8')
    render(md, OUT/f'chetvyortaya_vlast_part{i}_{p.split("_",1)[1]}.pdf', f'ЧЕТВЁРТАЯ ВЛАСТЬ — {pt}')
def doc(src, name, t, sub):
    txt=src.read_text(encoding='utf-8')
    md=S/(name+'.md'); md.write_text(cover(t,sub,src.name)+'\n<div class="pb"></div>\n\n'+txt+'\n',encoding='utf-8')
    render(md, OUT/(name+'.pdf'), f'{t} — {sub}')
if 'smol' in which:
  doc(R/'bible/continuity.md','smolenskaya_ploshchad_continuity','СМОЛЕНСКАЯ ПЛОЩАДЬ','연속성 바이블')
if 'docs' in which:
  doc(V/'기획서.md','chetvyortaya_vlast_plan','ЧЕТВЁРТАЯ ВЛАСТЬ','기획서')
  doc(V/'bible/continuity.md','chetvyortaya_vlast_continuity','ЧЕТВЁРТАЯ ВЛАСТЬ','연속성 바이블')
  doc(V/'bible/quotes_commentary.md','chetvyortaya_vlast_quotes','ЧЕТВЁРТАЯ ВЛАСТЬ','인용구 해설')
  doc(R/'기획서.md','smolenskaya_ploshchad_plan','СМОЛЕНСКАЯ ПЛОЩАДЬ','기획서')
  doc(R/'bible/continuity.md','smolenskaya_ploshchad_continuity','СМОЛЕНСКАЯ ПЛОЩАДЬ','연속성 바이블')
