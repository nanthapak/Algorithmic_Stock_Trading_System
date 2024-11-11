def check():
    import findindi
    import pandas as pd
    import numpy as np
    global signal,buy,sell,dfo,sellbuy
    dfo=findindi.c
    sl1=dfo['adx_signal']
    sl2=dfo['macd_signal']
    sl3=dfo['ma30_200_signal']
    sl4=dfo['ma50_200_signal']
    sl5=dfo['ma30_50_signal']
    sl6=dfo['cdc_signal']
    sl7=dfo['sar_signal']
    sl8=dfo['roc_signal']
    sl9=dfo['obv_signal']
    sl10=dfo['aroon_signal']
    sl11=dfo['adj_close_price']
    w=[0.10607762413686823, 0.15156331863166905, 0.07883386165874004,
    0.06871414126119149,  0.0852604234155046, 0.13452143197313385,
    0.12098422686625537, 0.06112249091135928, 0.06255874149627269,
    0.13036373964900538]
    td=0.23832909207286396
    
    buy=[]
    sell=[]
    signala=0
    signal = []
    for i in range(len(dfo)):
        decision_d= ((w[0]*sl1[i]+w[1]*sl2[i]+w[2]*sl3[i]+w[3]*sl4[i]+w[4]*sl5[i]+w[5]*sl6[i]+w[6]*sl7[i]+w[7]*sl8[i]+w[8]*sl9[i]+w[9]*sl10[i])/sum(w))
        if decision_d>td and signala!=1:
            signala=1
            buy.append(sl11[i])
            signal.append(signala)
            sell.append(np.nan)
        elif decision_d<-td and signala!=-1:
            signala=-1
            buy.append(np.nan)
            signal.append(signala)
            sell.append(sl11[i])
        else:
            
            buy.append(np.nan)
            sell.append(np.nan)
            signal.append(0)
    rai=dfo.drop(columns=['close_price','macd_signal','aroon_signal','obv_signal','roc_signal','sar_signal','cdc_signal','ma30_50_signal','ma50_200_signal','ma30_200_signal','adx_signal'])
    rai['buy']=buy
    rai['sell']=sell
    sellbuy=rai.reset_index()
    global result 
    if signal[-1]==1:
        result="BUY"
    elif signal[-1]==-1:
        result="SELL"
    elif signal[-1]==0:
        result="HOLD"
    else:
        result="ERROR!"
    return sellbuy,result
