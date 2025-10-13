#!/opt/homebrew/bin/python3
import csv, pandas

def load_data_naive():
    data = []
    datafname = 'weather_data.csv'
    with open(datafname) as datafile:
        for line in datafile:
            data.append(line.split())

    print(f"loaded CSV data: {data}")
    return data

def load_dataframe():
    datafname = 'weather_data.csv'
    dataframe = pandas.read_csv(datafname)
    return dataframe

def load_csv_data():
    data = []
    datafname = 'weather_data.csv'
    with open(datafname) as datafile:
        csv_reader = csv.reader(datafile)
        for row in csv_reader:
            data.append(row)
    print(f"loaded CSV data: {data}")
    return data

def print_tempratures(data):
    print("printing all the temperatures in the dataset")
    for row in data:
        print(row[1])
    
def main():
    data = load_dataframe()
    print(data)

    #data = load_csv_data()
    #print_tempratures(data[1:])

    #data = load_data_naive()

if __name__ == "__main__":
    main()
