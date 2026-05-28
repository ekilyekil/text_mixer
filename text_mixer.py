import os
import glob
import sys
import re
import random
from datetime import datetime
from pathlib import Path

# Absolute paths for environment stability
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

# Ensure output directory exists gracefully
OUTPUT_DIR.mkdir(exist_ok=True)

def mix_text(file_path, granularity):
    """
    Reads a file, partitions it into word-tail units, groups them into 
    chunks of size 'g', shuffles those chunks, and returns the result.
    """
    try:
        # pathlib handles opening files elegantly
        content = file_path.read_text(encoding='utf-8')

        # The regex identifies a word and its 'tail' (punctuation and whitespace)
        pattern = r'(\b\w+(?:[\'-]\w+)?\b[^\w\s]*\s*)'
        units = re.findall(pattern, content)

        if not units:
            print(f"\n[!] No words found in {file_path.name}.")
            return None

        # Partition into chunks of size 'g'
        chunks = ["".join(units[i:i + granularity]) for i in range(0, len(units), granularity)]

        # The core randomisation step
        random.shuffle(chunks)

        return "".join(chunks)

    except FileNotFoundError:
        print(f"\n[!] Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
        return None

def main():
    print("=== Persistent Text Mixer (2026 Edition) ===")
    
    if not INPUT_DIR.exists():
        INPUT_DIR.mkdir()
        print(f"[*] Created '{INPUT_DIR.name}' folder. Please place your source files there.")

    input_files = glob.glob(str(INPUT_DIR / "*.*"))
    if not input_files:
        print("[Error] No files found in input/ directory.")
        sys.exit(1)
    latest_file = max(input_files, key=os.path.getmtime)
    input_path = Path(latest_file)
    
    print(f"[*] Drop-and-Go selected latest file: {input_path.name}")

    while True:
        # 1. Get and Validate Granularity Input
        try:
            g_input = input("\nEnter granularity (1-9) or 'q' to quit: ").strip()
            if not g_input:
                continue
            if g_input.lower() == 'q':
                print("Exiting mixer. Goodbye!")
                break
            g = int(g_input)
            if not (1 <= g <= 9):
                print("[!] Error: Granularity must be between 1 and 9.")
                continue
        except ValueError:
            print("[!] Error: Please enter a valid whole number for granularity.")
            continue

        # 2. Process the Mix
        time_str = datetime.now().strftime("%Y%m%d_%H%M")
        print(f"--- Mixing '{input_path.name}' with Granularity g={g} ---")
        
        mixed_result = mix_text(input_path, g)

        if mixed_result:
            output_filename = f"mixed_g{g}_{time_str}_{input_path.name}"
            output_path = OUTPUT_DIR / output_filename
            
            output_path.write_text(mixed_result, encoding='utf-8')
            
            print(f"Success! Mixed version delivered to: {output_path}")
            print("\n--- Preview ---")
            print(mixed_result[:400] + "...")
            print("--- End Preview ---")

if __name__ == "__main__":
    main()