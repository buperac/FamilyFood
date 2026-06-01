import argparse
import base64
import os
import re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

HEAD = Font(bold=True, color="FFFFFF")
FILL = PatternFill("solid", fgColor="2C2620")
WRAP = Alignment(vertical="top", wrap_text=True)

def style_header(ws, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=1, column=c)
        cell.font = HEAD
        cell.fill = FILL
    ws.freeze_panes = "A2"

def main():
    parser = argparse.ArgumentParser(description="Create a customized Excel tracker for the AI Meal Planner.")
    parser.add_argument("--name", type=str, default="Family", help="Name of the family or user")
    args = parser.parse_args()
    
    # Strip characters that are invalid in Windows filenames: <>:"/\|?*
    clean_name = re.sub(r'[<>:"/\\|?*]', '', args.name)
    clean_name = clean_name.replace(" ", "-").strip()
    if not clean_name:
        clean_name = "Family"
    filename = f"{clean_name}-Kitchen-Tracker.xlsx"
    
    wb = Workbook()

    # ---------- Meal Log ----------
    ml = wb.active
    ml.title = "Meal Log"
    ml_head = ["Date cooked", "Week", "Day", "Meal", "Cuisine", "Cal/adult",
               "Est. cost", "Actual cost", "Rating (1-5)", "Favourite", "Notes"]
    ml.append(ml_head)
    
    # We leave rows empty so the sheet is ready to log meals dynamically
    for r in range(2, 50): # pre-format 50 rows
        ml.append(["", "", "", "", "", "", "", "", "", "", ""])
        ml.cell(row=r, column=4).alignment = WRAP  # Meal
        ml.cell(row=r, column=11).alignment = WRAP # Notes
        ml.cell(row=r, column=7).number_format = '"$"#,##0.00'
        ml.cell(row=r, column=8).number_format = '"$"#,##0.00'
        
    widths = [12, 6, 6, 34, 12, 9, 10, 11, 11, 10, 40]
    for i, wdt in enumerate(widths, 1):
        ml.column_dimensions[get_column_letter(i)].width = wdt
    style_header(ml, len(ml_head))

    # ---------- Ingredient Prices ----------
    ip = wb.create_sheet("Ingredient Prices")
    ip_head = ["Ingredient", "Category", "Est. price", "Actual / last paid",
               "Store / brand", "Size", "Per-unit", "Date updated", "Notes"]
    ip.append(ip_head)
    
    # Pre-format 100 rows
    for r in range(2, 100):
        ip.append(["", "", "", "", "", "", "", "", ""])
        ip.cell(row=r, column=1).alignment = WRAP  # Ingredient
        ip.cell(row=r, column=9).alignment = WRAP  # Notes
        ip.cell(row=r, column=3).number_format = '"$"#,##0.00'
        ip.cell(row=r, column=4).number_format = '"$"#,##0.00'
        
    ipw = [32, 14, 10, 16, 16, 12, 10, 12, 28]
    for i, wdt in enumerate(ipw, 1):
        ip.column_dimensions[get_column_letter(i)].width = wdt
    style_header(ip, len(ip_head))

    # ---------- Deals ----------
    dl = wb.create_sheet("Deals")
    dl_head = ["Date", "Item", "Store", "Sale per-unit", "Baseline per-unit",
               "Delta %", "Shelf-stable?", "Action / qty grabbed"]
    dl.append(dl_head)
    
    # Pre-format 50 rows
    for r in range(2, 50):
        dl.append(["", "", "", "", "", "", "", ""])
        dl.cell(row=r, column=2).alignment = WRAP  # Item
        dl.cell(row=r, column=8).alignment = WRAP  # Action/qty
        dl.cell(row=r, column=4).number_format = '"$"#,##0.00'
        dl.cell(row=r, column=5).number_format = '"$"#,##0.00'
        
    dlw = [12, 30, 12, 14, 16, 9, 14, 26]
    for i, wdt in enumerate(dlw, 1):
        dl.column_dimensions[get_column_letter(i)].width = dlw[i-1]
    style_header(dl, len(dl_head))

    # Save Excel file
    try:
        directory = os.path.dirname(os.path.abspath(__file__))
    except NameError:
        directory = os.getcwd()
        
    path = os.path.join(directory, filename)
    wb.save(path)
    print(f"Created customized tracker at: {path}")

if __name__ == "__main__":
    main()
