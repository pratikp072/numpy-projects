NeoPay Transaction Spike Analysis (NumPy-Only)

A lightweight analytics project to investigate a spike in night-time and high-value digital wallet transactions using NumPy only (no Pandas, no Matplotlib).
Designed for fast CSV processing, clean aggregates, and easy consumption by business or BI teams.

Project Objective

NeoPay Support has reported unusual increases in:

Night-time transactions (hour < 6 or hour > 22)

High-value transactions (amount > 200,000)

Your goal is to quantify the spike, understand where it’s coming from (time, month, cities), and produce small CSV summaries for reporting teams — using only built-in Python + NumPy.

What This Project Produces

The script generates the following outputs inside the outputs/ folder:

File	Description
np_monthly_totals.csv	Month-wise total transaction amounts
np_hourly_counts.csv	Number of transactions in each hour (0–23)
np_city_totals_top5.csv	Top-5 cities by total amount
np_night_high_by_month.csv	Total amount where transactions are both night-time AND high-value
(optional) np_kpis.txt	Summary: total amount, median, average, %night, %high
Input Data Structure

Your input CSV (e.g., transactions.csv) should have at least:

amount,txn_time,city
4500,23-05-2023 14:22,Delhi
265000,09-06-2023 23:48,Mumbai
...

Column meanings

amount → transaction amount (float)

txn_time → "DD-MM-YYYY HH:MM" string timestamp

city → city name (string)

🛠️ Features Implemented
✔ Data Loading

Uses csv.DictReader (no Pandas)

Columns converted into NumPy arrays

✔ Feature Engineering

Extract hour (0–23)

Extract month label "YYYY-MM"

Build masks:

is_night

is_high

is_night_high

✔ KPIs Calculated

Total rows

Total amount

Median ticket

Average ticket

% night-time transactions

% high-value transactions

✔ Aggregations

Month-wise sum

Hour-of-day distribution

Top-5 cities by total amount

Monthly Night+High totals

✔ CSV Output

All results exported using np.savetxt into the /outputs directory.