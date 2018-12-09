# CS 451 HW 2
# Mira Chugh and Julia Jaschke
# based on an assignment by Joe Redmon

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
		print("epoch=", epoch, " alpha= ", round(alpha, 4), " Accuracy=", accuracy(data, predictions))

	return model


# Extract features from raw data	
def extract_features(raw):	
	data = []
	for r in raw:
		features = []
		features.append(1.0)

		# age features
		features.append(float(r['age'])/100)
		features.append(float(r['age']) <= 23)
		features.append(float(r['age']) > 50)
		features.append(float(r['age'] in list(range(20,35))))
		features.append(float(r['age']) <= 25)
		features.append(float(r['age']) <= 15)
		features.append(float(r['age']) <= 30)
		features.append(float(r['age']) <= 35)
		features.append(float(r['age']) <= 40)
		features.append(float(r['age']) <= 45)
		features.append(float(r['age']) <= 50)
		features.append(float(r['age']) <= 55)
		features.append(float(r['age']) <= 60)
		features.append(float(r['age']) <= 65)
		features.append(float(r['age']) <= 70)
		features.append(float(r['age']) <= 75)
		features.append(float(r['age']) <= 80)
		features.append(float(r['age']) > 81)
		features.append(float(r['age']) > 50)

		# education features
		features.append(float(r['education'] == 'Bachelors'))
		features.append(float(r['education'] == 'Some-college'))
		features.append(float(r['education'] == {'11th', '9th', '7th-8th', '12th', '1st-4th', '10th', '5th-6th', 'Preschool'}))
		features.append(float(r['education'] == 'HS-grad'))
		features.append(float(r['education'] == 'Prof-school'))
		features.append(float(r['education'] == 'Assoc-acdm'))
		features.append(float(r['education'] == 'Assoc-voc'))
		features.append(float(r['education'] == 'Masters'))
		features.append(float(r['education'] == 'Doctorate'))

		# education num features
		features.append(float(r['education_num'])/20)
		features.append(float(r['education_num'] in list(range(13, 20))))

		# marital features
		features.append(float(r['marital'] == 'Married-civ-spouse'))
		features.append(float(r['marital'] == 'Divorced'))
		features.append(float(r['marital'] == 'Never-married'))
		features.append(float(r['marital'] == 'Separated'))
		features.append(float(r['marital'] == 'Widowed'))
		features.append(float(r['marital'] == 'Married-spouse-absent'))
		features.append(float(r['marital'] == 'Married-AF-spouse'))
	
		# occupation features
		features.append(float(r['occupation'] == {'Sales'}))
		features.append(float(r['occupation'] == {'Exec-managerial' }))
		features.append(float(r['occupation'] == {'Tech-support'}))
		features.append(float(r['occupation'] == {'Prof-specialty' }))
		features.append(float(r['occupation'] == {'Farming-fishing' }))
		features.append(float(r['occupation'] == {'Craft-repair' }))
		features.append(float(r['occupation'] == {'Other-service' }))
		features.append(float(r['occupation'] == {'Handlers-cleaners' }))
		features.append(float(r['occupation'] == {'Machine-op-inspct' }))
		features.append(float(r['occupation'] == {'Adm-clerical' }))
		features.append(float(r['occupation'] == {'Transport-moving' }))
		features.append(float(r['occupation'] == {'Priv-house-serv' }))
		features.append(float(r['occupation'] == {'Protective-serv' }))
		features.append(float(r['occupation'] == {'Armed-Forces' }))

		# relationship features
		features.append(float(r['relationship'] == 'Wife'))
		features.append(float(r['relationship'] == 'Own-child'))
		features.append(float(r['relationship'] == 'Not-in-family'))
		features.append(float(r['relationship'] == 'Husband'))
		features.append(float(r['relationship'] == 'Other-relative'))
		features.append(float(r['relationship'] == 'Unmarried'))

		# race features
		features.append(float(r['race'] == 'White'))
		features.append(float(r['race'] == 'Asian-Pac-Islander'))
		features.append(float(r['race'] == 'Amer-Indian-Eskimo'))
		features.append(float(r['race'] == 'Other'))
		features.append(float(r['race'] == 'Black'))

		# sex features
		features.append(float(r['sex'] == 'Female'))

		# country features
		features.append(float(r['country'] == {'Jamaica'}))
		features.append(float(r['country'] == {'Philippines'}))
		features.append(float(r['country'] == {'Trinadad&Tobago'}))
		features.append(float(r['country'] == {'Ecuador'}))
		features.append(float(r['country'] == {'Columbia'}))
		features.append(float(r['country'] == {'Dominican-Republic'})) 
		features.append(float(r['country'] == {'El-Salvador'})) 
		features.append(float(r['country'] == {'Puerto-Rico'})) 
		features.append(float(r['country'] == {'India'})) 
		features.append(float(r['country'] == {'Haiti'}))
		features.append(float(r['country'] == {'Cambodia'})) 
		features.append(float(r['country'] == {'Outlying-US(Guam-USVI-etc)' }))
		features.append(float(r['country'] == {'Iran' }))
		features.append(float(r['country'] == {'Honduras'}))
		features.append(float(r['country'] == {'Laos'})) 
		features.append(float(r['country'] == {'Guatemala'})) 
		features.append(float(r['country'] == {'Nicaragua'})) 
		features.append(float(r['country'] == {'Peru'}))
		features.append(float(r['country'] == {'Japan'}))
		features.append(float(r['country'] == {'Germany'}))
		features.append(float(r['country'] == {'Greece'}))
		features.append(float(r['country'] == {'China'}))
		features.append(float(r['country'] == {'South'}))
		features.append(float(r['country'] == {'Italy'}))
		features.append(float(r['country'] == {'Poland'}))
		features.append(float(r['country'] == {'Mexico'}))
		features.append(float(r['country'] == {'Vietnam'}))
		features.append(float(r['country'] == {'Ireland'}))
		features.append(float(r['country'] == {'France'}))
		features.append(float(r['country'] == {'Scotland'}))
		features.append(float(r['country'] == {'Holand-Netherlands'}))

		
		# hrs per week
		features.append(float(r['hr_per_week'])/50)
		features.append(float(r['hr_per_week']) >= 75)
		features.append(float(r['hr_per_week']) < 35)
		features.append(float(r['hr_per_week']) > 39)

		
		# workclass
		features.append(float(r['type_employer'] == {'Private'}))
		features.append(float(r['type_employer'] == {'Self-emp-inc'}))
		features.append(float(r['type_employer'] == {'Federal-gov'}))
		features.append(float(r['type_employer'] == {'Local-gov'}))
		features.append(float(r['type_employer'] == {'State-gov'}))
		features.append(float(r['type_employer'] == {'Without-pay'}))
		features.append(float(r['type_employer'] == {'Never-worked'}))
		
		# capital gain/loss
		features.append(float(r['capital_gain']) < 4000)
		features.append(float(r['capital_gain']) > 4000)
		features.append(float(r['capital_gain']) > 7000)
		features.append(float(r['capital_loss']) < 4000)
		features.append(float(r['capital_loss']) > 4000)
		features.append(float(r['capital_loss']) > 7000)
		

		point = {}
		point['features'] = features
		point['label'] = int(r['income'] == '>50K')
		data.append(point)

	return data


# Tune parameters for final submission
def submission(data):

	# change lambda to control overfitting - if have really low # of training
	# examples, model could probably perfectly fit data very well
	# if lambda is really high - then prevents theta from being too high

	# since we have pretty large # of training examples, low chance of 
	# overfitting so we set lambda to a very small number (.001)

	return train(data, epochs=7, alpha=.1, lambd=.001)
