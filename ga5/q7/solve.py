import csv, statistics

vals = []
with open('delivery_times.csv') as f:
    for row in csv.DictReader(f):
        vals.append(float(row['Delivery_Minutes']))

mean  = statistics.mean(vals)
stdev = statistics.stdev(vals)   # sample stdev (n-1) — matches Excel STDEV

outliers = sum(1 for v in vals if abs((v - mean) / stdev) > 2)
print(outliers)
