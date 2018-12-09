import csv

def load_csv(filename):
    lines = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for line in reader:
            lines.append(line)
    return lines

def load_dept3700027_data():
    return load_csv("../data-cleaned/Trial_SUBJECTROLE.csv")
    # return load_csv("./Trial_change_EstLatLong_TOSAVE.csv")

#TODO: Possibly use different data for training and validation
def load_dept3700027_train_data():
    data = load_dept3700027_data()
    partition = round(.9*len(data))
    train_set = data[:partition]
    return train_set

def load_dept3700027_valid_data():
    data = load_dept3700027_data()
    partition = round(.9*len(data))
    return data[partition:]

