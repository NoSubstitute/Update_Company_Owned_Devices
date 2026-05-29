
import sys
import csv
import argparse

def find_missing_devices(file1_path, col1_index, file2_path, col2_index, output_path, asset_tag_col_index=None, asset_tag_static_val=None):
    """
    Compares two CSV files and finds new devices from the second file.
    The output CSV will contain the new device ID and a corresponding asset tag.

    Args:
        file1_path (str): Path to the first CSV file (the reference list).
        col1_index (int): The 0-based index of the column to compare in file1.
        file2_path (str): Path to the second CSV file (the list that may have new devices).
        col2_index (int): The 0-based index of the column to compare in file2.
        output_path (str): Path to write the CSV of missing devices.
        asset_tag_col_index (int, optional): 0-based index of the column in file2 to use for the asset tag.
        asset_tag_static_val (str, optional): A static string to use for all asset tags.
    """
    try:
        # Step 1: Read all unique IDs from file1 into a set.
        existing_ids = set()
        with open(file1_path, 'r', newline='', encoding='utf-8') as f1:
            reader = csv.reader(f1)
            next(reader)  # Skip header
            for row in reader:
                if len(row) > col1_index:
                    existing_ids.add(row[col1_index])

        # Step 2: Find new devices in file2 and prepare the corresponding output rows.
        output_rows = []
        with open(file2_path, 'r', newline='', encoding='utf-8') as f2:
            reader = csv.reader(f2)
            next(reader)  # Skip header
            for row in reader:
                if len(row) > col2_index:
                    device_id = row[col2_index]
                    if device_id not in existing_ids:
                        asset_tag = ""  # Default empty asset tag
                        if asset_tag_col_index is not None:
                            if len(row) > asset_tag_col_index:
                                asset_tag = row[asset_tag_col_index]
                        elif asset_tag_static_val is not None:
                            asset_tag = asset_tag_static_val
                        
                        output_rows.append([device_id, asset_tag])

        # Step 3: Write the new devices and their asset tags to the output file.
        if output_rows:
            output_header = ["Serial Number", "Asset Tag"]
            with open(output_path, 'w', newline='', encoding='utf-8') as f_out:
                writer = csv.writer(f_out)
                writer.writerow(output_header)
                writer.writerows(output_rows)
        
        print(f"Found {len(output_rows)} new devices.")
        if output_rows:
            print(f"List of new devices saved to '{output_path}'")

    except FileNotFoundError as e:
        print(f"Error: File not found - {e.filename}")
    except IndexError:
        print(f"Error: A specified column index is out of range for a row in one of the files.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find new devices in file2 that are not in file1.")
    
    # Positional arguments
    parser.add_argument("file1", help="The first CSV file (reference list).")
    parser.add_argument("col1", type=int, help="1-based column number for device IDs in file1.")
    parser.add_argument("file2", help="The second CSV file (may contain new devices).")
    parser.add_argument("col2_id", type=int, help="1-based column number for device IDs in file2.")
    parser.add_argument("output", help="The output CSV file for new devices.")

    # Mutually exclusive group for asset tag options
    asset_group = parser.add_mutually_exclusive_group()
    asset_group.add_argument("--asset-tag-value", help="A static string to use for the 'Asset Tag' column.")
    asset_group.add_argument("--asset-tag-column", type=int, help="1-based column number from file2 to use for the 'Asset Tag'.")

    args = parser.parse_args()

    # Convert 1-based column numbers to 0-based indices
    col1_index = args.col1 - 1
    col2_id_index = args.col2_id - 1
    asset_col_index = args.asset_tag_column - 1 if args.asset_tag_column is not None else None

    find_missing_devices(
        args.file1, 
        col1_index, 
        args.file2, 
        col2_id_index, 
        args.output, 
        asset_tag_col_index=asset_col_index, 
        asset_tag_static_val=args.asset_tag_value
    )
