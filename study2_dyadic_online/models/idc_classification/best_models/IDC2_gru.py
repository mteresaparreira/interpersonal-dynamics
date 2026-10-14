# superBAD_lstm.py

"""
Description: This script trains a LSTM Model on the facial data extracted from the OpenFace library to classify human reactions into Control, Failure Human, Failure Robot classes
Author: Sukruth Gowdru Lingaraju
Date Created: August 18th, 2023
Python Version: 3.10.9
Email: sg2257@cornell.edu
"""

"""
Begin: Import Dependencies 
"""

import os
import random
import datetime
import pickle
import traceback
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
import matplotlib.pyplot as plt
import keras

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
#from tensorflow.keras.models import Sequential
#from tensorflow.keras.layers import LSTM, Dense, Dropout
from keras.models import Sequential
from keras import layers
from keras.layers import GRU, Dense, Dropout, Bidirectional

import sys
sys.path.insert(1, '../')
from get_metrics import get_metrics
from createDataSplits_idc import createDataSplits, createDataSplits_all

physical_devices = tf.config.list_physical_devices('GPU')
print("GPU available:", physical_devices)
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)

"""
End: Import Dependencies 
"""
"""
Begin: Method Definitions
"""



def executeModel_LSTM(df, results_directory, seed_value = 42, sequence_lengths = 1, units = 64, dropouts = 0.2, activations = 'softmax', losses = 'categorical_crossentropy', optimizers = 'adam', epochs = 1000, batch_sizes = 32):

    """
    executeModel_LSTM(): takes in the dataFrame along with the directory specification & hyper-parameters and trains a LSTM model

    Parameters:
    - df
    - results_directory
    - seed_value
    - sequence_length (a.k.a: lookback)
    - units
    - dropouts
    - activations
    - losses
    - optimizers
    - epochs
    """
    # Keep count of the number of different search combinations
    search_count = 0

    # Create a figure with subplots for plotting the training and validation accuracy for various batch_sizes against the # of epochs
    num_rows = 2
    num_cols = 2
    batch_figure, axs = plt.subplots(num_rows, num_cols, figsize=(15, 8))
    
    tf.compat.v1.reset_default_graph()

    for sequence_length in sequence_lengths:
        for unit in units:
            for dropout in dropouts:
                for activation in activations:
                    for loss in losses:
                        for optimizer in optimizers:
                            for epoch in epochs:
                                for i, batch_size in enumerate(batch_sizes):
                                    for fold_no in range(5):
                                        try:

                                            #seed
                                            np.random.seed(seed_value)
                                            tf.random.set_seed(seed_value)
                                            keras.utils.set_random_seed(seed_value)

                                            search_count += 1
                                            print('sequence_length:', sequence_length)
                                            print('unit:', unit)
                                            print('dropout:', dropout)
                                            print('activation:', activation)
                                            print('loss:', loss)
                                            print('optimizer:', optimizer)
                                            
                                            print('GETTING DATA')
                                            # # Retrieve the splits
                                            sessions,num_classes, X_train, X_val, X_test, y_train, y_val, y_test, X_train_sequences, y_train_sequences, X_val_sequences, y_val_sequences, X_test_sequences, y_test_sequences = createDataSplits_all(df,fold_no, with_val = 1, results_directory= '../logs/', sequence_length = sequence_length)
                                            
                                            print('num classes:', num_classes)

                                            
                                            """df, fold_no, with_val = 0, label_column = 'UserAkwardness', fold_column = 'fold_id', results_directory= '../logs/', seed_value = 42, sequence_length = 1):
                                            X_train, X_val, X_test, y_train, y_val, y_test, X_train_sequences, y_train_sequences, X_val_sequences, y_val_sequences, X_test_sequences, y_test_sequences
                                            ------------------------------------------------------------------------------------
                                            Begin: Model Architecture
                                            """
                                            # # Check GPU availability
                                            # gpus = tf.config.list_physical_devices('GPU')
                                            # print("GPU available:", gpus)
                                            # # tf.debugging.set_log_device_placement(True)

                                            # # Assuming there is at least one GPU available
                                            # if gpus:
                                            #     # Set TensorFlow to use GPU 0
                                            #     try:
                                            #         tf.config.experimental.set_visible_devices(gpus[0], 'GPU')
                                            #         logical_gpus = tf.config.experimental.list_logical_devices('GPU')
                                            #         # gpu_device = tf.config.list_physical_devices('GPU')[0]
                                            #         # tf.config.experimental.set_memory_growth(gpu_device, True)
                                            #         # print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
                                            #     except RuntimeError as e:
                                            #         print(e)
                                                    
                                            # # Specify the device used for computation
                                            with tf.device('/GPU:0'):  # Use GPU 0

                                                # Build and train your model here

                                                # # Create the LSTM model
                                                model =keras.Sequential()
                                                model.add(layers.GRU(units = unit, input_shape = (sequence_length, X_train_sequences.shape[2])))
                                                model.add(layers.Dropout(dropout))
                                                model.add(layers.Dense(units=num_classes, activation = activation))

                                                #if optimizer == 'Adam':
                                                #    optimizer = keras.optimizers.Adam(learning_rate=0.0001)
                                                #elif optimizer == 'Adadelta':
                                                #    optimizer = keras.optimizers.Adadelta(learning_rate=0.0001)


                                                # Compile the model
                                                model.compile(loss = loss, optimizer = optimizer, metrics = ['accuracy'])

                                                #implement early stopping
                                                early_stopping = keras.callbacks.EarlyStopping(
                                                    monitor='val_loss',
                                                    patience=5,
                                                    min_delta=0.001,
                                                    restore_best_weights=True,
                                                )


                                                # Train the model and capture the history data
                                                model_history = model.fit(
                                                    np.array(X_train_sequences),
                                                    y_train_sequences,
                                                    batch_size = batch_size,
                                                    epochs = epoch,
                                                    verbose = '2',
                                                    validation_data=(np.array(X_val_sequences), y_val_sequences)#,
                                                    #callbacks=[early_stopping]
                                                )


                                                
                                                # Obtain the training loss & accuracy data
                                                train_loss, train_accuracy = model_history.history['loss'], model_history.history['accuracy']
                                                
                                                # Obtain the validation loss & accuracy data
                                                val_loss, val_accuracy = model_history.history['val_loss'], model_history.history['val_accuracy']
                                                
                                                # Evaluate the model on test data
                                                #test_loss, test_accuracy = model.evaluate(np.array(X_test_sequences), y_test_sequences)
                                                #y_pred = model.predict(np.array(X_test_sequences))
                                                y_predict_probs = model.predict(np.array(X_test_sequences))
                                                y_pred = np.argmax(y_predict_probs, axis=1)  # Convert to class labels

                                                #transgorm y_test sequences so single array, from one-hot
                                                y_test_sequences = np.argmax(y_test_sequences, axis=1)
                                                print('sessions shape:', len(sessions))

                                                #calculate metrics
                                                test_metrics = get_metrics(y_pred, np.array(y_test_sequences), sessions = sessions, tolerance=1)
                                                print(test_metrics)

                                                """
                                                Save the model information data as an object
                                                Define the path to store the object data & create the directory if it does not exist
                                                """
                                                model_data_path = results_directory + 'model_data/'
                                            
                                                
                                                if not os.path.exists(model_data_path):
                                                    os.makedirs(model_data_path)

                                                # Store the model learning data using pickle
                                                model_data_information = {
                                                    'train_loss': train_loss,
                                                    'train_accuracy': train_accuracy,
                                                    'val_loss': val_loss,
                                                    'val_accuracy': val_accuracy,
                                                    'test accuracy': test_metrics['accuracy'],
                                                    'test precision': test_metrics['precision'],
                                                    'test recall': test_metrics['recall'],
                                                    'test f1': test_metrics['f1'],
                                                    'test accuracy_tolerant': test_metrics['accuracy_tolerant'],
                                                    'test precision_tolerant': test_metrics['precision_tolerant'],
                                                    'test recall_tolerant': test_metrics['recall_tolerant'],
                                                    'test f1_tolerant': test_metrics['f1_tolerant'],

                                                }

                                                #store the model itself
                                                model.save(model_data_path + f'model_{sequence_length}_{unit}_{dropout}_{activation}_{loss}_{optimizer}_{epoch}_{batch_size}_{fold_no}.h5')
                                                #model weights
                                                model.save_weights(model_data_path + f'model_weights_{sequence_length}_{unit}_{dropout}_{activation}_{loss}_{optimizer}_{epoch}_{batch_size}_{fold_no}.h5')


                                                
                                                """
                                                End: Model Architecture
                                                ------------------------------------------------------------------------------------
                                                """
                                                """
                                                ------------------------------------------------------------------------------------
                                                    Predictions using the Model
                                                    ===========================

                                                    When making predictions using the trained model, the output is in the form of predicted probabilities,
                                                    indicating the likelihood of each sample belonging to each target class.

                                                    Predicted Probabilities (y_predict_probs):
                                                    - Shape: (#samples, #target_classes)
                                                    - Each value in y_predict_probs represents the probability of the corresponding sample being classified
                                                    into the respective class.

                                                    Converting Probabilities to Class Labels (y_predict):
                                                    - The y_predict array is derived by finding the index of the maximum value along a specified axis.
                                                    - It represents the predicted class label for each sample based on the highest predicted probability.
                                                ------------------------------------------------------------------------------------
                                                """

                                                """
                                                ------------------------------------------------------------------------------------
                                                Begin: Logging 
                                                - Write all the information of the particular combination of the model to a file below
                                                """

                                                with open(f'{results_directory}/results.txt', 'a') as results_file:
                                                    results_file.write("\n")
                                                    results_file.write(f"------------ BEGIN SEARCH : {search_count} ------------" + "\n")
                                                    results_file.write("------------ TYPE ------------" + "\n")

                                                    results_file.write(
                                                        f'Sequence Length = {sequence_length}\n'
                                                        f'Units = {unit}\n'
                                                        f'Dropout = {dropout}\n'
                                                        f'Activation = {activation}\n'
                                                        f'Loss Function = {loss}\n'
                                                        f'Optimizer = {optimizer}\n'
                                                        f'Epochs = {epoch}\n'
                                                        f'Batch Size = {batch_size}\n'
                                                        f'Seed Value = {seed_value}\n'
                                                        f'Fold Number = {fold_no}\n'
                                                    )

                                                    results_file.write("------------ METRICS ------------" + "\n")

                                                    results_file.write(f'Train Loss: {train_loss}' + '\n')
                                                    results_file.write(f'Train Accuracy: {train_accuracy}' + '\n')
                                                    results_file.write(f'Validation Loss: {val_loss}' + '\n')
                                                    results_file.write(f'Validation Accuracy: {val_accuracy}' + '\n')
                                                    results_file.write(f'Test Accuracy: {test_metrics["accuracy"]}' + '\n')
                                                    results_file.write(f'Test Precision: {test_metrics["precision"]}' + '\n')
                                                    results_file.write(f'Test Recall: {test_metrics["recall"]}' + '\n')
                                                    results_file.write(f'Test F1: {test_metrics["f1"]}' + '\n')
                                                    results_file.write(f'Test Accuracy Tolerant: {test_metrics["accuracy_tolerant"]}' + '\n')
                                                    results_file.write(f'Test Precision Tolerant: {test_metrics["precision_tolerant"]}' + '\n')
                                                    results_file.write(f'Test Recall Tolerant: {test_metrics["recall_tolerant"]}' + '\n')
                                                    results_file.write(f'Test F1 Tolerant: {test_metrics["f1_tolerant"]}' + '\n')


                                                    results_file.write("------------ PARAMETERS ------------" + "\n")

                                                    results_file.write(f'Model Parameters: {model_history.params}' + '\n')
                                                    results_file.write(f'Model Keys: {model_history.history.keys()}' + '\n')
                                                

                                                #keras delete model weights
                                                keras.backend.clear_session()

                                                

                                        except Exception as e:
                                            with open(f'{results_directory}/results.txt', 'a') as results_file:
                                                results_file.write(
                                                    f'Exception {e} thrown for :- \n'
                                                    f'{traceback.print_exc()} \n'
                                                    f'Sequence Length = {sequence_length}\n'
                                                    f'Units = {unit}\n'
                                                    f'Dropout = {dropout}\n'
                                                    f'Activation = {activation}\n'
                                                    f'Loss Function = {loss}\n'
                                                    f'Optimizer = {optimizer}\n'
                                                    f'Epochs = {epoch}\n'
                                                    f'Batch Size = {batch_size}\n'
                                                    f'Seed Value = {seed_value}\n'
                                                )
                                        # break # batch_size break

            #                         break # epochs break
            #                     break # optimizers break
            #                 break # losses break
            #             break # activation functions break
            #         break # dropouts break
            #     break # units break
            # break # sequence_lengths break

def main():
    
    """
    Begin: Directories specification
    """
    
    # allParticipants dataset path
    train_df = pd.read_csv('../../data/all_data_05_sign.csv')  
    # results directory - make a new folder with the day and time of the run
    import datetime
    now = datetime.datetime.now()
    results_directory = './results/' + 'gru_05_s_all1_' + now.strftime("%Y-%m-%d_%H-%M-%S") + '/'
    
    # Create 'results_directory' if it doesn't exist
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)
    
    """
    End: Directories specification
    """

    """
    Begin: Hyperparameters definition
    """
    
    sequence_lengths = [5]
    units = [64]
    dropouts = [0.6]
    activations = ['softmax']
    losses = ['categorical_crossentropy']
    optimizers = ['Adam']
    epochs = [500]
    batch_sizes = [512] #, 2048, 4096]
    """
    End: Hyperparameters definition
    """
    
    """
    Begin: Call methods
    """

    # Call your model execution function with keyword arguments
    executeModel_LSTM(
        train_df,
        results_directory,
        seed_value = 42,
        sequence_lengths = sequence_lengths,
        units = units,
        dropouts = dropouts,
        activations = activations,
        losses = losses,
        optimizers = optimizers,
        epochs = epochs,
        batch_sizes = batch_sizes
    )

    """
    End: Call methods
    """
"""
End: Method Definitions
"""

if __name__ == "__main__":
    main()