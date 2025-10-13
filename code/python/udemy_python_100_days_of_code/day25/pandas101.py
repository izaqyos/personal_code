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

def type_checks(data):
    print(f"dataframe type is {type(data)}, temperature column type is {type(data['temp'])}")
    
def columns_work_demo(data):
    print("Panda. work on columns")
    print(f"mean temperature: {data['temp'].mean()}")
    print(f"max temperature: {data.temp.max()}") #cal call column as a property (like in JS) or as dictionary by key as above

def rows_work_demo(data):
    print("Panda. work on rows")
    print(data[data.day == 'Monday'])
    print(f"day in which temp was maximal: {data[data.temp == data.temp.max()]}")
    print("Extract a specific column from a specific row. say Monday row...")
    monday = data[data.day == 'Monday']
    print(monday.condition)
    print(f"convert Monday temperature from celsios to fahrenheit: {monday.temp*(9/5)+32}")

def working_with_data_frames(data):
    print("Create a DataFrame (table) from a dictionary")
    df_dict = {
            "kids": ["May", "Itay", "Kay", "Aimy"],
            "birthdates": ["14.03.2007", "21.06.2011", "08.06.2014", "02.03.2016"]
            }
    kids_df = pandas.DataFrame(df_dict)
    print(f"Created kids bdays DataFrame\n {kids_df}")
    print("Saving DataFrame to .csv file...")
    kids_df.to_csv("KidsBdays.csv")
    print("contents of csv file:")
    with open("KidsBdays.csv") as csv:
        lines = csv.readlines()
    print(lines)

def main():
    data = load_dataframe()
    print(data)
    type_checks(data)
    json_data = data.to_json()
    print(json_data)

    columns_work_demo(data)
    rows_work_demo(data)
    working_with_data_frames(data)

    



    #data = load_csv_data()
    #print_tempratures(data[1:])

    #data = load_data_naive()

if __name__ == "__main__":
    main()
