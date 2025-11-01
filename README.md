# CartellinoStanze – Room Cards PDF Generator

Generates an A4 **PDF with room cards** (“cartellini”) showing:
- Room ID (large)
- Student names (1–2 lines)
- Housekeeping timetable (full + partial cleanings)

Built with **Python** and **ReportLab**. Data come from **two CSV files**.

---

## ✨ Features

- 📄 Output: `cartellini_stanze.pdf` (A4, **2 cards per page**, 1 per column)
- 👥 Supports 1 or 2 student names per room
- 🧹 Shows “Pulizia Completa” and two “Ripristino” slots
- 🔤 Clean typography (Helvetica), bold titles
- 🖨️ Prints **all** rooms or **only selected** room IDs (prompt)

---

## ⚙️ Requirements

- Python 3.8+
- `reportlab`

Install:

```bash
pip install reportlab
```

> On Windows PowerShell, you may need:  
> `py -m pip install reportlab`

---

## 📁 Repository layout (suggested)

```
CartellinoStanzeAPP/
├─ CartellinoStanze.py        # main script (this file)
├─ nomiStudenti.csv           # students per room
├─ datiStanze.csv             # housekeeping timetable per room
├─ cartellini_stanze.pdf      # generated output (ignored by git)
├─ .gitignore                 # ignore data/build artifacts
└─ (optional build artifacts: dist/, build/, __pycache__/ ...)
```

---

## 🧾 Input data format (CSV)

> **Delimiter:** semicolon `;`  
> **Encoding:** `ISO-8859-1` (as enforced by the script)

### 1️⃣ `datiStanze.csv` — housekeeping timetable

**Headers (exact):**
```
CAMERA;C;C-ORE;R1;R1-ORE;R2;R2-ORE
```

**Example:**
```
CAMERA;C;C-ORE;R1;R1-ORE;R2;R2-ORE
101;Lunedì;08:30;Mercoledì;10:00;Venerdì;09:30
102;Martedì;08:30;Giovedì;10:00;Sabato;09:30
```

- `C`/`C-ORE` → “Pulizia Completa”  
- `R1`/`R1-ORE`, `R2`/`R2-ORE` → “Ripristino” 1 & 2  
- `CAMERA` must match the room IDs used in `nomiStudenti.csv`

### 2️⃣ `nomiStudenti.csv` — students per room

**Headers (exact):**
```
CAMERA;STUDENTE 1;STUDENTE 2
```

**Example:**
```
CAMERA;STUDENTE 1;STUDENTE 2
101;Mario Rossi;Luca Bianchi
102;Giulia Verdi;
```

- If `STUDENTE 2` is blank, the card shows a single name centered.

---

## 🧠 How it works

1. Reads `datiStanze.csv` into `general_housekeeping_timetable`
2. Reads `nomiStudenti.csv` and, for each row:
   - Looks up matching `CAMERA` in the timetable
   - Builds a `Room` object with names + housekeeping info
3. Lays out cards on A4 (2 per page) and saves `cartellini_stanze.pdf`
4. Optionally opens the PDF automatically (Windows/macOS)

---

## ▶️ Usage

Place `CartellinoStanze.py`, `nomiStudenti.csv`, and `datiStanze.csv` in the **same folder**, then run:

### Windows (PowerShell / CMD)
```powershell
py CartellinoStanze.py
```

### macOS / Linux
```bash
python3 CartellinoStanze.py
```

Follow the prompt:

- **Press ENTER** → prints **all** rooms  
- **Type specific rooms** → e.g. `101, 102, 205` (comma-separated), then ENTER  
  (Ranges are not implemented; use explicit IDs)

The script will:
- Generate `cartellini_stanze.pdf`
- Try to open it automatically (`os.startfile` on Windows, `open` on macOS)

---

## 🧩 Output layout

- Paper: **A4**
- Cards per page: **2** (1 column × 2 rows)
- Card size: **18 × 11.85 cm**
- Margins: **1.5 cm** (left/right), **1 cm** (top/bottom)
- Fonts: Helvetica / Helvetica-Bold (ReportLab built-ins)

### Elements
- Outer dashed border  
- Thick rounded frame for names (top area)  
- Very large room ID on the left  
- Right-side housekeeping info:
  - **Pulizia Completa** → `C C-ORE`
  - **Ripristino** → `R1 R1-ORE`, `R2 R2-ORE`

---

## 🧰 Configuration (inside the class)

In `CartellinoStanze.__init__` you can adjust:

```python
self.larghezza_cartellino = 18 * cm
self.altezza_cartellino   = 11.85 * cm
self.margine_x            = 1.5 * cm
self.margine_y            = 1 * cm
self.cartellini_per_riga  = 1
self.cartellini_per_colonna = 2
self.font_name            = "Helvetica"
```

And in `disegnaCartellino(...)`:
- `name_font_size = 33`
- `spazio_tra_righe = 0.9 * cm`
- Rounded frame radius, etc.

---

## 🧹 Troubleshooting

| Problem | Cause / Solution |
|----------|------------------|
| **FileNotFoundError** | Ensure `nomiStudenti.csv` and `datiStanze.csv` are in the same folder. |
| **Encoding issues (�)** | Save CSVs as **ISO-8859-1** or update the script to `encoding="utf-8"`. |
| **“Orari di pulizia non trovati”** | Room ID missing in `datiStanze.csv` → uses “N/D” placeholders. |
| **PDF not opening on Linux** | Replace `open` with `xdg-open` in the code. |
| **LF/CRLF warnings in Git** | Harmless. Use `git config --global core.autocrlf input` if needed. |

---

## 📄 Recommended `.gitignore`

```
nomiStudenti.csv
datiStanze.csv
cartellini_stanze.pdf
version_info.txt
dist/
build/
other/
__pycache__/
*.spec
*.exe
*.pyc
*.pyo
*.pyd
```

Remove tracked files (if needed):

```bash
git rm --cached <path>
```

---

## 🧱 Build an executable (optional)

If you use PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile CartellinoStanze.py
```

Output will appear in `dist/` (e.g., `CartellinoStanze.exe` on Windows).  
You can customize the `.spec` file as needed.

---

## 🪪 Version & Credits

- **Version:** 2.6  
- **Author:** Carlo Zambaldo (2025)  
- **Contact:** [carlo.zambaldo@gmail.com](mailto:carlo.zambaldo@gmail.com)

---

## ⚖️ License

Choose a license (e.g., MIT) and add a `LICENSE` file if you plan to share the project.
