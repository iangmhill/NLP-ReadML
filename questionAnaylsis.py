import pandas as pd
import numpy as np
from scipy.sparse import hstack
from sklearn.preprocessing import LabelBinarizer
from sklearn.cross_validation import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv("trainingData.csv")
data = data[0:100]

questionValues = data["Question"].values
text = data["Text"].values


print "Extracting TFIDF features"
featureExtractor = TfidfVectorizer()
featureExtractor.fit_transform(list(data["Text"]))

textTFIDF = featureExtractor.transform(list(data["Text"]))

textFeaturesPerf = np.zeros((100))

test_categories, train_categories, test_questions, train_questions = train_test_split(
textTFIDF, questionValues, random_state=iter)

model = Ridge()

print "Fitting the Model"

model.fit(train_categories, train_questions)
output = model.predict(test_categories)
textFeaturesPerf[iter] = mean_absolute_error(test_questions, output)
