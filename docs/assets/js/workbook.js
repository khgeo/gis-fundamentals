/* ============================================================
   Workbook tools: interactive lab maps and self-check boxes
   Fundamentals of GIS textbook (khgeo/gis-fundamentals)

   Requires Leaflet (loaded in mkdocs.yml extra_javascript).
   Works with Material's instant navigation via document$.

   1. LAB MAP
      <div class="lab-map" data-map="lab-10"></div>
      Layers for each lab are defined in LAB_MAPS below.
      Data paths are relative to the page, e.g. ../../assets/data/...

   2. SELF-CHECK
      Number:  <div class="self-check" data-min="139" data-max="141" markdown>question</div>
      Text:    <div class="self-check" data-answer="Peam Khnang" markdown>question</div>
      Optional data-hint="..." is shown after a wrong answer.
      Khmer digits (០–៩), spaces and commas are accepted in number answers.
      Answers are visible in the page source: this is for self-study
      feedback, not for graded assessment.
   ============================================================ */

(function () {
  "use strict";

  const KM_DIGITS = "០១២៣៤៥៦៧៨៩";
  const toKhmer = (n) => String(n).replace(/[0-9]/g, (d) => KM_DIGITS[d]);
  const fmt = (n) => toKhmer(Number(n).toLocaleString("en-US").replace(/,/g, " "));

  /* ---------------- Map definitions ---------------- */

  const LAB_MAPS = {
    "lab-10": {
      base: "../../assets/data/lab-10/",
      layers: [
        {
          file: "neighbours.geojson", name: "ខេត្តជិតខាង", on: true,
          style: { color: "#9e9e9e", weight: 1, fillColor: "#bdbdbd", fillOpacity: 0.25 },
          popup: (p) => `<b>${p.Name_KH}</b><br>${p.Name_EN}`,
        },
        {
          file: "buffer_5km.geojson", name: "បាហ្វ័រ ៥ គម ជុំវិញមណ្ឌលសុខភាព", on: true,
          style: { color: "#e65100", weight: 1, fillColor: "#ff9800", fillOpacity: 0.25 },
        },
        {
          file: "province.geojson", name: "ខេត្តកំពង់ឆ្នាំង", on: true, fit: true,
          style: { color: "#00695c", weight: 2.5, fill: false },
        },
        {
          file: "villages.geojson", name: "ភូមិ (ជំរឿន ២០០៨)", on: true,
          point: { radius: 3, color: "#1a237e", weight: 0.5, fillColor: "#3949ab", fillOpacity: 0.85 },
          popup: (p) =>
            `<b>${p.VILL_NAME}</b><br>លេខកូដ៖ ${p.VILL_CODE}<br>ប្រជាជន៖ ${fmt(p.TOTPOP)} នាក់`,
        },
        {
          file: "health_centres.geojson", name: "មណ្ឌលសុខភាព", on: true,
          point: (p) => ({
            radius: 6, color: "#ffffff", weight: 1.5,
            fillColor: p.in_prov ? "#c62828" : "#ef9a9a", fillOpacity: 1,
          }),
          popup: (p) =>
            `<b>${p.FACILITNAM}</b><br>ស្រុកប្រតិបត្តិ៖ ${p.ODNAME}<br>` +
            (p.in_prov ? "នៅក្នុងខេត្ត" : "នៅខេត្តជិតខាង"),
        },
      ],
      legend: [
        ["dot", "#c62828", "មណ្ឌលសុខភាពក្នុងខេត្ត"],
        ["dot", "#ef9a9a", "មណ្ឌលសុខភាពខេត្តជិតខាង"],
        ["dot-sm", "#3949ab", "ភូមិ"],
        ["box", "#ff9800", "ក្នុងចម្ងាយ ៥ គម"],
        ["line", "#00695c", "ព្រំខេត្តកំពង់ឆ្នាំង"],
      ],
    },
  };

  /* ---------------- Map builder ---------------- */

  async function buildMap(el) {
    if (el.dataset.ready) return;
    el.dataset.ready = "1";
    const cfg = LAB_MAPS[el.dataset.map];
    if (!cfg) { el.textContent = "រកមិនឃើញការកំណត់ផែនទី: " + el.dataset.map; return; }
    if (typeof L === "undefined") { el.textContent = "មិនអាចផ្ទុក Leaflet បានទេ។ សូមពិនិត្យអ៊ីនធឺណិត។"; return; }

    const map = L.map(el, { scrollWheelZoom: false });
    const osm = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 18, attribution: "© អ្នករួមចំណែក OpenStreetMap",
    }).addTo(map);
    const overlays = {};
    let fitBounds = null;

    for (const lyr of cfg.layers) {
      try {
        const url = new URL(cfg.base + lyr.file, window.location.href);
        const data = await (await fetch(url)).json();
        const gj = L.geoJSON(data, {
          style: lyr.style,
          pointToLayer: lyr.point
            ? (f, ll) => L.circleMarker(ll, typeof lyr.point === "function" ? lyr.point(f.properties) : lyr.point)
            : undefined,
          onEachFeature: lyr.popup ? (f, l) => l.bindPopup(lyr.popup(f.properties)) : undefined,
        });
        if (lyr.on) gj.addTo(map);
        overlays[lyr.name] = gj;
        if (lyr.fit) fitBounds = gj.getBounds();
      } catch (e) {
        console.error("Lab map layer failed:", lyr.file, e);
      }
    }

    map.fitBounds(fitBounds || [[10, 102], [14.7, 107.7]]);
    L.control.layers({ "OpenStreetMap": osm, "គ្មានផែនទីមូលដ្ឋាន": L.layerGroup() }, overlays, { collapsed: true }).addTo(map);
    L.control.scale({ metric: true, imperial: false }).addTo(map);

    if (cfg.legend) {
      const legend = L.control({ position: "bottomright" });
      legend.onAdd = () => {
        const d = L.DomUtil.create("div", "lab-map-legend");
        d.innerHTML = cfg.legend
          .map(([t, c, label]) => `<div><i class="lg-${t}" style="--c:${c}"></i>${label}</div>`)
          .join("");
        return d;
      };
      legend.addTo(map);
    }
    el.addEventListener("click", () => map.scrollWheelZoom.enable(), { once: true });
  }

  /* ---------------- Self-check ---------------- */

  const normNumber = (s) =>
    s.replace(/[០-៩]/g, (d) => KM_DIGITS.indexOf(d)).replace(/[\s,]/g, "");
  const normText = (s) => s.trim().toLowerCase().replace(/[^a-z0-9\u1780-\u17ff]/g, "");

  function buildCheck(box) {
    if (box.dataset.ready) return;
    box.dataset.ready = "1";
    const row = document.createElement("div");
    row.className = "sc-row";
    row.innerHTML =
      '<input type="text" class="sc-input" placeholder="ចម្លើយរបស់អ្នក" aria-label="ចម្លើយ">' +
      '<button type="button" class="md-button sc-button">ពិនិត្យ</button>' +
      '<span class="sc-result" role="status"></span>';
    box.appendChild(row);
    const input = row.querySelector(".sc-input");
    const out = row.querySelector(".sc-result");

    const check = () => {
      const raw = input.value;
      if (!raw.trim()) { out.textContent = ""; box.dataset.state = ""; return; }
      let ok = false, close = false;
      if (box.dataset.answer !== undefined) {
        ok = box.dataset.answer.split("|").some((a) => normText(a) === normText(raw));
      } else {
        const v = parseFloat(normNumber(raw));
        const min = parseFloat(box.dataset.min), max = parseFloat(box.dataset.max);
        if (isNaN(v)) { out.textContent = "សូមបញ្ចូលជាលេខ"; box.dataset.state = "bad"; return; }
        ok = v >= min && v <= max;
        const mid = (min + max) / 2;
        close = !ok && Math.abs(v - mid) <= Math.abs(mid) * 0.1;
      }
      box.dataset.state = ok ? "ok" : close ? "close" : "bad";
      out.textContent = ok
        ? "✓ ត្រឹមត្រូវ"
        : close
          ? "ជិតហើយ ពិនិត្យជំហានម្ដងទៀត"
          : "មិនទាន់ត្រឹមត្រូវ" + (box.dataset.hint ? " · " + box.dataset.hint : "");
    };
    row.querySelector(".sc-button").addEventListener("click", check);
    input.addEventListener("keydown", (e) => { if (e.key === "Enter") check(); });
  }

  /* ---------------- Init ---------------- */

  function init() {
    document.querySelectorAll(".lab-map").forEach(buildMap);
    document.querySelectorAll(".self-check").forEach(buildCheck);
  }

  if (typeof document$ !== "undefined") {
    document$.subscribe(init);          // Material instant navigation
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
