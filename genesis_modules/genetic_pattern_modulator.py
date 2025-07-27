"""
genetic_pattern_modulator.py
Module to encode settings into a unique DNA string.
"""

import hashlib
import json


def encode_settings_to_dna(settings: dict) -> str:
    """
    Encode a dictionary of settings into a unique DNA-like hash string.
    """
    settings_str = json.dumps(settings, sort_keys=True)
    dna = hashlib.sha256(settings_str.encode()).hexdigest()
    return dna


def decode_dna_to_settings(dna: str, reference_db: dict) -> dict:
    """
    Given a DNA string and a reference database, retrieve the matching settings.
    """
    for settings in reference_db.values():
        if encode_settiimport os
import random
import string
import json
from datetime import datetime

OUTPUT_DIR = "outputs/genetic_modulations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def encode_to_dna(settings: dict) -> str:
    """
    Μετατρέπει dictionary ρυθμίσεων σε DNA-like string
    """
    json_str = json.dumps(settings, sort_keys=True)
    encoded = ''.join(random.choice("AGTC") for _ in range(len(json_str) * 2))
    return encoded

def decode_from_dna(dna_string: str) -> dict:
    """
    Ανακατασκευάζει ένα dictionary από fake DNA string (placeholder)
    """
    return {"decoded": True, "length": len(dna_string)}

def save_to_file(data: dict, filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

def run():
    """
    Εκτελεί encoding και decoding, και αποθηκεύει αρχεία
    """
    settings = {
        "module": "DNA Modulator",
        "version": "1.0",
        "timestamp": datetime.now().isoformat()
    }

    encoded_dna = encode_to_dna(settings)
    decoded_data = decode_from_dna(encoded_dna)

    result = {
        "original_settings": settings,
        "encoded_dna": encoded_dna,
        "decoded_data": decoded_data
    }

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_to_file(result, f"modulation_{timestamp}.json")
ngs_to_dna(settings) == dna:
            return settings
    return {}


def run():
    # Example usage with test settings
    test_settings = {
        "mutation_rate": 0.02,
        "crossover_rate": 0.8,
        "selection_method": "tournament",
        "population_size": 100
    }

    dna = encode_settings_to_dna(test_settings)
    print(f"Encoded DNA: {dna}")

    # Simulated reference DB
    ref_db = {
        "template_1": test_settings
    }

    decoded = decode_dna_to_settings(dna, ref_db)
    print(f"Decoded settings: {decoded}")
