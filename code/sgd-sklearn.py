from sklearn.linear_model import SGDClassifier
import csv
import numpy as np 
import pandas as pd


def main():
	train_data = load_dept3700027_train_data()
	valid_data = load_dept3700027_valid_data()
	var_to_predict = 'SUBJECT_ROLE'

	# create training data
	X_train = extract_features(train_data)
	print(len(X_train))
	y_train = get_labels(train_data)
	print(len(y_train))

	# create cv
	X_valid = extract_features(valid_data)
	y_valid = get_labels(valid_data)


	clf = SGDClassifier(loss="log", penalty="l2", max_iter=1000)
	clf.fit(X_train, y_train)
	print(clf.coef_)


	print ("Train")
    sgd = SGDClassifier(loss="log", penalty="l2", max_iter=1000)
    sgd=sgd.fit(np.array(X_train),np.array(y_train))



    print ("Predict")
    test_labels=sgd.predict(np.array(X_valid))

    predictions_file = open("simple_sgd_result.csv", "w")
    open_file_object = csv.writer(predictions_file)
    open_file_object.writerow(["ID", "PredictedProb"])
    open_file_object.writerows(zip(test_id,test_labels))
    predictions_file.close()

def get_labels(raw):
	data = []
	for r in raw:
		label = int(r['SUBJECT_ROLE'] == "1")
		data.append(label)
	return data

def extract_features(raw):
	data = []
	for r in raw:
		features = []

		# race features
		features.append(float(r['SUBJECT_RACE'] == '1'))
		features.append(float(r['SUBJECT_RACE'] == '2'))
		features.append(float(r['SUBJECT_RACE'] == '3'))
		features.append(float(r['SUBJECT_RACE'] == '4'))
		features.append(float(r['SUBJECT_RACE'] == '5'))

		# gender features
		features.append(float(r['SUBJECT_GENDER'] == '1'))
		features.append(float(r['SUBJECT_GENDER'] == '2'))

		#added subject description as a feature
		features.append(float(r['SUBJECT_DESCRIPTION'] == "0"))
		features.append(float(r['SUBJECT_DESCRIPTION'] == "1"))
		features.append(float(r['SUBJECT_DESCRIPTION'] == "2"))

		features.append(float(r['INCIDENT_REASON'] == "0"))
		features.append(float(r['INCIDENT_REASON'] == "1"))
		features.append(float(r['INCIDENT_REASON'] == "2"))
		features.append(float(r['INCIDENT_REASON'] == "3"))

		data.append(features)
	return data

def load_csv(filename):
	lines = []
	with open(filename) as csvfile:
		reader = csv.DictReader(csvfile)
		for line in reader:
			lines.append(line)
	return lines

def load_dept3700027_data():
	return load_csv("../data-cleaned/Trial_SUBJECTROLE.csv")

def load_dept3700027_train_data():
	data = load_dept3700027_data()
	partition = round(.9*len(data))
	train_set = data[:partition]
	return train_set

def load_dept3700027_valid_data():
	data = load_dept3700027_data()
	partition = round(.9*len(data))
	return data[partition:]

if __name__ == '__main__':
	main()
