# RV.NEURAL — Personal AI Graph

This repository contains the **live interactive neural-network interface** for my GitHub profile.

It is not an SVG, screenshot, or static banner.

### Open the live interface

After enabling GitHub Pages for this repository:

**https://aarveewadhwa.github.io/rv-neural/**

Click the neurons to explore the systems I build:
- **TruthGraph** — explainable multi-agent fact verification
- **JOY** — multimodal AI therapist
- **Persona** — personalized safety navigation
- **Identif.ai** — forensic audio-to-3D face pipeline
- **LLM / RAG Core**
- **Computer Vision**

## Run locally

Open `index.html` directly in a browser, or run:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## GitHub Pages

Repository → **Settings** → **Pages** → Source: **Deploy from a branch** → `main` → `/ (root)` → Save.

The site is entirely client-side: HTML + CSS + JavaScript. No backend or GPU is required.
