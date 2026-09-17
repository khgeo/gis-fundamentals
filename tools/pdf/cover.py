"""Front and back cover for the Fundamentals of GIS book (A4, full bleed).
Artwork uses simplified real layers from the Cambodia dataset (coverdata.json)."""
import json, qrcode, qrcode.image.svg, io, html
import os
D=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"coverdata.json")))
W,H=794,1123
SITE="https://khgeo.github.io/gis-fundamentals/"
def proj(u,v,ox,oy,w,h,sk):  # oblique projection of normalised coords
    return (ox+u*w+(1-v)*sk, oy+(1-v)*h)
def paths(parts,ox,oy,w,h,sk,close=True):
    d=[]
    for poly in parts:
        for ring in poly:
            pts=[proj(u,v,ox,oy,w,h,sk) for u,v in ring]
            d.append("M"+" L".join(f"{x:.1f} {y:.1f}" for x,y in pts)+("Z" if close else ""))
    return " ".join(d)
def plate(ox,oy,w,h,sk,pad=18):
    a=proj(-0.06,1.08,ox,oy,w,h,sk); b=proj(1.06,1.08,ox,oy,w,h,sk); c=proj(1.06,-0.08,ox,oy,w,h,sk); d=proj(-0.06,-0.08,ox,oy,w,h,sk)
    return f"M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f} L{c[0]:.1f} {c[1]:.1f} L{d[0]:.1f} {d[1]:.1f}Z"
def art(ox,oy,w,h,sk,gap):
    L=[]
    layers=[("prov","poly","rgba(255,255,255,0.10)","rgba(178,223,219,0.9)",0.8,"ខេត្ត"),
            ("lake","poly","rgba(79,195,247,0.55)","rgba(129,212,250,0.95)",0.6,"ទឹក"),
            ("roads","line","none","#ffb74d",1.6,"ផ្លូវជាតិ"),
            ("pts","pt","#ff7043","#fff",0.6,"មណ្ឌលសុខភាព")]
    for i,(k,t,fill,stroke,sw,lab) in enumerate(layers):
        y=oy-i*gap
        L.append(f'<path d="{plate(ox,y,w,h,sk)}" fill="rgba(255,255,255,{0.05+0.02*i})" stroke="rgba(255,255,255,0.35)" stroke-width="1"/>')
        if t=="poly": L.append(f'<path d="{paths(D[k],ox,y,w,h,sk)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" fill-rule="evenodd"/>')
        elif t=="line": L.append(f'<path d="{paths(D[k],ox,y,w,h,sk,False)}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-linecap="round" opacity="0.95"/>')
        else:
            for u,v in D[k]:
                x,yy=proj(u,v,ox,y,w,h,sk); L.append(f'<circle cx="{x:.1f}" cy="{yy:.1f}" r="2.6" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
        px,py=proj(1.08,0.5,ox,y,w,h,sk)
        L.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px+46:.1f}" y2="{py:.1f}" stroke="rgba(255,255,255,.5)" stroke-dasharray="3 3"/><text x="{px+52:.1f}" y="{py+4:.1f}" class="lab">{lab}</text>')
    return "".join(L)
def qr_svg(url, size):
    q=qrcode.QRCode(border=1, box_size=10); q.add_data(url); q.make(fit=True); m=q.get_matrix(); n=len(m); c=size/n
    rects="".join(f'<rect x="{j*c:.2f}" y="{i*c:.2f}" width="{c+0.2:.2f}" height="{c+0.2:.2f}"/>' for i in range(n) for j in range(n) if m[i][j])
    return f'<g fill="#003d36">{rects}</g>', n
CSS="""<style>
@page{size:A4;margin:0} html,body{margin:0;padding:0}
.page{width:210mm;height:297mm;position:relative;overflow:hidden;page-break-after:always}
svg{display:block;width:210mm;height:297mm}
text{font-family:'Battambang',sans-serif;fill:#fff}
.moul{font-family:'Moul',serif}
.lab{font-size:13px;fill:rgba(255,255,255,.85)}
.en{font-family:'Georgia','DejaVu Serif',serif}
</style>"""
def front():
    grad='<defs><linearGradient id="bg" x1="0" y1="0" x2="0.35" y2="1"><stop offset="0" stop-color="#00251f"/><stop offset=".55" stop-color="#00493f"/><stop offset="1" stop-color="#00695c"/></linearGradient><pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="rgba(255,255,255,.05)"/></pattern></defs>'
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">{grad}<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/>']
    s.append(f'<rect x="0" y="0" width="{W}" height="8" fill="#ff7043"/>')
    s.append('<text x="60" y="70" font-size="15" fill="rgba(255,255,255,.8)">ស៊េរីសៀវភៅ GIS និងការយកព័ត៌មានពីចម្ងាយ</text>')
    s.append(f'<text x="{W-60}" y="70" font-size="15" text-anchor="end" fill="#ffab91" font-weight="700">សៀវភៅទី ២</text>')
    s.append('<line x1="60" y1="88" x2="734" y2="88" stroke="rgba(255,255,255,.25)"/>')
    s.append('<text x="60" y="165" class="moul" font-size="40">មូលដ្ឋានគ្រឹះនៃ</text>')
    s.append('<text x="60" y="232" class="moul" font-size="40">ប្រព័ន្ធព័ត៌មានភូមិសាស្ត្រ</text>')
    s.append('<rect x="60" y="258" width="90" height="4" fill="#ff7043"/>')
    s.append('<text x="60" y="300" class="en" font-size="23" fill="#e0f2f1" font-style="italic">Fundamentals of Geographic Information Systems</text>')
    s.append('<text x="60" y="338" font-size="17" fill="#b2dfdb">ទ្រឹស្ដី · ការអនុវត្តលើ QGIS · ទិន្នន័យពិតរបស់កម្ពុជា</text>')
    s.append(art(110,640,430,262,95,78))
    s.append(f'<rect x="0" y="{H-190}" width="{W}" height="190" fill="rgba(0,0,0,.28)"/>')
    s.append(f'<text x="60" y="{H-128}" font-size="26" font-weight="700" class="en">YAM Sarath</text>')
    s.append(f'<text x="60" y="{H-96}" font-size="15" fill="#b2dfdb">ថ្នាក់បរិញ្ញាបត្រ ឆ្នាំទី២ ឆមាសទី២ · ដេប៉ាតឺម៉ង់ភូមិវិទ្យា និងការគ្រប់គ្រងដីធ្លី</text>')
    s.append(f'<text x="60" y="{H-58}" font-size="14" fill="rgba(255,255,255,.75)">១៥ មេរៀន · ១៥ លំហាត់ QGIS · បោះពុម្ពលើកទី១ · ២០២៦</text>')
    s.append(f'<text x="{W-60}" y="{H-58}" font-size="13" text-anchor="end" fill="rgba(255,255,255,.75)" class="en">CC BY-SA 4.0</text>')
    s.append('</svg>')
    return "".join(s)
def back():
    q,n=qr_svg(SITE,120)
    items=["១៥ មេរៀនទ្រឹស្ដី ពីគំរូទិន្នន័យ ដល់ការវិភាគសមស្របភាពពហុលក្ខខណ្ឌ","១៥ លំហាត់ QGIS 3.34 ដែលប្រើទិន្នន័យពិត ៤៣ ស្រទាប់របស់កម្ពុជា","ឧទាហរណ៍ដែលបានដោះស្រាយ ជាមួយ «អ្វីដែលមិនអាចសន្និដ្ឋាន»","ផែនទីអន្តរកម្ម ពិសោធន៍ និងប្រអប់ពិនិត្យខ្លួនឯង នៅក្នុងកំណែអនឡាញ","វាក្យសព្ទខ្មែរ–អង់គ្លេស សម្រាប់ស៊េរីសៀវភៅទាំងបួន"]
    s=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg"><rect width="{W}" height="{H}" fill="#00493f"/><rect x="0" y="{H-8}" width="{W}" height="8" fill="#ff7043"/>']
    s.append('<text x="60" y="120" class="moul" font-size="22">អំពីសៀវភៅនេះ</text>')
    para=["សៀវភៅនេះណែនាំគោលគំនិត និងវិធីសាស្ត្រមូលដ្ឋាននៃប្រព័ន្ធព័ត៌មាន","ភូមិសាស្ត្រ (GIS) ជាភាសាខ្មែរ។ មេរៀននីមួយៗចាប់ផ្ដើមពីសំណួរជាក់ស្ដែង","នៅកម្ពុជា៖ ភូមិណានៅឆ្ងាយពីមណ្ឌលសុខភាព ព្រៃឈើកោះកុងបាត់បង់ទៅណា","សាលាណាប្រឈមទឹកជំនន់ ហើយបង្ហាញជំហានវិភាគ ព្រមទាំងដែនកំណត់នៃលទ្ធផល។"]
    for i,t in enumerate(para): s.append(f'<text x="60" y="{175+i*32}" font-size="16.5" fill="#e0f2f1">{html.escape(t)}</text>')
    s.append('<text x="60" y="340" font-size="18" font-weight="700" fill="#ffab91">អ្វីដែលមាននៅក្នុងសៀវភៅ</text>')
    for i,t in enumerate(items):
        y=385+i*40; s.append(f'<rect x="60" y="{y-13}" width="10" height="10" fill="#ff7043"/><text x="84" y="{y-3}" font-size="15.5" fill="#fff">{html.escape(t)}</text>')
    s.append('<text x="60" y="640" font-size="18" font-weight="700" fill="#ffab91">ស៊េរីសៀវភៅ</text>')
    series=[("១","ផែនទីវិទ្យា","ឆ្នាំទី២ ឆមាសទី១",False),("២","មូលដ្ឋានគ្រឹះនៃ GIS","ឆ្នាំទី២ ឆមាសទី២",True),("៣","មូលដ្ឋានគ្រឹះនៃការយកព័ត៌មានពីចម្ងាយ","ឆ្នាំទី៣ ឆមាសទី១",False),("៤","GIS និងការយកព័ត៌មានពីចម្ងាយអនុវត្តន៍","ឆ្នាំទី៣ ឆមាសទី២",False)]
    for i,(n_,t,y_,cur) in enumerate(series):
        y=680+i*44
        s.append(f'<rect x="60" y="{y-26}" width="674" height="36" rx="4" fill="{"rgba(255,112,67,.25)" if cur else "rgba(255,255,255,.06)"}"/>')
        s.append(f'<text x="78" y="{y-2}" font-size="15" font-weight="700" fill="#ffab91">សៀវភៅទី{n_}</text><text x="185" y="{y-2}" font-size="15">{html.escape(t)}</text><text x="716" y="{y-2}" font-size="13" text-anchor="end" fill="#b2dfdb">{y_}</text>')
    s.append(f'<g transform="translate(60 {H-230})"><rect x="-8" y="-8" width="136" height="136" fill="#fff" rx="6"/>{q}</g>')
    s.append(f'<text x="215" y="{H-190}" font-size="16" font-weight="700">អានកំណែអនឡាញអន្តរកម្ម</text><text x="215" y="{H-162}" font-size="14" class="en" fill="#b2dfdb">{SITE}</text>')
    s.append(f'<text x="215" y="{H-132}" font-size="14" fill="#e0f2f1">ទិន្នន័យ៖ github.com/khgeo/gis-fundamentals</text>')
    s.append(f'<text x="215" y="{H-104}" font-size="13" fill="rgba(255,255,255,.75)">ចេញផ្សាយក្រោមអាជ្ញាបណ្ណ CC BY-SA 4.0 · ចែកចាយដោយឥតគិតថ្លៃ</text>')
    s.append('</svg>')
    return "".join(s)
def wrap(pages, paper_mm=0.1, bleed=3):
    """Print-shop wraparound cover: bleed + back + spine + front + bleed (A4 trim)."""
    spine = round(pages / 2 * paper_mm, 1)
    wmm, hmm = 2 * 210 + spine + 2 * bleed, 297 + 2 * bleed
    sp = f'''<div style="position:absolute;left:{bleed+210}mm;top:0;width:{spine}mm;height:{hmm}mm;background:#003d36;display:flex;align-items:center;justify-content:center">
<div style="transform:rotate(90deg);white-space:nowrap;color:#fff;font-family:Battambang;font-size:{min(11, spine*0.9):.1f}pt;display:flex;gap:10mm;align-items:center">
<span style="font-family:Moul">មូលដ្ឋានគ្រឹះនៃប្រព័ន្ធព័ត៌មានភូមិសាស្ត្រ</span><span style="font-family:Georgia">YAM Sarath</span><span style="color:#ffab91">សៀវភៅទី ២</span></div></div>'''
    page = lambda x, svg: f'<div style="position:absolute;left:{x}mm;top:{bleed}mm;width:210mm;height:297mm">{svg}</div>'
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>@page{{size:{wmm}mm {hmm}mm;margin:0}}html,body{{margin:0}}"
            f"body{{width:{wmm}mm;height:{hmm}mm;position:relative;background:#00493f;overflow:hidden}}svg{{display:block;width:210mm;height:297mm}}"
            f"text{{font-family:'Battambang',sans-serif;fill:#fff}}.moul{{font-family:'Moul',serif}}.lab{{font-size:13px;fill:rgba(255,255,255,.85)}}.en{{font-family:Georgia,serif}}</style></head><body>"
            f"<div style='position:absolute;inset:0;background:#00493f'></div>{page(bleed, back())}{sp}{page(bleed+210+spine, front())}</body></html>"), wmm, hmm, spine

def write(outdir):
    for name, fn in (("cover", front), ("backcover", back)):
        with open(os.path.join(outdir, name + ".html"), "w", encoding="utf-8") as f:
            f.write(f"<!doctype html><html><head><meta charset='utf-8'>{CSS}</head><body><div class='page'>{fn()}</div></body></html>")

if __name__ == "__main__":
    write(".")
