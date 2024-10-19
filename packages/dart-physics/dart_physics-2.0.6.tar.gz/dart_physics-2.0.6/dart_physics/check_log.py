import time
import os
from pathlib import Path

def follow(file_path):
    with open(file_path, 'r') as file:
        # Move to the end of the file
        file.seek(0, 2)
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)  # Sleep briefly
                continue
            yield line

def main():
    # Get the directory of the current script
    current_dir = Path(__file__).resolve().parent
    
    # Construct the path to subprocess_output.log
    log_path = current_dir / 'subprocess_output.log'
    
    print(f"Monitoring: {log_path}")
    print("Press Ctrl+C to stop...")
    
    try:
        for line in follow(log_path):
            print(line, end='')
    except KeyboardInterrupt:
        print("\nStopped monitoring.")

if __name__ == "__main__":
    main()