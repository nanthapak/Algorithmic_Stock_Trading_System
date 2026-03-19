# Algorithmic Stock Trading System

An automated trading signal generator that combines **10 technical indicators** with a **Differential Evolution** optimization algorithm to produce Buy / Sell / Hold decisions for both Thai (SET) and US equities.  The project won multiple awards and is backed by a peer-reviewed research paper.

---

## Table of Contents
- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [System Architecture & Workflow](#system-architecture--workflow)
- [Data](#data)
- [Technical Indicators](#technical-indicators)
- [Optimization Model](#optimization-model)
- [Signal Generation](#signal-generation)
- [Backtesting & Performance](#backtesting--performance)
- [Web Application](#web-application)
- [Key Parameters](#key-parameters)
- [Technologies Used](#technologies-used)
- [Awards & Research](#awards--research)

---

## Project Overview

Traditional technical analysis requires a trader to manually pick and interpret indicators.  This system automates that process:

1. **Calculate** 10 technical indicators from raw OHLCV data.
2. **Optimize** the weight of each indicator and a decision threshold using Differential Evolution so that a weighted combination of the signals maximises back-tested profit.
3. **Deploy** the optimised weights in a Flask web application that gives real-time Buy / Sell / Hold signals for any ticker.

---

## Repository Structure

```
├── Codes/                          # Jupyter notebooks (data → indicators → training)
│   ├── Data.ipynb                  # Data download & preprocessing
│   ├── THAI_stock_selection.ipynb  # Thai stock universe selection
│   ├── US_stock_selection.ipynb    # US stock universe selection
│   ├── label.ipynb                 # Ground-truth label generation
│   ├── create_signal_45/50.ipynb   # Indicator signal generation (v45, v50)
│   ├── create_56_adxbad.ipynb      # Signal generation with ADX refinement
│   ├── create_61_vernsc*.ipynb     # Signal generation (v61 variants)
│   ├── create_75_vernsc_paper.ipynb# Final signal set used in the paper
│   ├── finak_create_52.ipynb       # Final signal generation (v52)
│   ├── trainfinal_nscversion.ipynb # Differential Evolution training
│   ├── Model_RAC_1.ipynb           # ML classifier comparison (SVM/LR/KNN)
│   ├── Graph_maker (1).ipynb       # Result visualisation
│   └── customs_datasets.ipynb      # Custom dataset utilities
├── Streamlit/                      # Flask web application
│   ├── app.py                      # Flask server & routes
│   ├── findindi.py                 # Indicator calculation engine
│   ├── checksignal.py              # Weighted signal & decision logic
│   └── ...
├── Paper/                          # Research paper, certificates & awards
└── README.md
```

---

## System Architecture & Workflow

```
┌──────────────────────────────────────────────────────────────┐
│ 1. DATA COLLECTION                                           │
│    yfinance / pandas_datareader → OHLCV                      │
│    Train: 2017-12-31 → 2022-01-01  |  Test: 2022            │
└───────────────────────────┬──────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────┐
│ 2. TECHNICAL INDICATOR CALCULATION  (findindi.py)            │
│    10 indicators → individual +1/0/−1 signals per day        │
└───────────────────────────┬──────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────┐
│ 3. PARAMETER OPTIMISATION  (trainfinal_nscversion.ipynb)     │
│    Differential Evolution                                     │
│    Optimise: 10 weights + 1 decision threshold               │
│    Objective: maximise profit on training set                │
│    Constraint: Σ weights = 1.0                               │
└───────────────────────────┬──────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────┐
│ 4. SIGNAL GENERATION  (checksignal.py)                       │
│    score = Σ(weight[i] × signal[i]) / Σ(weights)            │
│    score > +threshold → BUY                                  │
│    score < −threshold → SELL                                 │
│    otherwise          → HOLD                                 │
└───────────────────────────┬──────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────┐
│ 5. BACKTEST & VALIDATION                                     │
│    ATS returns vs Buy-and-Hold baseline                      │
│    Transaction costs included (0.2% buy / 0.2% sell)        │
└───────────────────────────┬──────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────┐
│ 6. REAL-TIME WEB APP  (app.py)                               │
│    User inputs ticker → latest data → indicators →           │
│    weighted signal → BUY / SELL / HOLD + Plotly chart        │
└──────────────────────────────────────────────────────────────┘
```

---

## Data

| Property | Detail |
|---|---|
| **Source** | `yfinance`, `pandas_datareader` |
| **Fields** | Open, High, Low, Close, Adjusted Close, Volume |
| **Training period** | 2017-12-31 → 2022-01-01 |
| **Test period** | 2022-01-01 → 2022-11-27 |
| **Initial capital** | $100,000 USD |

### Stock Universes

**Thai Stocks (SET) — 15 symbols**

| Symbol | Symbol | Symbol | Symbol | Symbol |
|---|---|---|---|---|
| CPALL.BK | JASIF.BK | BDMS.BK | SCC.BK | MINT.BK |
| PTT.BK | TKN.BK | SIRI.BK | KBANK.BK | HANA.BK |
| BBL.BK | FORTH.BK | ANAN.BK | BTS.BK | MALEE.BK |

**US Stocks — 15 symbols**

| Symbol | Symbol | Symbol | Symbol | Symbol |
|---|---|---|---|---|
| OXY | XOM | AAPL | TSLA | AMZN |
| AMP | COP | NFLX | GOOG | PXD |
| MSFT | META | TROW | PEP | WMT |

---

## Technical Indicators

Ten indicators are calculated from OHLCV data (via **TA-Lib**).  Each produces a discrete signal: **+1 (Buy)**, **−1 (Sell)**, or **0 (Hold)**.

| # | Indicator | Library Param | Buy Condition | Sell Condition | Learned Weight |
|---|---|---|---|---|---|
| 1 | **ADX** (Average Directional Index) | Period = 14 | ADX crosses above 25 AND +DMI > −DMI | ADX crosses above 25 AND −DMI > +DMI | 10.61% |
| 2 | **MACD** | Fast=12, Slow=26, Signal=9 | MACD line > Signal line | MACD line < Signal line | 15.16% |
| 3 | **MA30 / MA200 Crossover** | SMA periods 30, 200 | MA30 > MA200 | MA30 < MA200 | 7.88% |
| 4 | **MA50 / MA200 Crossover** | SMA periods 50, 200 | MA50 > MA200 | MA50 < MA200 | 6.87% |
| 5 | **MA30 / MA50 Crossover** | SMA periods 30, 50 | MA30 > MA50 | MA30 < MA50 | 8.53% |
| 6 | **CDC Action Zone** *(custom)* | OHLC4 → EMA2 → EMA12 / EMA26 | EMA12 > EMA26 AND EMA2 > EMA12 | EMA12 < EMA26 AND EMA2 < EMA12 | 13.45% |
| 7 | **Parabolic SAR** | Acceleration=0.02, Max=0.2 | Close > SAR for 2 consecutive bars | Close < SAR for 2 consecutive bars | 12.10% |
| 8 | **ROC** (Rate of Change) | Period = 10 | ROC > 0 | ROC < 0 | 6.11% |
| 9 | **OBV** (On-Balance Volume) | 20-period rolling mean | OBV > OBV_MA | OBV < OBV_MA | 6.26% |
| 10 | **Aroon** | Period = 14 | Aroon Up ≥ 70 AND Aroon Down ≤ 30 | Aroon Up ≤ 30 AND Aroon Down ≥ 70 | 13.04% |

> **CDC Action Zone** is a custom indicator derived from OHLC4 = (Close + Low + High + Open) / 4, with a two-stage EMA applied.  It produces four states: Strong Buy (1), Weak Buy (0.5), Weak Sell (−0.5), Strong Sell (−1).

---

## Optimization Model

### Differential Evolution (DE)

`scipy.optimize.differential_evolution` is used to find the optimal indicator weights and decision threshold.

| Hyperparameter | Value |
|---|---|
| Max iterations | 1500 |
| Population size | 80 |
| Recombination rate | 0.8 |
| Weight bounds | [0.0, 1.0] per indicator |
| Threshold bounds | [0.125, 0.3] |
| Constraint | Σ weights = 1.0 (100%) |

**Fitness function**: `profit = Final Portfolio Value − $100,000`

### ML Classifier Comparison

Standard classifiers were also evaluated (see `Model_RAC_1.ipynb`) to benchmark the DE approach:

| Classifier | Configuration |
|---|---|
| SVM | Polynomial kernel, C = 1.0 |
| Logistic Regression | Default |
| KNN | k = 3 |
| K-Means | Pattern identification |

---

## Signal Generation

The final decision at each trading day:

```
score = Σ(weight[i] × signal[i]) / Σ(weights)   # signals are +1, 0, or −1

Decision:
  score > +0.2383  →  BUY
  score < −0.2383  →  SELL
  otherwise        →  HOLD
```

The threshold **±0.2383** was determined by the optimiser.

---

## Backtesting & Performance

- **Baseline**: Simple Buy-and-Hold strategy
- **Transaction costs**: 0.2% per buy order + 0.2% per sell order
- **Stop-loss**: Position closed if daily drop exceeds 20%
- **Validation**: Out-of-sample test on 2022 data

---

## Web Application

A **Flask** web application provides real-time signal generation.

**Stack**

| Component | Technology |
|---|---|
| Backend | Flask (Python) |
| Indicator engine | `findindi.py` (TA-Lib) |
| Signal engine | `checksignal.py` |
| Charts | Plotly (interactive) |
| Frontend | HTML / Jinja2 |
| Data storage | SQLite |

**User flow**

1. User enters a ticker symbol (e.g., `AAPL`, `PTT.BK`)
2. Latest OHLCV data is downloaded via `yfinance`
3. All 10 indicators are computed
4. Learned weights are applied → weighted score
5. Decision (BUY / SELL / HOLD / ERROR) is displayed alongside an interactive Plotly chart with Buy (green) and Sell (red) markers

---

## Key Parameters

| Parameter | Value | Description |
|---|---|---|
| Moving average periods | 30, 50, 200 | SMA windows |
| MACD | 12 / 26 / 9 | Fast / Slow / Signal |
| ADX period | 14 | Trend strength window |
| ADX threshold | 25 | Minimum ADX to enter |
| SAR acceleration | 0.02 | Sensitivity factor |
| SAR maximum | 0.2 | Acceleration cap |
| ROC period | 10 | Look-back for rate of change |
| Aroon period | 14 | Look-back for Aroon Up/Down |
| OBV MA period | 20 | OBV smoothing window |
| Decision threshold | ±0.2383 | Minimum confidence to trade |
| Buy commission | 0.2% | Per-trade cost |
| Sell commission | 0.2% | Per-trade cost |
| Stop-loss | −20% (daily) | Forced exit threshold |
| Initial capital | $100,000 | Simulation starting value |

---

## Technologies Used

- **Python 3**
- **TA-Lib** — technical indicator calculations
- **yfinance / pandas_datareader** — market data
- **SciPy** (`differential_evolution`) — parameter optimisation
- **scikit-learn** — SVM, Logistic Regression, KNN, K-Means
- **pandas / NumPy** — data manipulation
- **Plotly** — interactive charting
- **Flask** — web application framework
- **SQLite** — lightweight data persistence
- **Jupyter Notebook** — research & experimentation

---

## Awards & Research

- Won **multiple awards** in national / international competitions
- Accompanied by a full research paper (see `Paper/` folder)
- Covers both **Thai SET** and **US equity** markets  
