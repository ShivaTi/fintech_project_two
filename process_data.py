import pandas as pd
import hvplot.pandas
import numpy as np


def make_tweeting_price_curve():
    '''
    Make plots that shows Elon Musk's crypto related tweeting times vs the crypto's historical prices

    Returns: A tuple of Hvplot objects.

    Items in the tutple:
    1. A line plot showing Bitcoin's historical price with some markers on the top indicating when Elon Musk tweets something about Bitcoin
    1. A line plot showing Dogecoin's historical price with some markers on the top indicating when Elon Musk tweets something about Dogecoin
    '''

    # Load data for Dogecoin
    df_elon_doge = pd.read_pickle('./data/elon_doge.plk')

    # Visualize tweeting times for Dogecoin
    tweeting_doge = df_elon_doge[df_elon_doge["Does Elon Musk's Tweet Tention the Word DOGE?"] == 1]['Dogecoin Price'].hvplot.scatter(
        color='royalblue',
        marker='circle',
        size=50,
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400,
        shared_axes=False
    )

    # Visualize close price of Dogecoin
    price_curve_doge = df_elon_doge[['Dogecoin Price']].hvplot(
        line_color='lightgray',
        ylabel='Price in $',
        width=1000,
        height=400,
        shared_axes=False
    )

    # Overlay plots for Dogecoin
    tweeting_price_curve_doge = price_curve_doge * tweeting_doge
    tweeting_price_curve_doge.opts(width=1000, title='When Elon Musk tweets about Dogecoin', ylabel='Dogecoin price in $')

    # Load data for Bitcoin
    df_elon_btc = pd.read_pickle('./data/elon_btc.plk')

    # Visualize tweeting times for Bitcoin
    tweeting_point_btc = df_elon_btc[df_elon_btc["Does Elon Musk's Tweet Tention the Word Bitcoin or BTC?"] == 1]['Bitcoin Price'].hvplot.scatter(
        color='royalblue',
        marker='circle',
        size=50,
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400,
        shared_axes=False
    )

    # Visualize close price of Bitcoin
    price_curve_btc = df_elon_btc[['Bitcoin Price']].hvplot(
        line_color='lightgray',
        ylabel='Price in $',
        width=1000,
        height=400,
        shared_axes=False
    )

    # Overlay plots for Bitcoin
    tweeting_price_curve_btc = price_curve_btc * tweeting_point_btc
    tweeting_price_curve_btc.opts(width=1000, title='When Elon Musk tweets about Bitcoin', ylabel='Bitcoin price in $')

    # Return tweeting vs price curves
    return tweeting_price_curve_btc, tweeting_price_curve_doge


    # _________________________________________________________________________________________________________________________________________________________ 


def make_cumulative_curve():                   
    '''
    Make plots that shows crypto's cumulative returns

    Returns: A tuple of Hvplot objects.

    Items in the tutple:
    1. A line plot showing Bitcoin's cumulative returns 
    2. A line plot showing Dogecoin's cumulative returns 
    '''
    
    df1 = pd.read_pickle("data/elon_doge.plk")
          
    # Drop unnecessary columns
    df1_doge = df1.drop(columns=["Elon Musk's Tweet in List", 
                                "Elon Musk's Tweet in String",
                                "Elon Musk's Tweet That Mentions the Word DOGE",
                                "Does Elon Musk's Tweet Tention the Word DOGE?"])
           
    # Calculate the daily return using the 'shift()' function
    daily_returns = (df1_doge - df1_doge.shift(1)) / df1_doge.shift(1)

    # Calculate the cumulative returns using the 'cumprod()' function
    cumulative_returns = (1 + daily_returns).cumprod()-1
    
    # Plot the daily returns of dogecoin over the last 5 years
    cumulative_doge_curve =cumulative_returns.hvplot(
        figsize=(10,5),
        title='Cumulative Returns for Dogeoin',
        ylabel='% Change in Dogecoin Price',
        shared_axes=False
    )
    
    df2 = pd.read_pickle("data/elon_btc.plk")

    # Drop unnecessary columns
    df2_bit = df2.drop(columns=["Elon Musk's Tweet in List",
                               "Elon Musk's Tweet in String",                               
                               "Elon Musk's Tweet That Mentions the Word Bitcoin",
                               "Elon Musk's Tweet That Mentions the Word BTC",
                               "Elon Musk's Tweet That Mentions the Word Bitcoin or BTC",
                               "Does Elon Musk's Tweet Tention the Word Bitcoin or BTC?"])
 

    # Calculate the daily return using the 'shift()' function
    daily_returns = (df2_bit - df2_bit.shift(1)) / df2_bit.shift(1)

    #Calculate the cumulative returns using the 'cumprod()' function
    cumulative_returns = (1 + daily_returns).cumprod()-1


    # Plot the daily returns of the S&P 500 over the last 2 years
    cumulative_bitcoin_curve = cumulative_returns.hvplot(figsize=(10,5), shared_axes=False)


       
    return cumulative_bitcoin_curve, cumulative_doge_curve


    # _________________________________________________________________________________________________________________________________________________________


def make_price_curve():
    '''
    Make plots that shows crypto's historical price

    Returns: A tuple of Hvplot objects.

    Items in the tutple:
    1. A line plot showing Bitcoin's historical price
    2. A line plot showing Dogecoin's historical price 
    '''
    
    # Bitcoin data
    df2 = pd.read_pickle("data/elon_btc.plk")
    df2 = df2.rename(columns={"Bitcoin Price": "Bitcoin_Price"})
  
    # Historical price curve of Bitcoin
    bitcoin_price_curve = df2.Bitcoin_Price.hvplot(shared_axes=False)
    
    # Doge data
    df1 = pd.read_pickle("data/elon_doge.plk")
    df1 = df1.rename(columns={"Dogecoin Price": "Dogecoin_price"})


    # Historical price curve of Doge
    dogecoin_price_curve = df1.Dogecoin_price.hvplot(shared_axes=False)

    
    return bitcoin_price_curve, dogecoin_price_curve


    # _________________________________________________________________________________________________________________________________________________________


def make_random_forest(): 
    '''
    Make plots that shows results of an algorithmic trading based on Random Forest

    Returns: A tuple of Hvplot objects.

    Items in the tutple:
    @TODO: Need more polish as tweets are not taken into account for now
    '''
    
    # Import libraries and dependencies
    import pandas as pd
    import numpy as np
    from pathlib import Path
    import hvplot.pandas
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification

    rf_ema_closing_prices = None
    rf_ema_daily_return_volatility = None
    rf_plot3 = None
    rf_plot4 = None
    rf_plot5 = None
    rf_plot6 = None
    rf_plot7 = None

    # Set path to Pickle and read in data
    trading_signals_df= pd.read_pickle("data/elon_btc.plk")

    # Drop NAs and calculate daily percent return
    trading_signals_df['daily_return'] = trading_signals_df['Bitcoin Price'].dropna().pct_change()
    
    # Set short and long windows
    short_window = 1
    long_window = 10

    # Construct a `Fast` and `Slow` Exponential Moving Average from short and long windows, respectively
    trading_signals_df['fast_close'] = trading_signals_df['Bitcoin Price'].ewm(halflife=short_window).mean()
    trading_signals_df['slow_close'] = trading_signals_df['Bitcoin Price'].ewm(halflife=long_window).mean()

    # Construct a crossover trading signal
    trading_signals_df['crossover_long'] = np.where(trading_signals_df['fast_close'] > trading_signals_df['slow_close'], 1.0, 0.0)
    trading_signals_df['crossover_short'] = np.where(trading_signals_df['fast_close'] < trading_signals_df['slow_close'], -1.0, 0.0)
    trading_signals_df['crossover_signal'] = trading_signals_df['crossover_long'] + trading_signals_df['crossover_short']

    # Plot the EMA of BTC closing prices
    rf_ema_closing_prices = trading_signals_df[['Bitcoin Price', 'fast_close', 'slow_close']].hvplot(title="Title - change me", 
                                                                                                     xlabel="X label - change me", 
                                                                                                     ylabel="Y label - change me", 
                                                                                                     width = 800, height = 400, 
                                                                                                     shared_axes=False).opts(yformatter="%.1f")
    
    # Set short and long volatility windows
    short_vol_window = 1
    long_vol_window = 10

    # Construct a `Fast` and `Slow` Exponential Moving Average from short and long windows, respectively
    trading_signals_df['fast_vol'] = trading_signals_df['daily_return'].ewm(halflife=short_vol_window).std()
    trading_signals_df['slow_vol'] = trading_signals_df['daily_return'].ewm(halflife=long_vol_window).std()

    # Construct a crossover trading signal
    trading_signals_df['vol_trend_long'] = np.where(trading_signals_df['fast_vol'] < trading_signals_df['slow_vol'], 1.0, 0.0)
    trading_signals_df['vol_trend_short'] = np.where(trading_signals_df['fast_vol'] > trading_signals_df['slow_vol'], -1.0, 0.0) 
    trading_signals_df['vol_trend_signal'] = trading_signals_df['vol_trend_long'] + trading_signals_df['vol_trend_short']

    # Plot the EMA of BTC/USD daily return volatility
    rf_ema_daily_return_volatility = trading_signals_df[['fast_vol', 'slow_vol']].hvplot(title="Title - change me", 
                                                                   xlabel="X label - change me", 
                                                                   ylabel="Y label - change me", 
                                                                   width = 800, height = 400, 
                                                                   shared_axes=False).opts(yformatter="%.1f")
    
    # Set bollinger band window
    bollinger_window = 20

    # Calculate rolling mean and standard deviation
    trading_signals_df['bollinger_mid_band'] = trading_signals_df['Bitcoin Price'].rolling(window=bollinger_window).mean()
    trading_signals_df['bollinger_std'] = trading_signals_df['Bitcoin Price'].rolling(window=20).std()

    # Calculate upper and lowers bands of bollinger band
    trading_signals_df['bollinger_upper_band']  = trading_signals_df['bollinger_mid_band'] + (trading_signals_df['bollinger_std'] * 1)
    trading_signals_df['bollinger_lower_band']  = trading_signals_df['bollinger_mid_band'] - (trading_signals_df['bollinger_std'] * 1)

    # Calculate bollinger band trading signal
    trading_signals_df['bollinger_long'] = np.where(trading_signals_df['Bitcoin Price'] < trading_signals_df['bollinger_lower_band'], 1.0, 0.0)
    trading_signals_df['bollinger_short'] = np.where(trading_signals_df['Bitcoin Price'] > trading_signals_df['bollinger_upper_band'], -1.0, 0.0)
    trading_signals_df['bollinger_signal'] = trading_signals_df['bollinger_long'] + trading_signals_df['bollinger_short']

    # Plot the Bollinger Bands for BTC/USD closing prices
    rf_plot3 = trading_signals_df[['Bitcoin Price','bollinger_mid_band','bollinger_upper_band','bollinger_lower_band']].hvplot(title="Title - change me", 
                                                                                                                               xlabel="X label - change me", 
                                                                                                                               ylabel="Y label - change me", 
                                                                                                                               width = 800, height = 400, 
                                                                                                                               shared_axes=False).opts(yformatter="%.1f")

    # Set x variable list of features
    x_var_list = ['crossover_signal', 'vol_trend_signal', 'bollinger_signal']

    # Filter by x-variable list
    trading_signals_df[x_var_list].tail()

    # Shift DataFrame values by 1
    trading_signals_df[x_var_list] = trading_signals_df[x_var_list].shift(1)
    trading_signals_df[x_var_list].tail()

    # Drop NAs and replace positive/negative infinity values
    trading_signals_df.dropna(subset=x_var_list, inplace=True)
    trading_signals_df.dropna(subset=['daily_return'], inplace=True)
    trading_signals_df = trading_signals_df.replace([np.inf, -np.inf], np.nan)
    # trading_signals_df.tail()

    # Construct the dependent variable where if daily return is greater than 0, then 1, else, 0.
    trading_signals_df['Positive Return'] = np.where(trading_signals_df['daily_return'] > 0, 1.0, 0.0)
    # trading_signals_df.tail()

    # Construct training start and end dates
    training_start = trading_signals_df.index.min().strftime(format= '%Y-%m-%d')
    training_end = '2021-01-29'

    # Construct testing start and end dates
    testing_start =  '2021-01-30'
    testing_end = trading_signals_df.index.max().strftime(format= '%Y-%m-%d')

    # Construct the x train and y train datasets
    x_train = trading_signals_df[x_var_list][training_start:training_end]
    y_train = trading_signals_df['Positive Return'][training_start:training_end]
    # x_train.tail()
    # y_train.tail()

    # Construct the x test and y test datasets
    x_test = trading_signals_df[x_var_list][testing_start:testing_end]
    y_test = trading_signals_df['Positive Return'][testing_start:testing_end]
    # x_test.tail()
    # y_test.tail()

    # Fit a SKLearn linear regression using just the training set (x_train, y_train):
    model = RandomForestClassifier(n_estimators=100, max_depth=3, random_state=0)
    model.fit(x_train, y_train)

    # Make a prediction of "y" values from the x test dataset
    predictions = model.predict(x_test)

    # Assemble actual y data (y_test) with predicted y data (from just above) into two columns in a dataframe:
    results = y_test.to_frame()
    results["Predicted Value"] = predictions

    # Rename 'Positive Return' column to 'Actual Value' to be more descriptive for the plots below
    results.rename(columns={'Positive Return': 'Actual Value'}, inplace=True)

    # Add 'Return' column from trading_signals_df for the plots below
    results = pd.concat([results, trading_signals_df["daily_return"]], axis=1, join="inner")
    # results.tail()

    # Plot predicted results vs. actual results
    rf_plot4 = results[['Actual Value', 'Predicted Value']].hvplot(title="Title - change me", 
                                                                   xlabel="X label - change me", 
                                                                   ylabel="Y label - change me", 
                                                                   width = 800, height = 400, 
                                                                   shared_axes=False).opts(yformatter="%.1f")

    # Plot last 10 records of predicted vs. actual results
    rf_plot5 = results[['Actual Value', 'Predicted Value']].tail(10).hvplot(title="Title - change me", 
                                                                            xlabel="X label - change me", 
                                                                            ylabel="Y label - change me", 
                                                                            width = 800, height = 400, 
                                                                            shared_axes=False).opts(yformatter="%.1f")

    # Replace predicted values 0 to -1 to account for shorting
    results['Predicted Value'].replace(0, -1, inplace=True)
    # results.tail()

    # Calculate cumulative return of model and plot the result
    rf_plot6 = (1 + (results['daily_return'] * results['Predicted Value'])).cumprod().hvplot(title="Title - change me", 
                                                                                             xlabel="X label - change me", 
                                                                                             ylabel="Y label - change me", 
                                                                                             width = 800, height = 400, 
                                                                                             shared_axes=False).opts(yformatter="%.1f")
    
    # Set initial capital allocation
    initial_capital = 100000  ## <- replace this with user entered value!

    # Plot cumulative return of model in terms of capital
    cumulative_return_capital = initial_capital * (1 + (results['daily_return'] * results['Predicted Value'])).cumprod()
    rf_plot7 = cumulative_return_capital.hvplot(title="Title - change me", 
                                                xlabel="X label - change me", 
                                                ylabel="Y label - change me", 
                                                width = 800, 
                                                height = 400, 
                                                shared_axes=False).opts(yformatter="%.1f")
    
    
    return rf_ema_closing_prices, rf_ema_daily_return_volatility, rf_plot3, rf_plot4, rf_plot5, rf_plot6, rf_plot7

    
    # _________________________________________________________________________________________________________________________________________________________


def algo_trading_fixed_strategy():
    '''
    Make plots that show the results of an algorithmic trading based on a fixed staretegy, i.e. buy whenever Elon Musk tweets something about a crypto, and sell after 24 hours.

    Returns: A tuple of Hvplot objects.

    Items in the tutple:
    1. A line plot showing Bitcoin's historical price with some markers on the top indicating buy/sell actions
    2. A line plot showing portfolio value of the Bitcoin investment with some markers on the top indicating buy/sell actions
    3. A table showing the evaluation results of the performance of the Bitcoin investment portfolio
    4. A line plot showing Dogecoin's historical price with some markers on the top indicating buy/sell actions
    5. A line plot showing portfolio value of the Dogecoin investment with some markers on the top indicating buy/sell actions
    6. A table showing the evaluation results of the performance of the Dogecoin investment portfolio
    '''

    # Load Dogecoin data
    df_doge = pd.read_pickle('./data/elon_doge.plk')
    df_doge

    # Slice only the columns needed
    signals_df_doge = df_doge[['Dogecoin Price', "Does Elon Musk's Tweet Tention the Word DOGE?"]].copy()
    signals_df_doge

    # Create a Entry column, 1 for entry, 0 for hold
    signals_df_doge['Entry'] = signals_df_doge["Does Elon Musk's Tweet Tention the Word DOGE?"]
    signals_df_doge

    # Create an Exit column, -1 for Exit, 0 for hold

    # Set Exit time as 24 hours after Entry
    signals_df_doge['Exit'] = signals_df_doge['Entry'].shift(24)
    signals_df_doge['Exit'] = signals_df_doge['Exit'].replace(1, -1)
    signals_df_doge

    # Create an Extry/Exit column
    signals_df_doge['Entry/Exit'] = signals_df_doge['Entry'] + signals_df_doge['Exit']
    signals_df_doge['Entry/Exit'] = signals_df_doge['Entry/Exit'].fillna(0)
    signals_df_doge

    # Visualize exit position relative to close price
    exit = signals_df_doge[signals_df_doge['Entry/Exit'] == -1.0]['Dogecoin Price'].hvplot.scatter(
        color='red',
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400
    )

    # Visualize entry position relative to close price
    entry = signals_df_doge[signals_df_doge['Entry/Exit'] == 1.0]['Dogecoin Price'].hvplot.scatter(
        color='green',
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400
    )

    # Visualize close price for the investment
    security_close = signals_df_doge[['Dogecoin Price']].hvplot(
        line_color='lightgray',
        ylabel='Price in $',
        width=1000,
        height=400
    )


    # Overlay plots
    entry_exit_price_plot_doge = security_close * entry * exit
    entry_exit_price_plot_doge.opts(width=1000, title='Entry/Exit vs Price')

    # Set initial capital
    initial_capital = float(100000)

    # Set the share size
    share_size = 2000000

    # Find the points in time where a 500 share position is bought or sold
    signals_df_doge['Entry/Exit Position'] = share_size * signals_df_doge['Entry/Exit']

    # Multiply share price by entry/exit positions and get the cumulatively sum
    signals_df_doge['Portfolio Holdings'] = signals_df_doge['Dogecoin Price'] * signals_df_doge['Entry/Exit Position'].cumsum()

    # Subtract the initial capital by the portfolio holdings to get the amount of liquid cash in the portfolio
    signals_df_doge['Portfolio Cash'] = initial_capital - (signals_df_doge['Dogecoin Price'] * signals_df_doge['Entry/Exit Position']).cumsum()

    # Get the total portfolio value by adding the cash amount by the portfolio holdings (or investments)
    signals_df_doge['Portfolio Total'] = signals_df_doge['Portfolio Cash'] + signals_df_doge['Portfolio Holdings']

    # Calculate the portfolio daily returns
    signals_df_doge['Portfolio Hourly Returns'] = signals_df_doge['Portfolio Total'].pct_change()

    # Calculate the cumulative returns
    signals_df_doge['Portfolio Cumulative Returns'] = (1 + signals_df_doge['Portfolio Hourly Returns']).cumprod() - 1


    # Visualize exit position relative to total portfolio value
    exit = signals_df_doge[signals_df_doge['Entry/Exit'] == -1.0]['Portfolio Total'].hvplot.scatter(
        color='red',
        legend=False,
        ylabel='Total Portfolio Value',
        width=1000,
        height=400
    )

    # Visualize entry position relative to total portfolio value
    entry = signals_df_doge[signals_df_doge['Entry/Exit'] == 1.0]['Portfolio Total'].hvplot.scatter(
        color='green',
        legend=False,
        ylabel='Total Portfolio Value',
        width=1000,
        height=400
    )

    # Visualize total portoflio value for the investment
    total_portfolio_value = signals_df_doge[['Portfolio Total']].hvplot(
        line_color='lightgray',
        ylabel='Total Portfolio Value',
        width=1000,
        height=400
    )

    # Overlay plots
    entry_exit_portfolio_plot_doge = total_portfolio_value * entry * exit
    entry_exit_portfolio_plot_doge.opts(width=1000, title='Entry/Exit vs Total Portfolio Value')

    # Prepare DataFrame for metrics
    metrics = [
        'Annual Return',
        'Cumulative Returns',
        'Annual Volatility',
        'Sharpe Ratio'
        ]

    columns = ['Backtest']

    # Initialize the DataFrame with index set to evaluation metrics and column as `Backtest` (just like PyFolio)
    portfolio_evaluation_df = pd.DataFrame(index=metrics, columns=columns)

    # Calculate cumulative return
    portfolio_evaluation_df.loc['Cumulative Returns'] = signals_df_doge['Portfolio Cumulative Returns'][-1]


    # Calculate annualized return
    portfolio_evaluation_df.loc['Annual Return'] = (
        signals_df_doge['Portfolio Hourly Returns'].mean() * 252 *24
    )

    # Calculate annual volatility
    portfolio_evaluation_df.loc['Annual Volatility'] = (
        signals_df_doge['Portfolio Hourly Returns'].std() * np.sqrt(252*24)
    )

    # Calculate Sharpe Ratio
    portfolio_evaluation_df.loc['Sharpe Ratio'] = (
        signals_df_doge['Portfolio Hourly Returns'].mean() * 252*24) / (
        signals_df_doge['Portfolio Hourly Returns'].std() * np.sqrt(252*24)
    )


    # Convert portfolio evaluation matrics to an Hvplot table
    portfolio_evaluation_df.reset_index(inplace=True)
    portfolio_evaluation_table_doge = portfolio_evaluation_df.hvplot.table(title='Portfolio Evaluation Metrics')
    portfolio_evaluation_table_doge


    # Load Bitcoin data
    df_btc = pd.read_pickle('./data/elon_btc.plk')
    df_btc

    # Slice only the columns needed
    signals_df_btc = df_btc[['Bitcoin Price', "Does Elon Musk's Tweet Tention the Word Bitcoin or BTC?"]].copy()
    signals_df_btc

    # Create a Entry column, 1 for entry, 0 for hold
    signals_df_btc['Entry'] = signals_df_btc["Does Elon Musk's Tweet Tention the Word Bitcoin or BTC?"]
    signals_df_btc

    # Create an Exit column, -1 for Exit, 0 for hold
    # Set Exit time as 24 hours after Entry
    signals_df_btc['Exit'] = signals_df_btc['Entry'].shift(24)
    signals_df_btc['Exit'] = signals_df_btc['Exit'].replace(1, -1)
    signals_df_btc

    # Create an Extry/Exit column
    signals_df_btc['Entry/Exit'] = signals_df_btc['Entry'] + signals_df_btc['Exit']
    signals_df_btc['Entry/Exit'] = signals_df_btc['Entry/Exit'].fillna(0)
    signals_df_btc

    # Visualize exit position relative to close price
    exit = signals_df_btc[signals_df_btc['Entry/Exit'] == -1.0]['Bitcoin Price'].hvplot.scatter(
        color='red',
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400
    )

    # Visualize entry position relative to close price
    entry = signals_df_btc[signals_df_btc['Entry/Exit'] == 1.0]['Bitcoin Price'].hvplot.scatter(
        color='green',
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400
    )

    # Visualize close price for the investment
    security_close = signals_df_btc[['Bitcoin Price']].hvplot(
        line_color='lightgray',
        ylabel='Price in $',
        width=1000,
        height=400
    )


    # Overlay plots
    entry_exit_price_plot_btc = security_close * entry * exit
    entry_exit_price_plot_btc.opts(width=1000, title='Entry/Exit vs Price')

    # Set initial capital
    initial_capital = float(100000)

    # Set the share size
    share_size = 3

    # Find the points in time where a 500 share position is bought or sold
    signals_df_btc['Entry/Exit Position'] = share_size * signals_df_btc['Entry/Exit']

    # Multiply share price by entry/exit positions and get the cumulatively sum
    signals_df_btc['Portfolio Holdings'] = signals_df_btc['Bitcoin Price'] * signals_df_btc['Entry/Exit Position'].cumsum()

    # Subtract the initial capital by the portfolio holdings to get the amount of liquid cash in the portfolio
    signals_df_btc['Portfolio Cash'] = initial_capital - (signals_df_btc['Bitcoin Price'] * signals_df_btc['Entry/Exit Position']).cumsum()

    # Get the total portfolio value by adding the cash amount by the portfolio holdings (or investments)
    signals_df_btc['Portfolio Total'] = signals_df_btc['Portfolio Cash'] + signals_df_btc['Portfolio Holdings']

    # Calculate the portfolio daily returns
    signals_df_btc['Portfolio Hourly Returns'] = signals_df_btc['Portfolio Total'].pct_change()

    # Calculate the cumulative returns
    signals_df_btc['Portfolio Cumulative Returns'] = (1 + signals_df_btc['Portfolio Hourly Returns']).cumprod() - 1

    # Print the DataFrame
    signals_df_btc

    # Visualize exit position relative to total portfolio value
    exit = signals_df_btc[signals_df_btc['Entry/Exit'] == -1.0]['Portfolio Total'].hvplot.scatter(
        color='red',
        legend=False,
        ylabel='Total Portfolio Value',
        width=1000,
        height=400
    )

    # Visualize entry position relative to total portfolio value
    entry = signals_df_btc[signals_df_btc['Entry/Exit'] == 1.0]['Portfolio Total'].hvplot.scatter(
        color='green',
        legend=False,
        ylabel='Total Portfolio Value',
        width=1000,
        height=400
    )

    # Visualize total portoflio value for the investment
    total_portfolio_value = signals_df_btc[['Portfolio Total']].hvplot(
        line_color='lightgray',
        ylabel='Total Portfolio Value',
        width=1000,
        height=400
    )

    # Overlay plots
    entry_exit_portfolio_plot_btc = total_portfolio_value * entry * exit
    entry_exit_portfolio_plot_btc.opts(width=1000, title='Entry/Exit vs Total Portfolio Value')

    # Prepare DataFrame for metrics
    metrics = [
        'Annual Return',
        'Cumulative Returns',
        'Annual Volatility',
        'Sharpe Ratio'
        ]

    columns = ['Backtest']

    # Initialize the DataFrame with index set to evaluation metrics and column as `Backtest` (just like PyFolio)
    portfolio_evaluation_df = pd.DataFrame(index=metrics, columns=columns)
    portfolio_evaluation_df

    # Calculate cumulative return
    portfolio_evaluation_df.loc['Cumulative Returns'] = signals_df_btc['Portfolio Cumulative Returns'][-1]


    # Calculate annualized return
    portfolio_evaluation_df.loc['Annual Return'] = (
        signals_df_btc['Portfolio Hourly Returns'].mean() * 252 *24
    )

    # Calculate annual volatility
    portfolio_evaluation_df.loc['Annual Volatility'] = (
        signals_df_btc['Portfolio Hourly Returns'].std() * np.sqrt(252*24)
    )

    # Calculate Sharpe Ratio
    portfolio_evaluation_df.loc['Sharpe Ratio'] = (
        signals_df_btc['Portfolio Hourly Returns'].mean() * 252*24) / (
        signals_df_btc['Portfolio Hourly Returns'].std() * np.sqrt(252*24)
    )

    portfolio_evaluation_df

    # Make a portfolio evaluation matrix table
    portfolio_evaluation_df.reset_index(inplace=True)
    portfolio_evaluation_table_btc = portfolio_evaluation_df.hvplot.table(title='Portfolio Evaluation Metrics')
    portfolio_evaluation_table_btc

    # Return plots
    return (
        entry_exit_price_plot_btc,
        entry_exit_portfolio_plot_btc,
        portfolio_evaluation_table_btc,
        entry_exit_price_plot_doge,
        entry_exit_portfolio_plot_doge,
        portfolio_evaluation_table_doge
    )
    

    # _________________________________________________________________________________________________________________________________________________________


def load_algo_trading_result_rnn():
    '''
    Make plots that show the results of an algorithmic trading based on RNN LSTM

    Returns: A tuple of Hvplot objects.

    Items in the tutple:
    1. A line plot showing the algo's predictions on whether Bitcoin price will rise or fall in each hour
    2. A line plot showing the algo trading's cumulative returns on Bitcoin 
    3. A line plot showing the algo's predictions on whether Dogecoin price will rise or fall in each hour
    4. A line plot showing the algo trading's cumulative returns on Dogecoin 
    '''

    # ----------------- Dogecoin Section -----------------

    # Load rnn algo trading result
    result = pd.read_pickle('data/rnn_result_doge.plk')
    result

    # Meke predicted positive return curve
    rnn_predicted_positive_return_curve_doge = result['Predicted Positive Return'].hvplot(title='Dogecoin Predicted Positive Return')
    rnn_predicted_positive_return_curve_doge

    # Calculate cumulative return of model and plot the result
    cumulative_return = (1 + (result['Daily Return'] * result['Predicted Positive Return'])).cumprod() -1
    cumulative_return

    rnn_cumulative_return_plot_doge = cumulative_return.hvplot(title='Dogecoin Cumulative Returns')
    rnn_cumulative_return_plot_doge

    # ----------------- Bitcoin Section -----------------

    # Load rnn algo trading result
    result = pd.read_pickle('data/rnn_result_btc.plk')

    # Meke predicted positive return curve
    rnn_predicted_positive_return_curve_btc = result['Predicted Positive Return'].hvplot(title='Bitcoin Predicted Positive Return')
    rnn_predicted_positive_return_curve_btc

    # Calculate cumulative return of model and plot the result
    cumulative_return = (1 + (result['Daily Return'] * result['Predicted Positive Return'])).cumprod() -1
    cumulative_return

    rnn_cumulative_return_plot_btc = cumulative_return.hvplot(title='Bitcoin Cumulative Returns')
    rnn_cumulative_return_plot_btc

    # Retrn plots
    return (
        rnn_predicted_positive_return_curve_btc, 
        rnn_cumulative_return_plot_btc,
        rnn_predicted_positive_return_curve_doge, 
        rnn_cumulative_return_plot_doge
    )


    # _________________________________________________________________________________________________________________________________________________________


def load_algo_trading_result_rf():
    '''
    Make plots that show the results of an algorithmic trading based on Random Forest

    Returns: A tuple of Hvplot objects.

    Items in the tutple:
    1. A line plot showing the algo's predictions on whether Bitcoin price will rise or fall in each hour
    2. A line plot showing the algo trading's cumulative returns on Bitcoin 
    3. A line plot showing the algo's predictions on whether Dogecoin price will rise or fall in each hour
    4. A line plot showing the algo trading's cumulative returns on Dogecoin 
    '''

    # ----------------- Dogecoin Section -----------------

    # Load rnn algo trading result
    result = pd.read_pickle('data/rf_result_doge.plk')

    # Meke predicted positive return curve
    rf_predicted_positive_return_curve_doge = result['Predicted Positive Return'].hvplot(title='Dogecoin Predicted Positive Return')
    rf_predicted_positive_return_curve_doge

    # Calculate cumulative return of model and plot the result
    cumulative_return = (1 + (result['Daily Return'] * result['Predicted Positive Return'])).cumprod() -1
    cumulative_return

    rf_cumulative_return_plot_doge = cumulative_return.hvplot(title='Dogecoin Cumulative Returns')
    rf_cumulative_return_plot_doge

    # ----------------- Bitcoin Section -----------------

    # Load rnn algo trading result
    result = pd.read_pickle('data/rf_result_btc.plk')
    result

    # Meke predicted positive return curve
    rf_predicted_positive_return_curve_btc = result['Predicted Positive Return'].hvplot(title='Bitcoin Predicted Positive Return')
    rf_predicted_positive_return_curve_btc

    # Calculate cumulative return of model and plot the result
    cumulative_return = (1 + (result['Daily Return'] * result['Predicted Positive Return'])).cumprod() -1
    cumulative_return

    rf_cumulative_return_plot_btc = cumulative_return.hvplot(title='Bitcoin Cumulative Returns')
    rf_cumulative_return_plot_btc

    # Retrn plots
    return (
        rf_predicted_positive_return_curve_btc, 
        rf_cumulative_return_plot_btc,
        rf_predicted_positive_return_curve_doge, 
        rf_cumulative_return_plot_doge
    )