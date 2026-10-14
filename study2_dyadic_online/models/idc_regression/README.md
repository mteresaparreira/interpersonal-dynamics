# IDC regression (2023)

Regress the **continuous** Interpersonal Dynamics Curve from multimodal interaction
features. This is the benchmark reported in the Q1 2023–24 progress report.

**Data:** `all_data_l{2.5,5,7.5}t{2.5,5}_norm[_pca].csv` — 12 datasets crossing
feature lookback `l` with IDC horizon `h`. 60 192 samples; PCA to 88–92 components.

**Loss and metric:** Concordance Correlation Coefficient. `CCCLoss` (`1 − CCC`) is
implemented inline in each PyTorch script; the sklearn scripts wrap CCC as a
`make_scorer` for `GridSearchCV`.

**Protocol:** tune on 80/20, then retrain the winner over 5 folds for 1000 epochs,
report the fold average.

| File | Model | Search |
|---|---|---|
| `train_linreg.py` | LinearRegression | — |
| `train_mlpreg.py` | MLPRegressor | hidden {50,100,250,500} × activation {logistic,tanh,relu} × solver {lbfgs,sgd,adam} × alpha {0.05,0.0005,0.5} |
| `train_rfreg.py` | RandomForestRegressor | n_estimators {10,100,250,500} |
| `train_svr.py` | SVR | kernel {linear,poly,rbf,sigmoid} × C {0.1,0.5,1.0} × ε {0.1,0.01,0.3} |
| `train_lstm_5_norm.py` | LSTM | W&B sweep |
| `train_gru_10.py`, `train_gru_final.py` | GRU | W&B sweep |
| `train_blstm_10_ccc.py` | BiLSTM | W&B sweep |
| `train_transformer_10.py` | Transformer | W&B sweep, also tested single-sample input |
| `FINAL_BEST_GRU.py` | the winning GRU, retrained over all folds | — |
| `createDataSplits.py` | shared 5-fold session-grouped splitter + sequence builder | — |
| `obtain_best_model_csv.py` | pulls the best epoch per sweep out of the W&B exports | — |
| `train_lstm_5_norm.sub` | representative SLURM job spec | — |

All RNNs use sequence length 10 samples (= 5 s at 2 Hz); an initial sweep over
{5, 10, 15} settled that.

Results table: [`../../../docs/results.md`](../../../docs/results.md#1-idc-regression-2023--modelsidc_regression).
