# Doremon.ai — Interactive Learning Pocket 🤖🐍

A free, static educational prototype with a friendly original robot teacher and interactive learning gadgets.

## Working features
- **Python Playground:** edit and run real Python code in the browser using Pyodide, with output, errors, stop button, 12-second timeout, and example programs.
- **Python Academy:** six guided lessons with hints and knowledge checks.
- **Python Challenge:** twelve multiple-choice questions with scoring and explanations.
- **Robot Teacher:** five prepared explanations for beginner topics.
- **Other gadgets:** Fraction Pizza, Planet Explorer, Story Spark, and Brain Boost.
- **Python source:** `python/quiz_engine.py` is a standalone 10-question terminal quiz; `examples/*.py` are runnable beginner programs.

## Run the website
Use a local static server such as `python3 -m http.server 8000` and open `http://localhost:8000`. Python execution requires internet access to download the Pyodide runtime from a CDN. Do not open the site directly as a `file://` URL because Web Workers may be blocked.

## Run the native Python quiz
```bash
python3 python/quiz_engine.py
```

## Publish
GitHub Pages: Settings → Pages → Deploy from a branch → main → /(root).

## Safety and scope
This is a prototype, not a generative AI teacher. Python runs in a disposable browser Web Worker with a 12-second timeout; it is **not** a hardened security sandbox for untrusted code. Avoid sensitive data and use adult supervision. No student accounts or personal data collection are implemented. A production children's app requires a dedicated security, accessibility, privacy, and parental-consent review.

The character is an original mascot, not an official Doraemon product.
