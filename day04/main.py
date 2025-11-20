from uniprot_downloader import download_uniprot_entry
from analyze_amino_acids import extract_sequence_from_json, categorize_amino_acids

def main():
    print("=== UniProt Data Downloader ===")
    uniprot_id = input("Enter UniProt ID (example: Q9LQT8 for Arabidopsis FLC): ")

    output_file = f"{uniprot_id}.json"

    try:
        download_uniprot_entry(uniprot_id, output_file)
        print(f"Data saved successfully to: {output_file}")

        sequence = extract_sequence_from_json(output_file)

        categorized = categorize_amino_acids(sequence)

        for category, aa_list in categorized.items():
            print(f"{category}: {len(aa_list)} amino acids")
            print("".join(aa_list))
            print()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

