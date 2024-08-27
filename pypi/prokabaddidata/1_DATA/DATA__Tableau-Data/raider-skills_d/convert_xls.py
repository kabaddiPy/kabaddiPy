import os
import pandas as pd
import argparse

def convert_excel_to_csv(input_dir):
    # Ensure the input directory exists
    if not os.path.isdir(input_dir):
        print(f"Error: The directory {input_dir} does not exist.")
        return

    # Get all Excel files in the directory
    excel_files = [f for f in os.listdir(input_dir) if f.endswith(('.xlsx', '.xls'))]

    if not excel_files:
        print(f"No Excel files found in {input_dir}")
        return

    for excel_file in excel_files:
        # Construct full file paths
        excel_path = os.path.join(input_dir, excel_file)
        csv_path = os.path.join(input_dir, os.path.splitext(excel_file)[0] + '.csv')

        try:
            # Read the Excel file
            df = pd.read_excel(excel_path)

            # Write to CSV
            df.to_csv(csv_path, index=False)
            print(f"Converted {excel_file} to CSV successfully.")
        except Exception as e:
            print(f"Error converting {excel_file}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Convert Excel files to CSV in a directory")
    parser.add_argument("input_dir", help="Path to the directory containing Excel files")
    args = parser.parse_args()

    convert_excel_to_csv(args.input_dir)

if __name__ == "__main__":
    main()