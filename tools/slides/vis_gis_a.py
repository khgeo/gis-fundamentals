from vis_core import *
import numpy as np
from PIL import Image
from shapely.geometry import shape, Point, mapping
RD = "/home/claude/realdata"
PRV = gj("lab-10/province.geojson")["features"]; VIL = gj("lab-10/villages.geojson")["features"]; HC = gj("lab-10/health_centres.geojson")["features"]
NB = gj("lab-10/neighbours.geojson")["features"]
C01 = gj("lab-01/communes.geojson")["features"]; R01 = gj("lab-01/roads.geojson")["features"]; S01 = gj("lab-01/schools.geojson")["features"]
H01 = gj("lab-01/health.geojson")["features"]; V01 = gj("lab-01/villages.geojson")["features"]; W01 = gj("lab-01/water.geojson")["features"]
def town(f, T, labels=False):
    draw_gj(f, C01, T, lambda x: "#f1f8e9", lambda x: "#9e9e9e", 1)
    draw_gj(f, W01, T, lambda x: "#bbdefb", lambda x: "#64b5f6", .8)
    for ft in R01:
        prim = "Primary" in str(ft["properties"].get("Type"))
        draw_gj(f, [ft], T, stroke=lambda x: "#c62828" if prim else "#8d6e63", sw=2.6 if prim else 1)
    for ft in S01: x, y = T(*ft["geometry"]["coordinates"]); f.rect(x - 5, y - 5, 10, 10, "#1565c0", "#fff", 1)
    for ft in H01: x, y = T(*ft["geometry"]["coordinates"]); f.circle(x, y, 6, "#fff", "#2e7d32", 2)
    for ft in V01: x, y = T(*ft["geometry"]["coordinates"]); f.circle(x, y, 2.5, "#ff7043")
    if labels:
        for ft in C01:
            c = shape(ft["geometry"]).representative_point(); x, y = T(c.x, c.y); f.text(x, y, ft["properties"]["COMNAME_KH"], 13, INK, "middle", "bold")

def L01():
    T = geo_frame(C01, (60, 80, 520, 460))
    # layer stack exploded
    f = Fig(1000, 560).title("ស្រទាប់ទិន្នន័យ GIS", "ក្រុងកំពង់ឆ្នាំង · ស្រទាប់ពិតពីលំហាត់ទី១")
    layers = [("ឃុំ (ផ្ទៃ)", C01, lambda x: "#f1f8e9", "#9e9e9e"), ("ទឹក (ផ្ទៃ)", W01, lambda x: "#bbdefb", "#64b5f6"), ("ផ្លូវ (បន្ទាត់)", R01, lambda x: "none", "#c62828"), ("សាលា · មណ្ឌលសុខភាព (ចំណុច)", S01 + H01, lambda x: "#1565c0", "#fff")]
    for i, (nm, fe, fl, st) in enumerate(layers):
        Ti = geo_frame(C01, (0, 0, 360, 170)); oy = 420 - i * 105; ox = 120 + i * 10
        g = Fig(360, 170, None); draw_gj(g, fe, Ti, fl, lambda x, st=st: st, 1.2, r=4)
        f.add(f'<g transform="translate({ox} {oy}) skewX(-35) scale(1 .55)"><rect width="360" height="170" fill="#fff" fill-opacity=".85" stroke="#b0bec5"/>{"".join(g.o)}</g>')
        f.text(560, oy + 55, nm, 17, IND, weight="bold"); f.line(520, oy + 50, 555, oy + 50, "#b0bec5", 1)
    f.source("ទិន្នន័យលំហាត់ទី១ · ក្រសួង និងទិន្នន័យបើកចំហ")
    entry(1, f.save("g01-layer-stack"), "GIS រៀបចំពិភពលោកជាស្រទាប់",
          ["ស្រទាប់នីមួយៗមានប្រធានបទតែមួយ៖ ឃុំ ទឹក ផ្លូវ សាលា។", "ស្រទាប់ទាំងអស់មានប្រព័ន្ធកូអរដោនេដូចគ្នា ទើបត្រួតគ្នាបាន។", "ការវិភាគកើតឡើងពេលយើងសួរសំណួររវាងស្រទាប់ (ឧ. សាលាណានៅជិតផ្លូវធំ?)។"], .1)
    # full town map
    f = Fig(1000, 560).title("ផែនទីក្រុងកំពង់ឆ្នាំង ពីស្រទាប់ប្រាំមួយ")
    town(f, T, labels=True)
    lx = 640
    for i, (t, dr) in enumerate([("សាលារៀន", lambda y: f.rect(lx, y - 10, 12, 12, "#1565c0")), ("មណ្ឌលសុខភាព", lambda y: f.circle(lx + 6, y - 4, 6, "#fff", "#2e7d32", 2)), ("ភូមិ", lambda y: f.circle(lx + 6, y - 4, 3, "#ff7043")),
                                 ("ផ្លូវជាតិ", lambda y: f.line(lx, y - 4, lx + 16, y - 4, "#c62828", 3)), ("ផ្លូវផ្សេងៗ", lambda y: f.line(lx, y - 4, lx + 16, y - 4, "#8d6e63", 1.2)), ("ទឹក", lambda y: f.rect(lx, y - 10, 16, 12, "#bbdefb", "#64b5f6"))]):
        dr(160 + i * 36); f.text(lx + 26, 160 + i * 36, t, 16)
    entry(1, f.save("g01-town-map"), "ទិន្នន័យពិតក្នុង GIS",
          ["ផែនទីនេះមកពីស្រទាប់ទិន្នន័យដែលអ្នកនឹងប្រើក្នុងលំហាត់ទី១។", "ចំណុច បន្ទាត់ ផ្ទៃ នីមួយៗមានតារាងគុណលក្ខណៈភ្ជាប់មកជាមួយ។", "ផែនទីជាលទ្ធផលមួយរបស់ GIS មិនមែនជា GIS ទាំងមូលទេ។"], .2)
    # location + attribute
    f = Fig(1000, 520).title("ទីតាំង + គុណលក្ខណៈ = ទិន្នន័យលំហ")
    Tk = geo_frame(C01, (40, 90, 420, 400)); town(f, Tk)
    v = sorted(V01, key=lambda x: -x["properties"]["TOTPOP"])[:6]
    for i, ft in enumerate(v):
        x, y = Tk(*ft["geometry"]["coordinates"]); f.circle(x, y, 6, "none", "#e65100", 2); f.text(x + 8, y - 6, kh(i + 1), 13, "#e65100", weight="bold")
    heads = ["#", "VILL_NAME", "TOTPOP", "HH_TOT"]; xs = [520, 560, 760, 870]
    for j, h in enumerate(heads): f.text(xs[j], 120, h, 15, "#fff", weight="bold") if False else None
    f.rect(505, 100, 460, 32, IND)
    for j, h in enumerate(heads): f.text(xs[j], 122, h, 15, "#fff", weight="bold")
    for i, ft in enumerate(v):
        y = 160 + i * 38; p = ft["properties"]; f.rect(505, y - 24, 460, 36, BG if i % 2 else "#fff")
        for j, val in enumerate([kh(i + 1), p["VILL_NAME"], khn(p["TOTPOP"]), khn(p.get("HH_TOT") or 0)]): f.text(xs[j], y, val, 15)
    f.text(505, 420, "ជួរដេកមួយ = វត្ថុមួយលើផែនទី", 17, "#e65100", weight="bold")
    entry(1, f.save("g01-location-attribute"), "ទីតាំង និងគុណលក្ខណៈ",
          ["វត្ថុនីមួយៗមានទីតាំង (កូអរដោនេ) និងព័ត៌មាន (ឈ្មោះ ប្រជាជន គ្រួសារ)។", "ចុចលើចំណុច → ឃើញជួរដេក · ជ្រើសជួរដេក → ឃើញចំណុច។", "សំណួរ «នៅឯណា?» និង «អ្វី?» ឆ្លើយបានក្នុងពេលតែមួយ។"], .3)
    # spatial questions
    f = Fig(1000, 480).title("ប្រភេទសំណួរដែល GIS ឆ្លើយ")
    qs = [("ទីតាំង", "នៅឯណា?", "#00897b"), ("លក្ខខណ្ឌ", "កន្លែងណាមាន...?", "#1e88e5"), ("និន្នាការ", "ប្រែប្រួលយ៉ាងណា?", "#8e24aa"), ("លំនាំ", "មានលំនាំអ្វី?", "#f4511e"), ("គំរូ", "បើ... នឹងកើតអ្វី?", "#6d4c41")]
    for i, (a, b, c) in enumerate(qs):
        x = 40 + i * 190; f.rect(x, 130, 170, 200, c, rx=16); f.text(x + 85, 200, a, 22, "#fff", "middle", "bold"); f.text(x + 85, 250, b, 16, "#fff", "middle")
    f.text(500, 400, "ឧ. «ភូមិណាខ្លះនៅឆ្ងាយជាង ៥ គម ពីមណ្ឌលសុខភាព?» = សំណួរលក្ខខណ្ឌ", 16, INK, "middle")
    entry(1, f.save("g01-questions"), "សំណួរប្រាំប្រភេទ",
          ["សំណួរកាន់តែស្មុគស្មាញ ពីទីតាំងសាមញ្ញទៅគំរូព្យាករ។", "សំណួរល្អត្រូវមានទីតាំង វត្ថុ និងលក្ខខណ្ឌច្បាស់។", "មុនបើក QGIS សរសេរសំណួរជាប្រយោគមួយ។"], .6)
    # distance decay (villages vs nearest HC)
    hcs = [shape(h["geometry"]) for h in HC]; kmdeg = 111.32 * math.cos(math.radians(12.2))
    d = [min(shape(v["geometry"]).distance(h) for h in hcs) * 111 for v in VIL]
    f = Fig(1000, 460).title("ចម្ងាយពីភូមិទៅមណ្ឌលសុខភាពជិតបំផុត", "ខេត្តកំពង់ឆ្នាំង · ៥៦៨ ភូមិ")
    bins = np.arange(0, 22, 2); cnt = np.histogram(d, bins=bins)[0]; mx = cnt.max()
    for i, c in enumerate(cnt):
        x = 90 + i * 80; h = c / mx * 280; f.rect(x, 380 - h, 66, h, "#26a69a" if bins[i] < 5 else "#ef6c00"); f.text(x + 33, 372 - h, kh(c), 13, INK, "middle"); f.text(x + 33, 400, f"{kh(bins[i])}–{kh(bins[i+1])}", 12, "#607d8b", "middle")
    far = sum(1 for x in d if x > 5); f.text(620, 150, f"{kh(far)} ភូមិ ឆ្ងាយជាង ៥ គម", 22, "#ef6c00", weight="bold"); f.text(90, 435, "ចម្ងាយត្រង់ (គម)", 14, INK)
    entry(1, f.save("g01-distance-hist"), "ការគិតតាមលំហ៖ ចម្ងាយសំខាន់",
          ["ភាគច្រើននៃភូមិនៅក្នុងចម្ងាយ ៥ គម ពីមណ្ឌលសុខភាព។", "ប៉ុន្តែមានភូមិខ្លះនៅឆ្ងាយ ដែលត្រូវការការយកចិត្តទុកដាក់។", "ចម្ងាយត្រង់តិចជាងចម្ងាយផ្លូវពិត (មេរៀនទី១០)។"], .75)
    # province context
    f = Fig(1000, 540).title("ខេត្តកំពង់ឆ្នាំង និងខេត្តជិតខាង")
    Tp = geo_frame(NB + PRV, (40, 80, 600, 440)); draw_gj(f, NB, Tp, lambda x: "#eceff1", lambda x: "#b0bec5", 1); draw_gj(f, PRV, Tp, lambda x: "#b2dfdb", lambda x: IND, 2)
    for ft in NB:
        c = shape(ft["geometry"]).representative_point(); x, y = Tp(c.x, c.y); f.text(x, y, ft["properties"]["Name_KH"], 14, "#546e7a", "middle")
    for ft in VIL: x, y = Tp(*ft["geometry"]["coordinates"]); f.circle(x, y, 1.6, "#ff7043")
    for ft in HC:
        if ft["properties"].get("in_prov"): x, y = Tp(*ft["geometry"]["coordinates"]); f.circle(x, y, 4, "#fff", "#2e7d32", 1.6)
    f.text(680, 200, f"ភូមិ៖ {khn(len(VIL))}", 20, "#ff7043", weight="bold"); f.text(680, 240, f"មណ្ឌលសុខភាពក្នុងខេត្ត៖ {kh(sum(1 for h in HC if h['properties'].get('in_prov')))}", 18, "#2e7d32", weight="bold")
    f.text(680, 280, f"ប្រជាជនសរុប៖ {khn(sum(v['properties']['TOTPOP'] for v in VIL))}", 18, INK)
    entry(1, f.save("g01-province"), "តំបន់សិក្សារបស់វគ្គនេះ",
          ["លំហាត់ជាច្រើនប្រើខេត្តកំពង់ឆ្នាំង៖ ភូមិ មណ្ឌលសុខភាព ផ្លូវ។", "មណ្ឌលក្នុងខេត្តជិតខាងក៏សំខាន់ ព្រោះប្រជាជនមិនគោរពព្រំខេត្តពេលទៅព្យាបាល។", "នេះជាឧទាហរណ៍នៃ «ឥទ្ធិពលគែម» (មេរៀនទី១០)។"], .88)

def L02():
    T = geo_frame(C01, (40, 80, 440, 440))
    f = Fig(1000, 540).title("ធរណីមាត្របីប្រភេទ", "ចំណុច · បន្ទាត់ · ពហុកោណ")
    for i, (nm, fe, kind) in enumerate([("ចំណុច", S01 + H01 + V01, "pt"), ("បន្ទាត់", R01, "ln"), ("ពហុកោណ", C01 + W01, "pg")]):
        Ti = geo_frame(C01, (20 + i * 330, 90, 300, 330)); f.rect(20 + i * 330, 90, 300, 330, "#fafafa", "#e0e0e0")
        draw_gj(f, fe, Ti, lambda x: "#80cbc4" if kind == "pg" else "#00695c", lambda x: "#00695c", 1.4 if kind == "ln" else .8, r=3.5)
        f.text(170 + i * 330, 460, nm, 20, IND, "middle", "bold"); f.text(170 + i * 330, 488, ["សាលា មណ្ឌល ភូមិ", "ផ្លូវ", "ឃុំ ទឹក"][i], 15, "#607d8b", "middle")
    entry(2, f.save("g02-geometries"), "វត្ថុក្នុងពិភពពិត → ធរណីមាត្រ",
          ["ចំណុច៖ ទីតាំងមួយ (x, y) · បន្ទាត់៖ លំដាប់ចំណុច · ពហុកោណ៖ បន្ទាត់បិទ។", "ការជ្រើសធរណីមាត្រ អាស្រ័យលើមាត្រដ្ឋាន៖ សាលាអាចជាចំណុច ឬពហុកោណ។", "ស្រទាប់មួយមានធរណីមាត្រតែមួយប្រភេទ។"], .05)
    # vertices of a commune
    ft = C01[0]; g = shape(ft["geometry"]); ring = list((g.geoms[0] if hasattr(g, "geoms") else g).exterior.coords)
    f = Fig(1000, 520).title("ពហុកោណមួយ = បញ្ជីកូអរដោនេ", ft["properties"]["COMNAME_KH"])
    Ti = geo_frame([ft], (40, 80, 480, 420)); f.path("M" + " L".join("%.1f %.1f" % Ti(*q) for q in ring) + "Z", "#e0f2f1", IND, 1.5)
    for q in ring[::max(1, len(ring) // 40)]: x, y = Ti(*q); f.circle(x, y, 2.8, "#ff7043")
    f.text(560, 120, f"ចំនួនចំណុចកំពូល៖ {kh(len(ring))}", 18, INK, weight="bold")
    for i, q in enumerate(ring[:8]): f.text(560, 160 + i * 30, f"{kh(i+1)}.  {q[0]:.5f},  {q[1]:.5f}", 15, "#455a64", extra='font-family="monospace"')
    f.text(560, 420, "ចំណុចចុងក្រោយ = ចំណុចដំបូង (បិទ)", 15, "#e65100")
    entry(2, f.save("g02-vertices"), "រចនាសម្ព័ន្ធពហុកោណ",
          ["កុំព្យូទ័រមិនឃើញ «ឃុំ» ទេ ឃើញតែបញ្ជីលេខកូអរដោនេ។", "ចំណុចកំពូលកាន់តែច្រើន ព្រំកាន់តែលម្អិត និងឯកសារកាន់តែធំ។", "ចំណុចចុងក្រោយត្រូវស្មើចំណុចដំបូង ទើបពហុកោណបិទ។"], .15)
    # topology errors
    f = Fig(1000, 440).title("កំហុសឋានលេខាទូទៅ")
    errs = ["ចន្លោះ (gap)", "ជាន់គ្នា (overlap)", "ខ្សែអណ្ដែត (dangle)", "ខ្សែមិនប៉ះ (undershoot)"]
    for i, e in enumerate(errs):
        x = 30 + i * 245; f.rect(x, 90, 225, 230, "#fafafa", "#e0e0e0")
        if i == 0: f.path(f"M{x+20} 120 L{x+110} 120 L{x+105} 290 L{x+20} 290Z", "#b2dfdb", IND); f.path(f"M{x+118} 120 L{x+205} 120 L{x+205} 290 L{x+112} 290Z", "#ffe0b2", "#e65100"); f.rect(x + 104, 120, 14, 170, "#ffcdd2", op=None) if False else f.add(f'<path d="M{x+110} 120 L{x+118} 120 L{x+112} 290 L{x+105} 290Z" fill="#e53935"/>')
        if i == 1: f.rect(x + 20, 120, 110, 170, "#b2dfdb", IND); f.rect(x + 100, 120, 105, 170, "#ffe0b2", "#e65100", 1, extra='fill-opacity=".7"'); f.rect(x + 100, 120, 30, 170, "#e53935", extra='fill-opacity=".6"')
        if i == 2: f.line(x + 20, 200, x + 160, 200, "#546e7a", 3); f.line(x + 160, 110, x + 160, 300, "#546e7a", 3); f.line(x + 160, 200, x + 205, 200, "#e53935", 3); f.circle(x + 205, 200, 6, "#e53935")
        if i == 3: f.line(x + 20, 200, x + 145, 200, "#546e7a", 3); f.line(x + 160, 110, x + 160, 300, "#546e7a", 3); f.circle(x + 145, 200, 6, "#e53935")
        f.text(x + 112, 350, e, 16, INK, "middle", "bold")
    f.text(500, 410, "QGIS៖ Vector → Geometry Tools → Check Validity · Topology Checker", 15, IND, "middle")
    entry(2, f.save("g02-topology-errors"), "កំហុសឋានលេខា",
          ["ចន្លោះ និងជាន់គ្នា ធ្វើឲ្យផ្ទៃសរុបខុស និងការត្រួតស្រទាប់ខុស។", "ខ្សែអណ្ដែត ឬមិនប៉ះ ធ្វើឲ្យការវិភាគបណ្ដាញផ្លូវបរាជ័យ។", "កំណត់ snapping ពេលគូស ដើម្បីការពារកំហុសទាំងនេះ។"], .5)
    # multipart & holes (water polygons / province)
    pg = shape(PRV[0]["geometry"]); parts = list(pg.geoms) if hasattr(pg, "geoms") else [pg]
    f = Fig(1000, 480).title("ពហុវត្ថុ និងរន្ធ")
    Tp = geo_frame(PRV, (40, 80, 440, 380)); draw_gj(f, PRV, Tp, lambda x: "#b2dfdb", lambda x: IND, 1.2)
    f.text(260, 470, f"ខេត្តកំពង់ឆ្នាំង៖ {kh(len(parts))} ផ្នែក ក្នុងវត្ថុតែមួយ", 15, INK, "middle")
    f.path("M 600 120 L 940 120 L 940 400 L 600 400 Z M 700 200 L 840 200 L 840 320 L 700 320 Z", "#b2dfdb", IND, 2, extra='fill-rule="evenodd"')
    f.text(770, 265, "រន្ធ (បឹង)", 16, "#1565c0", "middle", "bold"); f.text(770, 440, "ពហុកោណដែលមានរន្ធ៖ ផ្ទៃ = ក្រៅ − ក្នុង", 15, INK, "middle")
    entry(2, f.save("g02-multipart"), "ពហុវត្ថុ (multipart) និងរន្ធ",
          ["ខេត្តដែលមានកោះ ឬដីដាច់ៗ រក្សាទុកជាវត្ថុមួយដែលមានផ្នែកច្រើន។", "រន្ធក្នុងពហុកោណ (ឧ. បឹងក្នុងឃុំ) មិនត្រូវរាប់បញ្ចូលផ្ទៃទេ។", "Multipart to Singleparts បំបែកផ្នែកនីមួយៗ ពេលត្រូវការ។"], .3)
    # file formats
    f = Fig(1000, 420).title("Shapefile ធៀបនឹង GeoPackage")
    files = [".shp  ធរណីមាត្រ", ".shx  លិបិក្រម", ".dbf  តារាង", ".prj  ប្រព័ន្ធកូអរដោនេ", ".cpg  ការអ៊ិនកូដ"]
    for i, t in enumerate(files): f.rect(60, 100 + i * 50, 320, 40, "#fff3e0", "#ffb74d"); f.text(76, 127 + i * 50, "📄 kampong" + t, 16, INK)
    f.rect(560, 100, 380, 240, "#e0f2f1", IND, 2, 14); f.text(750, 150, "📦 kampong.gpkg", 20, IND, "middle", "bold")
    for i, t in enumerate(["ស្រទាប់ច្រើនក្នុងឯកសារតែមួយ", "ឈ្មោះវាលវែង និងអក្សរខ្មែរ", "ទំហំលើស ២ GB", "រ៉ាស្ទ័រ និងរចនាប័ទ្មបាន"]): f.text(590, 195 + i * 36, "✓ " + t, 16)
    entry(2, f.save("g02-formats"), "ទម្រង់ឯកសារវ៉ិចទ័រ",
          ["Shapefile មានឯកសារយ៉ាងតិច ៣–៥ ដែលត្រូវនៅជាមួយគ្នា។", "ឈ្មោះវាល Shapefile មានត្រឹម ១០ តួអក្សរ ហើយមានបញ្ហាអក្សរខ្មែរ។", "GeoPackage ជាទម្រង់ស្តង់ដារ OGC ដែលណែនាំសម្រាប់វគ្គនេះ។"], .75)
    # simplification tolerance on commune
    f = Fig(1000, 420).title("ចំនួនចំណុចកំពូល និងភាពលម្អិត")
    gg = shape(PRV[0]["geometry"])
    for i, tol in enumerate([0, .002, .01, .03]):
        sg = gg.simplify(tol) if tol else gg; Ti = geo_frame(PRV, (20 + i * 245, 90, 220, 250))
        draw_gj(f, [{"geometry": mapping(sg)}], Ti, lambda x: "#b2dfdb", lambda x: IND, 1)
        n = sum(len(p.exterior.coords) for p in (sg.geoms if hasattr(sg, "geoms") else [sg])); f.text(130 + i * 245, 370, f"{khn(n)} ចំណុច", 16, IND, "middle", "bold")
    entry(2, f.save("g02-vertex-detail"), "ភាពលម្អិតមានតម្លៃ",
          ["ចំណុចច្រើន៖ ព្រំត្រឹមត្រូវ ប៉ុន្តែឯកសារធំ និងគណនាយឺត។", "ចំណុចតិច៖ លឿន ប៉ុន្តែផ្ទៃ និងបរិមាត្រខុសពីការពិត។", "ជ្រើសភាពលម្អិតឲ្យត្រូវនឹងមាត្រដ្ឋាន និងគោលបំណង។"], .88)

def L03():
    z = np.array(TERRAIN["z"]); n = z.shape[0]
    def ras(Z, name, pal):
        P = np.array([[int(c[i:i + 2], 16) for i in (1, 3, 5)] for c in pal], np.uint8); t = np.clip(((Z - Z.min()) / (np.ptp(Z) + 1e-9) * len(pal)).astype(int), 0, len(pal) - 1)
        Image.fromarray(P[t]).resize((300, 300), Image.NEAREST).save(os.path.join(IMGDIR, name))
    GR = ["#1a9641", "#a6d96a", "#ffffbf", "#fdae61", "#d7191c"]
    # resolutions
    f = Fig(1000, 440).title("គុណភាពបង្ហាញរ៉ាស្ទ័រ", "DEM ដូចគ្នា · ក្រឡា ២០០ ម · ៦០០ ម · ២ គម")
    for i, b in enumerate([1, 3, 10]):
        Zb = z[: n // b * b, : n // b * b].reshape(n // b, b, n // b, b).mean((1, 3)); ras(Zb, f"g03-res{i}.png", GR)
        f.add(f'<image href="../assets/img/slides/g03-res{i}.png" x="{30+i*325}" y="90" width="290" height="290"/>'); f.text(175 + i * 325, 410, ["២០០ ម · ៣ ៦៦០ ក្រឡា", "៦០០ ម · ៤០០ ក្រឡា", "២ គម · ៣៦ ក្រឡា"][i], 16, IND, "middle", "bold")
    entry(3, f.save("g03-resolution"), "ក្រឡាតូច = លម្អិតច្រើន",
          ["ក្រឡាតូចបង្ហាញជ្រលង និងកំពូលតូចៗ។", "ពង្រីកក្រឡា ៣ ដង → ចំនួនក្រឡាថយ ៩ ដង។", "គុណភាពបង្ហាញត្រូវសមនឹងសំណួរ៖ ស្រែមួយក្បាល ឬខេត្តទាំងមូល?"], .25)
    # cell grid values
    f = Fig(1000, 480).title("រ៉ាស្ទ័រ = ក្រឡាចត្រង្គ ដែលក្រឡានីមួយៗមានតម្លៃមួយ")
    sub = z[20:28, 20:28]
    for i in range(8):
        for j in range(8):
            v = sub[i, j]; t = (v - sub.min()) / np.ptp(sub); c = GR[min(4, int(t * 5))]
            f.rect(80 + j * 48, 90 + i * 48, 48, 48, c, "#fff", 1); f.text(104 + j * 48, 120 + i * 48, kh(int(v)), 12, INK, "middle")
    f.text(560, 150, "ជួរដេក × ជួរឈរ = ៨ × ៨", 18, INK); f.text(560, 190, "ក្រឡាមួយ = ២០០ ម × ២០០ ម", 18, INK); f.text(560, 230, "តម្លៃ = កម្ពស់ (ម)", 18, INK)
    f.text(560, 290, "ទីតាំងក្រឡា គណនាពី៖", 17, IND, weight="bold"); f.text(560, 322, "ជ្រុងឆ្វេងលើ + ជួរ × ទំហំក្រឡា", 17)
    entry(3, f.save("g03-cells"), "រចនាសម្ព័ន្ធក្រឡា",
          ["ក្រឡានីមួយៗមានតម្លៃតែមួយ (កម្ពស់ ប្រភេទដី សីតុណ្ហភាព)។", "រ៉ាស្ទ័រមិនរក្សាកូអរដោនេនីមួយៗទេ៖ ប្រើចំណុចដើម និងទំហំក្រឡា។", "តម្លៃក្រឡាជាមធ្យម ឬជាតម្លៃកណ្ដាល នៃផ្ទៃក្រឡា។"], .1)
    # types of raster: continuous / thematic / image
    f = Fig(1000, 440).title("ប្រភេទរ៉ាស្ទ័របី")
    ras(z, "g03-cont.png", GR); f.add('<image href="../assets/img/slides/g03-cont.png" x="30" y="90" width="290" height="290"/>')
    lc = np.digitize(z, [60, 120, 200]); P = np.array([[33, 150, 243], [139, 195, 74], [56, 142, 60], [141, 110, 99]], np.uint8)
    Image.fromarray(P[lc]).resize((300, 300), Image.NEAREST).save(os.path.join(IMGDIR, "g03-them.png")); f.add('<image href="../assets/img/slides/g03-them.png" x="355" y="90" width="290" height="290"/>')
    if os.path.exists(os.path.join(RD, "crop_true.png")):
        Image.open(os.path.join(RD, "crop_true.png")).convert("RGB").resize((300, 300)).save(os.path.join(IMGDIR, "g03-img.jpg"), quality=86)
        f.add('<image href="../assets/img/slides/g03-img.jpg" x="680" y="90" width="290" height="290"/>')
    for i, t in enumerate(["បន្ត៖ កម្ពស់ (ម)", "ប្រធានបទ៖ ប្រភេទដី", "រូបភាព៖ Landsat 8 ភ្នំពេញ"]): f.text(175 + i * 325, 410, t, 16, IND, "middle", "bold")
    entry(3, f.save("g03-types"), "រ៉ាស្ទ័របន្ត ប្រធានបទ និងរូបភាព",
          ["បន្ត៖ តម្លៃលេខគ្រប់ក្រឡា (កម្ពស់ ទឹកភ្លៀង)។", "ប្រធានបទ៖ លេខកូដប្រភេទ (១ = ទឹក ២ = ស្រែ...) មិនអាចបូកដកបាន។", "រូបភាព៖ ក្រុមរលកច្រើន (ក្រហម បៃតង ខៀវ...) ពីផ្កាយរណប ឬដ្រូន។"], .4)
    # vector vs raster same feature
    f = Fig(1000, 440).title("វ៉ិចទ័រ ធៀបនឹងរ៉ាស្ទ័រ៖ ទន្លេ និងផ្លូវតែមួយ")
    import math as m
    pts = [(60 + i * 8, 240 + 60 * m.sin(i / 7)) for i in range(50)]
    f.path("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts), "none", "#1e88e5", 6); f.line(60, 140, 460, 340, "#c62828", 3)
    f.text(260, 400, "វ៉ិចទ័រ៖ បន្ទាត់ច្បាស់ ត្រឹមត្រូវ", 16, IND, "middle", "bold")
    for gx in range(20):
        for gy in range(12):
            x0, y0 = 540 + gx * 20, 130 + gy * 20; cx, cy = x0 + 10, y0 + 10; c = "#fafafa"
            if min(abs(cy - (240 + 60 * m.sin((cx - 540) / 56))) for _ in [0]) < 12: c = "#64b5f6"
            if abs((cy - 140) - (cx - 540) * .5) < 10: c = "#e57373"
            f.rect(x0, y0, 20, 20, c, "#e0e0e0", .4)
    f.text(740, 400, "រ៉ាស្ទ័រ៖ ជណ្ដើរតាមក្រឡា", 16, IND, "middle", "bold")
    entry(3, f.save("g03-vector-raster"), "ជ្រើសគំរូទិន្នន័យ",
          ["វ៉ិចទ័រ៖ ល្អសម្រាប់វត្ថុដាច់ៗ ព្រំច្បាស់ ផ្លូវ ព្រំរដ្ឋបាល។", "រ៉ាស្ទ័រ៖ ល្អសម្រាប់បាតុភូតបន្ត និងរូបភាព។", "រ៉ាស្ទ័របង្ហាញខ្សែជាជណ្ដើរ ដែលអាស្រ័យលើទំហំក្រឡា។"], .6)
    # vector to raster conversion
    f = Fig(1000, 460).title("បំប្លែងពហុកោណទៅរ៉ាស្ទ័រ", "ក្រឡាដែលកណ្ដាលធ្លាក់ក្នុងពហុកោណ = ១")
    poly = [(120, 120), (380, 150), (420, 330), (200, 380), (90, 260)]
    from shapely.geometry import Polygon
    P = Polygon(poly); s = 30
    for gx in range(12):
        for gy in range(10):
            x0, y0 = 80 + gx * s, 100 + gy * s; inside = P.contains(Point(x0 + s / 2, y0 + s / 2))
            f.rect(x0 + 480, y0, s, s, "#26a69a" if inside else "#fafafa", "#cfd8dc", .5)
    f.path("M" + " L".join(f"{x} {y}" for x, y in poly) + "Z", "#b2dfdb", IND, 2); f.line(460, 250, 540, 250, "#607d8b", 3, arrow=True)
    f.text(250, 430, "ពហុកោណ", 16, IND, "middle", "bold"); f.text(740, 430, "រ៉ាស្ទ័រ (ក្រឡា ៣០ ភីកសែល)", 16, IND, "middle", "bold")
    entry(3, f.save("g03-rasterize"), "Rasterize",
          ["ក្រឡាដែលកណ្ដាលនៅក្នុងពហុកោណ ទទួលតម្លៃពហុកោណ។", "គែមពហុកោណក្លាយជាជណ្ដើរ ហើយផ្ទៃប្រែប្រួលតិចតួច។", "ក្រឡាកាន់តែតូច ផ្ទៃកាន់តែជិតនឹងពហុកោណដើម។"], .8)
    # bands of Landsat as rasters
    try:
        import rasterio, math as mm
        se = mm.radians(51.56434261)
        f = Fig(1000, 440).title("រូបភាពផ្កាយរណប = រ៉ាស្ទ័រច្រើនក្រុមរលក", "Landsat 8 · ភ្នំពេញ")
        for i, (b, nm) in enumerate([(2, "B2 ខៀវ"), (3, "B3 បៃតង"), (4, "B4 ក្រហម"), (5, "B5 NIR")]):
            a = rasterio.open(f"{RD}/L8_Zone48n/L8_Zone48n/L8_B{b}.tif").read(1).astype(float)[520:900, 620:1060]
            a = np.clip((a - np.percentile(a, 2)) / (np.percentile(a, 98) - np.percentile(a, 2)), 0, 1)
            Image.fromarray((a * 255).astype(np.uint8)).resize((220, 190)).save(os.path.join(IMGDIR, f"g03-band{b}.jpg"), quality=85)
            f.add(f'<image href="../assets/img/slides/g03-band{b}.jpg" x="{20+i*245}" y="100" width="225" height="195"/>'); f.text(132 + i * 245, 325, nm, 16, IND, "middle", "bold")
        f.text(500, 390, "ក្រុមរលកនីមួយៗជារ៉ាស្ទ័រមួយ · បន្សំបីជាពណ៌ · ទឹកងងឹតក្នុង NIR", 15, "#607d8b", "middle")
        entry(3, f.save("g03-bands"), "រូបភាពពហុក្រុមរលក",
              ["ក្រុមរលកនីមួយៗរក្សាពន្លឺក្នុងរលកចម្ងាយមួយ។", "ក្នុង NIR (B5) រុក្ខជាតិភ្លឺ ហើយទឹកងងឹត។", "វគ្គសៀវភៅទី៣ (Remote Sensing) សិក្សាលម្អិត។"], .5)
    except Exception as e: print("bands skipped", e)

def L04():
    # table ↔ map
    T = geo_frame(C01, (30, 90, 420, 400))
    f = Fig(1000, 520).title("តារាងគុណលក្ខណៈ និងផែនទី ភ្ជាប់គ្នា")
    town(f, T); sel = S01[:3]
    for ft in sel: x, y = T(*ft["geometry"]["coordinates"]); f.circle(x, y, 10, "none", "#ffeb3b", 3)
    heads = ["SCHOOL_NAM", "SCHOOL_TYP", "Location"]
    f.rect(480, 100, 490, 32, IND); [f.text(495 + j * 160, 122, h, 14, "#fff", weight="bold") for j, h in enumerate(heads)]
    for i, ft in enumerate(S01[:8]):
        y = 162 + i * 34; f.rect(480, y - 24, 490, 32, "#fff59d" if i < 3 else (BG if i % 2 else "#fff"))
        for j, h in enumerate(heads): f.text(495 + j * 160, y, str(ft["properties"].get(h)), 14)
    f.text(480, 460, "ជ្រើស ៣ ជួរដេក → បង្ហាញលឿងលើផែនទី", 16, "#e65100", weight="bold")
    entry(4, f.save("g04-table-map"), "ជួរដេក ↔ វត្ថុ",
          ["ជួរដេក = វត្ថុ · ជួរឈរ (វាល) = គុណលក្ខណៈ។", "ជ្រើសក្នុងតារាង ឬលើផែនទី ផ្ដល់លទ្ធផលដូចគ្នា។", "តារាងល្អ៖ វាលមួយមានព័ត៌មានតែមួយប្រភេទ។"], .1)
    # field types
    f = Fig(1000, 420).title("ប្រភេទវាល (field types)")
    ft_ = [("Integer", "TOTPOP = ១ ៦១៣", "#1e88e5"), ("Real / Double", "area_km2 = ៩,៣៨", "#00897b"), ("String / Text", "VILL_NAME = Phsar Leu", "#8e24aa"), ("Date", "survey = 2024-03-15", "#f4511e"), ("Boolean", "in_prov = true", "#6d4c41")]
    for i, (a, b, c) in enumerate(ft_):
        y = 95 + i * 60; f.rect(60, y, 240, 46, c, rx=8); f.text(180, y + 30, a, 18, "#fff", "middle", "bold"); f.text(330, y + 30, b, 18, INK, extra='font-family="monospace"')
    f.text(60, 410, "ប្រភេទខុស → គណនាមិនបាន (ឧ. ប្រជាជនរក្សាជាអក្សរ តម្រៀប «១០» មុន «៩»)", 15, "#c62828")
    entry(4, f.save("g04-field-types"), "ជ្រើសប្រភេទវាលឲ្យត្រូវ",
          ["ចំនួនគត់ (Integer) សម្រាប់រាប់ · ទសភាគ (Real) សម្រាប់ផ្ទៃ និងអត្រា។", "អក្សរ (String) សម្រាប់ឈ្មោះ និងលេខកូដ (លេខកូដភូមិ ០៤០១០១០១ ត្រូវរក្សាលេខ ០)។", "កាលបរិច្ឆេទត្រូវប្រើទម្រង់ YYYY-MM-DD។"], .3)
    # levels of measurement with real maps
    f = Fig(1000, 480).title("កម្រិតរង្វាស់បួន")
    lv = [("Nominal", "ប្រភេទផ្លូវ", "ឈ្មោះ លេខកូដ"), ("Ordinal", "ស្ថានភាពផ្លូវ", "ល្អ មធ្យម ខូច"), ("Interval", "សីតុណ្ហភាព °C", "គ្មានសូន្យពិត"), ("Ratio", "ប្រជាជន ផ្ទៃ", "មានសូន្យពិត · គុណចែកបាន")]
    for i, (a, b, c) in enumerate(lv):
        x = 30 + i * 245; f.rect(x, 100, 225, 270, [BG, "#fff3e0", "#e3f2fd", "#fce4ec"][i], rx=12)
        f.text(x + 112, 150, a, 22, IND, "middle", "bold"); f.text(x + 112, 200, b, 17, INK, "middle"); f.text(x + 112, 240, c, 14, "#607d8b", "middle")
        f.text(x + 112, 320, ["= ≠", "= ≠ < >", "= ≠ < > + −", "= ≠ < > + − × ÷"][i], 18, "#e65100", "middle", "bold")
    f.text(500, 430, "កម្រិតកំណត់ប្រតិបត្តិការ និងនិមិត្តសញ្ញាដែលអនុញ្ញាត", 16, INK, "middle")
    entry(4, f.save("g04-levels"), "កម្រិតរង្វាស់",
          ["Nominal៖ តែឈ្មោះ · Ordinal៖ មានលំដាប់ តែចន្លោះមិនស្មើ។", "Interval៖ ចន្លោះស្មើ តែគ្មានសូន្យពិត · Ratio៖ មានសូន្យពិត។", "មធ្យមនៃលេខកូដភូមិ (Nominal) គ្មានន័យ ទោះកុំព្យូទ័រគណនាបាន។"], .5)
    # NULL vs zero
    f = Fig(1000, 400).title("NULL ធៀបនឹង ០")
    f.rect(80, 110, 360, 200, "#e0f2f1", IND, 2, 12); f.text(260, 170, "០", 60, IND, "middle", "bold"); f.text(260, 240, "បានវាស់ ហើយតម្លៃគឺសូន្យ", 17, INK, "middle"); f.text(260, 275, "ឧ. ករណីជំងឺ = ០", 15, "#607d8b", "middle")
    f.rect(560, 110, 360, 200, "#fff3e0", "#ff7043", 2, 12); f.text(740, 170, "NULL", 44, "#ff7043", "middle", "bold"); f.text(740, 240, "មិនដឹង · មិនបានវាស់", 17, INK, "middle"); f.text(740, 275, "ឧ. ភូមិមិនបានរាយការណ៍", 15, "#607d8b", "middle")
    f.text(500, 360, "មធ្យម (៥, ០, NULL) = ២,៥ · មធ្យម (៥, ០, ០) = ១,៦៧", 17, "#c62828", "middle", "bold")
    entry(4, f.save("g04-null"), "តម្លៃបាត់",
          ["NULL មិនមែនសូន្យទេ៖ វាមានន័យថា «មិនដឹង»។", "ការជំនួស NULL ដោយ ០ ប្ដូរមធ្យម និងផែនទីទាំងស្រុង។", "QGIS៖ \"field\" IS NULL សម្រាប់រកតម្លៃបាត់។"], .7)
    # village population histogram
    pop = [v["properties"]["TOTPOP"] for v in VIL]
    f = Fig(1000, 440).title("ស្ថិតិវាល៖ ប្រជាជនក្នុងភូមិ", "ខេត្តកំពង់ឆ្នាំង · ៥៦៨ ភូមិ")
    bins = np.arange(0, 5500, 500); cnt = np.histogram(pop, bins=bins)[0]; mx = cnt.max()
    for i, c in enumerate(cnt): x = 80 + i * 78; h = c / mx * 260; f.rect(x, 360 - h, 66, h, "#4db6ac"); f.text(x + 33, 352 - h, kh(c), 12, INK, "middle"); f.text(x + 33, 380, kh(bins[i]), 11, "#607d8b", "middle")
    f.text(900, 140, f"មធ្យម៖ {khn(np.mean(pop))}", 17, INK, "end"); f.text(900, 170, f"មេដ្យាន៖ {khn(np.median(pop))}", 17, INK, "end"); f.text(900, 200, f"អតិបរមា៖ {khn(max(pop))}", 17, INK, "end")
    entry(4, f.save("g04-histogram"), "Basic Statistics for Fields",
          ["ភូមិភាគច្រើនមានប្រជាជន ៥០០–២ ០០០ នាក់។", "មធ្យមធំជាងមេដ្យាន ព្រោះភូមិធំៗមួយចំនួនទាញមធ្យមឡើង។", "ពិនិត្យអ៊ីស្តូក្រាមមុនជ្រើសវិធីចាត់ថ្នាក់ ឬកំណត់លក្ខខណ្ឌ។"], .88)

def L05():
    # join diagram
    f = Fig(1000, 460).title("ភ្ជាប់តារាងតាមវាលរួម (join)")
    f.rect(40, 100, 330, 220, BG, IND, 1.5, 10); f.text(205, 130, "ស្រទាប់ភូមិ", 18, IND, "middle", "bold")
    for i, (c, n) in enumerate([("04030101", "Phsar Leu"), ("04030102", "Phsar Kraom"), ("04030103", "Kandal")]): f.text(60, 170 + i * 40, c, 16, "#e65100", extra='font-family="monospace"'); f.text(200, 170 + i * 40, n, 16)
    f.rect(620, 100, 340, 220, "#fff3e0", "#ff7043", 1.5, 10); f.text(790, 130, "តារាងជំរឿន (CSV)", 18, "#e65100", "middle", "bold")
    for i, (c, v) in enumerate([("04030101", "៣ ១២៧"), ("04030103", "២ ២០៤"), ("04030102", "១ ៨៦៥")]): f.text(640, 170 + i * 40, c, 16, "#e65100", extra='font-family="monospace"'); f.text(820, 170 + i * 40, v, 16)
    for a, b in [(0, 0), (1, 2), (2, 1)]: f.line(330, 165 + a * 40, 632, 165 + b * 40, "#26a69a", 2, arrow=True)
    f.text(500, 380, "វាលភ្ជាប់ត្រូវមានតម្លៃ និងប្រភេទដូចគ្នា (អក្សរ ↔ អក្សរ)", 17, INK, "middle")
    entry(5, f.save("g05-join"), "ការភ្ជាប់តារាងតាមគុណលក្ខណៈ",
          ["លំដាប់ជួរដេកមិនសំខាន់ទេ៖ ការផ្គូផ្គងធ្វើតាមលេខកូដ។", "លេខកូដ «4030101» (លេខ) មិនផ្គូផ្គងនឹង «04030101» (អក្សរ) ទេ។", "ក្រោយភ្ជាប់ ពិនិត្យចំនួនជួរដេកដែលគ្មានគូ (NULL)។"], .2)
    # one-to-many
    f = Fig(1000, 440).title("មួយទល់មួយ ធៀបនឹងមួយទល់ច្រើន")
    f.rect(60, 110, 200, 60, "#b2dfdb", IND, 1.5, 8); f.text(160, 147, "ភូមិ A", 18, INK, "middle")
    f.rect(360, 110, 200, 60, "#ffe0b2", "#ff7043", 1.5, 8); f.text(460, 147, "ជំរឿន A", 18, INK, "middle"); f.line(262, 140, 356, 140, "#26a69a", 2.5, arrow=True)
    f.text(310, 210, "១ : ១", 22, IND, "middle", "bold")
    f.rect(60, 270, 200, 60, "#b2dfdb", IND, 1.5, 8); f.text(160, 307, "ឃុំ X", 18, INK, "middle")
    for i in range(4): f.rect(360 + i * 30, 250 + i * 20, 200, 44, "#ffe0b2", "#ff7043", 1, 8); f.line(262, 300, 356 + i * 30, 272 + i * 20, "#26a69a", 1.5)
    f.text(460 + 90, 250 + 3 * 20 + 30, "សាលា ៤", 16, INK, "middle"); f.text(310, 400, "១ : ច្រើន", 22, "#e65100", "middle", "bold")
    f.text(700, 180, "Join ធម្មតាយកតែគូដំបូង", 17, INK); f.text(700, 215, "→ បាត់ព័ត៌មាន", 17, "#c62828", weight="bold")
    f.text(700, 300, "ដំណោះស្រាយ៖ សរុប (count, sum)", 17, INK); f.text(700, 335, "ឬ Join attributes by location (summary)", 15, IND)
    entry(5, f.save("g05-one-many"), "ទំនាក់ទំនងរវាងតារាង",
          ["១:១ ឧ. ភូមិមួយ ↔ ជួរដេកជំរឿនមួយ។", "១:ច្រើន ឧ. ឃុំមួយ ↔ សាលាច្រើន៖ ត្រូវសរុបមុនភ្ជាប់។", "ច្រើន:១ ឧ. ភូមិច្រើន ↔ ឃុំតែមួយ៖ ភ្ជាប់ពីភូមិទៅឃុំ។"], .45)
    # count vs density map (provinces)
    f = Fig(1000, 480).title("ចំនួន ធៀបនឹងអត្រា", "Field Calculator៖ \"pop\" / \"area_km2\"")
    import vis_core as vc
    bp = sorted(p["pop"] for p in PROV["prov"]); qb = [bp[int(i * (len(bp) - 1) / 5)] for i in range(6)]
    c1 = lambda p: SEQ[min(4, sum(1 for b in qb[1:-1] if p["pop"] > b))]; c2 = classify(0, [0, 50, 100, 200, 400], SEQ)
    prov_map(f, 20, 90, 1.25, fill=c1, sw=.5); f.text(210, 420, "ប្រជាជនសរុប", 17, "#c62828", "middle", "bold")
    prov_map(f, 520, 90, 1.25, fill=lambda p: c2(p["dens"]), sw=.5); f.text(710, 420, "ដង់ស៊ីតេ (នាក់/គម²)", 17, "#2e7d32", "middle", "bold")
    entry(5, f.save("g05-count-rate"), "គណនាអត្រាដោយ Field Calculator",
          ["ផែនទីឆ្វេង៖ ខេត្តធំមើលទៅសំខាន់ ព្រោះមានផ្ទៃធំ។", "ផែនទីស្ដាំ៖ អត្រាធ្វើឲ្យប្រៀបធៀបបានត្រឹមត្រូវ។", "កន្សោម៖ \"TOTPOP\" / ($area / 1000000) បង្កើតដង់ស៊ីតេ។"], .8)
    # field calculator expressions visual
    f = Fig(1000, 440).title("កន្សោម Field Calculator ដែលប្រើញឹកញាប់")
    ex = [("$area / 10000", "ផ្ទៃ (ហិកតា) ក្នុង CRS ម៉ែត្រ"), ("\"TOTPOP\" / \"HH_TOT\"", "ទំហំគ្រួសារមធ្យម"), ("round(\"pct\", 1)", "បង្គត់ ១ ខ្ទង់ទសភាគ"),
          ("upper(\"COM_NAME\")", "អក្សរធំ"), ("CASE WHEN \"TOTPOP\" > 2000 THEN 'ធំ' ELSE 'តូច' END", "ចាត់ថ្នាក់")]
    for i, (a, b) in enumerate(ex):
        y = 100 + i * 60; f.rect(40, y, 560, 44, "#263238", rx=6); f.text(56, y + 29, a, 16, "#80cbc4", extra='font-family="monospace"'); f.text(620, y + 29, b, 17, INK)
    entry(5, f.save("g05-expressions"), "សរសេរកន្សោម",
          ["ឈ្មោះវាលក្នុងសញ្ញា \"ពីរ\" · អក្សរក្នុងសញ្ញា 'មួយ'។", "$area គណនាផ្ទៃតាម CRS៖ ប្រើ UTM 48N ដើម្បីបានម៉ែត្រការ៉េ។", "សាកល្បងលើជួរដេកតិចៗ (Preview) មុនអនុវត្តលើទាំងអស់។"], .6)
    # join mismatch report
    f = Fig(1000, 400).title("ពិនិត្យលទ្ធផលភ្ជាប់")
    vals = [("ភូមិសរុប", 568, IND), ("ផ្គូផ្គងបាន", 541, "#2e7d32"), ("គ្មានគូ (NULL)", 27, "#c62828")]
    for i, (t, v, c) in enumerate(vals): f.rect(80 + i * 290, 120, 250, 160, c, rx=14); f.text(205 + i * 290, 200, khn(v), 44, "#fff", "middle", "bold"); f.text(205 + i * 290, 250, t, 18, "#fff", "middle")
    f.text(500, 340, "ហេតុផលទូទៅ៖ ដកឃ្លាលើស · លេខ ០ បាត់ពីខាងមុខ · ភូមិថ្មី/បញ្ចូលគ្នា", 16, INK, "middle")
    f.text(500, 370, "(តួលេខជាឧទាហរណ៍)", 13, "#90a4ae", "middle")
    entry(5, f.save("g05-join-check"), "ការភ្ជាប់មិនដែលល្អឥតខ្ចោះទេ",
          ["រាប់ជួរដេកដែលគ្មានគូ រាល់ពេលភ្ជាប់។", "កែលេខកូដ មុនភ្ជាប់ម្ដងទៀត ជាជាងលុបជួរដេកចោល។", "សរសេរចំនួនជួរដេកដែលមិនផ្គូផ្គងក្នុងមេតាទិន្នន័យ។"], .9)

def L06():
    rng = np.random.default_rng(4)
    # GNSS scatter
    f = Fig(1000, 480).title("កំហុស GNSS៖ ទូរស័ព្ទ ធៀបនឹងឧបករណ៍ពិសេស")
    for i, (sd, nm, c) in enumerate([(4.0, "ទូរស័ព្ទ ~៣–៥ ម", "#ef6c00"), (.4, "GNSS ពិសេស (RTK) < ០,៥ ម", "#00897b")]):
        cx, cy = 250 + i * 500, 270; f.circle(cx, cy, 150, "none", "#cfd8dc"); f.circle(cx, cy, 75, "none", "#cfd8dc")
        f.text(cx + 150, cy + 16, "១០ ម", 12, "#90a4ae"); f.text(cx + 75, cy + 16, "៥ ម", 12, "#90a4ae")
        for _ in range(60): f.circle(cx + rng.normal(0, sd) * 15, cy + rng.normal(0, sd) * 15, 3, c, op=.7)
        f.circle(cx, cy, 5, "#212121"); f.text(cx, 460, nm, 17, c, "middle", "bold")
    entry(6, f.save("g06-gnss"), "ភាពត្រឹមត្រូវ GNSS",
          ["ទូរស័ព្ទធម្មតាផ្ដល់កំហុស ៣–៥ ម នៅទីវាល និងច្រើនជាងនៅក្បែរអគារ ឬដើមឈើ។", "ឧបករណ៍ RTK អាចត្រឹមត្រូវដល់សង់ទីម៉ែត្រ ប៉ុន្តែថ្លៃ។", "រង់ចាំ និងកត់មធ្យមនៃការវាស់ច្រើនដង ដើម្បីកាត់បន្ថយកំហុសចៃដន្យ។"], .45)
    # random vs bias
    f = Fig(1000, 440).title("កំហុសចៃដន្យ និងកំហុសលំអៀង")
    cases = [("ត្រឹមត្រូវ និងជាក់លាក់", 0, 0, .5), ("ជាក់លាក់ តែលំអៀង", 45, -30, .5), ("មិនជាក់លាក់ តែមិនលំអៀង", 0, 0, 2.5), ("អាក្រក់ទាំងពីរ", 40, 30, 2.5)]
    for i, (t, bx, by, sd) in enumerate(cases):
        cx, cy = 130 + i * 245, 230
        for r in (90, 60, 30): f.circle(cx, cy, r, ["#ffebee", "#ffcdd2", "#ef9a9a"][r // 30 - 1], "#e57373", .8)
        for _ in range(14): f.circle(cx + bx + rng.normal(0, sd) * 9, cy + by + rng.normal(0, sd) * 9, 4, "#1565c0")
        f.text(cx, 360, t, 15, INK, "middle", "bold")
    entry(6, f.save("g06-accuracy-precision"), "ភាពត្រឹមត្រូវ (accuracy) និងភាពជាក់លាក់ (precision)",
          ["ជាក់លាក់៖ ការវាស់ជិតគ្នា · ត្រឹមត្រូវ៖ ជិតតម្លៃពិត។", "កំហុសលំអៀង (ឧ. ដាតុមខុស) មិនបាត់ទេ ទោះវាស់ច្រើនដង។", "កំហុសចៃដន្យ ថយចុះពេលយកមធ្យម។"], .7)
    # data source timeline
    f = Fig(1000, 440).title("ប្រភពទិន្នន័យសំខាន់ៗសម្រាប់កម្ពុជា")
    src = [("ជំរឿន NIS", "ប្រជាជន ភូមិ ឃុំ", "#1e88e5"), ("OpenStreetMap", "ផ្លូវ អគារ POI", "#43a047"), ("Open Development Cambodia", "ព្រៃ សម្បទាន ដីធ្លី", "#8e24aa"), ("Sentinel / Landsat", "រូបភាពផ្កាយរណប", "#f4511e"), ("HDX / geoBoundaries", "ព្រំរដ្ឋបាល", "#6d4c41"), ("ការស្ទង់ផ្ទាល់", "GNSS · KoBo · QField", "#00897b")]
    for i, (a, b, c) in enumerate(src):
        x, y = 40 + (i % 3) * 315, 100 + (i // 3) * 150; f.rect(x, y, 290, 120, c, rx=12); f.text(x + 145, y + 52, a, 18, "#fff", "middle", "bold"); f.text(x + 145, y + 88, b, 15, "#fff", "middle")
    f.text(500, 420, "ពិនិត្យជានិច្ច៖ អាជ្ញាបណ្ណ · ឆ្នាំ · មាត្រដ្ឋាន · CRS", 16, INK, "middle")
    entry(6, f.save("g06-sources"), "ទិន្នន័យបន្ទាប់បន្សំ",
          ["ទិន្នន័យជាច្រើនអាចទាញយកឥតគិតថ្លៃ ប៉ុន្តែមានលក្ខខណ្ឌអាជ្ញាបណ្ណ។", "OSM គ្របដណ្ដប់ក្រុងល្អ ប៉ុន្តែជនបទខ្វះ។", "កត់ត្រាប្រភព និងកាលបរិច្ឆេទទាញយក ក្នុងមេតាទិន្នន័យ។"], .2)
    # form design
    f = Fig(1000, 480).title("ទម្រង់ប្រមូលទិន្នន័យល្អ (KoBo / QField)")
    f.rect(330, 80, 340, 380, "#263238", rx=28); f.rect(345, 110, 310, 320, "#fff", rx=6)
    fields = [("ឈ្មោះអណ្ដូង", "ជ្រើសពីបញ្ជី ▾"), ("ស្ថានភាព", "○ ដំណើរការ  ○ ខូច"), ("ជម្រៅ (ម)", "០–២០០"), ("រូបថត", "📷"), ("ទីតាំង GPS", "📍 ±៤ ម")]
    for i, (a, b) in enumerate(fields): f.text(360, 145 + i * 58, a, 14, IND, weight="bold"); f.rect(360, 152 + i * 58, 280, 26, BG, "#b2dfdb", 1, 4); f.text(370, 170 + i * 58, b, 13, "#455a64")
    for i, t in enumerate(["ជម្រើសជាបញ្ជី ជំនួសការវាយអក្សរ", "កំណត់ដែនតម្លៃ (០–២០០)", "ថតទីតាំង និងភាពត្រឹមត្រូវ", "រូបថតជាភស្តុតាង"]): f.text(700, 150 + i * 50, "✓ " + t, 16)
    entry(6, f.save("g06-form"), "រចនាទម្រង់ដើម្បីការពារកំហុស",
          ["បញ្ជីជ្រើសរើស ធ្វើឲ្យតម្លៃដូចគ្នា និងងាយវិភាគ។", "ដែនតម្លៃការពារការវាយខុស (ឧ. ជម្រៅ ២០០០ ម)។", "ថតភាពត្រឹមត្រូវ GPS ជាមួយចំណុចនីមួយៗ។"], .85)

def L07():
    # scanned map
    scan = os.path.join(DOCS, "assets/data/lab-07/kampong_chhnang_scan.jpg")
    if os.path.exists(scan):
        f = Fig(1000, 540).title("ផែនទីស្កេន៖ គ្មានកូអរដោនេ")
        f.add('<image href="../assets/data/lab-07/kampong_chhnang_scan.jpg" x="40" y="80" width="560" height="440" preserveAspectRatio="xMidYMid meet"/>')
        for i, (x, y) in enumerate([(120, 150), (520, 160), (140, 460), (500, 430)]): f.circle(x, y, 9, "none", "#e53935", 3); f.text(x + 12, y - 8, f"GCP {kh(i+1)}", 14, "#e53935", weight="bold")
        f.text(640, 170, "១. ជ្រើសចំណុចដែលស្គាល់", 17); f.text(640, 210, "   (ផ្លូវប្រសព្វ ស្ពាន ក្រឡា)", 15, "#607d8b"); f.text(640, 260, "២. បញ្ចូលកូអរដោនេពិត", 17); f.text(640, 310, "៣. ជ្រើសការបំប្លែង", 17); f.text(640, 360, "៤. ពិនិត្យ RMS", 17)
        entry(7, f.save("g07-scan"), "Georeferencing ផែនទីក្រដាស",
              ["រូបភាពស្កេនមានតែជួរដេក និងជួរឈរភីកសែល មិនមែនកូអរដោនេ។", "GCP ភ្ជាប់ភីកសែល (x, y) ទៅកូអរដោនេពិត (E, N)។", "ជ្រើស GCP នៅជ្រុងទាំងបួន និងកណ្ដាល។"], .1)
    # GCP spread good/bad
    f = Fig(1000, 440).title("ការចែកចាយ GCP")
    for i, pts in enumerate([[(0.1, .1), (.2, .15), (.15, .2), (.25, .12)], [(.08, .1), (.9, .1), (.1, .9), (.92, .88), (.5, .5), (.5, .1)]]):
        x0 = 60 + i * 480; f.rect(x0, 90, 380, 280, "#fafafa", "#b0bec5")
        for gx in range(1, 6): f.line(x0 + gx * 63, 90, x0 + gx * 63 + (18 if i == 0 else 3) * (gx % 2), 370, "#cfd8dc", 1)
        for (a, b) in pts: f.circle(x0 + a * 380, 90 + b * 280, 7, "#e53935")
        f.text(x0 + 190, 405, "ប្រមូលផ្ដុំជ្រុងមួយ → ខូចឆ្ងាយ" if i == 0 else "ចែកសព្វ → ស្ថិរភាព", 16, "#c62828" if i == 0 else "#2e7d32", "middle", "bold")
    entry(7, f.save("g07-gcp-spread"), "ដាក់ GCP ឲ្យសព្វ",
          ["GCP ប្រមូលផ្ដុំ ធ្វើឲ្យតំបន់ឆ្ងាយខូចទ្រង់ទ្រាយខ្លាំង។", "ចែកសព្វ រួមទាំងជ្រុងទាំងបួន។", "ទុក GCP ២–៣ ជាចំណុចពិនិត្យ (មិនប្រើក្នុងការគណនា)។"], .35)
    # transformation grids
    f = Fig(1000, 420).title("ការបំប្លែងបីកម្រិត")
    for i, nm in enumerate(["Linear/Helmert (៣ GCP)", "Affine / Polynomial 1 (៣+)", "Polynomial 2 (៦+)"]):
        x0 = 40 + i * 320
        for a in range(6):
            pts_h = [(x0 + b * 50, 110 + a * 45) for b in range(6)]; pts_v = [(x0 + a * 50, 110 + b * 45) for b in range(6)]
            def warp(x, y, i=i):
                u, v = (x - x0) / 250, (y - 110) / 225
                if i == 0: return x, y
                if i == 1: return x0 + (u + .25 * v) * 230, 110 + (v * .9 + .1 * u) * 225
                return x0 + (u + .15 * v * v) * 250, 110 + (v + .15 * u * u - .1 * u * v) * 225
            f.path("M" + " L".join("%.1f %.1f" % warp(*p) for p in pts_h), "none", IND, 1.2); f.path("M" + " L".join("%.1f %.1f" % warp(*p) for p in pts_v), "none", IND, 1.2)
        f.text(x0 + 125, 385, nm, 15, INK, "middle", "bold")
    entry(7, f.save("g07-transforms"), "ជ្រើសការបំប្លែង",
          ["Helmert៖ រំកិល បង្វិល និងពង្រីកស្មើ (រាងមិនប្ដូរ)។", "Affine៖ បន្ថែមការទ្រេត និងពង្រីកខុសគ្នាតាមអ័ក្ស។", "Polynomial 2+៖ ពត់ក្រឡា ប៉ុន្តែអាចខូចឆ្ងាយពី GCP។"], .5)
    # RMS residual arrows
    f = Fig(1000, 440).title("កំហុសសំណល់ (residual) និង RMS")
    rng = np.random.default_rng(3); res = []
    for i in range(8):
        x, y = 100 + rng.uniform(0, 440), 110 + rng.uniform(0, 260); dx, dy = rng.normal(0, 12, 2); res.append(math.hypot(dx, dy))
        f.circle(x, y, 5, "#1565c0"); f.line(x, y, x + dx * 3, y + dy * 3, "#e53935", 2, arrow=True)
    rms = math.sqrt(np.mean(np.square(res)))
    f.text(620, 160, "RMS = √(មធ្យម(សំណល់²))", 20, INK); f.text(620, 210, f"≈ {kh(round(rms/10, 1))} ភីកសែល", 22, "#e53935", weight="bold")
    f.text(620, 270, "គោលដៅ៖ < ទំហំភីកសែលមួយ", 17, "#607d8b"); f.text(620, 305, "លុប ឬកែ GCP ដែលមានព្រួញវែងខុសគេ", 17, "#607d8b")
    entry(7, f.save("g07-rms"), "វាយតម្លៃ Georeferencing",
          ["ព្រួញក្រហម៖ ភាពខុសគ្នារវាងទីតាំងដែលព្យាករ និងទីតាំងពិតនៃ GCP។", "RMS តូច មិនមែនមានន័យថាផែនទីត្រឹមត្រូវគ្រប់កន្លែងទេ។", "ពិនិត្យដោយចំណុចពិនិត្យឯករាជ្យ។"], .65)
    # snapping
    f = Fig(1000, 420).title("Snapping ពេលគូស")
    f.line(80, 220, 380, 220, "#546e7a", 3); f.line(400, 120, 400, 330, "#546e7a", 3); f.circle(380, 220, 6, "#e53935"); f.text(230, 370, "គ្មាន snapping៖ ខ្វះ ២០ ម", 16, "#c62828", "middle", "bold")
    f.line(580, 220, 900, 220, "#546e7a", 3); f.line(900, 120, 900, 330, "#546e7a", 3); f.circle(900, 220, 16, "none", "#26a69a", 2, ); f.circle(900, 220, 6, "#26a69a"); f.text(740, 370, "Snapping ១០ ភីកសែល៖ ភ្ជាប់ពិត", 16, "#2e7d32", "middle", "bold")
    entry(7, f.save("g07-snapping"), "ការពារចន្លោះ និងខ្សែអណ្ដែត",
          ["Snapping ទាញចំណុចថ្មីឲ្យភ្ជាប់នឹងចំណុច ឬខ្សែដែលមានស្រាប់។", "Tolerance ធំពេក ធ្វើឲ្យចំណុចលោតទៅកន្លែងខុស។", "QGIS៖ Project → Snapping Options (Vertex and segment, ១០ px)។"], .85)

def L08():
    # completeness map
    rng = np.random.default_rng(9)
    f = Fig(1000, 520).title("ភាពពេញលេញ៖ ភូមិដែលខ្វះទិន្នន័យ", "ឧទាហរណ៍បង្រៀន")
    Tp = geo_frame(PRV, (40, 80, 560, 420)); draw_gj(f, PRV, Tp, lambda x: "#f5f5f5", lambda x: "#90a4ae", 1.2)
    miss = 0
    for v in VIL:
        x, y = Tp(*v["geometry"]["coordinates"]); m = rng.random() < (.25 if x > 350 else .05); miss += m
        f.circle(x, y, 2.6, "#e53935" if m else "#26a69a")
    f.legend_boxes(650, 180, ["#26a69a", "#e53935"], ["មានទិន្នន័យ", "ខ្វះ (NULL)"]); f.text(650, 290, f"ខ្វះ {kh(miss)} ក្នុង {kh(len(VIL))} ភូមិ", 18, "#c62828", weight="bold")
    f.text(650, 330, "ការខ្វះមិនចៃដន្យ៖ ប្រមូលផ្ដុំខាងកើត", 16, INK)
    entry(8, f.save("g08-completeness"), "ភាពពេញលេញ",
          ["ទិន្នន័យខ្វះចៃដន្យ ប៉ះពាល់តិច ប៉ុន្តែខ្វះជាក្រុម បង្កើតលំអៀង។", "ផែនទីនៃទិន្នន័យខ្វះ ជួយរកបញ្ហាមុនវិភាគ។", "រាយការណ៍ភាគរយពេញលេញក្នុងមេតាទិន្នន័យ។"], .3)
    # positional error band
    f = Fig(1000, 420).title("កំហុសទីតាំងជាតំបន់មិនច្បាស់")
    f.line(100, 220, 900, 220, "#546e7a", 2); f.rect(100, 190, 800, 60, "#ffcc80", op=None) if False else f.add('<rect x="100" y="190" width="800" height="60" fill="#ffcc80" opacity=".5"/>')
    f.circle(520, 205, 8, "#1565c0"); f.text(530, 180, "សាលា", 15, "#1565c0", weight="bold")
    f.text(100, 290, "ផ្លូវ ± ១៥ ម (ពីរូបភាពចាស់)", 16, INK); f.text(100, 320, "សំណួរ៖ «សាលានៅក្នុង ១០ ម ពីផ្លូវឬទេ?» → ឆ្លើយមិនបានប្រាកដ", 16, "#c62828")
    entry(8, f.save("g08-positional"), "កំហុសកំណត់ចម្លើយ",
          ["ខ្សែលើផែនទីមានទំហំកំហុសមួយ ទោះបីមើលទៅស្ដើងក៏ដោយ។", "សំណួរដែលត្រូវការភាពជាក់លាក់ជាងកំហុស ឆ្លើយមិនបាន។", "ត្រូវដឹងកំហុសនៃស្រទាប់នីមួយៗ មុនធ្វើការត្រួតស្រទាប់។"], .5)
    # quality dimensions wheel
    f = Fig(1000, 480).title("ធាតុផ្សំប្រាំនៃគុណភាពទិន្នន័យ (ISO 19157)")
    dims = [("ទីតាំង", "ត្រឹមត្រូវប៉ុណ្ណា?"), ("គុណលក្ខណៈ", "តម្លៃត្រូវទេ?"), ("ពេញលេញ", "ខ្វះ ឬលើស?"), ("ស្របគ្នាតាមតក្កវិជ្ជា", "ឋានលេខា ច្បាប់"), ("ពេលវេលា", "ទាន់សម័យទេ?")]
    for i, (a, b) in enumerate(dims):
        ang = -math.pi / 2 + i * 2 * math.pi / 5; x, y = 500 + 170 * math.cos(ang), 270 + 170 * math.sin(ang)
        f.line(500, 270, x, y, "#b2dfdb", 2); f.circle(x, y, 62, QUAL[i], op=.9); f.text(x, y - 4, a, 15, "#fff", "middle", "bold"); f.text(x, y + 18, b, 12, "#fff", "middle")
    f.circle(500, 270, 50, IND); f.text(500, 276, "គុណភាព", 18, "#fff", "middle", "bold")
    entry(8, f.save("g08-dimensions"), "គុណភាពមានច្រើនវិមាត្រ",
          ["ទិន្នន័យអាចត្រឹមត្រូវទីតាំង ប៉ុន្តែហួសសម័យ។", "ភាពស្របគ្នាតាមតក្កវិជ្ជា៖ គ្មានចន្លោះ គ្មានជាន់គ្នា លេខកូដមិនស្ទួន។", "«សមស្របសម្រាប់គោលបំណង» ជាសំណួរចុងក្រោយ។"], .15)
    # metadata card
    f = Fig(1000, 480).title("មេតាទិន្នន័យ៖ ទិន្នន័យអំពីទិន្នន័យ")
    f.rect(200, 90, 600, 360, "#fff", IND, 2, 12); f.rect(200, 90, 600, 50, IND, rx=12); f.text(500, 123, "villages_kampong_chhnang.gpkg", 18, "#fff", "middle", "bold")
    rows = [("ចំណងជើង", "ភូមិខេត្តកំពង់ឆ្នាំង"), ("ប្រភព", "NIS · ជំរឿន ២០១៩"), ("CRS", "EPSG:32648 (UTM 48N)"), ("មាត្រដ្ឋាន/កំហុស", "១ : ៥០ ០០០ · ±២៥ ម"), ("ឆ្នាំ", "២០១៩"), ("អាជ្ញាបណ្ណ", "CC BY 4.0"), ("ទំនាក់ទំនង", "gis@example.org")]
    for i, (a, b) in enumerate(rows): f.text(230, 180 + i * 38, a, 16, IND, weight="bold"); f.text(420, 180 + i * 38, b, 16)
    entry(8, f.save("g08-metadata"), "មេតាទិន្នន័យ",
          ["គ្មានមេតាទិន្នន័យ = គ្មាននរណាដឹងថាអាចទុកចិត្តបានប៉ុណ្ណា។", "យ៉ាងតិច៖ ប្រភព ឆ្នាំ CRS ភាពត្រឹមត្រូវ អាជ្ញាបណ្ណ។", "QGIS៖ Layer Properties → Metadata រក្សាទុកក្នុង GeoPackage។"], .8)
