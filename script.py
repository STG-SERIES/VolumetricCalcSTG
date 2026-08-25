import sys
import tkinter as tk
from tkinter import messagebox

# Try to remove the console window on Windows (if script is run with python.exe).
# If you prefer running without a console, using pythonw.exe or saving as .pyw is another option.
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.kernel32.FreeConsole()
    except Exception:
        pass

def parse_float(value_str, field_name):
    """Parse a string into float; replace comma with dot like original script."""
    value_str = value_str.strip().replace(",", ".")
    try:
        return float(value_str)
    except ValueError:
        raise ValueError(f"Please input a valid number for {field_name}.")

def calculate(event=None):
    global final_numeric
    try:
        w = parse_float(entry_width.get(), "Width")
        h = parse_float(entry_height.get(), "Height")
        l = parse_float(entry_length.get(), "Length")
        g = parse_float(entry_grams.get(), "Grams")
    except ValueError as e:
        messagebox.showerror("Invalid input", str(e))
        return

    whl = (w * h * l) / 5
    if whl >= g:
        result_text = f"Your product is {whl:.2f} grams (Volumetric).\n({w} * {h} * {l}) / 5"
        final_numeric = whl
    else:
        result_text = f"Your product is {g:.2f} grams (Actual)."
        final_numeric = g

    label_result.config(text=result_text)
    btn_copy.config(state=tk.NORMAL)

def clear_fields():
    global final_numeric, copy_timer_id
    entry_width.delete(0, tk.END)
    entry_height.delete(0, tk.END)
    entry_length.delete(0, tk.END)
    entry_grams.delete(0, tk.END)
    label_result.config(text="")
    final_numeric = None
    btn_copy.config(state=tk.DISABLED)
    # revert copy button text immediately
    if copy_timer_id is not None:
        try:
            root.after_cancel(copy_timer_id)
        except Exception:
            pass
    btn_copy.config(text=original_copy_text)
    entry_width.focus_set()

def copy_result():
    global copy_timer_id
    if final_numeric is None:
        messagebox.showwarning("Nothing to copy", "No result to copy yet.")
        return

    # Truncate decimals (do not round) and copy only the integer part, no "grams" suffix.
    try:
        int_value = int(final_numeric)
    except Exception:
        # Fallback: try converting from string
        try:
            int_value = int(float(final_numeric))
        except Exception:
            messagebox.showerror("Copy failed", "Could not determine numeric value to copy.")
            return

    # Copy to clipboard
    root.clipboard_clear()
    root.clipboard_append(str(int_value))
    try:
        root.update()  # ensure clipboard is set
    except Exception:
        pass

    # Change button text: replace "Copy" with "Copied" for 5 seconds (no popup).
    current_text = btn_copy['text']
    if "Copy" in current_text:
        new_text = current_text.replace("Copy", "Copied", 1)
    else:
        new_text = "Copied"
    btn_copy.config(text=new_text)

    # Cancel previous timer if any
    if copy_timer_id is not None:
        try:
            root.after_cancel(copy_timer_id)
        except Exception:
            pass
        copy_timer_id = None

    # Revert button text after 5 seconds
    copy_timer_id = root.after(5000, lambda: btn_copy.config(text=original_copy_text))

def focus_next(event, next_widget):
    next_widget.focus_set()
    # select all text for easy overwrite
    try:
        next_widget.selection_range(0, tk.END)
    except Exception:
        pass
    return "break"  # prevent default handling

root = tk.Tk()
root.title("Volumetric Weight Calculator")

# State
final_numeric = None        # holds the numeric final grams (float)
copy_timer_id = None        # holds after() id for reverting copy button text
original_copy_text = "Copy final grams"

# Layout
frm = tk.Frame(root, padx=12, pady=12)
frm.pack(fill=tk.BOTH, expand=True)

tk.Label(frm, text="Width (cm):").grid(row=0, column=0, sticky="e", pady=4)
entry_width = tk.Entry(frm, width=20)
entry_width.grid(row=0, column=1, pady=4)

tk.Label(frm, text="Height (cm):").grid(row=1, column=0, sticky="e", pady=4)
entry_height = tk.Entry(frm, width=20)
entry_height.grid(row=1, column=1, pady=4)

tk.Label(frm, text="Length (cm):").grid(row=2, column=0, sticky="e", pady=4)
entry_length = tk.Entry(frm, width=20)
entry_length.grid(row=2, column=1, pady=4)

tk.Label(frm, text="Grams (g):").grid(row=3, column=0, sticky="e", pady=4)
entry_grams = tk.Entry(frm, width=20)
entry_grams.grid(row=3, column=1, pady=4)

# Bind Enter to move focus to the next field, last field runs calculate
entry_width.bind("<Return>", lambda e: focus_next(e, entry_height))
entry_height.bind("<Return>", lambda e: focus_next(e, entry_length))
entry_length.bind("<Return>", lambda e: focus_next(e, entry_grams))
entry_grams.bind("<Return>", calculate)

btn_frame = tk.Frame(frm)
btn_frame.grid(row=4, column=0, columnspan=2, pady=(8, 4))

btn_calc = tk.Button(btn_frame, text="Calculate", command=calculate, width=10)
btn_calc.pack(side=tk.LEFT, padx=4)

btn_clear = tk.Button(btn_frame, text="Clear", command=clear_fields, width=10)
btn_clear.pack(side=tk.LEFT, padx=4)

btn_quit = tk.Button(btn_frame, text="Quit", command=root.destroy, width=10)
btn_quit.pack(side=tk.LEFT, padx=4)

# Copy button for final grams (disabled until a result exists)
btn_copy = tk.Button(frm, text=original_copy_text, command=copy_result, state=tk.DISABLED, width=18)
btn_copy.grid(row=5, column=0, columnspan=2, pady=(4, 0))

label_result = tk.Label(frm, text="", justify="left", anchor="w")
label_result.grid(row=6, column=0, columnspan=2, sticky="w", pady=(8, 0))

# Focus first field
entry_width.focus_set()

root.mainloop()
