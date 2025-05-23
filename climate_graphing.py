import matplotlib.pyplot as plt
import csv

def translate_climate_var(var):
    translations = {
        't': 'Avg Temp (°C)',
        'tx': 'Avg Max Daily Temp (°C)',
        'txx': 'Highest Max Temp (°C)',
        'txxD1': 'Day of Highest Max Temp (°C)',
        'tn': 'Avg Min Daily Temp (°C)',
        'tnn': 'Lowest Min Temp (°C)',
        'tnnD1': 'Day of Lowest Min Temp (°C)',
        'rh': 'Avg Relative Humidity (%)',
        'r': 'Total Precipitation (mm)',
        'rx': 'Max 24-Hour Precipitation (mm)',
        'rxD1': 'Day of Max Precipitation (mm)',
        'p': 'Avg Sea Level Pressure (mb)',
        'nh': 'Avg Cloud Cover (Oktas)',
        'sun': 'Bright Sunshine Hours',
        'f': 'Avg Wind Speeds (m/s)'
    }
    
    return translations[var]
    
def get_csv_data(input_file):
    
    with open(input_file, 'r') as file:
        data = csv.reader(file)
        next(data) # skip name header
        rows = [row for row in data]
        return rows

def get_avail_years(data):
    data = data[1:]
    begin_year = data[0][1]
    end_year = data[-1][1]
    return begin_year, end_year

def get_start_end_index(data, range_start_year, range_end_year):
    start_index = None
    for i, row in enumerate(data[1:]):
        if float(row[1]) == float(range_start_year):
            start_index = i + 1
            break
        
    end_index = None
    for i, row in enumerate(data[1:]):
        if float(row[1]) == float(range_end_year):
            end_index = i + 1
    
    return start_index, end_index

def extract_climate_data(data, climate, index_start, index_end):
    climate_index = None
    for i, item in enumerate(data[0]):
        if str(item) == str(climate):
            climate_index = i

    sliced_data = data[index_start:index_end + 1]

    climate_data = []
    for row in sliced_data:
        year = row[1]
        month = int(row[2])
        value = None if row[climate_index] == 'NA' else float(row[climate_index])
        climate_data.append([year, month, value])

    complete_data = []
    i = 0
    while i < len(climate_data):
        current_year = climate_data[i][0]
        expected_months = list(range(1, 13))
        current_month_index = 0

        while current_month_index < 12:
            if i < len(climate_data) and climate_data[i][0] == current_year:
                actual_month = climate_data[i][1]
                if actual_month == expected_months[current_month_index]:
                    complete_data.append([current_year, f"{actual_month:02}", climate_data[i][2]])
                    i += 1
                else:
                    complete_data.append([current_year, f"{expected_months[current_month_index]:02}", None])
            else:
                complete_data.append([current_year, f"{expected_months[current_month_index]:02}", None])
            current_month_index += 1

    for j in range(len(complete_data)):
        if complete_data[j][2] is None:
            prev_idx = j - 1
            while prev_idx >= 0 and complete_data[prev_idx][2] is None:
                prev_idx -= 1

            next_idx = j + 1
            while next_idx < len(complete_data) and complete_data[next_idx][2] is None:
                next_idx += 1

            if 0 <= prev_idx < len(complete_data) and 0 <= next_idx < len(complete_data):
                prev_val = complete_data[prev_idx][2]
                next_val = complete_data[next_idx][2]
                gap_size = next_idx - prev_idx
                step = (next_val - prev_val) / gap_size
                complete_data[j][2] = prev_val + step * (j - prev_idx)
            else:
                complete_data[j][2] = 0.0

    return complete_data

def get_one_file_data(file, climate):
    data = get_csv_data(file)
    
    begin_year, end_year = get_avail_years(data)
    
    print(f"Year range: {begin_year}-{end_year}")
    range_start_year = input("Choose year range start:")
    range_end_year = input("Choose year range end:")

    start_index, end_index = get_start_end_index(data, range_start_year, range_end_year)

    climate_data = extract_climate_data(data, climate, start_index, end_index)

    return climate_data

def get_two_files_data(file1, file2, climate):
    data1 = get_csv_data(file1)
    data2 = get_csv_data(file2)
    
    begin_year1, end_year1 = get_avail_years(data1)
    begin_year2, end_year2 = get_avail_years(data2)
    
    overlap = f"{max([begin_year1, begin_year2])}-{min([end_year1, end_year2])}"
    print(f"Both files overlap between: {overlap}")

    range_start_year = input("Choose year range start:")
    range_end_year = input("Choose year range end:")

    start_index1, end_index1 = get_start_end_index(data1, range_start_year, range_end_year)
    start_index2, end_index2 = get_start_end_index(data2, range_start_year, range_end_year)

    climate_data1 = extract_climate_data(data1, climate, start_index1, end_index1)
    climate_data2 = extract_climate_data(data2, climate, start_index2, end_index2)

    return climate_data1, climate_data2

def plot_one_file(data, name, climate_var):

    name = name.split('/')[1].split('.')[0].split('_')[0]
    
    x_vals = [f"{row[1]}/{row[0][2:]}" for row in data]
    y_vals = [float(row[2]) for row in data]

    y_label = translate_climate_var(climate_var)
    
    plt.figure(figsize=(10, 5))
    plt.plot(x_vals, y_vals, color='blue', marker='.', ms=10, label=name)

    plt.xticks(rotation=45)
    plt.xlabel("Date (MM/YY)")
    plt.ylabel(y_label)
    plt.title(name)
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def plot_two_files(data1, data2, name1, name2, climate_var):

    name1 = name1.split('/')[1].split('.')[0].split('_')[0]
    name2 = name2.split('/')[1].split('.')[0].split('_')[0]
    
    x_vals1 = [f"{row[1]}/{row[0][2:]}" for row in data1]
    y_vals1 = [float(row[2]) for row in data1]

    x_vals2 = [f"{row[1]}/{row[0][2:]}" for row in data2]
    y_vals2 = [float(row[2]) for row in data2]

    y_label = translate_climate_var(climate_var)
    
    plt.figure(figsize=(10, 5))
    plt.plot(x_vals1, y_vals1, color='blue', marker='.', ms=10, label=name1)
    plt.plot(x_vals2, y_vals2, color='red', marker='.', ms=10, label=name2)

    plt.xticks(rotation=45)
    plt.xlabel("Date (MM/YY)")
    plt.ylabel(y_label)
    plt.title(f"{name1} vs {name2}")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

# do the stuff with the stuff
if __name__ == "__main__":
    #file1, file2, climate_var = "station_data/dalatangi.csv", "station_data/seydisfjordur.csv", "f"
    #data1, data2 = get_two_files_data(file1, file2, climate_var)
    #plot_two_files(data1, data2, file1, file2, climate_var)
    file, climate_var = "station_data/dalatangi.csv", "t"
    data = get_one_file_data(file, climate_var)
    plot_one_file(data, file, climate_var)
