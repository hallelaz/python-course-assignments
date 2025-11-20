# day04 – UniProt Data Downloader

This project downloads protein data from the UniProt REST API and saves it locally as a JSON file.  
The logic is split into two separate files as required:

- **`uniprot_downloader.py` – business logic**  
  Downloads a UniProt entry using the REST endpoint:  
  `https://rest.uniprot.org/uniprotkb/{accession}.json`

- **`main.py` – user interface (UI)**  
  A simple CLI that asks the user for a UniProt ID, calls the logic module, and reports success or errors.

An example output file included in this folder is **`Q9LQT8.json`** (Arabidopsis thaliana FLC protein).

---

## What the program does (in a few words)

The program takes a UniProt protein ID (e.g., `Q9LQT8`), sends a request to UniProt’s API, retrieves the full protein record in JSON format, and saves the data locally.

---

## Interaction with AI

I used ChatGPT-5 to assist in restructuring the code into a clean, modular format.  
Specifically, I asked ChatGPT-5 to:

- separate the business logic into its own module (`uniprot_downloader.py`)
- write a simple CLI script (`main.py`) that imports and uses that logic
- ensure that the program follows the course requirement of UI vs. logic separation
- confirm that the program communicates correctly with the UniProt REST API and saves the returned data

The AI also helped refine the README structure and phrasing.

---

## Additional Analysis: Amino Acid Classification

After completing the downloader, I decided to extend the project and further analyze the retrieved data.  
Using ChatGPT-5, I wrote an additional script (`analyze_amino_acids.py`) that:

- loads the downloaded UniProt JSON file  
- extracts the protein sequence  
- classifies each amino acid into its biochemical category:  
  - **Nonpolar (Hydrophobic)**  
  - **Polar (Uncharged)**  
  - **Positively Charged (Basic)**  
  - **Negatively Charged (Acidic)**  
- outputs a grouped summary of the amino acid composition

This allowed me to go beyond downloading the record and perform basic biochemical analysis directly from UniProt data.

---
