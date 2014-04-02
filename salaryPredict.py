import pandas as pd
import numpy as np
from scipy.sparse import hstack
from sklearn.preprocessing import LabelBinarizer
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv("Train_rev1.csv")
data = data[0:1000]

alltext = np.concatenate((data["FullDescription"].values, data["Title"].values));

salaries = data["SalaryNormalized"].values


print "Extracting TFIDF features"
featureExtractor = TfidfVectorizer()
featureExtractor.fit_transform(list(data["FullDescription"]))

titleTFIDF = featureExtractor.transform(list(data["Title"]))
descriptionTFIDF = featureExtractor.transform(list(data["FullDescription"]))

allTFIDF = hstack((titleTFIDF,descriptionTFIDF))

allFeaturesPerf = np.zeros((100))
justTitleFeaturesPerf = np.zeros((100))
justFullDescriptionFeaturesPerf = np.zeros((100))

for iter in range(0,100):
	test_categories,train_categories,test_salaries,train_salaries=train_test_split(allTFIDF,salaries,random_state=iter)

	model=Ridge()

	print "Fitting the Model"

	model.fit(train_categories,train_salaries)
	output=model.predict(test_categories)
	allFeaturesPerf[iter] = mean_absolute_error(test_salaries,output)

	model.fit(train_categories[:,0:train_categories.shape[1]/2],train_salaries)
	output=model.predict(test_categories[:,0:train_categories.shape[1]/2])
	justTitleFeaturesPerf[iter] = mean_absolute_error(test_salaries,output)

	model.fit(train_categories[:,train_categories.shape[1]/2:],train_salaries)
	output=model.predict(test_categories[:,train_categories.shape[1]/2:])
	justFullDescriptionFeaturesPerf[iter] = mean_absolute_error(test_salaries,output)
