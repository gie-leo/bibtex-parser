#script to turn apa citation lists into bibtex entries for data-import without IDs, articles only

import re

def apa_to_bibtex(entry, citekey):
    # Regex für APA-ähnliche Artikelzitationen
    match = re.match(
        r"^(.*?)\s+\((\d{4})\)\.\s+(.*?)\.\s+(\*?)([^*]+)(\*?),\s+(\d+)\((\d+)\),\s+(Article\s+)?(\w+)\.\s+(https?://doi\.org/\S+)",
        entry

    )

    if not match:
        # Wenn keine Übereinstimmung, gib eine Kommentarzeile zurück
        return f"% Konnte nicht automatisch verarbeitet werden: {entry}\n"

    #alle Infos aus re extrahieren
    authors_raw, year, title, _, journal, _, volume, number, _, pages, url = match.groups()
    
    # DOI aus url extrahieren, ansonsten bleibt das Feld leer
    doi_match = re.search(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", url, re.I)
    doi = doi_match.group(0) if doi_match else ""

    #Aufbau bibtex-Artikel mit Formatierung
    bibtex_entry = f"""@article{{{citekey},
  author = {{{authors_raw.strip()}}},
  title = {{{title.strip()}}},
  journal = {{{journal.strip()}}},
  year = {{{year}}},
  volume = {{{volume}}},
  number = {{{number}}},
  pages = {{{pages}}},
  doi = {{{doi}}},
  url = {{{url}}}
}}\n"""
    return bibtex_entry

#real work starts here; apa-zitate aus Datei werden umgewandelt und als bibtex-Datei abgespeichert
def process_apa_file(input_file, output_file):
    print('start') # debug
    with open(input_file, "r", encoding="utf-8") as f:
        print('Inputfile opened') # debug
        #alle belegten zeilen sollen gelesen werden
        lines = [line.strip() for line in f if line.strip()]

    with open(output_file, "w", encoding="utf-8") as out:
        print('Outputfile opened') # Debug
        for i, line in enumerate(lines):
            print(i)
            citekey = f"apa_entry_{i+1}"
            bib = apa_to_bibtex(line, citekey)
            out.write(bib + "\n")

    print(f"✔️ {len(lines)} APA-Zitation(en) verarbeitet und gespeichert in: {output_file}")

# Funktion aufrufen
process_apa_file("sample/apa-zitate.txt", "sample/bibtex.bib")