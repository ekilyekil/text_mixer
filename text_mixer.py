import os
import glob
import sys
import re
import random
from datetime import datetime
from pathlib import Path
from rich.console import Console
console = Console()

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
            console.print(f"\n[bold red][!] No words found in {file_path.name}.[/bold red]")
            return None

        # Partition into chunks of size 'g'
        chunks = ["".join(units[i:i + granularity]) for i in range(0, len(units), granularity)]

        # The core randomisation step
        random.shuffle(chunks)

        return "".join(chunks)

    except FileNotFoundError:
        console.print(f"\n[bold red][!] Error: The file at {file_path} was not found.[/bold red]")
        return None
    except Exception as e:
        console.print(f"\n[bold red][!] An unexpected error occurred: {e}[/bold red]")
        return None

def main():
    console.print("\n[bold magenta]=== Persistent Text Mixer (2026 Edition) ===[/bold magenta]")
    
    if not INPUT_DIR.exists():
        INPUT_DIR.mkdir()
        console.print(f"[bold yellow][*] Created '{INPUT_DIR.name}' folder.[/bold yellow] Please place your source files there.")

    input_files = glob.glob(str(INPUT_DIR / "*.*"))
    if not input_files:
        console.print("[bold red][!] Error: No files found in the 'input/' directory.[/bold red]")
        sys.exit(1)
    latest_file = max(input_files, key=os.path.getmtime)
    input_path = Path(latest_file)
    
    console.print(f"[bold cyan][*] Drop-and-Go selected latest file:[/bold cyan] {input_path.name}")

    while True:
        # 1. Get and Validate Granularity Input
        try:
            g_input = input("\nEnter granularity (1-9) or 'q' to quit: ").strip()
            if not g_input:
                continue
            if g_input.lower() == 'q':
                console.print("[bold magenta]Exiting mixer. Goodbye![/bold magenta]")
                break
            g = int(g_input)
            if not (1 <= g <= 9):
                console.print("[bold red][!] Error: Granularity must be between 1 and 9.[/bold red]")
                continue
        except ValueError:
            console.print("[bold red][!] Error: Please enter a valid whole number for granularity.[/bold red]")
            continue

        # 2. Process the Mix
        time_str = datetime.now().strftime("%Y%m%d_%H%M")
        console.print(f"\n[bold blue]--- Mixing '{input_path.name}' with Granularity g={g} ---[/bold blue]")
        
        mixed_result = mix_text(input_path, g)

        if mixed_result:
            output_filename = f"mixed_g{g}_{time_str}_{input_path.name}"
            output_path = OUTPUT_DIR / output_filename
            
            output_path.write_text(mixed_result, encoding='utf-8')
            
            console.print(f"[bold green]✓ Success![/bold green] Mixed version delivered to: [cyan]{output_path}[/cyan]")
            console.print("\n[bold yellow]--- Preview ---[/bold yellow]")
            console.print(mixed_result[:400] + "...")
            console.print("[bold yellow]--- End Preview ---[/bold yellow]")

if __name__ == "__main__":
    main()