import sys
from part_a import parta
from part_b import partb
from part_c import partc

def launch(fn):
    window = fn()
    window.mainloop()

while True:
    print("\n--- MENU ---")
    print("1. Part A (N-Queens)")
    print("2. Part B (Connect-4)")
    print("3. Part C (Sudoku CSP)")
    print("4. Exit")
    
    try:
        choice = input("Choice: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting.")
        sys.exit(0)
        
    if choice == '1':
        launch(parta)
    elif choice == '2':
        launch(partb)
    elif choice == '3':
        launch(partc)
    elif choice == '4':
        print("Exiting.")
        sys.exit(0)
