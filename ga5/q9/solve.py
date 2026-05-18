import csv, math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

HQ = (28.6139, 77.209)
distances, revenues = [], []

with open('store_locations.csv') as f:
    for row in csv.DictReader(f):
        distances.append(haversine(*HQ, float(row['Latitude']), float(row['Longitude'])))
        revenues.append(float(row['Monthly_Revenue']))

n   = len(distances)
md  = sum(distances) / n
mr  = sum(revenues)  / n
num = sum((distances[i] - md) * (revenues[i] - mr) for i in range(n))
den = math.sqrt(sum((d - md)**2 for d in distances) * sum((r - mr)**2 for r in revenues))
print(round(num / den, 4))
