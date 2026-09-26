from vis_core import *
from vis_gis_a import PRV, VIL, HC, C01, S01, R01, H01, V01, W01, town
from vis_gis_b import KKC
import numpy as np
from PIL import Image
from shapely.geometry import shape, Point, MultiPoint, mapping
from shapely.ops import unary_union

def boxes(f, items, y=140, h=110, w=None, gap=20, x0=40, fs=18):
    w = w or (920 - gap * (len(items) - 1)) / len(items)
    for i, (t, sub, c) in enumerate(items):
        x = x0 + i * (w + gap); f.rect(x, y, w, h, c, rx=14); f.text(x + w / 2, y + h / 2 - (6 if sub else -6), t, fs, "#fff", "middle", "bold")
        if sub: f.text(x + w / 2, y + h / 2 + 22, sub, 14, "#fff", "middle")

def run():
    # L1 components
    f = Fig(1000, 420).title("សមាសធាតុប្រាំនៃ GIS")
    boxes(f, [("មនុស្ស", "អ្នកប្រើ អ្នកវិភាគ", "#00897b"), ("ទិន្នន័យ", "វ៉ិចទ័រ រ៉ាស្ទ័រ តារាង", "#1e88e5"), ("កម្មវិធី", "QGIS GEE", "#8e24aa"), ("ឧបករណ៍", "កុំព្យូទ័រ GPS", "#f4511e"), ("វិធីសាស្ត្រ", "ជំហាន ស្តង់ដារ", "#6d4c41")], 150, 140)
    f.text(500, 360, "ខ្វះសមាសធាតុមួយ → គម្រោងមិនដំណើរការ (ឧ. មានកម្មវិធី តែគ្មានទិន្នន័យទាន់សម័យ)", 16, INK, "middle")
    entry(1, f.save("g01-components"), "GIS មិនមែនត្រឹមតែកម្មវិធីទេ",
          ["មនុស្ស និងវិធីសាស្ត្រ ជាញឹកញាប់សំខាន់ជាងកម្មវិធី។", "ទិន្នន័យជាផ្នែកថ្លៃបំផុត និងប្រើពេលច្រើនបំផុត។", "QGIS ឥតគិតថ្លៃ ធ្វើឲ្យស្ថាប័នតូចៗអាចប្រើ GIS បាន។"], .35)
    # L1 spatial concepts
    f = Fig(1000, 440).title("គំនិតលំហប្រាំ")
    boxes(f, [("ទីតាំង", "នៅឯណា", "#26a69a"), ("ចម្ងាយ", "ឆ្ងាយប៉ុណ្ណា", "#42a5f5"), ("ទិស", "ទៅទិសណា", "#ab47bc"), ("លំនាំ", "ប្រមូលផ្ដុំ ឬរាយ", "#ff7043"), ("តំបន់", "ក្រុមដែលស្រដៀង", "#8d6e63")], 130, 130)
    rng = np.random.default_rng(1)
    for i in range(3):
        x0 = 120 + i * 300
        pts = rng.normal([x0 + 60, 340], 15, (20, 2)) if i == 0 else (rng.uniform([x0, 300], [x0 + 120, 390], (20, 2)) if i == 1 else np.array([[x0 + a * 30, 300 + b * 30] for a in range(5) for b in range(4)]))
        for x, y in pts: f.circle(x, y, 4, IND)
        f.text(x0 + 60, 420, ["ប្រមូលផ្ដុំ", "ចៃដន្យ", "ទៀងទាត់"][i], 15, INK, "middle", "bold")
    entry(1, f.save("g01-concepts"), "គិតតាមលំហ",
          ["លំនាំចំណុចបីប្រភេទ៖ ប្រមូលផ្ដុំ ចៃដន្យ និងទៀងទាត់។", "ឧ. ភូមិតាមដងទន្លេប្រមូលផ្ដុំ · សាលាតាមគោលនយោបាយអាចទៀងទាត់។", "សួរជានិច្ច៖ ហេតុអ្វីលំនាំនេះកើតនៅទីនេះ?"], .5)
    # L2 line storage
    f = Fig(1000, 420).title("បន្ទាត់ = លំដាប់ចំណុច")
    pts = [(80, 300), (180, 220), (300, 250), (420, 160), (520, 190)]
    f.path("M" + " L".join(f"{x} {y}" for x, y in pts), "none", "#c62828", 4)
    for i, (x, y) in enumerate(pts): f.circle(x, y, 7, "#fff", IND, 2); f.text(x, y - 16, kh(i + 1), 14, IND, "middle", "bold")
    f.text(620, 180, "LINESTRING (", 17, INK, extra='font-family="monospace"'); f.text(640, 215, "104.66 12.25, 104.67 12.26,", 15, "#455a64", extra='font-family="monospace"'); f.text(640, 245, "104.68 12.26, 104.69 12.27,", 15, "#455a64", extra='font-family="monospace"'); f.text(620, 280, ")", 17, INK, extra='font-family="monospace"')
    f.text(620, 330, "ទិសដៅ៖ ចំណុច ១ → ៥", 16, "#e65100")
    entry(2, f.save("g02-linestring"), "WKT៖ ធរណីមាត្រជាអក្សរ",
          ["បន្ទាត់រក្សាលំដាប់ចំណុច ដែលកំណត់ទិសដៅ។", "ទិសដៅសំខាន់សម្រាប់ផ្លូវមួយទិស និងទិសទឹកហូរ។", "WKT (Well-Known Text) ជាទម្រង់អក្សរស្តង់ដារសម្រាប់ធរណីមាត្រ។"], .25)
    # L2 topology rules
    f = Fig(1000, 440).title("ច្បាប់ឋានលេខាទូទៅ")
    rules = [("ពហុកោណមិនត្រូវជាន់គ្នា", "ឃុំ ខេត្ត"), ("មិនត្រូវមានចន្លោះ", "ព្រំរដ្ឋបាល"), ("ខ្សែត្រូវភ្ជាប់នៅចុង", "បណ្ដាញផ្លូវ ទន្លេ"), ("ចំណុចត្រូវនៅក្នុងពហុកោណ", "សាលាក្នុងឃុំ"), ("ខ្សែមិនត្រូវកាត់ខ្លួនឯង", "ព្រំ")]
    for i, (a, b) in enumerate(rules):
        y = 100 + i * 60; f.rect(60, y, 560, 48, BG, rx=8); f.text(80, y + 31, "✓ " + a, 17, IND, weight="bold"); f.text(650, y + 31, b, 16, "#607d8b")
    entry(2, f.save("g02-rules"), "ឋានលេខា = ទំនាក់ទំនងដែលត្រូវតែពិត",
          ["ច្បាប់ឋានលេខាបកប្រែការពិតលើដីទៅជាលក្ខខណ្ឌពិនិត្យ។", "QGIS Topology Checker រកការបំពានច្បាប់ដោយស្វ័យប្រវត្តិ។", "ពិនិត្យឋានលេខាមុនការវិភាគណាមួយ។"], .6)
    # L3 file size vs resolution
    f = Fig(1000, 440).title("ទំហំឯកសាររ៉ាស្ទ័រ និងទំហំក្រឡា", "កម្ពុជាទាំងមូល (~១៨១ ០០០ គម²) · ១ ក្រុមរលក · ២ បៃ/ក្រឡា")
    res = [(10, "Sentinel-2"), (30, "Landsat"), (90, "SRTM"), (250, "MODIS"), (1000, "")]
    for i, (r, nm) in enumerate(res):
        mb = 181000e6 / (r * r) * 2 / 1e6; h = min(260, math.log10(mb) / math.log10(4000) * 260); x = 100 + i * 170
        f.rect(x, 360 - h, 110, h, "#26a69a"); f.text(x + 55, 352 - h, (f"{kh(round(mb/1000,1))} GB" if mb > 1000 else f"{kh(round(mb))} MB"), 14, INK, "middle", "bold")
        f.text(x + 55, 385, f"{kh(r)} ម", 15, IND, "middle", "bold"); f.text(x + 55, 408, nm, 12, "#607d8b", "middle")
    entry(3, f.save("g03-filesize"), "ក្រឡាតូច = ឯកសារធំ",
          ["កាត់ទំហំក្រឡាពាក់កណ្ដាល → ឯកសារធំ ៤ ដង។", "Sentinel-2 ១០ ម លើកម្ពុជាទាំងមូល ≈ ៣,៦ GB ក្នុងមួយក្រុមរលក។", "កាត់ (clip) តំបន់សិក្សា និងបង្ហាប់ (compress) ដើម្បីសន្សំទំហំ។"], .7)
    # L3 3D wire
    z = np.array(TERRAIN["z"]); n = z.shape[0]
    f = Fig(1000, 440).title("DEM ជាទិដ្ឋភាព ៣ វិមាត្រ")
    for i in range(0, n, 2):
        pts = [(160 + j * 11 + i * 5, 380 - i * 3.2 - z[i, j] * .55) for j in range(n)]; f.path("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts), "#e0f2f1", IND, .7)
    entry(3, f.save("g03-3d"), "រ៉ាស្ទ័របន្ត៖ កម្ពស់",
          ["តម្លៃក្រឡានីមួយៗជាកម្ពស់ គឺជាផ្ទៃបន្ត។", "ទិដ្ឋភាព ៣ វិមាត្រជួយឲ្យយល់រលកដី។", "មេរៀនទី១៣ វិភាគជម្រាល និងទិសពី DEM។"], .9)
    # L4 table anatomy
    f = Fig(1000, 440).title("កាយវិភាគតារាងគុណលក្ខណៈ")
    heads = ["fid", "VILL_CODE", "VILL_NAME", "TOTPOP", "HH_TOT"]; xs = [100, 180, 330, 540, 680]
    f.rect(80, 110, 720, 36, IND)
    for j, h in enumerate(heads): f.text(xs[j], 134, h, 15, "#fff", weight="bold")
    for i, v in enumerate(V01[:5]):
        y = 175 + i * 36; p = v["properties"]; f.rect(80, y - 24, 720, 34, "#fff59d" if i == 2 else (BG if i % 2 else "#fff"))
        for j, val in enumerate([kh(i + 1), p["VILL_CODE"], p["VILL_NAME"], khn(p["TOTPOP"]), khn(p.get("HH_TOT") or 0)]): f.text(xs[j], y, val, 14)
    f.line(850, 128, 810, 128, "#e65100", 2, arrow=True); f.text(860, 133, "វាល (field)", 15, "#e65100", weight="bold")
    f.line(850, 247, 810, 247, "#e65100", 2, arrow=True); f.text(860, 252, "កំណត់ត្រា (record)", 15, "#e65100", weight="bold")
    f.line(560, 380, 560, 340, "#e65100", 2, arrow=True); f.text(560, 400, "ក្រឡា (តម្លៃ)", 15, "#e65100", "middle", "bold")
    entry(4, f.save("g04-anatomy"), "វាល កំណត់ត្រា តម្លៃ",
          ["វាលមួយ = អថេរមួយ · កំណត់ត្រាមួយ = វត្ថុមួយ។", "fid ជាលេខសម្គាល់ខាងក្នុង ដែល QGIS គ្រប់គ្រង។", "VILL_CODE ជាកូនសោ (key) សម្រាប់ភ្ជាប់តារាងផ្សេង។"], .2)
    # L5 relational schema
    f = Fig(1000, 440).title("មូលទិន្នន័យទំនាក់ទំនង")
    tabs = [("ខេត្ត", ["PRO_CODE 🔑", "PRO_NAME"], 60), ("ឃុំ", ["COM_CODE 🔑", "PRO_CODE", "COM_NAME"], 360), ("ភូមិ", ["VILL_CODE 🔑", "COM_CODE", "TOTPOP"], 660)]
    for t, fields, x in tabs:
        f.rect(x, 120, 260, 44, IND, rx=6); f.text(x + 130, 149, t, 18, "#fff", "middle", "bold")
        for i, fl in enumerate(fields): f.rect(x, 164 + i * 40, 260, 40, "#fff", "#b2dfdb"); f.text(x + 16, 190 + i * 40, fl, 15, extra='font-family="monospace"')
    f.line(320, 185, 360, 225, "#ff7043", 2, arrow=True); f.line(620, 185, 660, 225, "#ff7043", 2, arrow=True)
    f.text(500, 380, "១ ខេត្ត → ច្រើនឃុំ · ១ ឃុំ → ច្រើនភូមិ", 17, INK, "middle")
    entry(5, f.save("g05-schema"), "តារាងភ្ជាប់តាមកូនសោ",
          ["កូនសោចម្បង (🔑) មិនស្ទួន និងមិន NULL។", "កូនសោបរទេស (PRO_CODE ក្នុងឃុំ) ចង្អុលទៅតារាងខេត្ត។", "លេខកូដរដ្ឋបាលកម្ពុជា៖ ខេត្ត ២ · ស្រុក ៤ · ឃុំ ៦ · ភូមិ ៨ ខ្ទង់។"], .15)
    # L6 trilateration
    f = Fig(1000, 440).title("GNSS រកទីតាំងដោយចម្ងាយទៅផ្កាយរណប")
    for (x, y, r, c) in [(300, 220, 150, "#42a5f5"), (520, 200, 170, "#ab47bc"), (420, 380, 130, "#26a69a")]:
        f.circle(x, y, r, "none", c, 2); f.circle(x, y, 6, c); f.text(x, y - 12, "🛰", 18, INK, "middle")
    f.circle(410, 300, 8, "#e53935"); f.text(425, 305, "អ្នកទទួល", 15, "#e53935", weight="bold")
    f.text(680, 180, "ផ្កាយរណប ៤+ ចាំបាច់", 18, INK); f.text(680, 215, "(x, y, z, និងម៉ោង)", 16, "#607d8b"); f.text(680, 270, "កំហុស៖ បរិយាកាស អគារ", 16); f.text(680, 300, "ដើមឈើ ធរណីមាត្រផ្កាយរណប", 16)
    entry(6, f.save("g06-trilateration"), "GNSS ដំណើរការយ៉ាងដូចម្ដេច",
          ["អ្នកទទួលវាស់ពេលវេលាសញ្ញា ហើយបម្លែងទៅចម្ងាយ។", "ចម្ងាយពីផ្កាយរណបច្រើន ប្រសព្វគ្នានៅទីតាំងរបស់អ្នក។", "ផ្កាយរណបរាយលើមេឃ ផ្ដល់ភាពត្រឹមត្រូវល្អជាងប្រមូលផ្ដុំ (DOP)។"], .6)
    # L6 licences
    f = Fig(1000, 400).title("អាជ្ញាបណ្ណទិន្នន័យទូទៅ")
    boxes(f, [("Public domain", "Natural Earth · Landsat", "#43a047"), ("CC BY", "ដកស្រង់ប្រភព", "#1e88e5"), ("ODbL", "OSM · ចែករំលែកដូចគ្នា", "#8e24aa"), ("ផ្ទាល់ខ្លួន", "សុំការអនុញ្ញាត", "#e53935")], 150, 130, fs=17)
    entry(6, f.save("g06-licences"), "ប្រើទិន្នន័យដោយស្របច្បាប់",
          ["ទិន្នន័យ «ឥតគិតថ្លៃ» មិនមែនមានន័យថាគ្មានលក្ខខណ្ឌទេ។", "OSM (ODbL) តម្រូវឲ្យដកស្រង់ និងចែករំលែកទិន្នន័យកែសម្រួលក្រោមអាជ្ញាបណ្ណដដែល។", "សរសេរអាជ្ញាបណ្ណក្នុងមេតាទិន្នន័យ និងលើផែនទី។"], .35)
    # L7 digitizing on scan
    scan = os.path.join(DOCS, "assets/data/lab-07/kampong_chhnang_scan.jpg")
    if os.path.exists(scan):
        f = Fig(1000, 520).title("គូសវ៉ិចទ័រលើរូបភាពដែលបាន Georeference")
        f.add('<image href="../assets/data/lab-07/kampong_chhnang_scan.jpg" x="40" y="80" width="560" height="420" preserveAspectRatio="xMidYMid slice" opacity=".75"/>')
        f.path("M 120 400 L 220 330 L 330 300 L 430 220 L 560 170", "none", "#e53935", 4); f.path("M 150 150 L 300 130 L 330 250 L 170 270 Z", "#1e88e5", "#0d47a1", 2, .45)
        for x, y in [(360, 380), (250, 200), (480, 330)]: f.circle(x, y, 7, "#ffeb3b", "#212121", 1.5)
        f.text(640, 170, "ចំណុច៖ សាលា វត្ត", 17); f.text(640, 210, "បន្ទាត់៖ ផ្លូវ ទន្លេ", 17); f.text(640, 250, "ពហុកោណ៖ បឹង ភូមិ", 17); f.text(640, 310, "គូសនៅមាត្រដ្ឋានថេរ", 16, "#607d8b"); f.text(640, 340, "ឧ. ១ : ៥ ០០០ រាល់ពេល", 16, "#607d8b")
        entry(7, f.save("g07-digitize"), "Digitizing",
              ["គូសនៅមាត្រដ្ឋានថេរ ដើម្បីឲ្យភាពលម្អិតស្មើគ្នា។", "ប្រើ snapping និងបិទពហុកោណឲ្យត្រឹមត្រូវ។", "ទិន្នន័យដែលគូសល្អបំផុត អាចត្រឹមត្រូវស្មើតែផែនទីដើមប៉ុណ្ណោះ។"], .8)
    # L8 sliver polygons from overlay
    f = Fig(1000, 420).title("ពហុកោណតូចៗ (slivers) ពីកំហុសព្រំ")
    f.path("M 150 120 L 450 120 L 450 330 L 150 330 Z", "#b2dfdb", IND, 2, .7); f.path("M 157 118 L 455 126 L 446 334 L 144 327 Z", "none", "#ff7043", 2)
    f.text(300, 370, "ព្រំដដែលពីប្រភពពីរ", 16, INK, "middle")
    for i, (x, y, w, h) in enumerate([(560, 150, 300, 8), (850, 150, 8, 170), (560, 320, 300, 8)]): f.rect(x, y, w, h, "#e53935")
    f.text(710, 370, "Intersect → ពហុកោណស្ដើងៗរាប់រយ", 16, "#c62828", "middle", "bold")
    entry(8, f.save("g08-slivers"), "កំហុសផ្គុំគ្នាពេលត្រួតស្រទាប់",
          ["ព្រំដែនដដែលដែលគូសដោយប្រភពពីរ មិនដែលត្រួតគ្នាល្អឥតខ្ចោះទេ។", "Intersect បង្កើតពហុកោណស្ដើងៗដែលគ្មានន័យ។", "ដោះស្រាយ៖ ប្រើប្រភពព្រំតែមួយ ឬលុបពហុកោណតូចជាងកម្រិតកំណត់។"], .65)
    # L9 SQL anatomy
    f = Fig(1000, 380).title("កាយវិភាគកន្សោម SQL")
    f.rect(60, 130, 880, 70, "#263238", rx=8); f.text(90, 175, '"TOTPOP"  >  2000   AND   "COM_NAME"  =  \'Phsar Chhnang\'', 20, "#80cbc4", extra='font-family="monospace"')
    for x, t in [(130, "វាល"), (230, "ប្រតិបត្តិករ"), (300, "តម្លៃ"), (410, "តក្កវិជ្ជា"), (560, "វាល"), (650, "="), (800, "អក្សរ 'ក្នុងសញ្ញាមួយ'")]:
        f.line(x, 205, x, 240, "#ff7043", 1.5); f.text(x, 262, t, 14, "#e65100", "middle", "bold")
    entry(9, f.save("g09-sql"), "សរសេរលក្ខខណ្ឌ",
          ["ឈ្មោះវាល \"ពីរ\" · អក្សរ 'មួយ' · លេខគ្មានសញ្ញា។", "AND ទាំងពីរពិត · OR មួយពិតគ្រប់គ្រាន់។", "ប្រើវង់ក្រចក ពេលផ្សំ AND និង OR។"], .2)
    # L9 schools within 300 m of primary roads (real)
    T = geo_frame(C01, (40, 80, 480, 430))
    f = Fig(1000, 520).title("សាលាក្នុង ៣០០ ម ពីផ្លូវជាតិ", "Select by location · ទិន្នន័យលំហាត់ទី១")
    town(f, T); prim = unary_union([shape(r["geometry"]) for r in R01 if "Primary" in str(r["properties"].get("Type"))]); zone = prim.buffer(.0027)
    draw_gj(f, [{"geometry": mapping(zone)}], T, lambda x: "#ffcc80", lambda x: "#ff7043", .6, op=.35); cnt = 0
    for s in S01:
        p = shape(s["geometry"]); x, y = T(p.x, p.y); ins = zone.contains(p); cnt += ins
        f.circle(x, y, 9, "none", "#e53935" if ins else "#90a4ae", 2.5)
    f.text(580, 200, f"{kh(cnt)} ក្នុង {kh(len(S01))} សាលា", 26, "#e53935", weight="bold"); f.text(580, 240, "នៅជិតផ្លូវជាតិ (ហានិភ័យចរាចរណ៍)", 16, INK)
    entry(9, f.save("g09-schools-roads"), "សំណួរលំហលើទិន្នន័យពិត",
          ["បាហ្វ័រផ្លូវជាតិ ៣០០ ម រួចជ្រើសសាលាដែលនៅខាងក្នុង។", "លទ្ធផលជួយកំណត់សាលាដែលត្រូវការសញ្ញាចរាចរណ៍។", "ចម្ងាយ ៣០០ ម ជាការសន្មត៖ ត្រូវពិភាក្សាជាមួយអ្នកជំនាញ។"], .45)
    # L10 buffer types
    from shapely.geometry import LineString
    f = Fig(1000, 400).title("ប្រភេទបាហ្វ័រ")
    line = LineString([(0, 0), (1, .4), (2, 0)])
    for i, (nm, g) in enumerate([("ជ្រុងមូល", line.buffer(.3)), ("ជ្រុងរាប", line.buffer(.3, cap_style=2)), ("ម្ខាង", line.buffer(.3, single_sided=True))]):
        tr = lambda x, y, i=i: (60 + i * 320 + x * 110, 240 - y * 110)
        f.path("M" + " L".join("%.1f %.1f" % tr(*q) for q in g.exterior.coords) + "Z", "#b2dfdb", IND, 1); f.path("M" + " L".join("%.1f %.1f" % tr(*q) for q in line.coords), "none", "#c62828", 3)
        f.text(60 + i * 320 + 110, 350, nm, 17, IND, "middle", "bold")
    entry(10, f.save("g10-buffer-types"), "ជម្រើសបាហ្វ័រ",
          ["ជ្រុងមូល៖ ចម្ងាយពិតគ្រប់ទិស (លំនាំដើម)។", "ជ្រុងរាប៖ សម្រាប់ផ្លូវ ឬប្រឡាយដែលចប់ត្រឹមចុង។", "ម្ខាង៖ ឧ. តំបន់ការពារច្រាំងទន្លេតែម្ខាង។"], .25)
    # L11 union attribute table
    f = Fig(1000, 420).title("Union៖ តារាងលទ្ធផលផ្សំគុណលក្ខណៈ")
    f.rect(80, 120, 380, 60, IND); f.text(270, 157, "lc1997 · lc2015 · ha", 17, "#fff", "middle", "bold")
    rows = [("ព្រៃ", "ព្រៃ", "៤៥ ២០០"), ("ព្រៃ", "កសិកម្ម", "១២ ៨០០"), ("ព្រៃ", "វាលស្មៅ", "៨ ៤០០"), ("កសិកម្ម", "សំណង់", "៩០០")]
    for i, r in enumerate(rows):
        y = 210 + i * 40; f.rect(80, y - 26, 380, 36, BG if i % 2 else "#fff")
        for j, v in enumerate(r): f.text(110 + j * 130, y, v, 16)
    f.text(560, 220, "ជួរដេកនីមួយៗ = ផ្ទៃដែលមាន", 17); f.text(560, 250, "បន្សំប្រភេទដូចគ្នាក្នុងឆ្នាំទាំងពីរ", 17); f.text(560, 310, "(តួលេខជាឧទាហរណ៍)", 14, "#90a4ae")
    entry(11, f.save("g11-union-table"), "គុណលក្ខណៈក្រោយការត្រួតស្រទាប់",
          ["Union/Intersect បំបែកពហុកោណតាមព្រំនៃស្រទាប់ទាំងពីរ។", "គុណលក្ខណៈនៃស្រទាប់ទាំងពីរ មាននៅក្នុងជួរដេកតែមួយ។", "គណនាផ្ទៃម្ដងទៀតក្រោយ overlay ព្រោះពហុកោណបានបំបែក។"], .5)
    # L12 zonal stats bars (Koh Kong communes loss)
    top = sorted(KKC, key=lambda c: -c["properties"]["loss_ha"])[:8]; mx = top[0]["properties"]["loss_ha"]
    f = Fig(1000, 460).title("ស្ថិតិតាមតំបន់ (zonal)៖ ការបាត់បង់ព្រៃតាមឃុំ", "ខេត្តកោះកុង · ៨ ឃុំខ្ពស់ជាងគេ")
    for i, c in enumerate(top):
        y = 100 + i * 40; p = c["properties"]; f.text(40, y + 20, p["COMNAME_KH"], 15); f.rect(260, y + 4, p["loss_ha"] / mx * 560, 26, "#e53935"); f.text(270 + p["loss_ha"] / mx * 560, y + 22, khn(p["loss_ha"]) + " ហ.ត", 13)
    entry(12, f.save("g12-zonal"), "Zonal statistics",
          ["តំបន់ (ឃុំ) ជាវ៉ិចទ័រ · តម្លៃ (ការបាត់បង់) ជារ៉ាស្ទ័រ ឬផ្ទៃ។", "លទ្ធផល៖ ផលបូក មធ្យម អតិបរមា ក្នុងតំបន់នីមួយៗ។", "QGIS៖ Raster analysis → Zonal statistics។"], .75)
    # L13 TIN triangles
    rng = np.random.default_rng(8); P = rng.uniform(40, 460, (25, 2))
    from shapely.ops import triangulate
    f = Fig(1000, 520).title("TIN៖ ត្រីកោណពីចំណុចវាស់")
    for tri in triangulate(MultiPoint([tuple(p) for p in P])):
        f.path("M" + " L".join(f"{x + 60:.1f} {y + 40:.1f}" for x, y in tri.exterior.coords) + "Z", "#e0f2f1", IND, 1)
    for x, y in P: f.circle(x + 60, y + 40, 4, "#e53935")
    f.text(600, 200, "ត្រីកោណ Delaunay", 20, IND, weight="bold"); f.text(600, 240, "មុំតូចបំផុតធំតាមដែលអាច", 16); f.text(600, 290, "តម្លៃក្នុងត្រីកោណ = លីនេអ៊ែរ", 16); f.text(600, 320, "ពីកំពូលទាំងបី", 16)
    entry(13, f.save("g13-tin"), "Triangulated Irregular Network",
          ["TIN រក្សាចំណុចវាស់ដើម ហើយតភ្ជាប់ជាត្រីកោណ។", "តំបន់ដែលមានចំណុចច្រើន មានត្រីកោណតូច និងលម្អិត។", "ល្អសម្រាប់ទិន្នន័យស្ទង់ដីដែលមិនទៀងទាត់។"], .4)
    # L14 AHP matrix
    f = Fig(1000, 420).title("ប្រៀបធៀបជាគូ (AHP)")
    crit = ["ជម្រាល", "ផ្លូវ", "ទឹក"]; M = [["១", "៣", "៥"], ["១/៣", "១", "២"], ["១/៥", "១/២", "១"]]
    for j, c in enumerate(crit): f.text(300 + j * 110, 130, c, 16, IND, "middle", "bold"); f.text(170, 180 + j * 60, c, 16, IND, "middle", "bold")
    for i in range(3):
        for j in range(3): f.rect(245 + j * 110, 150 + i * 60, 110, 56, BG if i != j else "#b2dfdb", "#fff", 2); f.text(300 + j * 110, 185 + i * 60, M[i][j], 18, INK, "middle")
    f.text(640, 190, "ទម្ងន់៖ ជម្រាល ០,៦៥", 18); f.text(640, 225, "ផ្លូវ ០,២៣ · ទឹក ០,១២", 18); f.text(640, 280, "៣ = សំខាន់ជាងបន្តិច", 15, "#607d8b"); f.text(640, 305, "៥ = សំខាន់ជាងច្រើន", 15, "#607d8b")
    entry(14, f.save("g14-ahp"), "កំណត់ទម្ងន់ដោយការប្រៀបធៀបជាគូ",
          ["ងាយជាងឲ្យអ្នកពាក់ព័ន្ធប្រៀបធៀបកត្តាពីរៗ ជាជាងឲ្យលេខទម្ងន់ផ្ទាល់។", "AHP បម្លែងម៉ាទ្រីសទៅជាទម្ងន់ដែលបូកគ្នា = ១។", "ពិនិត្យ Consistency Ratio < ០,១។"], .55)
    # L15 versions
    f = Fig(1000, 380).title("កំណែ និងកាលបរិច្ឆេទ")
    vs = [("v1", "ទិន្នន័យដើម"), ("v2", "កែកំហុស"), ("v3", "បន្ថែមជំរឿន ២០១៩"), ("v4", "របាយការណ៍ចុងក្រោយ")]
    f.line(100, 200, 900, 200, "#b0bec5", 3)
    for i, (a, b) in enumerate(vs): x = 120 + i * 250; f.circle(x, 200, 16, IND); f.text(x, 206, a, 13, "#fff", "middle", "bold"); f.text(x, 250, b, 15, INK, "middle")
    f.text(500, 320, "ឈ្មោះឯកសារ៖ villages_2025-03-15_v3.gpkg · ឬប្រើ Git", 16, "#607d8b", "middle")
    entry(15, f.save("g15-versions"), "គ្រប់គ្រងកំណែ",
          ["កុំសរសេរជាន់ឯកសារចាស់ដោយមិនមានច្បាប់ចម្លង។", "ឈ្មោះមានកាលបរិច្ឆេទ ឬលេខកំណែ ជួយស្វែងរកលទ្ធផលមុន។", "Git/GitHub រក្សាប្រវត្តិការផ្លាស់ប្ដូរស្គ្រីប និងឯកសារ។"], .6)
