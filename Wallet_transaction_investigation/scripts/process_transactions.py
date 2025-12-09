from pathlib import Path
import csv
from datetime import datetime
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]   

DATA_DIR = PROJECT_ROOT / "data"
CSV_PATH = DATA_DIR / "transactions.csv"

OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

print("Project root:", PROJECT_ROOT)
print("CSV path:", CSV_PATH)
print("CSV exists?", CSV_PATH.exists())


# Load and process the CSV file
with open(CSV_PATH, newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))
N = len(rows)
print("Loaded rows:", N)

# Convert columns to NumPy arrays
amount = np.array([float(r["amount"]) for r in rows], dtype=float)
dt_py = [datetime.strptime(r["txn_time"], "%d-%m-%Y %H:%M") for r in rows]
txn_time = np.array(dt_py, dtype='datetime64[m]')
city = np.array([r["city"].strip() for r in rows], dtype=object)

# Derived features
hour = np.array([t.astype('datetime64[h]').astype(int) % 24 for t in txn_time], dtype=int)
month64 = txn_time.astype('datetime64[M]')

# Convert month to string label "YYYY-MM"
def month_str(m):
    o = m.astype(object)
    return f"{o.year:04d}-{o.month:02d}"

month_labels = np.array([month_str(m) for m in month64], dtype=object)

# Masks
is_night = (hour < 6) | (hour > 22)
is_high  = amount > 200_000
is_night_high = is_night & is_high

# KPIs
print("Total Amount:", float(amount.sum()))
print("Median:", float(np.median(amount)), "\nAvg:", float(amount.mean()))
print("% Night:", float(is_night.mean()*100), "\n% High:", float(is_high.mean()*100))

# Monthly totals
months = np.unique(month_labels)
monthly_totals = np.array([[m, float(amount[month_labels==m].sum())] for m in months], dtype=object)
monthly_totals = monthly_totals[np.argsort(monthly_totals[:,0])]

# Hourly counts
hour_counts = np.bincount(hour, minlength=24)
hour_table = np.column_stack([np.arange(24), hour_counts])

# Night+High trend by month
nh = np.array([[m, float(amount[(month_labels==m)&is_night_high].sum())] for m in months], dtype=object)
nh = nh[np.argsort(nh[:,0])]

# Top-5 cities by amount
agg = {}
for c,a in zip(city, amount):
    agg[c] = agg.get(c, 0.0) + float(a)

cities = np.array(list(agg.keys()), dtype=object)
totals = np.array(list(agg.values()), dtype=float)
ordr = np.argsort(totals)[::-1]
top_cities = np.column_stack([cities[ordr][:5], totals[ordr][:5]])

# Export CSV files
np.savetxt(OUTPUT_DIR / "np_monthly_totals.csv",
           monthly_totals, fmt="%s", delimiter=",",
           header="month,total_amount", comments="")

np.savetxt(OUTPUT_DIR / "np_hourly_counts.csv",
           hour_table, fmt="%d,%d", delimiter=",",
           header="hour,count", comments="")

np.savetxt(OUTPUT_DIR / "np_city_totals_top5.csv",
           top_cities, fmt="%s,%.2f", delimiter=",",
           header="city,total_amount", comments="")

np.savetxt(OUTPUT_DIR / "np_night_high_by_month.csv",
           nh, fmt="%s,%.2f", delimiter=",",
           header="month,night_high_amount", comments="")

# Validation (Check correctness)
print("Rows vs sum(hour_counts):", len(hour), int(np.sum(np.bincount(hour, minlength=24))))
print("Monthly totals summed:", float(np.sum(monthly_totals[:,1].astype(float))))
print("All-amount sum:", float(amount.sum()))
print("Top cities sorted desc? first two:\n", top_cities[:2])
# End of script