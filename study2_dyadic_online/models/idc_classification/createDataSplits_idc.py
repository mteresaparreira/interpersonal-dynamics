
import numpy as np
import pandas as pd
import pickle
import os
import random
import torch
#no warnings
import warnings
warnings.filterwarnings('ignore')


#def create_sequences(data, target, sequence_length):
#    sequences = [data[i : i + sequence_length] for i in range(len(data) - sequence_length + 1)]
#    targets = target[sequence_length - 1 : ]
#    return np.array(sequences), np.array(targets)

def create_sequences(data, target, sessions, sequence_length, num_classes):
    sequences = []
    targets = []

    #hot one encode the target
    
    # Split data by session and then create sequences
    unique_sessions = np.unique(sessions)
    for session in unique_sessions:
        session_indices = np.where(sessions == session)[0]
        session_data = data[session_indices]
        session_target = target[session_indices]
        
        if len(session_data) >= sequence_length:
            for i in range(len(session_data) - sequence_length + 1):
                sequences.append(session_data[i : i + sequence_length])
                targets.append(session_target[i + sequence_length - 1])

    #hot one encode the target, based on number of classes (array should have num_classses columns)
    #print(targets[:10])
    #make all targets positive
    if num_classes == 15:
        targets = np.array(targets) + 7 #num_classes = 15, including 0. min value is -7

    targets_oh = np.zeros((len(targets), num_classes))
    for i in range(len(targets)):
        targets_oh[i, targets[i]] = 1
    #print(targets_oh[:10,:])
    targets = targets_oh
    return np.array(sequences), np.array(targets)


def createDataSplits(df, with_val = 0, results_directory= '../logs/', seed_value = 42, sequence_length = 1):

    """
    Split the data into train, validation, and test sets for each fold.
    df - dataframe containing the data
    fold_no - number of fold to get the data for
    with_val - whether to include validation set or not
    label_column - column name for the target class
    fold_column - column name for the fold number
    results_directory - directory to store the results
    seed_value - seed value for reproducibility
    sequence_length - length of the sequence for RNNs or transformers
    
    """

    try:

        # # Set seed
        random.seed(seed_value)
        np.random.seed(seed_value)
        #tf.random.set_seed(seed_value)
        torch.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value)
    

        # get features and target class
        features = df.iloc[:,5:]
        target_class = df['groundtruth'].values
        target_class = target_class.astype('int')
        sessions = df['session'].values


        #get number of classes
        num_classes = len(np.unique(target_class))

             
        participants = np.unique(df['session'])
        print(participants)

        if with_val > 0:
            #Number of participants for train, validation, and test
            train_fold_size = 36
            val_fold_size = 6
            test_fold_size = 12

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
            train_set = df[df['session'].isin(train_fold)].index
            X_train = features.loc[train_set]
            val_set = df[df['session'].isin(val_fold)].index
            X_val = features.loc[val_set]
            test_set = df[df['session'].isin(test_fold)].index
            X_test  = features.loc[test_set]
        
           
            labels_ohe = target_class
            #get y train, val, test set values corresponding to same indexes, from labels_ohe

            y_train = labels_ohe[X_train.index]
            y_val = labels_ohe[X_val.index]
            y_test = labels_ohe[X_test.index]

            #print size of all sets
            print(X_train.shape, y_train.shape)
            print(X_val.shape, y_val.shape)
            print(X_test.shape, y_test.shape)

            sessions_train = sessions[train_set]
            sessions_val = sessions[val_set]
            sessions_test = sessions[test_set]

            #reset indexes
            X_train = X_train.reset_index(drop=True)
            X_val = X_val.reset_index(drop=True)
            X_test = X_test.reset_index(drop=True)

            
            # Split data into train and test sets
            ###X_train, X_test, y_train, y_test = train_test_split(features, labels_ohe, test_size=0.2, random_state=seed_value)

            ####T EDIT (end)
            
            X_train_sequences, y_train_sequences = create_sequences(X_train.values, y_train, sessions_train, sequence_length,num_classes)
            X_val_sequences, y_val_sequences = create_sequences(X_val.values, y_val, sessions_val, sequence_length,num_classes)
            X_test_sequences, y_test_sequences = create_sequences(X_test.values, y_test, sessions_test, sequence_length,num_classes)
            
            #print size of all sets
            print(X_train_sequences.shape, y_train_sequences.shape)
            print(X_test_sequences.shape, y_test_sequences.shape)


            return sessions, num_classes, X_train, X_val, X_test, y_train, y_val, y_test, X_train_sequences, y_train_sequences, X_val_sequences, y_val_sequences, X_test_sequences, y_test_sequences

        else:

            # # Set seed
            random.seed(seed_value)
            np.random.seed(seed_value)
            #tf.random.set_seed(seed_value)
            torch.manual_seed(seed_value)
            torch.cuda.manual_seed_all(seed_value)
            #Number of participants for train, validation, and test
            train_fold_size = 42
            test_fold_size = 12

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
            train_set = df[df['session'].isin(train_fold)].index
            X_train = features.loc[train_set]
            test_set = df[df['session'].isin(test_fold)].index
            X_test  = features.loc[test_set]
        
            
            
            labels_ohe = target_class
            #get y train, val, test set values corresponding to same indexes, from labels_ohe

            y_train = labels_ohe[X_train.index]
            y_test = labels_ohe[X_test.index]
            #print size of all sets
            print(X_train.shape, y_train.shape)
            print(X_test.shape, y_test.shape)

            sessions_train = sessions[train_set]
            sessions_test = sessions[test_set]

            #reset indexes
            X_train = X_train.reset_index(drop=True)
            X_test = X_test.reset_index(drop=True)

            
            X_train_sequences, y_train_sequences = create_sequences(X_train.values, y_train, sessions_train, sequence_length,num_classes)
            X_test_sequences, y_test_sequences = create_sequences(X_test.values, y_test, sessions_test, sequence_length,num_classes)

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



def createDataSplits_all(df, fold_no, with_val = 0, results_directory= '../logs/', seed_value = 42, sequence_length = 1):

    """
    Split the data into train, validation, and test sets for each fold.
    df - dataframe containing the data
    fold_no - number of fold to get the data for
    with_val - whether to include validation set or not
    label_column - column name for the target class
    fold_column - column name for the fold number
    results_directory - directory to store the results
    seed_value - seed value for reproducibility
    sequence_length - length of the sequence for RNNs or transformers
    
    """

    try:

        # # Set seed
        random.seed(seed_value)
        np.random.seed(seed_value)
        #tf.random.set_seed(seed_value)
        torch.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value)
    

        # get features and target class
        features = df.iloc[:,5:]
        target_class = df['groundtruth'].values
        target_class = target_class.astype('int')
        sessions = df['session'].values


        #get number of classes
        num_classes = len(np.unique(target_class))

             
        participants = np.unique(df['session'])
        print(participants)

        if with_val > 0:
            #Number of participants for train, validation, and test
            train_fold_size = 36
            val_fold_size = 6
            test_fold_size = 12

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

            #print('all folds')
            #print(train_folds)
            #print(val_folds)
            #print(test_folds)
            # Create train, validation, and test sets for each fold
            #for now, do only for fold 0
            train_fold = train_folds[fold_no]
            val_fold = val_folds[fold_no]
            test_fold = test_folds[fold_no]

            # Split the data into train, validation, and test sets
            train_set = df[df['session'].isin(train_fold)].index
            X_train = features.loc[train_set]
            val_set = df[df['session'].isin(val_fold)].index
            X_val = features.loc[val_set]
            test_set = df[df['session'].isin(test_fold)].index
            X_test  = features.loc[test_set]
        
           
            labels_ohe = target_class
            #get y train, val, test set values corresponding to same indexes, from labels_ohe

            y_train = labels_ohe[X_train.index]
            y_val = labels_ohe[X_val.index]
            y_test = labels_ohe[X_test.index]

            #print size of all sets
            print(X_train.shape, y_train.shape)
            print(X_val.shape, y_val.shape)
            print(X_test.shape, y_test.shape)

            sessions_train = sessions[train_set]
            sessions_val = sessions[val_set]
            sessions_test = sessions[test_set]

            #reset indexes
            X_train = X_train.reset_index(drop=True)
            X_val = X_val.reset_index(drop=True)
            X_test = X_test.reset_index(drop=True)

            
            # Split data into train and test sets
            ###X_train, X_test, y_train, y_test = train_test_split(features, labels_ohe, test_size=0.2, random_state=seed_value)

            ####T EDIT (end)
            
            X_train_sequences, y_train_sequences = create_sequences(X_train.values, y_train, sessions_train, sequence_length,num_classes)
            X_val_sequences, y_val_sequences = create_sequences(X_val.values, y_val, sessions_val, sequence_length,num_classes)
            X_test_sequences, y_test_sequences = create_sequences(X_test.values, y_test, sessions_test, sequence_length,num_classes)
            
            #print size of all sets
            print(X_train_sequences.shape, y_train_sequences.shape)
            print(X_test_sequences.shape, y_test_sequences.shape)


            return sessions, num_classes, X_train, X_val, X_test, y_train, y_val, y_test, X_train_sequences, y_train_sequences, X_val_sequences, y_val_sequences, X_test_sequences, y_test_sequences

        else:

            # # Set seed
            random.seed(seed_value)
            np.random.seed(seed_value)
            #tf.random.set_seed(seed_value)
            torch.manual_seed(seed_value)
            torch.cuda.manual_seed_all(seed_value)
            #Number of participants for train, validation, and test
            train_fold_size = 42
            test_fold_size = 12

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
            train_fold = train_folds[fold_no]
            test_fold = test_folds[fold_no]

            # Split the data into train, validation, and test sets
            train_set = df[df['session'].isin(train_fold)].index
            X_train = features.loc[train_set]
            test_set = df[df['session'].isin(test_fold)].index
            X_test  = features.loc[test_set]
        
            
            
            labels_ohe = target_class
            #get y train, val, test set values corresponding to same indexes, from labels_ohe

            y_train = labels_ohe[X_train.index]
            y_test = labels_ohe[X_test.index]
            #print size of all sets
            print(X_train.shape, y_train.shape)
            print(X_test.shape, y_test.shape)

            sessions_train = sessions[train_set]
            sessions_test = sessions[test_set]

            #reset indexes
            X_train = X_train.reset_index(drop=True)
            X_test = X_test.reset_index(drop=True)

            
            X_train_sequences, y_train_sequences = create_sequences(X_train.values, y_train, sessions_train, sequence_length,num_classes)
            X_test_sequences, y_test_sequences = create_sequences(X_test.values, y_test, sessions_test, sequence_length,num_classes)

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




        

def createDataSplits_test(df, num_classes, label_column = 'UserAkwardness', results_directory= '../logs/', seed_value = 42, sequence_length = 1):

    """
    Split the data into train, validation, and test sets for each fold.
    df - dataframe containing the data
    fold_no - number of fold to get the data for
    with_val - whether to include validation set or not
    label_column - column name for the target class
    fold_column - column name for the fold number
    results_directory - directory to store the results
    seed_value - seed value for reproducibility
    sequence_length - length of the sequence for RNNs or transformers
    
    """

    try:

        # # Set seed
        random.seed(seed_value)
        np.random.seed(seed_value)
        #tf.random.set_seed(seed_value)
        torch.manual_seed(seed_value)
        torch.cuda.manual_seed_all(seed_value)
    

        # get features and target class
        features = df.iloc[:,6:]
        target_class = df[label_column].values
        target_class = target_class.astype('int')
        sessions = df['session'].values

        X_test = features
        y_test = target_class


        print(X_test.shape, y_test.shape)

        X_test = X_test.reset_index(drop=True)

        # Create sequences for LSTM
        
        X_test_sequences, y_test_sequences = create_sequences(X_test.values, y_test, sessions, sequence_length)


        return sessions, X_test, y_test, X_test_sequences, y_test_sequences
    
    except Exception as e:
        print(f"An error occurred: {e}")



        