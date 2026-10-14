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
#log regression

from sklearn.metrics import mean_squared_error
import joblib
import random

import torch
import torch.nn as nn
from scipy.stats import pearsonr

import wandb
wandb.login()


from torch.utils.data import DataLoader, TensorDataset

from createDataSplits import createDataSplits
import pprint



# Define the model
class GRUModel(nn.Module):
    def __init__(self, input_size, hidden_size, dropout_prob, output_size):
        super(GRUModel, self).__init__()
        self.lstm = nn.GRU(input_size, hidden_size, batch_first=True)
        self.dropout = nn.Dropout(dropout_prob)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        lstm_out = self.dropout(lstm_out[:, -1, :])
        output = self.fc(lstm_out)
        return output






def build_dataset(train_data, seq_len, results_directory, batch_size, num_workers = 4):
   
    #create data splits - imported function
    X_train, X_test, y_train, y_test, X_train_sequences, y_train_sequences, X_test_sequences, y_test_sequences = createDataSplits(train_data, with_val = 0,sequence_length=seq_len, results_directory= results_directory, seed_value = 42)
    
    # Create the dataset and dataloaders (adjust this part based on your dataset)
    X_train_tensor = torch.tensor(X_train_sequences, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train_sequences, dtype=torch.float32)
    X_test_tensor = torch.tensor(X_test_sequences, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test_sequences, dtype=torch.float32)
    #print dimensions
    print(X_train_tensor.shape, y_train_tensor.shape)
    print(X_test_tensor.shape, y_test_tensor.shape)
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, num_workers = num_workers, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    #write

    with open(results_directory, 'a') as f:
        f.write(str('X_train shape: ' + str(X_train.shape)))
        f.write(str('\n'))
        f.write(str('X_test shape: ' + str(X_test.shape)))
        f.write(str('\n'))
        f.write(str('y_train shape: ' + str(y_train.shape)))
        f.write(str('\n'))
        f.write(str('y_test shape: ' + str(y_test.shape)))
        f.write(str('\n'))
        f.write(str('X_train_sequences shape: ' + str(X_train_sequences.shape)))
        f.write(str('\n'))
        f.write(str('X_test_sequences shape: ' + str(X_test_sequences.shape)))
        f.write(str('\n'))
        f.write(str('y_train_sequences shape: ' + str(y_train_sequences.shape)))
        f.write(str('\n'))
        f.write(str('y_test_sequences shape: ' + str(y_test_sequences.shape)))
        f.write(str('\n'))
        f.write(str('X_train_tensor shape: ' + str(X_train_tensor.shape)))
        f.write(str('\n'))
        f.write(str('X_test_tensor shape: ' + str(X_test_tensor.shape)))
        f.write(str('\n'))
        f.write(str('y_train_tensor shape: ' + str(y_train_tensor.shape)))
        f.write(str('\n'))
        f.write(str('y_test_tensor shape: ' + str(y_test_tensor.shape)))
        f.write(str('\n'))

    return train_loader, test_loader, X_train_tensor, y_train_tensor, X_test_tensor, y_test_tensor


#calculate ccc
def calc_ccc(x, y):
    mean_x = torch.mean(x)
    mean_y = torch.mean(y)
    std_x = torch.std(x)
    std_y = torch.std(y)
    #calculate person correlation coefficient (pearson r)
    x = x.cpu().numpy()
    y = y.cpu().numpy()
    r = pearsonr(x, y)[0]
    ccc = 2.0 *  r*std_x*std_y / (std_x**2 + std_y**2 + (mean_x - mean_y)**2)
    return ccc

#calculate ccc for numpy arrays
def calc_ccc_np(x, y):
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    pearson_r = pearsonr(x, y)[0]
    std_x = np.std(x)
    std_y = np.std(y)
    ccc = 2.0 * pearson_r*std_x*std_y / (std_x**2 + std_y**2 + (mean_x - mean_y)**2)
    return ccc

class CCCLoss(nn.Module):
    def forward(self, y_pred, y_true):
        return 1.0 - self.calc_ccc(y_pred, y_true)

    def calc_ccc(self, x, y):
        mean_x = torch.mean(x)
        mean_y = torch.mean(y)
        std_x = torch.std(x)
        std_y = torch.std(y)
        
        # Calculate Pearson correlation coefficient (pearson r)
        x_np = x.detach().cpu().numpy()
        y_np = y.detach().cpu().numpy()
        r = pearsonr(x_np, y_np)[0]
        
        ccc = 2.0 * r * std_x * std_y / (std_x**2 + std_y**2 + (mean_x - mean_y)**2)
        return ccc

def train_wrapper(train_data,results_directory, seq_len, device, config= None):
            #

    def train(config=None):
        with wandb.init(config=config):
            config = wandb.config
            hidden_size = config.hidden_size
            dropout_prob = config.dropout_prob
            lr = config.lr
            batch_size =config.batch_size


            NUM_WORKERS = 4
            print('GOT HERE 1')
            wandb.log({'message': 'GOT HERE 1'})
            train_loader, test_loader,X_train_tensor,y_train_tensor,X_test_tensor,y_test_tensor = build_dataset(train_data, seq_len=seq_len, batch_size=batch_size, results_directory=results_directory, num_workers = NUM_WORKERS)

            X_train_tensor = X_train_tensor.to(device)
            y_train_tensor = y_train_tensor.to(device)
            X_test_tensor = X_test_tensor.to(device)
            y_test_tensor = y_test_tensor.to(device)
           
            input_size = X_train_tensor.shape[2]
            output_size = 1
            wandb.log({'message': 'GOT HERE 2'})
            print(input_size, output_size)


            model = GRUModel(input_size, hidden_size, dropout_prob, output_size)

            #model to cude
            model.to(device)

        
            criterion = CCCLoss()
            #create criterion with CCC
            

            optimizer = torch.optim.Adam(model.parameters(), lr=lr)

            #best_train_ccc = -1.0
            #patience = 20
            #early_stopping_counter = 0

            for epoch in range(500):  # You can adjust the number of epochs

                model.train()
                for _, (data, target) in enumerate(train_loader):
                    data, target = data.to(device), target.to(device)
                    optimizer.zero_grad()
                    outputs = model(data)
                    #changeg here for ccc
                    outputs = outputs.view(-1)
                    loss = criterion(outputs, target)
                    loss.backward()
                    optimizer.step()

                


                #validate at every 2 epochs
                if epoch % 2 != 0:
                    continue
                model.eval()
                with torch.no_grad():
                    #get all of the loader at once, not in batches
                    y_pred = model(X_train_tensor)
                    #change shape of y pred to be 1 dimensional
                    y_pred = y_pred.view(-1)
                    #print('SHAPES', y_pred.shape, y_train_tensor.shape)
                    #get rmse

                    mse = mean_squared_error(y_train_tensor.cpu().numpy(), y_pred.cpu().numpy())
                    ccc = calc_ccc(torch.tensor(y_pred), y_train_tensor)
                    ccc_np = calc_ccc_np(y_train_tensor.cpu().numpy(), y_pred.cpu().numpy())

                print(f"Epoch [{epoch+1}], Loss: {loss.item():.20f}, CCC: {ccc:.20f}, MSE: {mse:.20f}, CCC_np: {ccc_np:.20f}")
                with open(results_directory, 'a') as f:
                    f.write(f"Epoch [{epoch+1}], Loss: {loss.item():.20f}, CCC: {ccc:.20f}, MSE: {mse:.20f}")
                    f.write(str('\n'))
                    
                wandb.log({"MSE": mse, "CCC": ccc})
                

                #now, the test
                model.eval()
                with torch.no_grad():
                    y_testpred = model(X_test_tensor)
                    #get rmse
                    y_testpred = y_testpred.view(-1)
                    mse = mean_squared_error(y_test_tensor.cpu().numpy(), y_testpred.cpu().numpy())
                    ccc = calc_ccc(torch.tensor(y_testpred), y_test_tensor)
                    ccc_np = calc_ccc_np(y_test_tensor.cpu().numpy(), y_testpred.cpu().numpy())
                print(f"Epoch [{epoch+1}],TESTS CCC: {ccc:.20f}, MSE: {mse:.20f}, CCC_np: {ccc_np:.20f}")
                with open(results_directory, 'a') as f:
                    f.write(f"Epoch [{epoch+1}], TEST Loss: {loss.item():.20f}, CCC: {ccc:.20f}, MSE: {mse:.20f}")
                    f.write(str('\n'))

                # Log the test performance to wandb
                wandb.log({"Test MSE": mse, "Test CCC": ccc})



                # Update best hyperparameters if better metrics are achieved
                global best_mse, best_ccc
                # Define a variable to store the best hyperparameters and their corresponding metrics
                best_hyperparameters = {}
                best_mse = float("inf")
                best_ccc = -1.0
                if mse < best_mse:
                    best_mse = mse
                    best_hyperparameters["MSE"] = mse
                    best_hyperparameters["hidden_size"] = hidden_size
                    best_hyperparameters["dropout_prob"] = dropout_prob
                    best_hyperparameters["lr"] = lr
                    best_hyperparameters["batch_size"] = batch_size

                if ccc > best_ccc:
                    best_ccc = ccc
                    best_hyperparameters["CCC"] = ccc

                
                

                with open(results_directory, 'a') as f:
                    f.write("Best Hyperparameters:\n")
                    for key, value in best_hyperparameters.items():
                        f.write(f"{key}: {value}\n")


    return train






def main():  

    path = '../'
    listfiles = os.listdir(path)

    training_files = [file for file in listfiles if file.endswith('.csv') and ('pca' in file or 'PCA' in file)]
    print(training_files)
    seed_value = 42
    # # Set seed
    random.seed(seed_value)
    np.random.seed(seed_value)
    #tf.random.set_seed(seed_value)
    torch.manual_seed(seed_value)
    torch.cuda.manual_seed_all(seed_value)

    for file in training_files:

        #global train_data, results_directory, seq_len, device


        #get training data

        train_data = pd.read_csv(path + file)


        print ('START NEW') 
        codename = 'lstm'
        seq_len = 10 #5,10,15

        codename = codename + file[8:-13]
        
        # results directory - make a new folder with the day and time of the run

        results_directory = '../logs/results_' + codename+'_seq'+ str(seq_len) + '.txt'

        print(results_directory)
        #check if cuda is available
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(device)

        with open(results_directory, 'w') as f:
            f.write(str('Results'))
            #enter
            f.write(str('\n'))
            f.write(str('Codename: ' + codename))
            f.write(str('\n'))
            f.write(str('device: ' + str(device)))
            f.write(str('\n'))
            f.close()


        

        # Define the sweep configuration
        sweep_config = {
            "method": "random",
            #goal is to minimize mse
            "metric": {"goal": "maximize", "name": "CCC"},
            "parameters": {
                "hidden_size": {"values": [32, 64, 128]},
                #"dropout_prob": {"min": 0.0, "max": 0.6},
                "dropout_prob": {"values": [0.0, 0.2, 0.4, 0.6]},
                #"lr": {"min": 0.0001, "max": 0.01},
                "lr": {"values": [0.0001, 0.001, 0.01]},
                "batch_size": {"values": [32, 64, 128]},
            },
        }


        # Initialize wandb sweep
        #wandb.init(project="lstm-hyperparameter-tuning")
        sweep_id = wandb.sweep(sweep_config,project="gru-hyperparameter-tuning_10_ccc")

        train_func = train_wrapper(train_data,results_directory, seq_len, device)

        wandb.agent(sweep_id, train_func)


if __name__ == '__main__':
    main()