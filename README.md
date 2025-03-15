# A Comprehensive Approach of Algorithmic Trading System based on Technical Analysis

## Table of Contents

1. [Introduction](#introduction)
2. [Related Works](#related-works)
3. [Methods](#methods)
   - 3.1 [Data](#data)
   - 3.2 [Data Preprocessing](#data-preprocessing)
   - 3.3 [Model Training](#model-training)
   - 3.4 [Optimization Search Model](#optimization-search-model)
   - 3.5 [Performance Evaluation](#performance-evaluation)

---

## Introduction

Stock trading is a popular investment choice for individuals seeking to grow their wealth. However, investing in stock markets is inherently risky, requiring careful decision-making to achieve desirable profits. To navigate this uncertainty, investors often rely on **Technical Analysis**, a method that analyzes historical price trends and trading activity to identify patterns and predict future market movements [3].

This research focuses on leveraging **Technical Analysis** to extract meaningful features for training machine learning models. The study evaluates the performance of three machine learning models—**Logistic Regression**, **Support Vector Machines (SVM)**, and **K-Nearest Neighbors (KNN)**—against an optimization-based model using **Differential Evolution (DE)**. The goal is to help investors understand the strengths and limitations of these algorithms in making efficient trading decisions.

---

## Related Works

Financial academics have long studied ways to improve technical trading systems. Hundreds of technical indicators have been developed using statistical and mathematical methods, categorized into types such as:

- **Trend Indicators**: Analyze trends (e.g., Exponential Moving Average (EMA), Directional Movement Index (DMI)).
- **Momentum Indicators**: Measure the rate of price changes (e.g., Relative Strength Index (RSI), On-Balance-Volume (OBV)) [8].

These indicators are used to suggest trends, reversal points, and trading signals [9]. Early attempts relied on simple rule-based approaches, but the dynamic nature of stock markets limited their effectiveness.

To address these limitations, optimization algorithms such as **Genetic Algorithms**, **Differential Evolution (DE)**, and **Particle Swarm Optimization (PSO)** have been applied to build trading recommendation systems [10]-[13]. These algorithms excel at handling nonlinearity, uncertainty, and large-scale problems.

In contrast, machine learning algorithms specialize in **pattern detection**. Unlike traditional methods, machine learning thrives on flexibility, rapidly analyzing complex data without requiring clearly defined patterns. It has been widely used with **Open-High-Low-Close (OHLC)** price data to build stock price prediction models [6][15][16]. Advanced techniques such as **Long Short-Term Memory (LSTM)**, **Artificial Neural Networks (ANN)**, and **Convolutional Neural Networks (CNN)** have also been employed to predict stock values using features like price and trading volume [17][18].

A critical step in training supervised machine learning models is **data labeling**. Since there is no definitive answer to when to buy or sell stocks, labeling data is challenging. Recent approaches, such as the **N-Period Min-Max (NPMM)** method, address this by labeling data at specific time points to reduce sensitivity to small price changes [2].

---

## Methods

### 3.1 Data

This study uses data from nine securities listed on the **Stock Exchange of Thailand (SET100)** index, categorized into three groups based on their market trends:

- **Uptrend**: SIRI, BDMS, ORI
- **Downtrend**: AAV, BANPU, SPALI
- **Sideway**: CENTEL, AOT, BCH

This selection allows for the evaluation of investment strategies across various market conditions. Daily **Open**, **High**, **Low**, **Close**, and **Volume** data for these securities from January 1, 2019, to October 31, 2023, were imported using the **y-finance** library. Technical indicators were calculated using the **TA-lib** library in Python, with additional manual calculations for unavailable indicators.

### 3.2 Data Preprocessing

#### 3.2.1 Technical Indicators and Trading Strategies

Ten trading strategies were developed by combining technical indicators and setting conditions for generating buy/sell signals. These strategies are widely used by investors to make informed decisions:

1. **Volume Profile (VP)**:
   - Identifies key price levels with high trading volume.
   - Generates buy signals when the current price is below significant peaks and sell signals when above [21].

2. **Stochastic Oscillator (STO)**:
   - A momentum indicator comparing closing prices to a range over a set period.
   - Signals overbought (sell) and oversold (buy) conditions [22].

3. **Bollinger Bands (BB)**:
   - Plots two standard deviations around a moving average.
   - Identifies overbought and oversold conditions [23].

4. **Commodity Channel Index (CCI)**:
   - A momentum oscillator identifying overbought/oversold conditions.
   - Helps traders decide entry/exit points [24].

5. **RSI and MACD**:
   - Combines MACD and RSI to assess trends and momentum.
   - Buy signal: MACD crosses above the MACD signal, and RSI < 35.
   - Sell signal: MACD crosses below the MACD signal, and RSI < 65 [25].

6. **OBV and MACD**:
   - Combines leading (OBV) and lagging (MACD) indicators.
   - Buy signal: OBV slope > 30 degrees, MACD line above the signal line.
   - Sell signal: MACD line below the signal line, OBV slope < 30 [5].

7. **ADX and DMI**:
   - Measures trend strength using ADX and direction using +DI and -DI.
   - Detects trend changes through crossovers [5].

8. **Crossover of SMA50 and SMA100**:
   - Buy signal: Shorter-term SMA crosses above longer-term SMA.
   - Sell signal: Shorter-term SMA crosses below longer-term SMA [5].

9. **Aroon**:
   - Detects trend shifts using Aroon Up and Aroon Down lines.
   - Indicates strong trends when new highs/lows occur regularly [5].

10. **Renko Charts**:
    - Filters market noise using bricks representing fixed price shifts.
    - New bricks indicate trend continuation or reversal [26].

#### 3.2.2 Data Labeling

The **N-Period Min-Max (NPMM)** method was used to label data, addressing the shortcomings of traditional up-down labeling. NPMM analyzes stock price trends over a defined period (N = 14 to 21 days) and identifies minimum (buy) and maximum (sell) points within that period.

### 3.3 Model Training

Three machine learning models were trained using the trading signals as parameters:

1. **Logistic Regression**:
   - A statistical method for binary classification tasks.
   - Models the relationship between features and class probabilities.

2. **K-Nearest Neighbors (KNN)**:
   - A supervised learning algorithm for classification and regression.
   - Predicts labels based on the k closest data points.

3. **Support Vector Machines (SVM)**:
   - A powerful supervised learning algorithm for classification and regression.
   - Finds the optimal hyperplane to separate data points into classes.

### 3.4 Optimization Search Model

The **Differential Evolution (DE)** algorithm was used to optimize trading strategies. DE follows these steps:

1. **Parameterization**: Identify key parameters (e.g., entry/exit signals, risk management).
2. **Population Initialization**: Create an initial population of potential solutions.
3. **Mutation and Crossover**: Introduce diversity and combine promising solutions.
4. **Selection**: Evaluate solutions based on a fitness function (e.g., profitability, risk).
5. **Iteration and Convergence**: Repeat until a stopping criterion is met.

The trading decision is calculated using the following equation:

# Trading Decision Algorithm

## Decision Formula

The decision is calculated using the weighted average of trading signals as follows:

\[
\text{Decision}_d = \frac{w_1 s_1 + w_2 s_2 + \dots + w_n s_n}{\sum_{i=1}^n w_i}
\]

Where:

- \( w_n \): Weighted value of the nth trading signal.
- \( s_n \): Trading signal (1 = buy, 0 = hold, -1 = sell).

## Decision-Making Process

Once the decision value \( \text{Decision}_d \) is calculated, it is compared with a threshold \( t_d \) to determine the action:

- **Buy** if \( \text{Decision}_d > t_d \).
- **Sell** if \( \text{Decision}_d < -t_d \).
- **Hold** if \( \text{Decision}_d \) is within the range \( (-t_d, t_d) \).

### 3.5 Performance Evaluation

A trading simulation was conducted for each stock, including both long and short positions. The average returns for each strategy were compared with the returns from a **buy-and-hold (B&H)** strategy. A 0.2% commission fee was applied to all transactions to account for realistic trading costs.


# ALGORITHMIC STOCK TRADING SYSTEM

I'm learn how to trade stock from my dad and when i do some research there are thing called technical indicator.
It's a tool calculated from stock's data which is very powerful if you use it wisely ,but there are so many of them.
It make me think that what if i create a algorithm that decide that based on the data wouldn't that be very powerful.  
So i build this project with my freind and its turn out to be very good and win multiple awards.

Automatic generating trading signal (Buy/Sell/Hold) through optimization using Differential Evolution Algorithm.  
The parameter of the optimization algorithm is the weigth of well-known technical indicator such as RSI, MA, and MACD and some other self researched ones.   

CODE - contain all of the code from creating a technical indicator to training a model.  
Papar - contain research papers, certificate and reward of the project.  
Streamlit - contain website code.  
