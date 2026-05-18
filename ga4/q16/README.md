# Q16: Cross-Lingual Entity Disambiguation

## Task

Map 1,000 document excerpts in 15 languages, each mentioning a historical figure, to one of 19 distinct `entity_id` values from a reference list.
The pipeline must handle cross-lingual name variants, disambiguate between similar entities, process minor typos, and utilize contextual clues (era, region, events).

---

## Requirements

* Build an LLM-powered pipeline
* Extract `mentioned_name`, `language`, `year`, and `source_region`
* Handle cross-lingual variations and \~8% typos
* Disambiguate contextually (e.g., Ivan III vs Ivan IV, Catherine the Great vs Catherine de' Medici)
* Accuracy threshold: ≥95% (950/1000 correct)
* Output: `output.csv` with exactly 1000 rows mapping `doc_id,entity_id`

---

## Approach

### Hybrid Disambiguation Pipeline
To balance accuracy, speed, and cost, the pipeline employs a **two-stage hybrid approach**:

1. **Strong Regex Signals (Deterministic Matching):**
   * Uses known translations, aliases, and character patterns for all 19 entities across the 15 languages.
   * Leverages geographic and era overlap logic. For instance, if "Catherine" is mentioned in a document sourced from "Russia" or with Russian language features, it deterministically maps to Catherine the Great (`E004`) rather than Catherine de' Medici (`E002`).
   * Handles about 80-90% of unambiguous cases and exact name matches quickly.

2. **OpenRouter LLM Fallback (Contextual Disambiguation):**
   * If the regex patterns and regional hints fail to find a single, confident match (e.g., due to extreme typos, ambiguous root names without clear regional contexts, or complex cross-lingual morphology), the pipeline falls back to querying the `google/gemini-2.0-flash-001` model via OpenRouter.
   * The LLM is provided with the document's full context (text, language, year, region, mentioned name) and the complete reference table of entities.
   * Prompting guides the LLM to apply cross-lingual equivalence rules and return exactly the `E###` identifier.

### Execution
The pipeline iterated through all 1000 JSON lines:
* Parsed the document parameters.
* First tested against the deterministic rules.
* Invoked the LLM API for any unresolved documents.
* Appended the result to the output CSV.

---

## Code

**Script:** [`solve.py`](./solve.py)

*(Note: The script uses the OpenRouter API with a bearer token to make LLM inferences for ambiguous documents.)*

---

## Verification

```bash
python solve.py
```

* **Processed:** 1,000 documents.
* **Format:** Validated `doc_id,entity_id` structure.
* **Output length:** Exactly 1000 content lines (1001 with header).
* **Entities Mapped:** All mapped successfully to the `E001`-`E019` range.

---

## Submission

The generated mappings are saved in [`output.csv`](./output.csv).

Example rows:
```csv
doc_id,entity_id
DOC-0001,E017
DOC-0002,E002
DOC-0003,E006
DOC-0004,E003
DOC-0005,E015
...
```
*(Copy the exact contents of `output.csv` into the submission box).*
