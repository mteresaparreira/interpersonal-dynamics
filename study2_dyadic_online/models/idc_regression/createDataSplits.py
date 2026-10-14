def createDataSplits(df, with_val = 0, results_directory= '../logs/', seed_value = 42, sequence_length = 1):
    
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
    #log regression

    from sklearn.metrics import mean_squared_error
    import joblib
    import random

    import torch





    try:

        # # Set seed
        random.seed(seed_value)
        np.random.seed(seed_value)
        #tf.random.set_seed(seed_value)
        torch.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value)

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
            X_train_sequences = np.array([X_train[i : i + sequence_length] for i in range(len(X_train) - sequence_length + 1)])
            y_train_sequences = np.array(y_train[sequence_length - 1 : ])

            #create validation sequences
            X_val_sequences = np.array([X_val[i : i + sequence_length] for i in range(len(X_val) - sequence_length + 1)])
            y_val_sequences = np.array(y_val[sequence_length - 1 : ])

            # Reshape the test data sequences
            X_test_sequences = np.array([X_test[i : i + sequence_length] for i in range(len(X_test) - sequence_length + 1)])
            y_test_sequences = np.array(y_test[sequence_length - 1 : ])

            
            #print size of all sets
            print(X_train_sequences.shape, y_train_sequences.shape)
            print(X_test_sequences.shape, y_test_sequences.shape)


            return X_train, X_val, X_test, y_train, y_val, y_test, X_train_sequences, y_train_sequences,X_val_sequences, y_val_sequences, X_test_sequences, y_test_sequences


        else:

            # # Set seed
            random.seed(seed_value)
            np.random.seed(seed_value)
            #tf.random.set_seed(seed_value)
            torch.manual_seed(seed_value)
            torch.cuda.manual_seed_all(seed_value)
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

            
           

            # Create sequences with a defined sequence length
            X_train_sequences = np.array([X_train[i : i + sequence_length] for i in range(len(X_train) - sequence_length + 1)])
            y_train_sequences = np.array(y_train[sequence_length - 1 : ])

            # Reshape the test data sequences
            X_test_sequences = np.array([X_test[i : i + sequence_length] for i in range(len(X_test) - sequence_length + 1)])
            y_test_sequences = np.array(y_test[sequence_length - 1 : ])

            
            #print size of all sets
            print(X_train_sequences.shape, y_train_sequences.shape)
            print(X_test_sequences.shape, y_test_sequences.shape)
            return X_train, X_test, y_train, y_test, X_train_sequences, y_train_sequences, X_test_sequences, y_test_sequences

    except Exception as e:
        print('FAILED')
        with open(f'{results_directory}', 'a') as results_file:
            results_file.write(
                f'Exception {e} thrown during splitting the dataset for :- '
              
            )
        pass