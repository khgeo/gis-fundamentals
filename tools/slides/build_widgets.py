"""Write docs/assets/js/gis-widgets.js from the template (embeds the terrain sample)."""
import json, os
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(H))
z = json.load(open(os.path.join(H, "data", "terrain_sample.json")))["z"]
t = open(os.path.join(H, "gis_widgets_template.js"), encoding="utf-8").read().replace("__TERRAIN__", json.dumps([[round(v) for v in r] for r in z], separators=(",", ":")))
open(os.path.join(ROOT, "docs", "assets", "js", "gis-widgets.js"), "w", encoding="utf-8").write(t); print("gis-widgets.js written")
