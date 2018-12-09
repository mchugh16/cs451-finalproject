# CS 451 Final Project
# Mira Chugh and Julia Jaschke
# based on an assignment by Joe Redmon, our HW 5

from math import exp
import random


# Calculate logistic
def logistic(x):

    return (1/(1+exp(-x)))

# Calculate dot product of two lists
def dot(x, y):
    s = 0.0
    for i in range(0,len(x)):
        s += x[i] * y[i]
    return s

# Calculate prediction based on model
def predict(model, point):
    # to predict new points multiply model's weights by 
    # the corresponding features, sum up the result, 
    # and pass it through the logistic function. 
    result = dot(model, point['features'])
    return logistic(result)

# Calculate accuracy of predictions on data
def accuracy(data, predictions):
    # values should be between 0 and 1, if < .5 --> 0, if > .5 --> 1
    # label on point is 0 or 1
    # correct = if label and prediction match

    correct = 0
    for point in range(0, len(data)):
        correct_label = data[point]['label'] 
        if predictions[point] <= .5:
            if correct_label == 0:
                correct += 1
        else:
            if correct_label == 1:
                correct+=1
    print("CORRECT: " + str(correct))
    return float(correct)/len(data)


# Update model using learning rate alpha and regularization lamba
def update(model, point, alpha, lambd):

    # compute h(x) - y only once - before updating theta0's
    prediction = predict(model, point)

    for j in range(0, len(model)):
        theta = model[j]
        xj = point["features"][j]
        error = (prediction - point["label"]) * (xj)

        # regularize everything except for theta 0
        regularization = 0
        if j!=0:
            regularization = (lambd*theta)

        model[j] = theta - alpha*(error + regularization)

    return model


# Initialize model with k random numbers that follow gaussian distribution
# so intital values have mean 0, sd 1
def initialize_model(k):
    return [random.gauss(0, 1) for x in range(k)]

# Train model using training data
def train(data, epochs, alpha, lambd):
    m = len(data) # number of training examples
    n = len(data[0]['features']) # number of features (+ 1)
    model = initialize_model(n)
    print("epoch=0 alpha=", alpha )
    for epoch in range(0, epochs):

        # adjust learning rate - when updating for each training ex vs. 
        # all training ex at once, accuracy can bounce around 
        # to make sure it converges - decrease alpha 
        alpha -= (alpha * .7)

        # update model based on m points for each epoch
        for point in range(0, m):

            # choose a random point from dataset
            random_num = random.randint(0, m-1)
            random_point = data[random_num]


            #update the model
            model = update(model, random_point, alpha, lambd)

        # print accuracy after each epoch 
        predictions = [predict(model, p) for p in data]
        print()
        print()
        # print("PREDICTIONS")
        # print(predictions)
        # print("num predictions = 1: " + str(num_predictions))
        print("epoch=", epoch, " alpha= ", round(alpha, 4), " Accuracy=", accuracy(data, predictions))

    return model



def extract_features(raw):
    data = []
    for r in raw:
        features = []
        features.append(1.0)

        # race features
        features.append(float(r['SUBJECT_RACE'] == '1'))
        features.append(float(r['SUBJECT_RACE'] == '2'))
        features.append(float(r['SUBJECT_RACE'] == '3'))
        features.append(float(r['SUBJECT_RACE'] == '4'))
        features.append(float(r['SUBJECT_RACE'] == '5'))

        # # gender features
        # features.append(float(r['SUBJECT_GENDER'] == '1'))
        # features.append(float(r['SUBJECT_GENDER'] == '2'))

        # #added location (street address) as a feature
        # # for i in range(3146):
        # #     features.append(float(r['LOCATION_FULL_STREET_ADDRESS_OR_INTERSECTION'] == str(i)))

        # #added subject description as a feature
        # features.append(float(r['SUBJECT_DESCRIPTION'] == "0"))
        # features.append(float(r['SUBJECT_DESCRIPTION'] == "1"))
        # features.append(float(r['SUBJECT_DESCRIPTION'] == "2"))

        # features.append(float(r['INCIDENT_REASON'] == "0"))
        # features.append(float(r['INCIDENT_REASON'] == "1"))
        # features.append(float(r['INCIDENT_REASON'] == "2"))
        # features.append(float(r['INCIDENT_REASON'] == "3"))
        # features.append(float(r['type_employer'] == {'State-gov'}))
        # features.append(float(r['type_employer'] == {'Without-pay'}))
        # features.append(float(r['type_employer'] == {'Never-worked'}))
        
        # years on force
        # features.append(float(r['OFFICER_YEARS_ON_FORCE']) < 10)
        # features.append(float(r['OFFICER_YEARS_ON_FORCE']) < 5)
        # features.append(float(r['OFFICER_YEARS_ON_FORCE']) >15)

        # features.append(float(r['LOCATION_DISTRICT'] == 1))
        # features.append(float(r['LOCATION_DISTRICT'] == "AP"))
        # features.append(float(r['LOCATION_DISTRICT'] == "BA"))
        # features.append(float(r['LOCATION_DISTRICT'] == "CH"))
        # features.append(float(r['LOCATION_DISTRICT'] == "DA"))
        # features.append(float(r['LOCATION_DISTRICT'] == "ED"))
        # features.append(float(r['LOCATION_DISTRICT'] == "FR"))
        # features.append(float(r['LOCATION_DISTRICT'] == "GE"))
        # features.append(float(r['LOCATION_DISTRICT'] == "HE"))
        # features.append(float(r['LOCATION_DISTRICT'] == "ID"))
        
        # features.append(float(r['SUBJECT_DESCRIPTION'] == "SUSPECTED UNDER INFLUENCE OF ALCOHOL/DRUGS"))
        # features.append(float(r['SUBJECT_DESCRIPTION'] == "EDP/MENTALLY UNSTABLE; SUSPECTED UNDER INFLUENCE OF ALCOHOL/DRUGS"))
        # features.append(float(r['SUBJECT_DESCRIPTION'] == "EDP/MENTALLY UNSTABLE"))



        point = {}
        point['features'] = features
        print(features)
        point['label'] = int(r['SUBJECT_GENDER'] == "0")
        data.append(point)

        # print out how many times it predicts 0 and 1 

    return data

# TODO: Tune your parameters for final submission
def submission(data):
    return train(data, epochs=20, alpha=2, lambd= .001)
