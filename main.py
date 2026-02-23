import re
import random
from datetime import datetime
from pathlib import Path

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
    
    # Using Path objects for directory management
    base_dir = Path(__file__).parent
    input_folder = base_dir / "input"
    output_folder = base_dir / "outputs"
    
    # Ensure folders exist
    output_folder.mkdir(exist_ok=True)
    if not input_folder.exists():
        input_folder.mkdir()
        print(f"[*] Created '{input_folder.name}' folder. Please place your source files there.")

    while True:
        # 1. Get Filename Input
        raw_input = input("\nEnter the filename (or 'q' to quit): ").strip()
        
        # Edge Case Refinement: Catch empty strings
        if not raw_input:
            continue
            
        if raw_input.lower() == 'q':
            print("Exiting mixer. Goodbye!")
            break

        # Pathlib makes joining and checking existence very readable
        input_path = input_folder / raw_input

        # 2. Check if file exists and is a file
        if not input_path.is_file():
            print(f"[!] Error: '{raw_input}' not found in the '{input_folder.name}' directory.")
            continue

        # 3. Get and Validate Granularity Input
        try:
            g_input = input("Enter granularity (1-9): ").strip()
            if not g_input:
                continue
            g = int(g_input)
            if not (1 <= g <= 9):
                print("[!] Error: Granularity must be between 1 and 9.")
                continue
        except ValueError:
            print("[!] Error: Please enter a valid whole number for granularity.")
            continue

        # 4. Process the Mix
        time_str = datetime.now().strftime("%Y%m%d_%H%M")
        print(f"--- Mixing '{input_path.name}' with Granularity g={g} ---")
        
        mixed_result = mix_text(input_path, g)

        if mixed_result:
            # Construct output filename using Path object features
            output_filename = f"mixed_g{g}_{time_str}_{input_path.name}"
            output_path = output_folder / output_filename
            
            output_path.write_text(mixed_result, encoding='utf-8')
            
            print(f"Success! Mixed version delivered to: {output_path}")
            print("\n--- Preview ---")
            print(mixed_result[:400] + "...")
            print("--- End Preview ---")

if __name__ == "__main__":
    main()