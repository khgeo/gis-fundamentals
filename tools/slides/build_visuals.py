"""Generate the Book 2 slide visuals and tools/slides/visuals.json (see BUILD.md)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vis_core, vis_gis_a, vis_gis_b, vis_gis_c
for mod, fns in ((vis_gis_a, ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08")), (vis_gis_b, ("L09", "L10", "L11", "L12", "L13", "L14", "L15")), (vis_gis_c, ("run",))):
    for fn in fns: getattr(mod, fn)()
W = [(9, "query-explorer", "ឧបករណ៍៖ សំណួរតាមគុណលក្ខណៈ និងចម្ងាយ", "ប្ដូរកម្រិតប្រជាជន និងចម្ងាយពីមណ្ឌលសុខភាព ហើយមើលភូមិដែលត្រូវបានជ្រើស។", .7),
     (10, "buffer-explorer", "ឧបករណ៍៖ បាហ្វ័រ និងការគ្របដណ្ដប់ប្រជាជន", "ប្ដូរចម្ងាយបាហ្វ័រ ហើយមើលភាគរយប្រជាជនដែលនៅក្នុងតំបន់សេវា។", .45),
     (3, "resolution-explorer", "ឧបករណ៍៖ ទំហំក្រឡារ៉ាស្ទ័រ", "ប្ដូរទំហំក្រឡា ហើយមើលថាកំពូល និងជ្រលងនៅតែមើលឃើញឬទេ។", .35),
     (12, "reclass-explorer", "ឧបករណ៍៖ Reclassify និង Raster Calculator", "ប្ដូរព្រំថ្នាក់កម្ពស់ និងជម្រាល ហើយមើលផ្ទៃដែលបំពេញលក្ខខណ្ឌ។", .6),
     (14, "weights-explorer", "ឧបករណ៍៖ ទម្ងន់ MCDA", "ប្ដូរទម្ងន់កត្តាទាំងបី ហើយមើលថាតំបន់សមស្របបំផុតផ្លាស់ទីយ៉ាងណា។", .8)]
for lesson, sim, title, instr, where in W:
    vis_core.MANIFEST.append(dict(lesson=lesson, sim=sim, title=title, bullets=[instr], where=where))
json.dump(vis_core.MANIFEST, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "visuals.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
n = sum(1 for m in vis_core.MANIFEST if "file" in m); print(f"{n} figures + {len(vis_core.MANIFEST)-n} widgets")
