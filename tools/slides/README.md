# Lesson slides (Book 2)

`build_slides.py` turns each lesson (`docs/lessons/lesson-XX.md`) into a full teaching deck
(`docs/slides/lesson-XX.html`, about 60–70 slides for a 3-hour lesson) and writes
`docs/slides/index.md`. Simulators and the five teaching widgets run live inside the slides.
The deploy workflow runs it automatically; edit the lessons, not the decks.

    python tools/slides/build_slides.py      # decks
    python tools/slides/build_widgets.py     # docs/assets/js/gis-widgets.js (from gis_widgets_template.js)
    python tools/slides/build_visuals.py     # 95 figures + visuals.json (needs shapely, scipy, matplotlib, Pillow)

Figures are committed, so CI only runs `build_slides.py`. Data: the book's lab data
(Kampong Chhnang villages, health centres, Koh Kong land cover), the Book 1 Cambodia datasets
and Natural Earth (public domain) in `tools/slides/data/`, and Landsat 8 imagery from Book 3
(optional; image panels are skipped when it is absent).

Keys in a deck: → / Space next · ← back · O overview · F fullscreen · N teacher notes · P print or PDF.
