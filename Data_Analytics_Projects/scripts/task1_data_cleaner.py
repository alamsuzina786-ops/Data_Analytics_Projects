import pandas as pd
import numpy as np

# File paths
input_file = "data/messy_employee_dataset.csv"
output_file = "output/cleaned_employee_data.csv"
report_file = "output/cleaning_report.csv"

# Load dataset
df = pd.read_csv(input_file)

print("===== DATA CLEANER & PROFILER =====")
print("Original Shape:", df.shape)

# Missing values before cleaning
missing_before = df.isnull().sum().sum()

# Duplicate rows
duplicates = df.duplicated().sum()

# Remove duplicates
df = df.drop_duplicates()

# Clean text columns
text_columns = df.select_dtypes(include="object").columns
df[text_columns] = df[text_columns].apply(lambda x: x.str.strip())

# Convert numeric columns
if "Age" in df.columns:
    df["Age"] = pd.to_numeric(df["Age"], errors="coerce")

if "Salary" in df.columns:
    df["Salary"] = pd.to_numeric(df["Salary"], errors="coerce")

# Convert date column
if "Join_Date" in df.columns:
    df["Join_Date"] = pd.to_datetime(df["Join_Date"], errors="coerce")

# Handle missing values
for column in df.columns:
    if df[column].isnull().any():
        if pd.api.types.is_numeric_dtype(df[column]):
            df[column] = df[column].fillna(df[column].median())
        else:
            df[column] = df[column].fillna("Unknown")

# Save cleaned dataset
df.to_csv(output_file, index=False)

# Create summary report
report = pd.DataFrame({
    "Metric": [
        "Original Rows",
        "Final Rows",
        "Columns",
        "Duplicates Removed",
        "Missing Values Before Cleaning"
    ],
    "Value": [
        len(pd.read_csv(input_file)),
        len(df),
        len(df.columns),
        duplicates,
        missing_before
    ]
})

report.to_csv(report_file, index=False)

print("\n===== CLEANING COMPLETED =====")
print("Final Shape:", df.shape)
print("Duplicates Removed:", duplicates)
print("Missing Values Before:", missing_before)
print("\nCleaned file:", output_file)
print("Report file:", report_file)