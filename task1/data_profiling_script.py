import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(filename='data_profiling.log', level=logging.DEBUG, filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def is_numeric(series):
    """ Check if a pandas Series is numeric """
    return np.issubdtype(series.dtype, np.number)

def calculate_statistics(data, column):
    """ Calculate statistics for a given column """
    return {
        f'Min({column})': data[column].min(),
        f'Max({column})': data[column].max(),
        f'Sum({column})': data[column].sum(),
        f'Avg({column})': data[column].mean()
    }

def profile_data(file_path):
    try:
        # Attempt to read the CSV file
        try:
            data = pd.read_csv(file_path)
        except FileNotFoundError:
            logging.error(f"File not found: {file_path}")
            return None
        except pd.errors.EmptyDataError:
            logging.error(f"No data: {file_path}")
            return None
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {e}")
            return None

        result = {'File Name': Path(file_path).name, 'Path': file_path}

        # Process each column
        for column in data.columns:
            if is_numeric(data[column]):
                try:
                    result.update(calculate_statistics(data, column))
                except Exception as e:
                    logging.warning(f"Error processing column {column}: {e}")

        # Record count
        result['Record Count'] = len(data)
        return result

    except Exception as e:
        logging.error(f"Unexpected error in profile_data: {e}")
        return None

def write_results_to_csv(result, output_file='result.csv'):
    """ Write the profiling results to a CSV file """
    try:
        pd.DataFrame([result]).to_csv(output_file, index=False)
        logging.info(f"Data profiling results written to {output_file}")
    except Exception as e:
        logging.error(f"Error writing results to {output_file}: {e}")

def main():
    file_path = 'Video-Games-Sales.csv'  # File path
    result = profile_data(file_path)

    if result:
        write_results_to_csv(result)

if __name__ == "__main__":
    main()
