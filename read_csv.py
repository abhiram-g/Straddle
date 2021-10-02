import csv, re

# Connect to file in format 'ind_close_all_<ddmmyyyy>.csv'
def read_index_data(filename, index_name, fields):
    res_dict = {}
    try: 
        with open(filename) as csvfile:
            csv_dict_reader = csv.DictReader(csvfile)
            for row in csv_dict_reader:
                if row['Index Name'] == index_name:
                    res_dict[index_name] = index_name
                    for field in fields:
                        res_dict[field] = float(row[field])
    # If file is not found, return error
    except(FileNotFoundError): 
        print('File '+ filename + ' not found.')
        res_dict['error'] = True
    return res_dict    

# Runs only when the file is run from CLI
if __name__ == '__main__':
    print(read_index_data('data/ind_close_all_01102021.csv', 'Nifty 50', 'High Index Value', 'Low Index Value', 'Closing Index Value'))