import openpyxl, csv, io
wb = openpyxl.load_workbook(r"C:\Users\kyle\Recipes\Gronning-Kitchen-Tracker.xlsx")
for ws in wb.worksheets:
    out = io.StringIO()
    w = csv.writer(out)
    for row in ws.iter_rows(values_only=True):
        w.writerow(["" if c is None else c for c in row])
    text = out.getvalue()
    fn = ws.title.replace(" ", "_") + ".csv"
    with open(r"C:\Users\kyle\Recipes" + "\\" + fn, "w", newline="", encoding="utf-8") as f:
        f.write(text)
    print("===== %s (%d chars) =====" % (ws.title, len(text)))
    print(text)
    print("===== END %s =====" % ws.title)
