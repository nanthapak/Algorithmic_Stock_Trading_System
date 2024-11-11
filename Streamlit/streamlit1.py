import streamlit as st
from findindi import*

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
t=True
st.set_page_config(page_title="My Streamlit App", page_icon=":guardsman:", layout="wide")
st.markdown("<style>body{background-color: red;}</style>", unsafe_allow_html=True)
def login(username, password):
    if username == "user" and password == "password":
        return True
    else:
        return False




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

box_style = """
<style>
    .box {
        background-color: white;
        border: 3px solid black;
        padding: 20px;
        margin: 20px;
        }
    .headername{
        font-size: 30px;
        font-weight: bolder;
        margin-left: 10px;
        color: #7e4545;
        padding-top: 0px;
        
        text-align:left;
        }
    hr {
    height: 5px;
    margin-top:0px;
    background-color: black;
    }
    body{background-color: powderblue;}
</style>
"""


global stockname
stockname="AAPL"
def main():
    with st.sidebar:
        st.title("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(username, password):
                st.success("You are logged in!")
            else:
                st.error("Incorrect username or password")
    left_column, right_column = st.columns([2, 1])
    # Add content to the left column
    with left_column:
        st.header("Left Column")
        st.write("This is some content in the left column")

# Add content to the right column
    with right_column:
        st.header("Right Column")
        st.write("This is some content in the right column")
    st.markdown(box_style, unsafe_allow_html=True)
    st.markdown("<div class='headername'><b>Algorithmic Trade Website</b></div>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    stockname = st.text_input("Enter stock name:", "")
    if st.button("ADD STOCK"):
        st.write("Stock name entered:", stockname)
        if stockname=="":
            findindis("AAPL","AAPL")
            fig = px.line(sellbuy, x='Date', y="adj_close_price")
            fig.add_trace(go.Scatter(x=sellbuy["Date"],y=sellbuy["sell"],mode='markers',name="SELL",marker=dict(color='Red',size=8,)))
            fig.add_trace(go.Scatter(x=sellbuy["Date"],y=sellbuy['buy'],mode='markers',name="BUY",marker=dict(color='Green',size=8,)))
            st.plotly_chart(fig, theme="streamlit", use_container_width=True)
            st.markdown(box_style, unsafe_allow_html=True)
            st.markdown("<div class='box'><b>RECOMMENDED : ERROR</b></div>", unsafe_allow_html=True)
        else:
            try:
                findindis(stockname,stockname)
                check()
                fig = px.line(sellbuy, x='Date', y="adj_close_price")
                fig.add_trace(go.Scatter(x=sellbuy["Date"],y=sellbuy["sell"],
                                mode='markers',name="SELL",marker=dict(
                        color='Green',
                        size=8,)))
                fig.add_trace(go.Scatter(x=sellbuy["Date"],y=sellbuy['buy'],
                                mode='markers',name="BUY",marker=dict(
                        color='Red',
                        size=8,)))
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                st.markdown(box_style, unsafe_allow_html=True)
                st.markdown(f"<div class='box'><b>RECOMMENDED : {result}</b></div>", unsafe_allow_html=True)
            except:
                findindis("AAPL","AAPL")
                fig = px.line(sellbuy, x='Date', y="adj_close_price")
                fig.add_trace(go.Scatter(x=sellbuy["Date"],y=sellbuy["sell"],mode='markers',name="SELL",marker=dict(color='Green',size=8,)))
                fig.add_trace(go.Scatter(x=sellbuy["Date"],y=sellbuy['buy'],mode='markers',name="BUY",marker=dict(color='Red',size=8,)))
                st.plotly_chart(fig, theme="streamlit", use_container_width=True)
                st.markdown(box_style, unsafe_allow_html=True)
                st.markdown("<div class='box'><b>RECOMMENDED : ERROR</b></div>", unsafe_allow_html=True)
        


if __name__ == "__main__":
    main()


