print('START')
#imports
import numpy as np
import pandas as pd
import math
import pickle
import os
import ast
import string
import scipy.stats as stats
#no warnings
import warnings
warnings.filterwarnings('ignore')
#train_test_split
from sklearn.model_selection import train_test_split
#log regression

#classification report
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
import joblib
import random
#import tensorflow as tf
#mlpregression
from sklearn.neural_network import MLPRegressor


from sklearn.utils.class_weight import compute_class_weight 
from sklearn.metrics import make_scorer

print('IMPORTS DONE')


def createDataSplits(df, with_val = 0, results_directory= '../logs/', seed_value = 42, sequence_length = 1):
    
    try:

        # # Set seed
        random.seed(seed_value)
        np.random.seed(seed_value)
        #tf.random.set_seed(seed_value)

        # # Extract features and labels

        # # for naive & naive_n datasets
        # features = df.iloc[:, 3:]
        # target_class = df['class'].values

        # # for full & full_n datasets
        features = df.iloc[:, 3:]
        target_class = df['groundtruth'].values
        #target_class = target_class.astype('int')
        
        ####T EDIT
        participants = np.unique(df['session'])
        print(participants)

        if with_val > 0:
            #Number of participants for train, validation, and test
            train_fold_size = 18
            val_fold_size = 3
            test_fold_size = 6

            #number of dataset folds
            num_folds = 5

            # Shuffle the list of participants
            np.random.shuffle(participants)

            # Initialize lists to store train, validation, and test participants for each fold
            train_folds = []
            val_folds = []
            test_folds = []

            # Create non-overlapping test folds and validation folds
            for i in range(num_folds):
                start_test_idx = i * test_fold_size
                end_test_idx = start_test_idx + np.min([test_fold_size, len(participants) - start_test_idx])

                test_fold = participants[start_test_idx:end_test_idx]
                #validation set selected from the remaining participants
                remaining_participants = np.setdiff1d(participants, test_fold)
                np.random.shuffle(remaining_participants)
                val_fold = remaining_participants[:val_fold_size]
                train_fold = np.setdiff1d(remaining_participants, val_fold)
                train_folds.append(train_fold)
                val_folds.append(val_fold)
                test_folds.append(test_fold)

            # Create train, validation, and test sets for each fold
            #for now, do only for fold 0
            train_fold = train_folds[0]
            val_fold = val_folds[0]
            test_fold = test_folds[0]

            # Split the data into train, validation, and test sets
            train_set = df[df['session'].isin(train_fold)]
            X_train = features.loc[train_set.index,:]
            val_set = df[df['session'].isin(val_fold)]
            X_val = features.loc[val_set.index,:]
            test_set = df[df['session'].isin(test_fold)]
            X_test  = features.loc[test_set.index,:]
        
            
            #print(X_train.head())
            

            # Convert labels to categorical format
           # num_classes = np.max(target_class) + 1 + np.abs(np.min(target_class)) #  Assuming labels start from 0
            #labels_ohe = np.eye(num_classes)[target_class]
            labels_ohe = target_class
            #get y train, val, test set values corresponding to same indexes, from labels_ohe

            y_train = labels_ohe[X_train.index]
            y_val = labels_ohe[X_val.index]
            y_test = labels_ohe[X_test.index]

            #print size of all sets
            print(X_train.shape, y_train.shape)
            print(X_val.shape, y_val.shape)
            print(X_test.shape, y_test.shape)

            #reset indexes
            X_train = X_train.reset_index(drop=True)
            X_val = X_val.reset_index(drop=True)
            X_test = X_test.reset_index(drop=True)

            
            # Split data into train and test sets
            ###X_train, X_test, y_train, y_test = train_test_split(features, labels_ohe, test_size=0.2, random_state=seed_value)

            ####T EDIT (end)

            # Create sequences with a defined sequence length
            X_train_sequences = [X_train[i : i + sequence_length] for i in range(len(X_train) - sequence_length + 1)]
            y_train_sequences = y_train[sequence_length - 1 : ]

            #create validation sequences
            X_val_sequences = [X_val[i : i + sequence_length] for i in range(len(X_val) - sequence_length + 1)]
            y_val_sequences = y_val[sequence_length - 1 : ]

            # Reshape the test data sequences
            X_test_sequences = [X_test[i : i + sequence_length] for i in range(len(X_test) - sequence_length + 1)]
            y_test_sequences = y_test[sequence_length - 1 : ]
            
            return X_train, X_val, X_test, y_train, y_val, y_test, X_train_sequences, y_train_sequences,X_val_sequences, y_val_sequences, X_test_sequences, y_test_sequences


        else:
            #Number of participants for train, validation, and test
            train_fold_size = 21
            test_fold_size = 6

            #number of dataset folds
            num_folds = 5

            # Shuffle the list of participants
            np.random.shuffle(participants)

            # Initialize lists to store train, validation, and test participants for each fold
            train_folds = []
            test_folds = []

            # Create non-overlapping test folds and validation folds
            for i in range(num_folds):
                start_test_idx = i * test_fold_size
                end_test_idx = start_test_idx + np.min([test_fold_size, len(participants) - start_test_idx])

                test_fold = participants[start_test_idx:end_test_idx]
                #validation set selected from the remaining participants
                remaining_participants = np.setdiff1d(participants, test_fold)
                
                train_folds.append(remaining_participants)
                test_folds.append(test_fold)

            # Create train, validation, and test sets for each fold
            #for now, do only for fold 0
            train_fold = train_folds[0]
            test_fold = test_folds[0]

            # Split the data into train, validation, and test sets
            train_set = df[df['session'].isin(train_fold)]
            X_train = features.loc[train_set.index,:]
            test_set = df[df['session'].isin(test_fold)]
            X_test  = features.loc[test_set.index,:]
        
            
            #print(X_train.head())
            

            # Convert labels to categorical format
            #num_classes = np.max(target_class) + 1 + np.abs(np.min(target_class)) #  Assuming labels start from 0
            #labels_ohe = np.eye(num_classes)[target_class]
            labels_ohe = target_class
            #get y train, val, test set values corresponding to same indexes, from labels_ohe

            y_train = labels_ohe[X_train.index]
            y_test = labels_ohe[X_test.index]
            #print size of all sets
            print(X_train.shape, y_train.shape)
            print(X_test.shape, y_test.shape)

            #reset indexes
            X_train = X_train.reset_index(drop=True)
            X_test = X_test.reset_index(drop=True)

            
            # Split data into train and test sets
            ###X_train, X_test, y_train, y_test = train_test_split(features, labels_ohe, test_size=0.2, random_state=seed_value)

            ####T EDIT (end)

            # Create sequences with a defined sequence length
            X_train_sequences = [X_train[i : i + sequence_length] for i in range(len(X_train) - sequence_length + 1)]
            y_train_sequences = y_train[sequence_length - 1 : ]

            # Reshape the test data sequences
            X_test_sequences = [X_test[i : i + sequence_length] for i in range(len(X_test) - sequence_length + 1)]
            y_test_sequences = y_test[sequence_length - 1 : ]

    
            return X_train, X_test, y_train, y_test, X_train_sequences, y_train_sequences, X_test_sequences, y_test_sequences

    except Exception as e:
        print('FAILED')
        with open(f'{results_directory}', 'a') as results_file:
            results_file.write(
                f'Exception {e} thrown during splitting the dataset for :- '
                #f'sequence_length = {sequence_length}\n'
                #f'Loss Function = {loss}\n'
                #f'Optimizer = {optimizer}\n'
                #f'Activation = {activation}\n'
                #f'Batch Size = {batch_size}\n'
                #f'Epochs = {epochs}\n'
                #f'Seed Value = {seed_value}\n'
            )
        pass
 

#function that calculates mean squared error and concordance correlation coefficient 
def calculate_metrics(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    root_mse = math.sqrt(mse)
    pearson = stats.pearsonr(y_true, y_pred)[0] * 2

    cor = np.corrcoef(y_true, y_pred)[0][1]
    # Means
    mean_true = np.mean(y_true)
    mean_pred = np.mean(y_pred)
    # Population variances
    var_true = np.var(y_true)
    var_pred = np.var(y_pred)
    # Population standard deviations
    sd_true = np.std(y_true)
    sd_pred = np.std(y_pred)
    # Calculate CCC
    numerator = 2 * cor * sd_true * sd_pred
    denominator = var_true + var_pred + (mean_true - mean_pred)**2
    ccc = numerator / denominator

    print(ccc)
    return mse, pearson, ccc

#just calculate ccc
def calc_ccc(y_true, y_pred):
    # Means
    mean_true = np.mean(y_true)
    mean_pred = np.mean(y_pred)
    # Population variances
    var_true = np.var(y_true)
    var_pred = np.var(y_pred)
    # Population standard deviations
    sd_true = np.std(y_true)
    sd_pred = np.std(y_pred)
    # Calculate CCC
    numerator = 2 * np.corrcoef(y_true, y_pred)[0][1] * sd_true * sd_pred
    denominator = var_true + var_pred + (mean_true - mean_pred)**2
    ccc = numerator / denominator
    return ccc


if __name__ == '__main__':

    
    path = '../'
    listfiles = os.listdir(path)

    training_files = [file for file in listfiles if file.endswith('.csv') and ('pca' in file or 'PCA' in file)]

    for file in training_files:

        #get training data

        train_data = pd.read_csv(path + file)



        print ('START NEW')
        codename = 'mlpreg'
        codename = codename + file[8:-13]
        
        # results directory - make a new folder with the day and time of the run

        results_directory = '../logs/results_' + codename+ '.txt'

        print(results_directory)

        with open(results_directory, 'w') as f:
            f.write(str('Results'))
            #enter
            f.write(str('\n'))
            f.write(str('Codename: ' + codename))



        #create data splits
        X_train, X_test, y_train, y_test, X_train_sequences, y_train_sequences, X_test_sequences, y_test_sequences = createDataSplits(train_data, with_val = 0, results_directory= results_directory, seed_value = 42)

        #write
        with open(results_directory, 'w') as f:
            f.write(str('X_train shape: ' + str(X_train.shape)))
            f.write(str('\n'))
            f.write(str('X_test shape: ' + str(X_test.shape)))
            f.write(str('\n'))
            f.write(str('y_train shape: ' + str(y_train.shape)))
            f.write(str('\n'))
            f.write(str('y_test shape: ' + str(y_test.shape)))
            f.write(str('\n'))



        param_grid  = {"hidden_layer_sizes": [50,100,250,500], "activation": [ "logistic", "tanh", "relu"], "solver": ["lbfgs", "sgd", "adam"], "alpha": [0.05,0.0005,0.5]}
        

        # Calculate class weights
        #class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
        #new_dict = {}
        #unique = np.unique(y_train)
        #for i,weight in enumerate(class_weights):
        #    #add to dictionary
        #    new_dict[unique[i]] = class_weights[i]

        #class_weights = new_dict

        # Create a Randomforest
        #classifier = svm.SVC(decision_function_shape='ovo', random_state = 42, class_weight=class_weights)  


        ccc_scorer = make_scorer(calc_ccc, greater_is_better=True)  # Set greater_is_better according to your scoring function


        classifier = MLPRegressor(max_iter=1000,random_state=42)
        grid = GridSearchCV(classifier, param_grid=param_grid,scoring=ccc_scorer, cv=5,verbose = 10, n_jobs=-1)

        
        
        grid.fit(X_train, y_train)

        
        grid_predictions = grid.predict(X_test)

        #now calculate ccc
        ccc = calc_ccc(y_test, grid_predictions)
        print(ccc)
        #print rmse
        rmse = math.sqrt(mean_squared_error(y_test, grid_predictions))

        #write
        with open(results_directory, 'w') as f:

            f.write(str('Grid search parameters: ' + str(param_grid)))
            f.write(str('\n'))
            


            #save in txt file
            f.write(str('Best params \n'))
            f.write(str(grid.best_params_))
            f.write(str('Best score \n'))
            f.write(str(grid.best_score_))
            f.write(str('Best estimator \n'))
            f.write(str(grid.best_estimator_))
            f.write(str('scoring \n'))
            f.write('ccc \n')
            f.write(str(ccc))
            f.write(str('rmse \n'))
            f.write(str(rmse))

            #close
            f.close()
