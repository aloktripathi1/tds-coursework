"""
solve.py — Cross-Lingual Entity Disambiguation using OpenRouter
Uses a hybrid approach:
  1. Regex patterns for clear cases (fast, no API cost)
  2. OpenRouter (google/gemini-2.0-flash-001) for ambiguous cases
"""
import zipfile, json, csv, io, re, requests, time

OPENROUTER_API_KEY = "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"
OR_MODEL = "google/gemini-2.0-flash-001"

# ── Load data ─────────────────────────────────────────────────
z = zipfile.ZipFile("q-cross-lingual-entity-disambiguation-server.zip")
entities_raw = z.read("entity_reference.csv").decode("utf-8")
entities = list(csv.DictReader(io.StringIO(entities_raw)))

docs_raw = z.read("documents.jsonl").decode("utf-8")
docs = [json.loads(l) for l in docs_raw.strip().split("\n") if l.strip()]

ENTITY_TABLE = "\n".join(
    f"{e['entity_id']}: {e['canonical_name']} ({e['role']}, {e['era']}, {e['region']})"
    for e in entities
)

# ── OpenRouter LLM call ───────────────────────────────────────
def llm_disambiguate(doc: dict) -> str:
    prompt = f"""You are a expert historian. Map this document to exactly ONE entity_id from the list.

Document:
- language: {doc['language']}
- year: {doc['year']}
- mentioned_name: {doc['mentioned_name']}
- source_region: {doc['source_region']}
- text: {doc['text']}

Entities:
{ENTITY_TABLE}

Cross-lingual hints: Pedro=Peter, Ivan=Иван=伊万=이반, Juan=João=Jean=Johann=Giovanni=John, 
Luis=Louis=Ludwig=Luigi=Lodewijk, Felipe=Philip=Philippe=Philipp=Filippo,
Catherine=Catalina=Katarina=Екатерина=凯瑟琳, Alexander=Aleksander=Alexandre=Alejandro=亚历山大,
Charles=Carlos=Karl=Carlo=Karel, Henry=Henri=Heinrich=Enrique=Henrique,
Frederick=Frédéric=Friedrich=Federico, William=Willem=Guillermo=Guglielmo,
George=Georg=Georges=Jorge=Джордж, Louis=Luis=Ludwig=Luigi=Людовик.

Reply with ONLY the entity_id (e.g. E004). No explanation, no punctuation."""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/student/tds",
        "X-Title": "Entity Disambiguation"
    }
    body = {
        "model": OR_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": 10
    }
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions",
                          headers=headers, json=body, timeout=30)
        raw = r.json()["choices"][0]["message"]["content"].strip()
        m = re.search(r"E\d{3}", raw)
        return m.group(0) if m else "E001"
    except Exception as ex:
        print(f"  LLM error for {doc['doc_id']}: {ex}")
        return "E001"

# ── Strong regex signals ───────────────────────────────────────
# Each tuple: (regex_pattern, region_hint_or_None, entity_id)
# Patterns target mentioned_name OR text, both lowercased
SIGNALS = [
    # E001 George I of Greece
    (r"george\s*i\b|georg.*griech|george.*gr[eè]c|george.*griek|게오르기|조지\s*1|ジョージ1|格奥尔基|георг.*грец", "greece", "E001"),
    # E002 Catherine de' Medici
    (r"catherin.*medici|katarin.*medici|caterina.*medici|katar[íi]na.*medici|凯瑟琳.*美第奇|카트린.*메디치|カトリーヌ.*メディシス| екатери.*медичи|médicis", None, "E002"),
    # E003 John II of Castile
    (r"\bjuan\s*ii\b|\bjoão\s*ii\b|\bjean\s*ii\b.*castil|\bjohn\s*ii\b.*castil|\bjohann\s*ii\b.*kastil|\bii[.\s]*juan\b", "castile", "E003"),
    # E004 Catherine the Great (Russia)
    (r"catherin.*great|katarin.*velik|caterina.*grande|katarin.*gross|catherine.*grande|grande.*caterina|葉卡捷琳娜大帝|예카테리나.*대제|叶卡捷琳娜大帝|екатерина.*велик|büyük.*katerin|катери.*велика", None, "E004"),
    # E005 Philip II of Spain
    (r"philip\s*ii.*spain|felipe\s*ii|filipe\s*ii|filippo\s*ii|philipp\s*ii|felipe\s*ii|فيليب\s*الثاني|腓力二世|펠리페\s*2|フェリペ2|філіп\s*ii", "spain", "E005"),
    # E006 Peter the Great
    (r"peter.*great|pedro.*grande|pierre.*grand|petrus.*groot|pjotr.*wielki|пётр.*велик|피터.*대제|ピョートル.*大帝|彼得大帝|peter.*grosse|büyük.*petro", None, "E006"),
    # E007 George III of Britain
    (r"george\s*iii\b|georg.*großbrit|george.*kingdom|ジョージ3|조지\s*3|格奥尔基.*三世", None, "E007"),
    # E008 Charles I of England
    (r"charles\s*i.*engl|carlos\s*i.*ingl|karl\s*i.*engl|carlo\s*i.*ingl|charles\s*premier.*angl|チャールズ1|찰스\s*1|карл\s*i.*англ", "england", "E008"),
    # E009 John I of Portugal
    (r"jo[aã]o\s*i\b.*portug|john\s*i.*portug|jean\s*i.*portug|juan\s*i.*portug|johann\s*i.*portug", "portugal", "E009"),
    # E010 Louis XVI
    (r"louis\s*xvi|ludwig\s*xvi|luigi\s*xvi|lodewijk\s*xvi|路易十六|루이\s*16|ルイ16|людовик\s*xvi|luis\s*xvi|لويس.*السادس.*عشر|luis xvi", None, "E010"),
    # E011 Henry IV of France
    (r"henry\s*iv.*franc|henri\s*iv|enrique\s*iv.*fran|henrique\s*iv.*fran|генрих\s*iv.*фран|アンリ4|앙리\s*4|هنري.*الرابع.*فرنسا", "france", "E011"),
    # E012 Henry VIII
    (r"henry\s*viii|henrik\s*viii|heinrich\s*viii|enrique\s*viii|henrique\s*viii|генрих\s*viii|헨리\s*8|ヘンリー8|هنري.*الثامن|亨利八世", None, "E012"),
    # E013 Louis XIV
    (r"louis\s*xiv|ludwig\s*xiv|luigi\s*xiv|ルイ14|루이\s*14|路易十四|людовик\s*xiv|luis\s*xiv|لويس.*الرابع.*عشر", None, "E013"),
    # E014 Frederick the Great
    (r"frederick.*great|fritz.*gross|friedrich.*gross|フリードリヒ大王|프리드리히.*대왕|federico.*grande.*prus|фридрих.*велик|büyük.*friedrich|büyük\s+frederik", None, "E014"),
    # E015 Alexander II of Russia
    (r"alexander\s*ii.*russia|aleksander\s*ii|aleksandr\s*ii|亚历山大.*二世|알렉산더\s*2|алексан.*ii.*росс|alexandre\s*ii.*russ|alejandro\s*ii.*rusi|アレクサンドル2", "russia", "E015"),
    # E016 Alexander the Great (Macedonia)
    (r"alexander.*great|alexandre.*grand|alejandro.*magno|亚历山大大帝|알렉산더.*대왕|アレクサンダー大王|إسكندر.*الأكبر|iskandar.*agung|alexander.*macedon|makedon.*alexandre|großen.*alexan", None, "E016"),
    # E017 Ivan IV (Terrible)
    (r"ivan\s*iv|iwan\s*iv|ivan.*terribl|иван.*грозн|伊万四世|이반\s*4|イヴァン4|iv.*иван|groznyi|корж.*иван", "russia", "E017"),
    # E018 Charles V Holy Roman Emperor
    (r"charles\s*v.*holy|karl\s*v.*kaiser|carlos\s*v.*sacro|carlo\s*v.*sacro|चार्ल्स\s*v|卡尔五世|카를\s*5|カール5|карл\s*v.*священ", None, "E018"),
    # E019 William III of England/Netherlands
    (r"william\s*iii|willem\s*iii|guillermo\s*iii|guglielmo\s*iii|ウィリアム3|빌렘\s*3|вильгельм\s*iii|威廉三世", None, "E019"),
]

# Unique region → entity (no ambiguity)
REGION_UNIQUE = {
    "greece": "E001",
    "castile": "E003",
    "macedonia": "E016",
    "prussia": "E014",
    "portugal": "E009",
}

# ── Main loop ─────────────────────────────────────────────────
results = []
llm_count = 0

for i, doc in enumerate(docs):
    doc_id  = doc["doc_id"]
    region  = doc.get("source_region", "").lower().strip()
    name    = doc.get("mentioned_name", "").lower()
    text    = doc.get("text", "").lower()
    combined = name + " " + text

    # 1. Unique region shortcut
    guessed = REGION_UNIQUE.get(region)

    # 2. Regex signals
    if not guessed:
        for pattern, region_hint, eid in SIGNALS:
            if re.search(pattern, combined, re.IGNORECASE):
                if region_hint is None or region_hint in region:
                    guessed = eid
                    break

    # 3. LLM fallback
    if not guessed:
        llm_count += 1
        print(f"  [{i+1:4d}] LLM: {doc_id} | {doc['mentioned_name']} | {region}")
        guessed = llm_disambiguate(doc)
        time.sleep(0.2)

    results.append({"doc_id": doc_id, "entity_id": guessed})

    if (i + 1) % 100 == 0:
        print(f"  Processed {i+1}/1000, LLM calls so far: {llm_count}")

print(f"\nDone. Total: {len(results)}, LLM calls: {llm_count}")

# Write CSV
with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["doc_id", "entity_id"])
    writer.writeheader()
    writer.writerows(results)

print("Saved → output.csv")
