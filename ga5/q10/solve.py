import csv, math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

WAREHOUSES = {
    'Delhi':   (28.6139, 77.2090),
    'Mumbai':  (19.0760, 72.8777),
    'Chennai': (13.0827, 80.2707),
}

counts = {w: 0 for w in WAREHOUSES}

with open('deliveries.csv') as f:
    for row in csv.DictReader(f):
        lat, lon = float(row['Latitude']), float(row['Longitude'])
        nearest = min(WAREHOUSES, key=lambda w: haversine(lat, lon, *WAREHOUSES[w]))
        counts[nearest] += 1

winner = max(counts, key=counts.get)
print(f"{winner}, {counts[winner]}")
