from vis_core import *
from vis_gis_a import PRV, VIL, HC, NB, town, C01, S01, R01
import numpy as np
from PIL import Image
from shapely.geometry import shape, Point, mapping
from shapely.ops import unary_union, voronoi_diagram
from shapely.geometry import MultiPoint
RD = "/home/claude/realdata"
KK = gj("lab-11/province.geojson")["features"]; LC97 = gj("lab-11/lc1997.geojson")["features"]; LC15 = gj("lab-11/lc2015.geojson")["features"]
LOSS = gj("lab-11/forest_loss.geojson")["features"]; PA = gj("lab-11/protected_areas.geojson")["features"]; KKC = gj("lab-11/communes.geojson")["features"]
LCC = {"Forest": "#2e7d32", "Agricultural land": "#dce775", "Urban or built-up area": "#e53935", "Water": "#64b5f6", "Wetland": "#4db6ac", "Rangeland": "#c5e1a5", "Barren land": "#bcaaa4"}
lcol = lambda ft: next((c for k, c in LCC.items() if k.lower() in str(ft["properties"].get("cls", "")).lower()), "#e0e0e0")
UTM = lambda lon, lat: (lon, lat)

def L09():
    T = geo_frame(PRV, (40, 80, 560, 440)); hc_in = [h for h in HC if h["properties"].get("in_prov")]
    # attribute query big villages
    f = Fig(1000, 540).title("សំណួរតាមគុណលក្ខណៈ", "\"TOTPOP\" > 3000")
    draw_gj(f, PRV, T, lambda x: "#f5f5f5", lambda x: "#90a4ae", 1.2)
    big = 0
    for v in VIL:
        x, y = T(*v["geometry"]["coordinates"]); b = v["properties"]["TOTPOP"] > 3000; big += b
        f.circle(x, y, 4.5 if b else 2, "#ffeb3b" if b else "#b0bec5", "#f57f17" if b else "none", 1)
    f.rect(630, 150, 330, 60, "#263238", rx=6); f.text(650, 188, "\"TOTPOP\" > 3000", 20, "#80cbc4", extra='font-family="monospace"')
    f.text(630, 260, f"បានជ្រើស {kh(big)} ភូមិ", 22, "#f57f17", weight="bold"); f.text(630, 300, "សំណួរនេះមិនប្រើទីតាំងទេ", 16, "#607d8b")
    entry(9, f.save("g09-attr-query"), "ជ្រើសតាមគុណលក្ខណៈ",
          ["លក្ខខណ្ឌលើតារាង៖ ប្រៀបធៀបតម្លៃវាល។", "លទ្ធផលជាការជ្រើសរើស (selection) ដែលអាចរក្សាទុកជាស្រទាប់ថ្មី។", "ផ្សំលក្ខខណ្ឌដោយ AND / OR។"], .1)
    # spatial predicates
    f = Fig(1000, 440).title("ទំនាក់ទំនងលំហ (predicates)")
    names = ["intersects", "within", "contains", "touches", "disjoint", "crosses"]
    for i, nm in enumerate(names):
        x0 = 30 + i * 160; cy = 220
        if nm == "intersects": f.rect(x0 + 20, cy - 50, 70, 70, "#80cbc4", IND); f.rect(x0 + 60, cy - 20, 70, 70, "#ffcc80", "#ff7043", extra='fill-opacity=".7"')
        if nm == "within": f.rect(x0 + 15, cy - 60, 120, 120, "#80cbc4", IND); f.rect(x0 + 50, cy - 25, 50, 50, "#ffcc80", "#ff7043")
        if nm == "contains": f.rect(x0 + 15, cy - 60, 120, 120, "#ffcc80", "#ff7043"); f.circle(x0 + 75, cy, 8, IND)
        if nm == "touches": f.rect(x0 + 10, cy - 45, 65, 90, "#80cbc4", IND); f.rect(x0 + 75, cy - 45, 65, 90, "#ffcc80", "#ff7043")
        if nm == "disjoint": f.rect(x0 + 10, cy - 45, 50, 60, "#80cbc4", IND); f.rect(x0 + 90, cy - 10, 50, 60, "#ffcc80", "#ff7043")
        if nm == "crosses": f.rect(x0 + 25, cy - 50, 100, 100, "#80cbc4", IND); f.line(x0 + 5, cy + 60, x0 + 145, cy - 60, "#ff7043", 3)
        f.text(x0 + 75, 330, nm, 16, IND, "middle", "bold")
    entry(9, f.save("g09-predicates"), "Select by location",
          ["intersects៖ ប៉ះ ឬជាន់គ្នាតាមណាមួយ (ប្រើញឹកញាប់បំផុត)។", "within / contains៖ នៅខាងក្នុងទាំងស្រុង។", "touches៖ ប៉ះតែព្រំ · disjoint៖ មិនប៉ះគ្នាសោះ។"], .35)
    # distance query
    f = Fig(1000, 540).title("សំណួរតាមចម្ងាយ", "ភូមិក្នុង ៣ គម ពីមណ្ឌលសុខភាព")
    draw_gj(f, PRV, T, lambda x: "#f5f5f5", lambda x: "#90a4ae", 1.2)
    hs = [shape(h["geometry"]) for h in hc_in]; near = 0
    for h in hc_in: x, y = T(*h["geometry"]["coordinates"]); f.circle(x, y, 3 * T.scale_km, "#b2dfdb", "#26a69a", .8, .5)
    for v in VIL:
        p = shape(v["geometry"]); d = min(p.distance(h) for h in hs) * 111; x, y = T(p.x, p.y); n_ = d <= 3; near += n_
        f.circle(x, y, 2.6, "#00695c" if n_ else "#bdbdbd")
    for h in hc_in: x, y = T(*h["geometry"]["coordinates"]); f.circle(x, y, 4, "#fff", "#2e7d32", 2)
    f.text(640, 200, f"{kh(near)} ភូមិ", 30, IND, weight="bold"); f.text(640, 240, "ក្នុង ៣ គម", 18, INK); f.text(640, 300, f"ពី {kh(len(VIL))} ភូមិសរុប", 16, "#607d8b")
    entry(9, f.save("g09-distance-query"), "ជ្រើសតាមចម្ងាយ",
          ["Select within distance ត្រូវការ CRS ជាម៉ែត្រ (UTM 48N)។", "ចម្ងាយត្រង់មិនស្មើចម្ងាយធ្វើដំណើរតាមផ្លូវ។", "ផ្សំជាមួយគុណលក្ខណៈ៖ ភូមិធំ AND ឆ្ងាយពីមណ្ឌល។"], .6)
    # combine: big AND far
    f = Fig(1000, 540).title("ផ្សំសំណួរ៖ ធំ AND ឆ្ងាយ", "ភូមិ > ២ ០០០ នាក់ AND ឆ្ងាយជាង ៥ គម ពីមណ្ឌល")
    draw_gj(f, PRV, T, lambda x: "#f5f5f5", lambda x: "#90a4ae", 1.2); cnt = 0
    for v in VIL:
        p = shape(v["geometry"]); d = min(p.distance(h) for h in hs) * 111; x, y = T(p.x, p.y); ok = d > 5 and v["properties"]["TOTPOP"] > 2000; cnt += ok
        f.circle(x, y, 5 if ok else 2, "#e53935" if ok else "#cfd8dc")
    for h in hc_in: x, y = T(*h["geometry"]["coordinates"]); f.circle(x, y, 4, "#fff", "#2e7d32", 2)
    f.text(640, 220, f"{kh(cnt)} ភូមិ", 34, "#e53935", weight="bold"); f.text(640, 262, "ជាអាទិភាពសម្រាប់មណ្ឌលថ្មី ឬសេវាចល័ត", 16, INK)
    entry(9, f.save("g09-combined"), "ពីសំណួរទៅការសម្រេចចិត្ត",
          ["លក្ខខណ្ឌពីរ (គុណលក្ខណៈ + លំហ) កាត់បន្ថយពី ៥៦៨ មកត្រឹមប៉ុន្មានភូមិ។", "លំដាប់៖ ជ្រើសដំបូង → ជ្រើសពីក្នុងការជ្រើស (select from selection)។", "លទ្ធផលត្រូវពិនិត្យនៅទីវាល មុនសម្រេចចិត្ត។"], .85)

def L10():
    T = geo_frame(PRV, (40, 80, 560, 440)); hc_in = [h for h in HC if h["properties"].get("in_prov")]
    hs = [shape(h["geometry"]) for h in hc_in]
    # buffer 5km dissolve vs not
    f = Fig(1000, 520).title("បាហ្វ័រ ៥ គម ជុំវិញមណ្ឌលសុខភាព", "មិន Dissolve ធៀបនឹង Dissolve")
    for i in range(2):
        Ti = geo_frame(PRV, (20 + i * 490, 90, 460, 360)); draw_gj(f, PRV, Ti, lambda x: "#f5f5f5", lambda x: "#90a4ae", 1)
        if i == 0:
            for h in hs: f.path(" ".join("M" + " L".join("%.1f %.1f" % Ti(*q) for q in r) + "Z" for r in [list(h.buffer(5 / 111).exterior.coords)]), "#80cbc4", IND, .6, .35)
        else:
            u = unary_union([h.buffer(5 / 111) for h in hs]); draw_gj(f, [{"geometry": mapping(u)}], Ti, lambda x: "#80cbc4", lambda x: IND, 1.2, op=.6)
        f.text(250 + i * 490, 480, ["រង្វង់ជាន់គ្នា → រាប់ផ្ទៃស្ទួន", "Dissolve → តំបន់គ្របដណ្ដប់តែមួយ"][i], 16, IND, "middle", "bold")
    entry(10, f.save("g10-buffer-dissolve"), "បាហ្វ័រ និង Dissolve",
          ["បាហ្វ័រ ៥ គម = តំបន់ដែលស្ថិតក្នុងចម្ងាយ ៥ គម។", "បើមិន Dissolve ផ្ទៃជាន់គ្នាត្រូវរាប់ច្រើនដង។", "ត្រូវគណនាបាហ្វ័រក្នុង CRS ម៉ែត្រ៖ ៥ ០០០ ម មិនមែន ០,០៥°។"], .15)
    # coverage stats
    u = unary_union([h.buffer(5 / 111) for h in hs]); inside = [v for v in VIL if u.contains(shape(v["geometry"]))]
    pin = sum(v["properties"]["TOTPOP"] for v in inside); ptot = sum(v["properties"]["TOTPOP"] for v in VIL)
    f = Fig(1000, 520).title("ប្រជាជនក្នុងតំបន់គ្របដណ្ដប់ ៥ គម")
    draw_gj(f, PRV, T, lambda x: "#f5f5f5", lambda x: "#90a4ae", 1); draw_gj(f, [{"geometry": mapping(u)}], T, lambda x: "#b2dfdb", lambda x: "#26a69a", .8, op=.7)
    for v in VIL: x, y = T(*v["geometry"]["coordinates"]); f.circle(x, y, 2.4, "#00695c" if u.contains(shape(v["geometry"])) else "#e53935")
    f.text(640, 180, f"{kh(round(pin/ptot*100))}%", 60, IND, weight="bold"); f.text(640, 230, "នៃប្រជាជនរស់នៅក្នុង ៥ គម", 18, INK)
    f.text(640, 290, f"{khn(ptot-pin)} នាក់ នៅក្រៅ", 22, "#e53935", weight="bold")
    entry(10, f.save("g10-coverage"), "ពីបាហ្វ័រទៅចំនួនមនុស្ស",
          ["រាប់ភូមិក្នុងបាហ្វ័រ ហើយបូកប្រជាជន៖ ចម្លើយដែលអ្នកសម្រេចចិត្តត្រូវការ។", "ភូមិពណ៌ក្រហមជាគោលដៅសេវាចល័ត។", "ចំណាំ៖ រាប់ភូមិតាមចំណុចកណ្ដាល មិនមែនតាមផ្ទៃភូមិពិតទេ។"], .35)
    # multi-ring
    f = Fig(1000, 520).title("បាហ្វ័រច្រើនជាន់ ២ · ៥ · ១០ គម")
    draw_gj(f, PRV, T, lambda x: "#f5f5f5", lambda x: "#90a4ae", 1)
    for d, c in [(10, "#e0f2f1"), (5, "#80cbc4"), (2, "#26a69a")]:
        draw_gj(f, [{"geometry": mapping(unary_union([h.buffer(d / 111) for h in hs]).intersection(shape(PRV[0]["geometry"])))}], T, lambda x, c=c: c, lambda x: "#fff", .5)
    for h in hc_in: x, y = T(*h["geometry"]["coordinates"]); f.circle(x, y, 3.5, "#fff", "#004d40", 1.5)
    f.legend_boxes(650, 180, ["#26a69a", "#80cbc4", "#e0f2f1"], ["< ២ គម", "២–៥ គម", "៥–១០ គម"], "ចម្ងាយ")
    entry(10, f.save("g10-multiring"), "តំបន់ចម្ងាយជាជាន់",
          ["Multi-ring buffer បង្ហាញកម្រិតលទ្ធភាពទទួលបានសេវា។", "ប្រៀបធៀបចំនួនប្រជាជនក្នុងជាន់នីមួយៗ។", "កាត់ (clip) តាមព្រំខេត្ត ដើម្បីកុំឲ្យលើសតំបន់សិក្សា។"], .5)
    # nearest lines
    f = Fig(1000, 520).title("ចម្ងាយទៅមណ្ឌលជិតបំផុត (hub lines)")
    draw_gj(f, PRV, T, lambda x: "#f5f5f5", lambda x: "#90a4ae", 1)
    for v in VIL[::2]:
        p = shape(v["geometry"]); h = min(hs, key=lambda h: p.distance(h)); a, b = T(p.x, p.y), T(h.x, h.y); d = p.distance(h) * 111
        f.line(a[0], a[1], b[0], b[1], "#26a69a" if d < 5 else "#ff7043", .8)
    for h in hc_in: x, y = T(*h["geometry"]["coordinates"]); f.circle(x, y, 4, "#fff", "#004d40", 1.8)
    f.legend_boxes(650, 200, ["#26a69a", "#ff7043"], ["< ៥ គម", "≥ ៥ គម"])
    entry(10, f.save("g10-hub-lines"), "Distance to nearest hub",
          ["ភូមិនីមួយៗភ្ជាប់ទៅមណ្ឌលជិតបំផុតរបស់វា។", "លទ្ធផលមានវាលចម្ងាយ ដែលអាចធ្វើផែនទី ឬស្ថិតិ។", "ពិចារណាមណ្ឌលក្នុងខេត្តជិតខាងផង (ឥទ្ធិពលគែម)។"], .65)
    # voronoi catchments
    f = Fig(1000, 520).title("តំបន់សេវា Thiessen (Voronoi)")
    prov = shape(PRV[0]["geometry"]); vd = voronoi_diagram(MultiPoint(hs), envelope=prov.envelope.buffer(.2))
    for i, cell in enumerate(vd.geoms):
        cl = cell.intersection(prov)
        if not cl.is_empty: draw_gj(f, [{"geometry": mapping(cl)}], T, lambda x, i=i: QUAL[i % 8], lambda x: "#fff", .8, op=.55)
    for h in hc_in: x, y = T(*h["geometry"]["coordinates"]); f.circle(x, y, 3.5, "#212121")
    entry(10, f.save("g10-voronoi"), "តំបន់ជិតបំផុត",
          ["ចំណុចក្នុងក្រឡានីមួយៗ ជិតមណ្ឌលក្នុងក្រឡានោះជាងមណ្ឌលផ្សេង។", "ប្រើសម្រាប់ប៉ាន់តំបន់សេវា ពេលគ្មានទិន្នន័យអ្នកជំងឺ។", "QGIS៖ Vector geometry → Voronoi polygons។"], .8)
    # edge effect
    f = Fig(1000, 520).title("ឥទ្ធិពលគែម៖ មណ្ឌលក្នុងខេត្តជិតខាង")
    Tn = geo_frame(NB + PRV, (40, 80, 600, 430)); draw_gj(f, NB, Tn, lambda x: "#eceff1", lambda x: "#b0bec5", 1); draw_gj(f, PRV, Tn, lambda x: "#e0f2f1", lambda x: IND, 1.6)
    for h in HC:
        x, y = Tn(*h["geometry"]["coordinates"]); f.circle(x, y, 4, "#fff" if h["properties"].get("in_prov") else "#ff7043", "#004d40" if h["properties"].get("in_prov") else "#bf360c", 1.5)
    f.legend_boxes(680, 200, ["#fff", "#ff7043"], ["មណ្ឌលក្នុងខេត្ត", "មណ្ឌលក្នុងខេត្តជិតខាង"])
    f.text(680, 300, "ភូមិនៅគែមខេត្ត អាចទៅមណ្ឌល", 16); f.text(680, 326, "ក្នុងខេត្តជិតខាងជិតជាង", 16)
    entry(10, f.save("g10-edge"), "កុំកាត់ទិន្នន័យដោយព្រំខេត្តមុនវិភាគ",
          ["បើប្រើតែមណ្ឌលក្នុងខេត្ត ភូមិនៅគែមមើលទៅឆ្ងាយជាងការពិត។", "រួមបញ្ចូលមណ្ឌលក្នុងខេត្តជិតខាង ក្នុងចម្ងាយសមស្រប។", "កាត់តាមព្រំតែលទ្ធផលចុងក្រោយ។"], .9)

def L11():
    T = geo_frame(KK, (30, 80, 560, 450))
    # land cover 1997 vs 2015
    f = Fig(1000, 520).title("គម្របដី ១៩៩៧ ធៀបនឹង ២០១៥", "ខេត្តកោះកុង")
    for i, (lc, yr) in enumerate([(LC97, "១៩៩៧"), (LC15, "២០១៥")]):
        Ti = geo_frame(KK, (20 + i * 490, 90, 460, 380)); draw_gj(f, lc, Ti, lcol, lambda x: "none", 0); draw_gj(f, KK, Ti, lambda x: "none", lambda x: "#37474f", 1)
        f.text(250 + i * 490, 495, yr, 20, IND, "middle", "bold")
    f.legend_boxes(420, 110, list(LCC.values())[:5], ["ព្រៃ", "កសិកម្ម", "សំណង់", "ទឹក", "ដីសើម"], horizontal=False) if False else None
    for i, (k, c) in enumerate(list(LCC.items())[:5]): f.rect(80 + i * 170, 500 - 480, 0, 0)
    entry(11, f.save("g11-lc-two-dates"), "ស្រទាប់ពីរកាលបរិច្ឆេទ",
          ["ព្រៃ (បៃតងចាស់) ថយចុះយ៉ាងច្បាស់ពី ១៩៩៧ ដល់ ២០១៥។", "ដីកសិកម្ម (លឿង) ពង្រីកតាមផ្លូវ និងឆ្នេរ។", "ការត្រួតស្រទាប់ (overlay) រកកន្លែងដែលប្ដូរពីប្រភេទមួយទៅប្រភេទមួយទៀត។"], .15)
    # forest loss & protected areas
    f = Fig(1000, 540).title("ការបាត់បង់ព្រៃ និងតំបន់ការពារ", "Intersect៖ ការបាត់បង់ព្រៃក្នុងតំបន់ការពារ")
    draw_gj(f, KK, T, lambda x: "#f5f5f5", lambda x: "#90a4ae", 1)
    draw_gj(f, PA, T, lambda x: "#c8e6c9", lambda x: "#2e7d32", 1.2, op=.8)
    draw_gj(f, LOSS, T, lambda x: "#e53935", lambda x: "none", 0, op=.8)
    try:
        pa = unary_union([shape(p["geometry"]).buffer(0) for p in PA]); lo = unary_union([shape(l["geometry"]).buffer(0) for l in LOSS]); ins = lo.intersection(pa)
        draw_gj(f, [{"geometry": mapping(ins)}], T, lambda x: "#6a1b9a", lambda x: "none", 0)
        share = ins.area / lo.area * 100
        f.text(640, 360, f"{kh(round(share))}% នៃការបាត់បង់ព្រៃ", 20, "#6a1b9a", weight="bold"); f.text(640, 390, "កើតក្នុងតំបន់ការពារ", 17, INK)
    except Exception as e: print("intersect skipped", e)
    f.legend_boxes(640, 170, ["#c8e6c9", "#e53935", "#6a1b9a"], ["តំបន់ការពារ", "បាត់បង់ព្រៃ ១៩៩៧–២០១៥", "បាត់បង់ក្នុងតំបន់ការពារ"])
    entry(11, f.save("g11-loss-pa"), "Intersect ឆ្លើយសំណួរគោលនយោបាយ",
          ["ការបាត់បង់ព្រៃ ត្រួតជាមួយតំបន់ការពារ → ផ្ទៃដែលបាត់ក្នុងតំបន់ការពារ។", "ចម្លើយជាហិកតា និងភាគរយ អាចប្រើក្នុងរបាយការណ៍។", "ភាពត្រឹមត្រូវអាស្រ័យលើស្រទាប់ទាំងពីរ (កំហុសផ្គុំគ្នា)។"], .35)
    # overlay operations diagram
    f = Fig(1000, 420).title("ប្រតិបត្តិការត្រួតស្រទាប់")
    ops = ["Clip", "Intersect", "Union", "Difference", "Sym. difference"]
    from shapely.geometry import Point as Pt
    A = Pt(0, 0).buffer(1); B = Pt(1, 0).buffer(1)
    res = {"Clip": A.intersection(B), "Intersect": A.intersection(B), "Union": A.union(B), "Difference": A.difference(B), "Sym. difference": A.symmetric_difference(B)}
    for i, nm in enumerate(ops):
        x0 = 40 + i * 190; tr = lambda x, y: (x0 + 50 + x * 45, 200 - y * 45)
        for g in (A, B): f.path("M" + " L".join("%.1f %.1f" % tr(*q) for q in g.exterior.coords) + "Z", "none", "#90a4ae", 1)
        r = res[nm]; geoms = r.geoms if hasattr(r, "geoms") else [r]
        for g in geoms: f.path("M" + " L".join("%.1f %.1f" % tr(*q) for q in g.exterior.coords) + "Z", "#26a69a", IND, 1.2, .8)
        f.text(x0 + 72, 320, nm, 16, IND, "middle", "bold")
    entry(11, f.save("g11-operations"), "Clip · Intersect · Union · Difference",
          ["Clip៖ កាត់តាមព្រំ យកតែគុណលក្ខណៈស្រទាប់ទីមួយ។", "Intersect៖ យកតែផ្ទៃរួម ជាមួយគុណលក្ខណៈទាំងពីរ។", "Union៖ រក្សាគ្រប់ផ្ទៃ · Difference៖ ដកផ្ទៃរួមចេញ។"], .05)
    # commune loss choropleth (spatial join summary)
    f = Fig(1000, 540).title("Spatial join៖ ការបាត់បង់ព្រៃតាមឃុំ", "ភាគរយនៃផ្ទៃឃុំ")
    vals = sorted(c["properties"]["pct"] for c in KKC); br = [vals[int(i * (len(vals) - 1) / 5)] for i in range(6)]
    cc = lambda ft: SEQ[min(4, sum(1 for b in br[1:-1] if ft["properties"]["pct"] > b))]
    draw_gj(f, KKC, T, cc, lambda x: "#fff", .8)
    f.legend_boxes(640, 180, SEQ, [f"{kh(round(br[i],1))}–{kh(round(br[i+1],1))}%" for i in range(5)], "ភាគរយបាត់បង់")
    entry(11, f.save("g11-commune-loss"), "សរុបតាមឯកតារដ្ឋបាល",
          ["Join attributes by location (summary) បូកផ្ទៃបាត់បង់ក្នុងឃុំនីមួយៗ។", "ចែកដោយផ្ទៃឃុំ ដើម្បីបានភាគរយ (អត្រា)។", "ផែនទីនេះងាយយល់សម្រាប់អាជ្ញាធរមូលដ្ឋាន។"], .65)
    # change matrix
    f = Fig(1000, 460).title("ម៉ាទ្រីសការផ្លាស់ប្ដូរ ១៩៩៧ → ២០១៥ (ហិកតា)")
    from collections import defaultdict
    M = defaultdict(float)
    for l in LOSS: M[l["properties"].get("to", "?")] += l["properties"].get("ha", 0)
    items = sorted(M.items(), key=lambda kv: -kv[1])[:6]; mx = max(v for k, v in items)
    for i, (k, v) in enumerate(items):
        y = 110 + i * 50; f.text(60, y + 20, "ព្រៃ → " + str(k), 16); f.rect(420, y + 2, v / mx * 460, 28, "#e53935"); f.text(430 + v / mx * 460, y + 22, khn(v), 14)
    entry(11, f.save("g11-change-matrix"), "ព្រៃប្ដូរទៅជាអ្វី?",
          ["តារាងការផ្លាស់ប្ដូរប្រាប់ «ពី → ទៅ» និងទំហំ។", "ផ្ទៃធំបំផុតប្ដូរទៅជាដីកសិកម្ម ឬវាលស្មៅ/គុម្ពោត។", "ធ្វើពី Intersect នៃ lc1997 និង lc2015 រួច Group by ប្រភេទ។"], .85)

def L12():
    z = np.array(TERRAIN["z"]); n = z.shape[0]
    def img(A, name, pal, vmin=None, vmax=None):
        vmin = A.min() if vmin is None else vmin; vmax = A.max() if vmax is None else vmax
        P = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in pal], np.uint8); t = np.clip(((A - vmin) / (vmax - vmin + 1e-9) * len(pal)).astype(int), 0, len(pal) - 1)
        Image.fromarray(P[t]).resize((280, 280), Image.NEAREST).save(os.path.join(IMGDIR, name))
    GR = ["#1a9641", "#a6d96a", "#ffffbf", "#fdae61", "#d7191c"]
    # map algebra local op
    f = Fig(1000, 440).title("ពីជគណិតផែនទី៖ ប្រតិបត្តិការមូលដ្ឋាន (local)")
    A = np.array([[2, 3, 5], [1, 4, 6], [0, 2, 7]]); B = np.array([[1, 1, 0], [0, 1, 1], [1, 0, 1]])
    for k, (M, t) in enumerate([(A, "កម្ពស់ (A)"), (B, "ស្រែ (B)"), (A * B, "A × B")]):
        x0 = 60 + k * 320
        for i in range(3):
            for j in range(3): f.rect(x0 + j * 70, 110 + i * 70, 70, 70, "#e0f2f1" if k < 2 else "#ffe0b2", "#fff", 2); f.text(x0 + j * 70 + 35, 110 + i * 70 + 45, kh(M[i, j]), 22, INK, "middle", "bold")
        f.text(x0 + 105, 360, t, 17, IND, "middle", "bold")
        if k < 2: f.text(x0 + 255, 220, "×" if k == 0 else "=", 34, "#ff7043", "middle", "bold")
    entry(12, f.save("g12-local"), "Raster Calculator ក្រឡាទល់ក្រឡា",
          ["ក្រឡានីមួយៗនៃលទ្ធផល គណនាពីក្រឡានៅទីតាំងដូចគ្នា។", "គុណដោយរ៉ាស្ទ័រ ០/១ (mask) រក្សាតែតំបន់ដែលចាប់អារម្មណ៍។", "រ៉ាស្ទ័រទាំងអស់ត្រូវមានទំហំក្រឡា វិសាលភាព និង CRS ដូចគ្នា។"], .1)
    # focal
    f = Fig(1000, 440).title("ប្រតិបត្តិការជិតខាង (focal)៖ មធ្យម ៣ × ៣")
    img(z, "g12-orig.png", GR); from scipy.ndimage import uniform_filter
    img(uniform_filter(z, 7), "g12-focal.png", GR, z.min(), z.max())
    f.add('<image href="../assets/img/slides/g12-orig.png" x="80" y="90" width="280" height="280"/>'); f.add('<image href="../assets/img/slides/g12-focal.png" x="560" y="90" width="280" height="280"/>')
    f.line(390, 230, 530, 230, "#607d8b", 3, arrow=True); f.text(460, 215, "ផ្ទៃ ៧ × ៧", 14, "#607d8b", "middle")
    f.text(220, 400, "ដើម", 16, IND, "middle", "bold"); f.text(700, 400, "រលោង (focal mean)", 16, IND, "middle", "bold")
    entry(12, f.save("g12-focal"), "Focal៖ ក្រឡា និងអ្នកជិតខាង",
          ["តម្លៃថ្មី = ស្ថិតិនៃក្រឡាក្នុងបង្អួចជុំវិញ។", "ប្រើសម្រាប់រលោង ជម្រាល រកគែម។", "បង្អួចធំ → រលោងច្រើន ប៉ុន្តែបាត់លម្អិត។"], .3)
    # reclass
    f = Fig(1000, 440).title("ចាត់ថ្នាក់ឡើងវិញ (Reclassify)")
    img(z, "g12-orig2.png", GR); rc = np.digitize(z, [80, 160, 240]).astype(float); img(rc, "g12-reclass.png", ["#e3f2fd", "#90caf9", "#1e88e5", "#0d47a1"], 0, 3)
    f.add('<image href="../assets/img/slides/g12-orig2.png" x="60" y="90" width="280" height="280"/>'); f.add('<image href="../assets/img/slides/g12-reclass.png" x="420" y="90" width="280" height="280"/>')
    for i, t in enumerate(["០–៨០ ម → ១", "៨០–១៦០ → ២", "១៦០–២៤០ → ៣", "> ២៤០ → ៤"]): f.rect(740, 130 + i * 50, 24, 24, ["#e3f2fd", "#90caf9", "#1e88e5", "#0d47a1"][i]); f.text(775, 150 + i * 50, t, 16)
    entry(12, f.save("g12-reclass"), "Reclassify",
          ["បម្លែងតម្លៃបន្តទៅជាថ្នាក់ដែលមានន័យ។", "ជំហានចាំបាច់មុន MCDA (មេរៀនទី១៤)។", "ពិនិត្យព្រំថ្នាក់៖ តម្លៃ ៨០ ធ្លាក់ថ្នាក់ណា?"], .5)
    # NoData
    f = Fig(1000, 400).title("NoData ក្នុងការគណនា")
    vals = [[5, 3, "∅"], [2, "∅", 4], [1, 6, 2]]
    for i in range(3):
        for j in range(3):
            v = vals[i][j]; f.rect(120 + j * 70, 110 + i * 70, 70, 70, "#eceff1" if v == "∅" else "#e0f2f1", "#fff", 2); f.text(155 + j * 70, 155 + i * 70, v if v == "∅" else kh(v), 22, "#e53935" if v == "∅" else INK, "middle", "bold")
    f.text(460, 170, "A + 10 → ∅ + 10 = ∅", 20, INK); f.text(460, 220, "មធ្យម focal៖ មិនរាប់ ∅", 20, INK); f.text(460, 270, "∅ ≠ ០ ៖ កុំជំនួសដោយសូន្យ", 20, "#e53935", weight="bold")
    entry(12, f.save("g12-nodata"), "NoData ឆ្លងកាត់ការគណនា",
          ["ក្រឡា NoData ផ្ដល់លទ្ធផល NoData ក្នុងប្រតិបត្តិការមូលដ្ឋាន។", "ពពកលើរូបភាពផ្កាយរណប ជាឧទាហរណ៍ NoData ទូទៅ។", "កំណត់តម្លៃ NoData ឲ្យត្រូវ មុនគណនា។"], .7)
    # NDVI from Landsat (real)
    try:
        import rasterio, math as mm
        se = mm.radians(51.56434261); rd = lambda b: (rasterio.open(f"{RD}/L8_Zone48n/L8_Zone48n/L8_B{b}.tif").read(1).astype(float)[520:900, 620:1060] * 2e-5 - .1) / mm.sin(se)
        red, nir = rd(4), rd(5); nd = (nir - red) / (nir + red + 1e-9)
        img(nd, "g12-ndvi.png", ["#a50026", "#f46d43", "#fee08b", "#a6d96a", "#1a9850"], -.2, .7)
        f = Fig(1000, 440).title("Raster Calculator ពិត៖ NDVI ពី Landsat 8", "(B5 − B4) / (B5 + B4)")
        if os.path.exists(os.path.join(IMGDIR, "g03-band4.jpg")):
            f.add('<image href="../assets/img/slides/g03-band4.jpg" x="30" y="100" width="260" height="225"/>'); f.add('<image href="../assets/img/slides/g03-band5.jpg" x="310" y="100" width="260" height="225"/>')
        f.add('<image href="../assets/img/slides/g12-ndvi.png" x="640" y="80" width="300" height="300"/>')
        f.text(160, 350, "B4 ក្រហម", 15, IND, "middle", "bold"); f.text(440, 350, "B5 NIR", 15, IND, "middle", "bold"); f.text(790, 405, "NDVI៖ បៃតង = រុក្ខជាតិ", 15, IND, "middle", "bold")
        entry(12, f.save("g12-ndvi"), "ពីជគណិតផែនទីលើរូបភាពពិត",
              ["NDVI គណនាក្រឡាទល់ក្រឡាពីក្រុមរលកពីរ។", "ទឹកមាន NDVI អវិជ្ជមាន · ទីក្រុងជិតសូន្យ · ដើមឈើខ្ពស់។", "រូបមន្តក្នុង QGIS៖ (\"B5@1\" - \"B4@1\") / (\"B5@1\" + \"B4@1\")។"], .9)
    except Exception as e: print("ndvi skipped", e)
    # distance raster
    f = Fig(1000, 460).title("រ៉ាស្ទ័រចម្ងាយ (Proximity)")
    hc_in = [h for h in HC if h["properties"].get("in_prov")]; Tp = geo_frame(PRV, (0, 0, 60, 60))
    gx, gy = np.meshgrid(np.arange(60) + .5, np.arange(60) + .5); pts = np.array([Tp(*h["geometry"]["coordinates"]) for h in hc_in])
    D = np.min(np.hypot(gx[..., None] - pts[:, 0], gy[..., None] - pts[:, 1]), -1) / Tp.scale_km
    img(D, "g12-dist.png", ["#004d40", "#26a69a", "#b2dfdb", "#fff3e0", "#ff7043"], 0, 15)
    f.add('<image href="../assets/img/slides/g12-dist.png" x="80" y="90" width="330" height="330"/>')
    f.legend_boxes(480, 150, ["#004d40", "#26a69a", "#b2dfdb", "#fff3e0", "#ff7043"], ["< ៣ គម", "៣–៦", "៦–៩", "៩–១២", "> ១២ គម"], "ចម្ងាយទៅមណ្ឌល")
    entry(12, f.save("g12-distance"), "ចម្ងាយជារ៉ាស្ទ័របន្ត",
          ["ក្រឡានីមួយៗរក្សាចម្ងាយទៅមណ្ឌលជិតបំផុត។", "អាចប្រើជាលក្ខខណ្ឌក្នុង MCDA។", "QGIS៖ Raster → Analysis → Proximity (Raster Distance)។"], .85)

def L13():
    z = np.array(TERRAIN["z"]); n = z.shape[0]
    gy, gx = np.gradient(z, 200.0); slope = np.degrees(np.arctan(np.hypot(gx, gy))); aspect = (np.degrees(np.arctan2(-gx, gy)) + 360) % 360
    def img(A, name, pal, vmin, vmax):
        P = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in pal], np.uint8); t = np.clip(((A - vmin) / (vmax - vmin + 1e-9) * len(pal)).astype(int), 0, len(pal) - 1)
        Image.fromarray(P[t]).resize((280, 280), Image.NEAREST).save(os.path.join(IMGDIR, name))
    img(slope, "g13-slope.png", ["#ffffcc", "#a1dab4", "#41b6c4", "#2c7fb8", "#253494"], 0, 12)
    img(aspect, "g13-aspect.png", ["#e53935", "#fb8c00", "#fdd835", "#43a047", "#1e88e5", "#3949ab", "#8e24aa", "#e53935"], 0, 360)
    hs = np.clip(np.sin(math.radians(45)) * np.cos(np.radians(slope)) + np.cos(math.radians(45)) * np.sin(np.radians(slope)) * np.cos(math.radians(315) - np.radians(aspect)), 0, 1)
    Image.fromarray((hs * 255).astype(np.uint8)).resize((280, 280)).save(os.path.join(IMGDIR, "g13-hs.png"))
    f = Fig(1000, 440).title("ផលិតផលពី DEM៖ ជម្រាល ទិស ស្រមោល")
    for i, (nm, t) in enumerate([("g13-slope.png", "ជម្រាល (ដឺក្រេ)"), ("g13-aspect.png", "ទិសជម្រាល"), ("g13-hs.png", "Hillshade")]):
        f.add(f'<image href="../assets/img/slides/{nm}" x="{40+i*320}" y="90" width="280" height="280"/>'); f.text(180 + i * 320, 400, t, 16, IND, "middle", "bold")
    entry(13, f.save("g13-derivatives"), "Terrain analysis",
          ["ជម្រាល៖ ល្បឿនប្ដូរកម្ពស់ · ទិស៖ ទិសដែលជម្រាលបែរទៅ។", "Hillshade៖ ពន្លឺសិប្បនិម្មិតសម្រាប់មើល មិនមែនសម្រាប់វាស់។", "DEM ត្រូវនៅ CRS ម៉ែត្រ ទើបជម្រាលត្រឹមត្រូវ។"], .8)
    # interpolation methods from sample points
    rng = np.random.default_rng(8); P = rng.uniform(3, 57, (25, 2)); V = np.array([z[int(y), int(x)] for x, y in P])
    gxx, gyy = np.meshgrid(np.arange(60), np.arange(60))
    def idw(pw):
        d = np.hypot(gxx[..., None] - P[:, 0], gyy[..., None] - P[:, 1]) + 1e-6; w = 1 / d ** pw; return (w * V).sum(-1) / w.sum(-1)
    from scipy.interpolate import griddata
    tin = griddata(P, V, (gxx, gyy), method="linear"); tin = np.where(np.isnan(tin), V.mean(), tin)
    GR = ["#1a9641", "#a6d96a", "#ffffbf", "#fdae61", "#d7191c"]
    img(z[:60, :60], "g13-truth.png", GR, z.min(), z.max()); img(idw(2), "g13-idw.png", GR, z.min(), z.max()); img(tin, "g13-tin.png", GR, z.min(), z.max())
    f = Fig(1000, 440).title("អាំងទែប៉ូឡាស្យុងពី ២៥ ចំណុច")
    for i, (nm, t) in enumerate([("g13-truth.png", "ផ្ទៃពិត"), ("g13-idw.png", "IDW (power ២)"), ("g13-tin.png", "TIN (លីនេអ៊ែរ)")]):
        x0 = 40 + i * 320; f.add(f'<image href="../assets/img/slides/{nm}" x="{x0}" y="90" width="280" height="280"/>')
        for x, y in P: f.circle(x0 + x * 280 / 60, 90 + y * 280 / 60, 3, "#212121")
        f.text(x0 + 140, 400, t, 16, IND, "middle", "bold")
    entry(13, f.save("g13-interp"), "ប្រៀបធៀបវិធីអាំងទែប៉ូឡាស្យុង",
          ["IDW បង្កើត «ពងៗ» ជុំវិញចំណុច ព្រោះទម្ងន់ផ្អែកលើចម្ងាយប៉ុណ្ណោះ។", "TIN ភ្ជាប់ចំណុចជាត្រីកោណ ហើយមិនលើសតម្លៃអតិបរមាដែលបានវាស់។", "គ្មានវិធីណាឃើញភ្នំដែលគ្មានចំណុចវាស់ទេ។"], .45)
    # cross validation plot
    f = Fig(1000, 440).title("Cross-validation៖ ទុកចំណុចមួយចេញ ហើយព្យាករ")
    pred = []
    for k in range(len(P)):
        m = np.ones(len(P), bool); m[k] = False; d = np.hypot(P[m, 0] - P[k, 0], P[m, 1] - P[k, 1]) + 1e-6; w = 1 / d ** 2; pred.append((w * V[m]).sum() / w.sum())
    X0, Y0, W = 120, 90, 300; mn, mx = V.min(), V.max()
    f.rect(X0, Y0, W, W, "#fafafa", "#cfd8dc"); f.line(X0, Y0 + W, X0 + W, Y0, "#90a4ae", 1, "5 4")
    for a, b in zip(V, pred): f.circle(X0 + (a - mn) / (mx - mn) * W, Y0 + W - (b - mn) / (mx - mn) * W, 5, "#26a69a", op=.8)
    rmse = math.sqrt(np.mean((np.array(pred) - V) ** 2)); f.text(X0 + W / 2, Y0 + W + 30, "តម្លៃវាស់", 14, INK, "middle"); f.text(X0 - 50, Y0 + W / 2, "ព្យាករ", 14, INK, "middle")
    f.text(520, 200, f"RMSE ≈ {kh(round(rmse))} ម", 30, IND, weight="bold"); f.text(520, 250, "ចំណុចកាន់តែជិតខ្សែ ១:១ កាន់តែល្អ", 17, INK)
    entry(13, f.save("g13-cv"), "វាយតម្លៃលទ្ធផលអាំងទែប៉ូឡាស្យុង",
          ["ដកចំណុចមួយ ព្យាករវាពីចំណុចផ្សេង ហើយប្រៀបធៀប។", "RMSE ប្រាប់កំហុសមធ្យមជាឯកតាទិន្នន័យ។", "ប្រៀបធៀប power ឬវិធីផ្សេងៗ ដោយ RMSE។"], .65)
    # first law
    f = Fig(1000, 400).title("ក្បួនទីមួយនៃភូមិសាស្ត្រ (Tobler)")
    f.text(500, 150, "«អ្វីៗទាំងអស់ទាក់ទងគ្នា ប៉ុន្តែអ្វីដែលនៅជិត", 22, INK, "middle"); f.text(500, 190, "ទាក់ទងគ្នាច្រើនជាងអ្វីដែលនៅឆ្ងាយ»", 22, INK, "middle")
    xs = np.linspace(0, 1, 40); f.path("M" + " L".join(f"{150 + x * 700:.1f} {360 - 110 * math.exp(-4 * x):.1f}" for x in xs), "none", IND, 3)
    f.text(150, 385, "ចម្ងាយ →", 14, "#607d8b"); f.text(140, 250, "ភាពស្រដៀង", 14, "#607d8b", "end")
    entry(13, f.save("g13-tobler"), "ហេតុអ្វីអាំងទែប៉ូឡាស្យុងដំណើរការ",
          ["តម្លៃនៅចំណុចជិតៗ ស្រដៀងគ្នាជាងចំណុចឆ្ងាយ។", "IDW ប្រើគំនិតនេះដោយផ្ទាល់៖ ទម្ងន់ = ១ / ចម្ងាយ^p។", "បើទិន្នន័យមិនមានលំនាំលំហ អាំងទែប៉ូឡាស្យុងគ្មានន័យ។"], .2)

def L14():
    z = np.array(TERRAIN["z"]); gy, gx = np.gradient(z, 200.0); slope = np.degrees(np.arctan(np.hypot(gx, gy)))
    n = z.shape[0]; yy, xx = np.mgrid[0:n, 0:n]
    road = np.abs(yy - (20 + 0.3 * xx)) * .2; water = np.hypot(xx - 45, yy - 45) * .2
    def img(A, name, pal, vmin, vmax):
        P = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in pal], np.uint8); t = np.clip(((A - vmin) / (vmax - vmin + 1e-9) * len(pal)).astype(int), 0, len(pal) - 1)
        Image.fromarray(P[t]).resize((240, 240), Image.NEAREST).save(os.path.join(IMGDIR, name))
    SU = ["#d73027", "#fc8d59", "#fee08b", "#91cf60", "#1a9850"]
    s1 = np.clip(1 - slope / 10, 0, 1); s2 = np.clip(1 - road / 6, 0, 1); s3 = np.clip(1 - np.abs(water - 4) / 6, 0, 1)
    for A, nm in [(s1, "g14-f1.png"), (s2, "g14-f2.png"), (s3, "g14-f3.png")]: img(A, nm, SU, 0, 1)
    f = Fig(1000, 420).title("កត្តា (factors) បន្ទាប់ពីធ្វើឲ្យស្តង់ដារ ០–១")
    for i, (nm, t) in enumerate([("g14-f1.png", "ជម្រាលតិច = ល្អ"), ("g14-f2.png", "ជិតផ្លូវ = ល្អ"), ("g14-f3.png", "ចម្ងាយពីទឹក ~៨០០ ម = ល្អ")]):
        f.add(f'<image href="../assets/img/slides/{nm}" x="{60+i*310}" y="90" width="240" height="240"/>'); f.text(180 + i * 310, 360, t, 15, IND, "middle", "bold")
    f.legend_boxes(80, 385, SU, ["០", "", "", "", "១"], horizontal=True)
    entry(14, f.save("g14-factors"), "ធ្វើឲ្យកត្តាទាំងអស់មានមាត្រដ្ឋានដូចគ្នា",
          ["ជម្រាល (ដឺក្រេ) និងចម្ងាយ (ម) មិនអាចបូកគ្នាដោយផ្ទាល់ទេ។", "ធ្វើឲ្យស្តង់ដារ ០ = មិនសមស្រប · ១ = សមស្របបំផុត។", "ទម្រង់មុខងារ (លីនេអ៊ែរ ឬមានចំណុចល្អបំផុត) ជាការសម្រេចចិត្ត។"], .45)
    # constraint mask
    cons = (slope < 8) & (road > 1)
    img(cons.astype(float), "g14-cons.png", ["#424242", "#ffffff"], 0, 1)
    wsum = .5 * s1 + .3 * s2 + .2 * s3; res = np.where(cons, wsum, np.nan)
    img(np.nan_to_num(res, nan=0), "g14-result.png", ["#616161"] + SU, 0, 1)
    f = Fig(1000, 440).title("ការបញ្ចូលគ្នា៖ Constraint × Σ(ទម្ងន់ × កត្តា)")
    f.add('<image href="../assets/img/slides/g14-cons.png" x="60" y="90" width="240" height="240"/>'); f.text(180, 360, "Constraint (០/១)", 15, IND, "middle", "bold")
    f.text(340, 215, "×", 40, "#ff7043", "middle", "bold")
    f.rect(390, 110, 220, 200, BG, rx=10); f.text(500, 160, "០,៥ × ជម្រាល", 17, INK, "middle"); f.text(500, 200, "+ ០,៣ × ផ្លូវ", 17, INK, "middle"); f.text(500, 240, "+ ០,២ × ទឹក", 17, INK, "middle")
    f.text(650, 215, "=", 40, "#ff7043", "middle", "bold")
    f.add('<image href="../assets/img/slides/g14-result.png" x="700" y="90" width="240" height="240"/>'); f.text(820, 360, "សមស្របភាព", 15, IND, "middle", "bold")
    entry(14, f.save("g14-combine"), "Weighted linear combination",
          ["Constraint កាត់តំបន់ដែលមិនអាចទទួលយកបាន (ពណ៌ប្រផេះ)។", "ទម្ងន់បូកគ្នា = ១ ហើយត្រូវយល់ព្រមជាមួយអ្នកពាក់ព័ន្ធ។", "លទ្ធផលជាពិន្ទុ ០–១ មិនមែនជាចម្លើយ «បាទ/ទេ» ទេ។"], .7)
    # sensitivity: two weight sets
    w2 = np.where(cons, .2 * s1 + .3 * s2 + .5 * s3, np.nan); img(np.nan_to_num(w2, nan=0), "g14-sens.png", ["#616161"] + SU, 0, 1)
    f = Fig(1000, 440).title("ការវិភាគភាពរសើបនៃទម្ងន់")
    f.add('<image href="../assets/img/slides/g14-result.png" x="120" y="90" width="260" height="260"/>'); f.add('<image href="../assets/img/slides/g14-sens.png" x="600" y="90" width="260" height="260"/>')
    f.text(250, 380, "ជម្រាល ០,៥ · ផ្លូវ ០,៣ · ទឹក ០,២", 15, IND, "middle", "bold"); f.text(730, 380, "ជម្រាល ០,២ · ផ្លូវ ០,៣ · ទឹក ០,៥", 15, IND, "middle", "bold")
    entry(14, f.save("g14-sensitivity"), "ទម្ងន់ប្ដូរ → ទីតាំងល្អបំផុតប្ដូរ",
          ["ប្ដូរទម្ងន់ ហើយមើលថាតំបន់ពណ៌បៃតងនៅដដែល ឬផ្លាស់ទី។", "តំបន់ដែលល្អគ្រប់សេណារីយ៉ូ ជាជម្រើសដែលរឹងមាំ។", "រាយការណ៍ទម្ងន់ និងលទ្ធផលភាពរសើបជានិច្ច។"], .88)
    # workflow
    f = Fig(1000, 380).title("ជំហាន MCDA")
    st = ["គោលដៅ", "Constraint", "Factor", "ស្តង់ដារ", "ទម្ងន់", "បញ្ចូលគ្នា", "ភាពរសើប"]
    for i, t in enumerate(st):
        x = 20 + i * 140; f.rect(x, 150, 125, 70, QUAL[i % 8], rx=10); f.text(x + 62, 192, t, 16, "#fff", "middle", "bold")
        if i < 6: f.line(x + 127, 185, x + 138, 185, "#607d8b", 2, arrow=True)
    entry(14, f.save("g14-workflow"), "ដំណើរការ MCDA ប្រាំពីរជំហាន",
          ["ចាប់ផ្ដើមពីសំណួរ៖ «ទីតាំងណាសមស្របសម្រាប់...?»", "Constraint = ច្បាប់ដាច់ខាត · Factor = កម្រិតល្អ/អាក្រក់។", "ជំហានចុងក្រោយ៖ ពិនិត្យនៅទីវាល និងជាមួយអ្នកពាក់ព័ន្ធ។"], .1)

def L15():
    f = Fig(1000, 480).title("រចនាសម្ព័ន្ធថតគម្រោង")
    tree = ["📁 kampong_health_2025/", "   📄 project.qgz", "   📁 data/", "      📁 raw/  (មិនកែ)", "      📁 processed/", "   📁 scripts/  (models, python)", "   📁 outputs/  (maps, tables)", "   📄 README.md", "   📄 metadata.xlsx"]
    for i, t in enumerate(tree): f.text(80, 110 + i * 38, t, 18, INK if i else IND, weight="bold" if i == 0 else "normal", extra='font-family="monospace"')
    f.text(600, 150, "✓ ឈ្មោះគ្មានដកឃ្លា", 17); f.text(600, 190, "✓ raw មិនដែលកែ", 17); f.text(600, 230, "✓ ផ្លូវ relative", 17); f.text(600, 270, "✓ README ពន្យល់ជំហាន", 17)
    entry(15, f.save("g15-folders"), "រៀបចំគម្រោងមុនចាប់ផ្ដើម",
          ["ទិន្នន័យដើម (raw) រក្សាទុកមិនកែ ដើម្បីចាប់ផ្ដើមឡើងវិញបាន។", "ឈ្មោះឯកសារជាអក្សរឡាតាំង គ្មានដកឃ្លា៖ health_2025.gpkg។", "គម្រោងមួយថតតែមួយ ងាយផ្ញើ និងរក្សាទុក។"], .1)
    f = Fig(1000, 420).title("ផ្លូវ absolute ធៀបនឹង relative")
    f.rect(60, 120, 400, 180, "#ffebee", "#e57373", 2, 10); f.text(80, 170, "C:\\Users\\Dara\\Desktop\\", 17, INK, extra='font-family="monospace"'); f.text(80, 205, "   gis\\villages.gpkg", 17, INK, extra='font-family="monospace"'); f.text(260, 270, "✗ ខូចពេលផ្ញើទៅកុំព្យូទ័រផ្សេង", 16, "#c62828", "middle", "bold")
    f.rect(540, 120, 400, 180, "#e8f5e9", "#81c784", 2, 10); f.text(560, 190, "./data/villages.gpkg", 18, INK, extra='font-family="monospace"'); f.text(740, 270, "✓ ដំណើរការគ្រប់កន្លែង", 16, "#2e7d32", "middle", "bold")
    f.text(500, 370, "QGIS៖ Project → Properties → General → Save paths: Relative", 16, IND, "middle")
    entry(15, f.save("g15-paths"), "ផ្លូវ relative",
          ["ផ្លូវ absolute ចង្អុលទៅថតក្នុងកុំព្យូទ័រអ្នកម្នាក់។", "ផ្លូវ relative ចង្អុលពីទីតាំងគម្រោង ដូច្នេះផ្ញើថតទាំងមូលបាន។", "សញ្ញាស្រទាប់បាត់ (!) ពេលបើកគម្រោង ជាសញ្ញានៃផ្លូវខូច។"], .3)
    f = Fig(1000, 400).title("ភាពអាចធ្វើឡើងវិញបាន (reproducibility)")
    st = [("ទិន្នន័យដើម", "#6d4c41"), ("Model / Script", "#1e88e5"), ("លទ្ធផល", "#00897b"), ("របាយការណ៍", "#8e24aa")]
    for i, (t, c) in enumerate(st):
        x = 60 + i * 230; f.rect(x, 150, 190, 80, c, rx=12); f.text(x + 95, 197, t, 18, "#fff", "middle", "bold")
        if i < 3: f.line(x + 192, 190, x + 226, 190, "#607d8b", 3, arrow=True)
    f.text(500, 300, "ចុចម្ដងទៀត → លទ្ធផលដដែល · ទិន្នន័យថ្មី → ចុចម្ដងទៀត", 17, INK, "middle")
    entry(15, f.save("g15-reproducible"), "Graphical Modeler និង Script",
          ["រក្សាជំហានជា Model ជំនួសការចុចដោយដៃម្ដងមួយៗ។", "ពេលទិន្នន័យជំរឿនថ្មីចេញ ដំណើរការ Model ម្ដងទៀតភ្លាម។", "អ្នកផ្សេងអាចពិនិត្យ និងទុកចិត្តលទ្ធផល។"], .5)
    f = Fig(1000, 440).title("ចែករំលែកលទ្ធផល")
    ch = [("GeoPackage", "សម្រាប់អ្នក GIS", "#00897b"), ("PDF / PNG", "សម្រាប់អ្នកសម្រេចចិត្ត", "#1e88e5"), ("CSV / Excel", "តារាងស្ថិតិ", "#43a047"), ("Web map (qgis2web)", "សម្រាប់សាធារណៈ", "#8e24aa"), ("QGIS Cloud / GitHub", "រក្សាទុក និងកំណែ", "#6d4c41")]
    for i, (a, b, c) in enumerate(ch):
        y = 90 + i * 64; f.rect(80, y, 360, 50, c, rx=10); f.text(260, y + 32, a, 18, "#fff", "middle", "bold"); f.text(470, y + 32, b, 17, INK)
    entry(15, f.save("g15-sharing"), "ទម្រង់ត្រូវនឹងអ្នកទទួល",
          ["អ្នកសម្រេចចិត្តត្រូវការផែនទី និងសេចក្ដីសង្ខេប មិនមែនឯកសារ .gpkg ទេ។", "ភ្ជាប់មេតាទិន្នន័យ និងអាជ្ញាបណ្ណជាមួយរាល់ការចែករំលែក។", "ជៀសវាងចែកទិន្នន័យកម្រិតផ្ទះបុគ្គលដែលមានព័ត៌មានឯកជន។"], .7)
    f = Fig(1000, 400).title("ពេលវេលាគម្រោងបញ្ចប់វគ្គ (៤ សប្ដាហ៍)")
    wk = [("សប្ដាហ៍ ១", "សំណួរ · ទិន្នន័យ"), ("សប្ដាហ៍ ២", "រៀបចំ · គុណភាព"), ("សប្ដាហ៍ ៣", "វិភាគ · ផែនទី"), ("សប្ដាហ៍ ៤", "របាយការណ៍ · បង្ហាញ")]
    for i, (a, b) in enumerate(wk):
        x = 60 + i * 225; f.rect(x, 150, 205, 110, QUAL[i], rx=12); f.text(x + 102, 195, a, 18, "#fff", "middle", "bold"); f.text(x + 102, 230, b, 15, "#fff", "middle")
    entry(15, f.save("g15-timeline"), "ផែនការគម្រោង",
          ["ចំណាយពេលច្រើនលើការរៀបចំ និងពិនិត្យទិន្នន័យ (ជាទូទៅ ៥០–៦០%)។", "កំណត់សំណួរច្បាស់នៅសប្ដាហ៍ទី១ ហើយកុំប្ដូរ។", "ទុកពេលសម្រាប់បញ្ហាដែលមិនបានរំពឹង។"], .9)
