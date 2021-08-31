from pathlib import Path
import csv

def connect_data():
    current_path = Path(__file__).parent.resolve()
    with open(str(current_path) + "/../movies_raw_v2.csv", 'r'
    , encoding = 'ISO-8859-1') as f:
        reader = csv.reader(f)
        your_list = list(reader)
        return your_list