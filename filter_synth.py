import pandas as pd
import os

input_path  = os.path.expanduser('~/Code/bring_data/synth_50k_CT')
output_path = os.path.expanduser('~/Code/bring_data/raw_data')

os.makedirs(output_path, exist_ok=True)

MI_CODES = {22298006, 401303003, 401314000}

# ---------------------------------------------------------------
# Step 1: Identify MI patients and their relevant encounter IDs
# ---------------------------------------------------------------
conditions = pd.read_csv(f'{input_path}/conditions.csv', low_memory=False)

mi_conditions = conditions[conditions['CODE'].isin(MI_CODES)].copy()
mi_ids = mi_conditions['PATIENT'].drop_duplicates()
print(f"  MI patients identified: {len(mi_ids):,}")

# Save conditions for MI patients only (already small at 0.66MB)
mi_conditions.to_csv(f'{output_path}/conditions.csv', index=False)
size_mb = os.path.getsize(f'{output_path}/conditions.csv') / 1_000_000
print(f"  conditions.csv saved: {len(mi_conditions):,} rows | {size_mb:.2f} MB")

# ---------------------------------------------------------------
# Step 2: Patients — trim to MI patients only
# ---------------------------------------------------------------
patients = pd.read_csv(f'{input_path}/patients.csv', low_memory=False)
mi_patients = patients[patients['Id'].isin(mi_ids)]
mi_patients.to_csv(f'{output_path}/patients.csv', index=False)
size_mb = os.path.getsize(f'{output_path}/patients.csv') / 1_000_000
print(f"  patients.csv saved: {len(mi_patients):,} rows | {size_mb:.2f} MB")

# ---------------------------------------------------------------
# Step 3: Encounters — MI patients, ED only, 2014–2024
# (keeping 2014 as a buffer year in case any logic needs it)
# ---------------------------------------------------------------
encounters = pd.read_csv(f'{input_path}/encounters.csv', low_memory=False)
enc_filtered = encounters[
    (encounters['PATIENT'].isin(mi_ids)) &
    (encounters['ENCOUNTERCLASS'] == 'emergency')
].copy()
enc_filtered['year'] = pd.to_datetime(enc_filtered['START']).dt.year
enc_filtered = enc_filtered[enc_filtered['year'].between(2014, 2024)]
enc_filtered = enc_filtered.drop(columns='year')

# Keep the encounter IDs — we'll use these to filter medications/procedures
relevant_encounter_ids = set(enc_filtered['Id'])

enc_filtered.to_csv(f'{output_path}/encounters.csv', index=False)
size_mb = os.path.getsize(f'{output_path}/encounters.csv') / 1_000_000
print(f"  encounters.csv saved: {len(enc_filtered):,} rows | {size_mb:.2f} MB")

# ---------------------------------------------------------------
# Step 4: Medications — only those linked to relevant encounters
# ---------------------------------------------------------------
medications = pd.read_csv(f'{input_path}/medications.csv', low_memory=False)
med_filtered = medications[
    medications['ENCOUNTER'].isin(relevant_encounter_ids)
]
med_filtered.to_csv(f'{output_path}/medications.csv', index=False)
size_mb = os.path.getsize(f'{output_path}/medications.csv') / 1_000_000
print(f"  medications.csv saved: {len(med_filtered):,} rows | {size_mb:.2f} MB")

# ---------------------------------------------------------------
# Step 5: Procedures — only those linked to relevant encounters
# ---------------------------------------------------------------
procedures = pd.read_csv(f'{input_path}/procedures.csv', low_memory=False)
proc_filtered = procedures[
    procedures['ENCOUNTER'].isin(relevant_encounter_ids)
]
proc_filtered.to_csv(f'{output_path}/procedures.csv', index=False)
size_mb = os.path.getsize(f'{output_path}/procedures.csv') / 1_000_000
print(f"  procedures.csv saved: {len(proc_filtered):,} rows | {size_mb:.2f} MB")

# ---------------------------------------------------------------
# Sanity checks
# ---------------------------------------------------------------
print("ED encounters by year (2015-2024):")
enc_check = pd.read_csv(f'{output_path}/encounters.csv', low_memory=False)
enc_check['year'] = pd.to_datetime(enc_check['START']).dt.year
print(enc_check.groupby('year').size().to_string())

print("Medications found (top 15 by frequency):")
med_check = pd.read_csv(f'{output_path}/medications.csv', low_memory=False)
print(med_check['DESCRIPTION'].value_counts().head(15).to_string())

print("Procedures found (top 15 by frequency):")
proc_check = pd.read_csv(f'{output_path}/procedures.csv', low_memory=False)
print(proc_check['DESCRIPTION'].value_counts().head(15).to_string())

print("Final file sizes:")
for f in sorted(os.listdir(output_path)):
    size_mb = os.path.getsize(os.path.join(output_path, f)) / 1_000_000
    print(f"  {f:<30} {size_mb:>8.2f} MB")