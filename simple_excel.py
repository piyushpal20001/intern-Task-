import pandas as pd
from pathlib import Path
csv_file = "influencers_2000_profiles_final_corrected.csv"
excel_file = Path('influencer_analysis_2000_profiles.xlsx')

df = pd.read_csv(csv_file)
df.to_excel(excel_file, index=False)

print(f'Created {excel_file}')