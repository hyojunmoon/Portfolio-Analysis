# Portfoilo Analyzer

The **Portfoilo Analyzer** is basic portfolio analyzing tool with **visualization** supporting both *cumulative return data* and *return data*


<img src="example.PNG" alt="drawing" width="850"/>


Supported Analysis

- CAGR
- Sharpe Ratio
- Sortino Ratio
- MDD
- Average Drawdown

Visualization

- Cumulative Return
- Log-scale Cumulative Return
- Drawdown
- Analysis data table

## Install
```Shell
    pip install PortfolioAnalysis
```
or

```Shell
    python setup.py install
```

## How to use
```Python
    #import
    from PortfolioAnalysis import PortfolioAnalysis

    #read csv to get dataframe
    returns = pd.read_csv(r'C:\Users\QRAFT1\Desktop\data\ks_etf\returns.csv', index_col=['Date'])

    #Analyze data during initialization
    analysis = PortfolioAnalysis(returns, cumulative=True, auto_drop=True, window='M')

    #Visualization (http)
    analysis.report()
```
