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
from torch.nn import TransformerEncoder, TransformerEncoderLayer


from createDataSplitsAll import createDataSplits
import pprint

#create final_plot folder
if not os.path.exists('../final_plot'):
    os.makedirs('../final_plot')



# Define the model
class TransformerModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_heads, dropout_prob, output_size):
        super(TransformerModel, self).__init__()
        
        self.transformer_encoder =  TransformerEncoder(TransformerEncoderLayer(input_size, num_heads, dim_feedforward=hidden_size, dropout=dropout_prob, batch_first=True), num_layers=1)
        self.fc = nn.Linear(input_size, output_size)

    def forward(self, x):
        #print(f"Before TransformerEncoder: {x.shape}")
        x = self.transformer_encoder(x)
        #print(f"After TransformerEncoder: {x.shape}") 
        x = x.mean(dim=1) 
        #print(f"After mean: {x.shape}")
        x = self.fc(x)
        #print(f"After fc: {x.shape}")
        return x



def build_dataset(train_data, seq_len=10, batch_size = 128, fold_index = 1):
   
    #create data splits - imported function
    X_train, X_test, y_train, y_test, X_train_sequences, y_train_sequences, X_test_sequences, y_test_sequences = createDataSplits(train_data, with_val = 0,sequence_length=seq_len, results_directory= '.', seed_value = 42, fold_index=
                                                                                                                                          fold_index)
   


    X_test_tensor = torch.tensor(X_test_sequences, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test_sequences, dtype=torch.float32)
    #print dimensions
    print(X_test_tensor.shape, y_test_tensor.shape)
    test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

   #save the x_test and y test as csvs
   #turn into pandas
    X_test_df = pd.DataFrame(X_test)
    y_test_df = pd.DataFrame(y_test)
    X_test_df.to_csv('../final_plot/x_test.csv')
    y_test_df.to_csv('../final_plot/y_test.csv')
      
    return X_test, y_test, X_test_tensor, y_test_tensor, test_loader


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


def train_wrapper(results_directory, seq_len, device, config= None):
            #

    def train(config=None):
        with wandb.init(config=config):
            config = wandb.config
            hidden_size = config.hidden_size
            dropout_prob = config.dropout_prob
            lr = config.lr
            batch_size =config.batch_size
           
            num_heads = config.num_heads


            NUM_WORKERS = 4
            print('GOT HERE 1')
            wandb.log({'message': 'GOT HERE 1'})
            #log which dataset is used (tr)
            wandb.log({'directory': results_directory})

            #create folder to save models
            model_dir = '../best_model'
            if not os.path.exists(model_dir):
                os.makedirs(model_dir)

            folds = np.arange(5)
            folds = [1]
            avg_train_ccc = []
            avg_test_ccc = []
            avg_train_rmse = []
            avg_test_rmse = []
            for fold in folds:
                #if fold <2:
                #    continue
                print('FOLD', fold)

                training_files = ['../all_data_l5t5_norm_pca.csv']
                file = training_files[0]
                train_data = pd.read_csv(file)
                train_loader, test_loader,X_train_tensor,y_train_tensor,X_test_tensor,y_test_tensor = build_dataset(train_data, seq_len=seq_len, batch_size=batch_size, results_directory=results_directory, num_workers = NUM_WORKERS, fold_index=
                                                                                                                                            fold)


                X_train_tensor = X_train_tensor.to(device)
                y_train_tensor = y_train_tensor.to(device)
                X_test_tensor = X_test_tensor.to(device)
                y_test_tensor = y_test_tensor.to(device)
            
                input_size = X_train_tensor.shape[2]
                output_size = 1
                print(input_size, output_size)

                #if the input size is not divisible by the number of heads, make number of heads 1
                if input_size % num_heads != 0:
                    num_heads = 1
                    print('num heads changed to 1')
                    #change this in wandb config
                    wandb.config.num_heads = num_heads
                    wandb.log({'heads': 'num heads changed to 1'})



                model = TransformerModel(input_size, hidden_size,num_heads, dropout_prob, output_size)

                #model to cude
                model.to(device)

            
                criterion = CCCLoss()
                #create criterion with CCC
                

                optimizer = torch.optim.Adam(model.parameters(), lr=lr)

                #best_train_ccc = -1.0
                #patience = 20
                #early_stopping_counter = 0

                for epoch in range(2000):  # You can adjust the number of epochs
                    #print('EPOCH', epoch)
                    model.train()
                    for _, (data, target) in enumerate(train_loader):
                        #get dims
                        
                        if target.shape[0] != batch_size:
                            continue
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

                    train_ccc = ccc
                    train_rmse = mse

                    #print('EVAL NOW')
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


                    #save model at every epoch, in the model_dir
                    torch.save(model.state_dict(), os.path.join(model_dir, f"model_{epoch}.pth"))
                

                    





def main():  

    
    seed_value = 42
    # # Set seed
    random.seed(seed_value)
    np.random.seed(seed_value)
    #tf.random.set_seed(seed_value)
    torch.manual_seed(seed_value)
    torch.cuda.manual_seed_all(seed_value)

    #global train_data, results_directory, seq_len, device


    #get model
    best_epoch = 806
    #model_folder
    model_folder = '../best_modelt'
    #get model, saved as model_best_epoch.pth
    model_path = os.path.join(model_folder, f"model_{best_epoch}.pth")
    print(model_path)
    state_dict = torch.load(model_path)
    print(state_dict.keys())
    #now, get the config
    #load model
    model = TransformerModel(input_size=89,hidden_size=1048,num_heads=1,dropout_prob=0.3,
                output_size=1)
    

    model.load_state_dict(torch.load(model_path))
    



    #now, get the test data
    fold_index = 1
    training_files = ['../all_data_l5t5_norm_pca.csv']
    file = training_files[0]
    seq_len = 10

    train_data = pd.read_csv(file)
    X_test, y_test,X_test_tensor,y_test_tensor,test_loader = build_dataset(train_data, seq_len=seq_len, fold_index=fold_index)



    model.eval()
    with torch.no_grad():
        y_testpred = model(X_test_tensor)
        #get rmse
        y_testpred = y_testpred.view(-1)
        mse = mean_squared_error(y_test_tensor.cpu().numpy(), y_testpred.cpu().numpy())
        ccc = calc_ccc(torch.tensor(y_testpred), y_test_tensor)
        ccc_np = calc_ccc_np(y_test_tensor.cpu().numpy(), y_testpred.cpu().numpy())
    print(f"TESTS CCC: {ccc:.20f}, MSE: {mse:.20f}, CCC_np: {ccc_np:.20f}")
                   
    #save the y_testpred and y_test as csvs
    y_testpred_df = pd.DataFrame(y_testpred.cpu().numpy())
    y_test_df = pd.DataFrame(y_test)
    y_testpred_df.to_csv('../final_plot/y_testpred.csv')
    y_test_df.to_csv('../final_plot/y_test_just_check.csv')

if __name__ == '__main__':
    main()
