import pandas as pd
from pathlib import Path
import argparse

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Convert CSV to Excel format.')
    parser.add_argument(
        'csv_file',
        nargs='?',
        default='influencers_2000_profiles_final_corrected.csv',
        help='Path to the CSV file to convert.',
    )
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    csv_file = Path(args.csv_file)
    if not csv_file.exists():
        print(f'Error: {csv_file} not found')
        exit(1)

    df = pd.read_csv(csv_file)
    excel_file = Path('influencer_analysis_2000_profiles.xlsx')

    df.to_excel(excel_file, index=False)
    print(f'Created {excel_file}')
