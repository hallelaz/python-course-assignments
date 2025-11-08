"""
pcr_interactive calculates results from user input.
"""

def main():
    print("PCR Amplification Calculator")
    cycles = int(input("Enter the number of PCR cycles: "))
    final_strands = (2 ** cycles)
    print(f"After {cycles} cycles, there will be approximately {final_strands:,} DNA strands.")

if __name__ == "__main__":
    main()

