from flask import Flask,render_template,url_for,request
from findindi import *
from flask_sqlalchemy import SQLAlchemy
from checksignal import *
import pandas as pd
import json
import plotly
import plotly.express as px
import plotly.graph_objects as go
app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'


    

@app.route('/', methods=['POST','GET'])
def index():
    if request.method == "POST":
       # getting input with name = fname in HTML form
        stockname = request.form.get("stockname")
        if stockname == "":
            return render_template("index.html")
        else :
            try:
                findindis(stockname,stockname)
                check()

                fig = px.line(sellbuy, x='Date', y="adj_close_price")
                fig.add_trace(go.Scatter(x=sellbuy["Date"],y=sellbuy["sell"],
                    mode='markers',name="sell"))
                fig.add_trace(go.Scatter(x=sellbuy["Date"],y=sellbuy['buy'],
                    mode='markers',name="buy"))

                graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
                return render_template("index.html",a=result,stockname=stockname,graphJSON=graphJSON)
            except:
                return render_template("index.html",a="ew",stockname=stockname)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
