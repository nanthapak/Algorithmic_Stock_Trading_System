def findindis(Name,RN):
    import datetime
    from datetime import date
    from datetime import timedelta
    import pandas_datareader.data as web
    import matplotlib.pyplot as plt
    import numpy as np
    import talib as ta
    import pandas as pd
    import yfinance as yf
    global df_signal
    global dfa1_all
    yesterday = date.today() - timedelta(hours = 12 )
    yesterday=str(yesterday)
    
    Eyear = int(yesterday[:4])
    Emonth = int(yesterday[5:7])
    Eday = int(yesterday[8:10])
    Syear=2016
    Smonth=1
    Sday=2
    Sdate ="%s-%s-%s" % (Syear,Smonth,Sday)
    Edate ="%s-%s-%s" % (Eyear,Emonth,Eday)
    Byear = Syear-1
    start=datetime.datetime(Syear,Smonth,Sday)
    end=datetime.datetime(Eyear,Emonth,Eday)
    Stockdata=yf.download(Name,start,end)
    dfa1=Stockdata

    start=datetime.datetime(Byear,Smonth,Sday)
    end=datetime.datetime(Eyear,Emonth,Eday)
    Stockdata=yf.download(Name,start,end)
    dfa1_all=Stockdata

    MA30=ta.MA(dfa1_all['Close'], timeperiod=30, matype=0)
    MA30=MA30.loc[Sdate:Edate]
    MA30=MA30.array
    dfa1['MA30']=MA30

    MA50=ta.MA(dfa1_all['Close'], timeperiod=50, matype=0)
    MA50=MA50.loc[Sdate:Edate]
    MA50=MA50.array
    dfa1['MA50']=MA50

    MA200=ta.MA(dfa1_all['Close'], timeperiod=200, matype=0)
    MA200=MA200.loc[Sdate:Edate]
    MA200=MA200.array
    dfa1['MA200']=MA200
    
    #ma30_200_signal
    prices = dfa1['Open']
    buy_price = []
    sell_price = []
    ma30_200_signal = []
    signal = 0
    
    for i in range(len(dfa1)):
        if dfa1['MA30'][i] > dfa1['MA200'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                ma30_200_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ma30_200_signal.append(0)
        elif dfa1['MA30'][i] < dfa1['MA200'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                ma30_200_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ma30_200_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            ma30_200_signal.append(0)
    #ma50_200_signal
    buy_price = []
    sell_price = []
    ma50_200_signal = []
    signal = 0

    for i in range(len(dfa1)):
        if dfa1['MA50'][i] > dfa1['MA200'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                ma50_200_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ma50_200_signal.append(0)
        elif dfa1['MA50'][i] < dfa1['MA200'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                ma50_200_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ma50_200_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            ma50_200_signal.append(0)    
    #3
    #ma30_50_signal
    buy_price = []
    sell_price = []
    ma30_50_signal = []
    signal = 0        
    for i in range(len(dfa1)):
        if dfa1['MA30'][i] > dfa1['MA50'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                ma30_50_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ma30_50_signal.append(0)
        elif dfa1['MA30'][i] < dfa1['MA50'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                ma30_50_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                ma30_50_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            ma30_50_signal.append(0)
       #4       
    obv = ta.OBV(dfa1_all["Close"], dfa1_all["Volume"])
    obv_mean=obv.rolling(20).mean()
    obv_mean=obv_mean.loc[Sdate:Edate]
    obv=obv.loc[Sdate:Edate]
    
    obv_signal = []
    signal = 0
    for i in range(len(obv_mean)):
        if obv[i] > obv_mean[i]:
            if signal != 1:
                signal = 1
                obv_signal.append(signal)
            else:
                obv_signal.append(0)
        elif obv[i] < obv_mean[i]:
            if signal != -1:
                signal = -1
                obv_signal.append(signal)
            else:
                obv_signal.append(0)
        else:
            obv_signal.append(0)
  

    #5
    macd, macdsignal, macdhist = ta.MACD(dfa1['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    MACD=macd.loc[Sdate:Edate]
    dfa1['MACD']=MACD
    dfa1['macdsignal']=macdsignal
    dfa1['macdhist']=macdhist

    data=dfa1
    prices=dfa1['Open']
    buy_price = []
    sell_price = []
    macd_signal = []
    signal = 0

    for i in range(len(data)):
        if data['MACD'][i] > data['macdsignal'][i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        elif data['MACD'][i] < data['macdsignal'][i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                macd_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                macd_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            macd_signal.append(0)
      #6      
    ADX=ta.ADX(dfa1_all['High'], dfa1_all['Low'], dfa1_all['Close'], timeperiod=14)
    ADX=ADX.loc[Sdate:Edate]
    ADX=ADX.array
    dfa1['ADX']=ADX
    
    plus_DMI = ta.PLUS_DM(dfa1_all['High'], dfa1_all['Low'], timeperiod=14)
    minus_DMI= ta.MINUS_DM(dfa1_all['High'], dfa1_all['Low'], timeperiod=14)
    plus_DMI=plus_DMI.loc[Sdate:Edate]
    minus_DMI=minus_DMI.loc[Sdate:Edate]
    plus_DMI=plus_DMI.array
    minus_DMI=minus_DMI.array
    dfa1['plus_DMI']=plus_DMI
    dfa1['minus_DMI']=minus_DMI
    
    prices, pdi, ndi, adx=dfa1['Close'], dfa1['plus_DMI'], dfa1['minus_DMI'], dfa1['ADX']
    buy_price = []
    sell_price = []
    adx_signal = []
    signal = 0
    
    for i in range(len(prices)):
        if adx[i-1] < 25 and adx[i] > 25 and pdi[i] > ndi[i]:
            if signal != 1:
                buy_price.append(prices[i])
                sell_price.append(np.nan)
                signal = 1
                adx_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                adx_signal.append(0)
        elif adx[i-1] < 25 and adx[i] > 25 and ndi[i] > pdi[i]:
            if signal != -1:
                buy_price.append(np.nan)
                sell_price.append(prices[i])
                signal = -1
                adx_signal.append(signal)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)
                adx_signal.append(0)
        else:
            buy_price.append(np.nan)
            sell_price.append(np.nan)
            adx_signal.append(0)
      #7
    roc = ta.ROC(dfa1_all["Close"], timeperiod=10)
    roc=roc.loc[Sdate:Edate]
    data=roc
    roc_signal = []
    signal = 0
    for i in range(len(data)):
        if data[i] > 0:
            if signal != 1:
                signal = 1
                roc_signal.append(signal)
            else:
                roc_signal.append(0)
        elif data[i] < 0:
            if signal != -1:
                signal = -1
                roc_signal.append(signal)
            else:
                roc_signal.append(0)
        else:
            roc_signal.append(0)
    #8

    ohlc4=(dfa1_all['Close']+dfa1_all['Low']+dfa1_all['High']+dfa1_all['Open'])/4

    EMA2=ta.EMA(ohlc4, timeperiod=2)
    EMA26=ta.EMA(EMA2, timeperiod=26)
    EMA12=ta.EMA(EMA2, timeperiod=12)

    EMA26=EMA26.loc[Sdate:Edate]
    EMA26=EMA26.array
    dfa1['EMA26']=EMA26

    EMA12=EMA12.loc[Sdate:Edate]
    EMA12=EMA12.array
    dfa1['EMA12']=EMA12

    EMA2=EMA2.loc[Sdate:Edate]
    EMA2=EMA2.array
    dfa1['EMA2']=EMA2

    ohlc4=ohlc4.loc[Sdate:Edate]
    ohlc4=ohlc4.array
    dfa1['ohlc4']=ohlc4
    fastslow = []
    for i in range(len(dfa1)):
        if dfa1['EMA12'][i] > dfa1['EMA26'][i]:
            fastslow.append(1)
        elif dfa1['EMA26'][i] > dfa1['EMA12'][i]:
            fastslow.append(-1)
        else:
            fastslow.append(0)

    color = []
    for i in range(len(dfa1)):
        if fastslow[i] == 1 and dfa1['EMA2'][i] > dfa1['EMA12'][i]:
            color.append(1) 
        elif fastslow[i] == -1 and dfa1['EMA2'][i] > dfa1['EMA12'][i]:
            color.append(0.5)
        elif fastslow[i] == -1 and dfa1['EMA2'][i] < dfa1['EMA12'][i]:
            color.append(-1) 
        elif fastslow[i] == 1 and dfa1['EMA2'][i] < dfa1['EMA12'][i]:
            color.append(-0.5) 
        else:
            color.append(0)
    
    signal=0
    cdc_signal=[]
    for i in range (len(color)):
        if color[i] == 1:
            if signal != 1:
                signal = 1
                cdc_signal.append(signal)
            else:
                cdc_signal.append(0)
        elif color[i] == -1:
            if signal != -1:
                signal = -1
                cdc_signal.append(signal)
            else:
                cdc_signal.append(0)
        elif color[i] == 0.5:
            if signal != 0.5:
                signal = 0.5
                cdc_signal.append(signal)
            else:
                cdc_signal.append(0)
        elif color[i] == -0.5:
            if signal != -0.5:
                signal = -0.5
                cdc_signal.append(signal)
            else:
                cdc_signal.append(0)

        else:
            signal=0
            cdc_signal.append(signal)
   
    dfa1['cdc']=cdc_signal
        #9
    SAR=ta.SAR(dfa1_all['High'], dfa1_all['Low'], acceleration=0.02, maximum=0.2)
    SAR=SAR.loc[Sdate:Edate]
    SAR=SAR.array
    dfa1['SAR']=SAR
    signal= 0
    countb,counts =0,0

    sar_signal = []
    for i in range(len(dfa1)):
        if dfa1['Close'][i] > dfa1['SAR'][i]:
            counts = 0
            countb =countb +1
            if countb == 2:
                signal = 1
                sar_signal.append(signal)
            else:
                sar_signal.append(0)
        elif dfa1['Close'][i] < dfa1['SAR'][i]:
            countb = 0
            counts =counts +1
            if counts == 2:
                signal = -1
                sar_signal.append(signal)
            else:
                sar_signal.append(0)
        else:
            sar_signal.append(0)
    dfa1['sar']=sar_signal
    #10
    down,up=ta.AROON(dfa1_all['High'], dfa1_all['Low'], timeperiod=14)
    down=down.loc[Sdate:Edate]
    up=up.loc[Sdate:Edate]
    down=down.array
    up=up.array
    aroon_signal = []
    signal = 0
    for i in range(len(dfa1)):
        if up[i] >= 70 and down[i] <= 30:
            if signal != 1:
                signal = 1
                aroon_signal.append(signal)
            else:
                aroon_signal.append(0)
        elif up[i] <= 30 and down[i] >= 70:
            if signal != -1:
                signal = -1
                aroon_signal.append(signal)
            else:
                aroon_signal.append(0)
        else:
            aroon_signal.append(0)
    # signal={'adx_signal':adx_signal,'macd_signal':macd_signal,'ma30_200_signal':ma30_200_signal,'ma50_200_signal':ma50_200_signal,
    #         'ma30_50_signal':ma30_50_signal,'cdc_signal':cdc_signal,'sar_signal':sar_signal,
    #         'roc_signal':roc_signal,'obv_signal':obv_signal,'rsi_signal':rsi_signal,'bb_signal':bb_signal,
    #         'wpr_signal':wpr_signal,'stoch_signal':stoch_signal,'cci_signal':cci_signal,'atr_signal':atr_signal,'aroon_signal':aroon_signal,'close_price':dfa1['Close']#print(dfa1)
    #        ,'adj_close_price':dfa1['Adj Close']}
    signal={'adx_signal':adx_signal,'macd_signal':macd_signal,'ma30_200_signal':ma30_200_signal,'ma50_200_signal':ma50_200_signal,
            'ma30_50_signal':ma30_50_signal,'cdc_signal':cdc_signal,'sar_signal':sar_signal,
            'roc_signal':roc_signal,'obv_signal':obv_signal,'aroon_signal':aroon_signal,'close_price':dfa1['Close']#print(dfa1)
           ,'adj_close_price':dfa1['Adj Close']}
    #globals()['df_of_'+RN]=pd.DataFrame(signal)  
    global c 
    c = pd.DataFrame(signal) 
    return c
