
import csv
import sys

def remove_duplicate_serials(input_file, output_file):
    """
    Reads a CSV file, removes rows with duplicate serial numbers, and saves the result to a new CSV file.

    This implementation uses only Python's built-in csv module.

    Args:
        input_file (str): The name of the input CSV file.
        output_file (str): The name of the output CSV file for the deduplicated data.
    """
    try:
        with open(input_file, 'r', newline='') as infile, open(output_file, 'w', newline='') as outfile:
            reader = csv.reader(infile)
            writer = csv.writer(outfile)

            header = next(reader)
            writer.writerow(header)

            try:
                serial_number_index = header.index('serialNumber')
            except ValueError:
                print(f"Error: 'serialNumber' column not found in '{input_file}'.")
                return

            seen_serials = set()
            duplicates_removed = 0
            
            for row in reader:
                if row: # handle empty rows
                    serial = row[serial_number_index]
                    if serial not in seen_serials:
                        writer.writerow(row)
                        seen_serials.add(serial)
                    else:
                        duplicates_removed += 1
            
            print(f"Removed {duplicates_removed} duplicate rows.")
            print(f"Deduplicated data saved to '{output_file}'")

    except FileNotFoundError:
        print(f"Error: Default or supplied file name '{input_file}' not found. Make sure the file is in the correct directory.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    if len(sys.argv) == 3:
        # Use filenames provided from the command line
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    elif len(sys.argv) == 1:
        # Use default filenames if no arguments are provided
        input_filename = 'company_devices.csv'
        output_filename = 'company_devices_deduplicated.csv'
    else:
        print("Usage: python3 remove_duplicates.py <input_file.csv> <output_file.csv>")
        print("Or run without arguments to use default 'company_devices.csv'.")
        sys.exit(1)

    remove_duplicate_serials(input_filename, output_filename)
