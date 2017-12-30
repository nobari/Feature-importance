print(__doc__)
# Preliminaries
# Load pandas
import pandas as pd

# Load numpy
import numpy as np
# Set random seed
np.random.seed(0)
rng = np.random.RandomState(0)

# Removing features with low variance, less than the var_threshold
from sklearn.feature_selection import VarianceThreshold
var_threshold = .8

# Training and testing permutation
from sklearn.model_selection import train_test_split
#
from sklearn.preprocessing import StandardScaler
# Regressors that we are going to use
from sklearn.neural_network import MLPRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF
from sklearn.linear_model import BayesianRidge, LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor,BaggingRegressor,ExtraTreesRegressor,GradientBoostingRegressor

# Name of the regressors to print
names=['RandomForest',"ExtraTrees","AdaBoost","Decision Tree","Gradient Boost","Linear","Neural Net","RBF SVM","Nearest N","Gaussian Process"]

# Initializing the regressors together with their input parameters
regressors = [RandomForestRegressor(n_estimators=100,random_state=0,max_depth=2),
             ExtraTreesRegressor(n_estimators=100,random_state=0,max_depth=2),
              AdaBoostRegressor(random_state=0),
              DecisionTreeRegressor(random_state=0,max_depth=2),
              GradientBoostingRegressor(random_state=0),
             LinearRegression(),MLPRegressor(alpha=1),SVR(gamma=2, C=1),KNeighborsRegressor(3),
             GaussianProcessRegressor(1.0 * RBF(1.0),random_state=0)]

# Path to the ready to play dataset
path_ds="sur_pos.csv"

# Load the dataset
df_all=pd.read_csv(path_ds,index_col='store_code')

# Set the features, targets and feature names, i.e. X and y and feat_names respectively
features=len(df_all.columns)-1 #=89
X, y,feat_names  = df_all.iloc[:,:features].values,df_all.purchase_count.values,df_all.columns[:features].values

sel = VarianceThreshold(threshold=(var_threshold))
X=sel.fit_transform(X)
selected=sel.get_support(indices=True)
#DEBUG: X.shape

# Print the feature together with their id
print("Features:")
for f in range(X.shape[1]):
    print("feature %d = %s" % (f, feat_names[selected[f]]))

# OUTPUT:
# Features:
# feature 0 = accounting
# feature 1 = art_gallery
# feature 2 = atm
# feature 3 = bakery
# feature 4 = bank
# feature 5 = bar
# feature 6 = beauty_salon
# feature 7 = book_store
# feature 8 = bus_station
# feature 9 = cafe
# feature 10 = car_repair
# feature 11 = church
# feature 12 = clothing_store
# feature 13 = dentist
# feature 14 = doctor
# feature 15 = electrician
# feature 16 = electronics_store
# feature 17 = embassy
# feature 18 = florist
# feature 19 = furniture_store
# feature 20 = gas_station
# feature 21 = gym
# feature 22 = hair_care
# feature 23 = home_goods_store
# feature 24 = hospital
# feature 25 = insurance_agency
# feature 26 = jewelry_store
# feature 27 = lawyer
# feature 28 = liquor_store
# feature 29 = local_government_office
# feature 30 = lodging
# feature 31 = meal_takeaway
# feature 32 = movie_theater
# feature 33 = museum
# feature 34 = night_club
# feature 35 = parking
# feature 36 = pharmacy
# feature 37 = physiotherapist
# feature 38 = real_estate_agency
# feature 39 = restaurant
# feature 40 = shoe_store
# feature 41 = shopping_mall
# feature 42 = spa
# feature 43 = store
# feature 44 = transit_station
# feature 45 = travel_agency
# feature 46 = university

# Datasets to process
datasets = [(X,y)]

# Figure size to plot
figure = plt.figure(figsize=(30, 15))
i = 1
# iterate over datasets and then algorithms
# Plotting all the algorithms results to a single figure
for ds_cnt, ds in enumerate(datasets):
    # preprocess dataset, split into training and test part
    # test_size=.4, random_state=42
    X, y = ds
    X = StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=.4, random_state=42)

    # iterate over regressors
    for name, reg in zip(names, regressors):
        print i
        ax = plt.subplot(len(datasets)+1, len(regressors)/2 , i)
        reg.fit(X_train, y_train)
        score = reg.score(X_test, y_test)
        hasstd=False
        if hasattr(reg, 'feature_importances_') and hasattr(reg,'estimators_'):
            try:
                importances = reg.feature_importances_
                std = np.std([tree.feature_importances_ for tree in reg.estimators_],
                         axis=0)
                hasstd=True
            except:
                pass
        elif hasattr(reg, 'coef_'):
            importances = reg.coef_

        indices = np.argsort(importances)[::-1]


        if hasstd:
            ax.bar(range(X.shape[1]), importances[indices],
                   color="r", yerr=std[indices], align="center")
        else:
            ax.bar(range(X.shape[1]), importances[indices],
                   color="r", align="center")
        ax.set_xticks(range(X.shape[1]))
        ax.set_xticklabels(indices,fontdict={'size':5})

        if ds_cnt == 0:
            ax.set_title(name)
        if hasstd:
            ax.text(40, std.max(), ('score= %.2f' % score).lstrip('0'),
                size=15, horizontalalignment='right')
        else:
            ax.text(40, importances.max(), ('score= %.2f' % score).lstrip('0'),
                size=15, horizontalalignment='right')
        i += 1


plt.tight_layout()
plt.savefig("all.pdf")


# Plotting each algorithm's results to a separate figure

figure = plt.figure(figsize=(30, 15))
i = 1
# iterate over datasets
for ds_cnt, ds in enumerate(datasets):
    # preprocess dataset, split into training and test part
    # test_size=.4, random_state=42
    X, y = ds
    X = StandardScaler().fit_transform(X)
    X_train, X_test, y_train, y_test = \
        train_test_split(X, y, test_size=.4, random_state=42)

    # iterate over regressors
    for name, reg in zip(names, regressors):
        print i
        reg.fit(X_train, y_train)
        score = reg.score(X_test, y_test)
        hasstd=False
        if hasattr(reg, 'feature_importances_') and hasattr(reg,'estimators_'):
            try:
                importances = reg.feature_importances_
                std = np.std([tree.feature_importances_ for tree in reg.estimators_],
                         axis=0)
                hasstd=True
            except:
                pass
        elif hasattr(reg, 'coef_'):
            importances = reg.coef_

        indices = np.argsort(importances)[::-1]


        if hasstd:
            plt.bar(range(X.shape[1]), importances[indices],
                   color="r", yerr=std[indices], align="center")
        else:
            plt.bar(range(X.shape[1]), importances[indices],
                   color="r", align="center")
        plt.xticks(range(X.shape[1]),indices)

        if ds_cnt == 0:
            plt.title(name)
        if hasstd:
            plt.text(40, std.max(), ('score= %.2f' % score).lstrip('0'),
                size=15, horizontalalignment='right')
        else:
            plt.text(40, importances.max(), ('score= %.2f' % score).lstrip('0'),
                size=15, horizontalalignment='right')
        i += 1

        plt.savefig(name+".pdf")
        plt.clf()
