# VolumetricCalcSTG 

A small Python/Tkinter GUI that calculates volumetric weight using the formula used in the original script:

    volumetric_grams = (width * height * length) / 5

Features
- Input Width, Height, Length (in cm) and Actual weight (in g).
- Keeps input parsing consistent with the original script (accepts comma or dot as decimal separator).
- Shows whether the volumetric or actual weight applies.
- Copy final grams: copies only the integer part (truncates decimals) to the clipboard, no units.
- Copy button text changes to "Copied ..." for 5 seconds instead of showing a popup.
- Press Enter to move to the next field; pressing Enter in the Grams field runs the calculation.
- Attempts to remove the Windows console window (if running under python.exe). Using `pythonw.exe` or saving as `.pyw` will run without a console on Windows.

Requirements
- Python 3.x (tkinter is included with standard Python distributions)
- No external dependencies

Notes
- The copy operation truncates decimals (no rounding). For example:
  - 12.67 -> copies "12"
  - 645.76 -> copies "645"
- The displayed result text still shows the full decimal value (e.g., "123.45 grams (Volumetric)").
- If you need rounding instead of truncation, let me know which rounding rule you prefer (nearest integer, round down/up, etc.).

License
- Use as you wish. No license file included.

Enjoy! *STGHECKER*
