from __future__ import print_function
from unittest import TestCase
import unittest
from sgd_final import logistic, dot, predict, accuracy, update, submission, extract_features
from data_final import load_dept3700027_train_data, load_dept3700027_valid_data


class SGDTest(unittest.TestCase):

    def test_submission(self):
    	# train_data = load_dept3700027_train_data()
        # print("Length training data")
        # print(len(train_data))

        # valid_data = load_dept3700027_valid_data()
        # print("Length validation data")
        # print(len(valid_data))
        
        train_data = extract_features(load_dept3700027_train_data())
        valid_data = extract_features(load_dept3700027_valid_data())
        model = submission(train_data)
        predictions = [predict(model, p) for p in train_data]
        print("Training Accuracy:", accuracy(train_data, predictions))
        predictions = [predict(model, p) for p in valid_data]
        print("Validation Accuracy:", accuracy(valid_data, predictions))



if __name__ == '__main__':
    unittest.main()
