import json

# 1. Amino acid categories
AMINO_ACID_CATEGORIES = {
    "Nonpolar (Hydrophobic)": set("GAVLIMFWP"),
    "Polar (Uncharged)": set("STNQYC"),
    "Positively Charged (Basic)": set("KRH"),
    "Negatively Charged (Acidic)": set("DE"),
}

def categorize_amino_acids(sequence: str):
    """
    Takes a protein sequence (string) and returns a dictionary
    grouping amino acids by their physicochemical category.
    """
    result = {
        "Nonpolar (Hydrophobic)": [],
        "Polar (Uncharged)": [],
        "Positively Charged (Basic)": [],
        "Negatively Charged (Acidic)": [],
        "Other / Unknown": []
    }

    for aa in sequence:
        placed = False
        for category, letters in AMINO_ACID_CATEGORIES.items():
            if aa in letters:
                result[category].append(aa)
                placed = True
                break
        if not placed:
            result["Other / Unknown"].append(aa)

    return result


# 2. Load JSON file and extract the sequence
def extract_sequence_from_json(json_path: str):
    with open(json_path, "r") as f:
        data = json.load(f)
    return data["sequence"]["value"]


