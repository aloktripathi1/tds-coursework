"""
solve_q10.py — ga4/q10: Extract Zip Codes
Reads addresses from CSV, uses gemini-2.0-flash-exp to extract zip codes, handles N/A, concatenates results.
"""
import os
import csv
import google.generativeai as genai

# Configure Gemini API
# Assuming OPENAI_API_KEY or GEMINI_API_KEY is available in the environment from ga3/ga5
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    # Try reading from Api-keys.md or .env if necessary, but assuming user has it exported
    print("Please export GEMINI_API_KEY")
    exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

addresses = []
with open("addresses_23f3003225@ds.study.iitm.ac.in.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        if row:
            addresses.append(row[0])

print(f"Loaded {len(addresses)} addresses.")

results = []
# Create a single prompt to process all at once to save time, or do it individually
# Given it's exactly 100, batching is safer and faster.

prompt = "Extract the zip code (or postal code) from each of the following addresses. " \
         "If no zip code exists for an address, return EXACTLY 'N/A' for that address. " \
         "Return the results as a clean comma-separated list of exactly 100 items, in the exact same order. " \
         "Do not include any numbering, quotes, or markdown formatting. Just the comma-separated values.\n\n"

for i, addr in enumerate(addresses):
    prompt += f"{i+1}. {addr}\n"

print("Calling Gemini API...")
response = model.generate_content(prompt)
output = response.text.strip()

# Cleanup just in case
output = output.replace('\n', '')
print("\n--- Result ---\n")
print(output)

with open("answer.txt", "w", encoding="utf-8") as f:
    f.write(output)
