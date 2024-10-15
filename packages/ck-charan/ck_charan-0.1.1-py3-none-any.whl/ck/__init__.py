def first():
    return '''
import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression 
# Sample data 
X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1) 
y = np.array([1, 3, 2, 3, 5]) 
# Create and fit the model 
model = LinearRegression() 
model.fit(X, y) 
# Predict 
y_pred = model.predict(X) 
# Plotting 
plt.scatter(X, y, color='blue') 
plt.plot(X, y_pred, color='red') 
plt.xlabel('X') 
plt.ylabel('y') 
plt.title('Simple Linear Regression') 
plt.show() '''

def second():
    return '''
import numpy as np 
from sklearn.linear_model import LinearRegression 
# Sample data 
X = np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]) 
y = np.array([2, 3, 4, 5, 6]) 
# Create and fit the model 
model = LinearRegression() 
model.fit(X, y) 
# Predict 
y_pred = model.predict(X) 
# Output coefficients and intercept 
model.coef_, model.intercept_

'''

def third():
    return '''Implement Simple Logistic Regression and Multivariate Logistic Regression 
import numpy as np 
from sklearn.linear_model import LogisticRegression 
# Sample data 
X = np.array([1, 2, 3, 4, 5]).reshape(-1, 1) 
y = np.array([0, 0, 0, 1, 1]) 
# Create and fit the model 
model = LogisticRegression() 
model.fit(X, y) 
# Predict 
y_pred = model.predict(X) 
# Output coefficients and intercept 
model.coef_, model.intercept_ 
OUTPUT: 
(array([[1.04697203]]), array([-3.74804785])) 
Multivariate Logistic Regression: 
import numpy as np 
from sklearn.linear_model import LogisticRegression 
# Sample data 
X = np.array([[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]]) 
y = np.array([0, 0, 0, 1, 1]) 
# Create and fit the model 
model = LogisticRegression() 
model.fit(X, y) 
# Predict 
y_pred = model.predict(X) 
# Output coefficients and intercept 
model.coef_, model.intercept_

'''

def fourth():
    return '''
from sklearn.datasets import load_iris 
from sklearn.tree import DecisionTreeClassifier 
from sklearn import tree 
import matplotlib.pyplot as plt 
# Load data 
iris = load_iris() 
X, y = iris.data, iris.target 
# Create and fit the model 
clf = DecisionTreeClassifier() 
clf.fit(X, y) 
# Plot the tree 
plt.figure(figsize=(15,10)) 
tree.plot_tree(clf, 
filled=True, feature_names=iris.feature_names,
class_names=iris.target_names) 
plt.show()

'''

def fifth():
    return '''
from sklearn.datasets import load_iris 
from sklearn.model_selection import train_test_split 
from sklearn.neighbors import KNeighborsClassifier 
from sklearn.metrics import accuracy_score 
# Load data 
iris = load_iris() 
X, y = iris.data, iris.target 
# Split data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, 
random_state=42) 
# Create and fit the model 
knn = KNeighborsClassifier(n_neighbors=3) 
knn.fit(X_train, y_train) 
# Predict 
y_pred = knn.predict(X_test) 
# Output accuracy 
accuracy_score(y_test, y_pred)
'''


def sixth():
    return '''
from sklearn.datasets import load_iris 
from sklearn.model_selection import train_test_split 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import accuracy_score 
# Load data 
iris = load_iris() 
X, y = iris.data, iris.target 
# Split data 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42) 
# Create and fit the model 
rf = RandomForestClassifier(n_estimators=100) 
rf.fit(X_train, y_train) 
# Predict 
y_pred = rf.predict(X_test) 
# Output accuracy 
accuracy_score(y_test, y_pred) 

'''




