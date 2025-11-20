import requests

UNIPROT_URL = "https://rest.uniprot.org/uniprotkb/{}.json"

def download_uniprot_entry(uniprot_id: str, output_path: str) -> None:
    """
    Downloads a UniProt entry in JSON format and saves it locally.
    """
    url = UNIPROT_URL.format(uniprot_id)
    response = requests.get(url)

    if response.status_code != 200:
        raise ValueError(f"Failed to download data. HTTP status: {response.status_code}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(response.text)
