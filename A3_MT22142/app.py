from flask import Flask, request, render_template_string, render_template
import datetime as d
from datetime import datetime
from datetime import timedelta
import pandas as pd
app = Flask(__name__)
@app.route('/')
def index1():
    return render_template('index.html')

def fun(a,b,c):
  l_high=[]
  l_low=[]
  Stock=a[0]
  Start_date=b[0]
  end_date=c[0]
  df = pd.read_csv(f"C:/Users/RITIK AGRAWAL/Desktop/New folder/{Stock}.csv")
  for i in range(len(df)):
    df["Date"][i]=datetime.strptime(df["Date"][i], "%Y-%m-%d").date()
  if(end_date == ""):
    try:    
      c=datetime.strptime(Start_date, "%d/%m/%Y")
      Start_date=c.date()  
      c=Start_date+timedelta(days=-52*7)
      temp = df["Date"].values[0]
      if(c<temp):
        end_date = temp
      else:
        end_date=c      
      delta = d.timedelta(days=1)
      while (Start_date >= end_date):
        try:          
          l_high.append(df.loc[df["Date"]==end_date,"High"].values[0])
          l_low.append(df.loc[df["Date"]==end_date,"Low"].values[0])          
        except:
          pass      
        end_date += delta
    except:
      error = "Error"
  else:
    try:
      c=datetime.strptime(Start_date, "%d/%m/%Y")
      Start_date=c.date()  
      c=datetime.strptime(end_date, "%d/%m/%Y")
      end_date=c.date()
      delta = d.timedelta(days=1)
      while(Start_date <= end_date):
        try:          
          l_high.append(df.loc[df["Date"]==Start_date,"High"].values[0])
          l_low.append(df.loc[df["Date"]==Start_date,"Low"].values[0])          
        except:
          pass      
        Start_date += delta
    except:
      error = "Error"
      print(error)  
  high=max(l_high)
  low=min(l_low)  
  return [high,low]

def check(Start_date,End_date,Stock):
  if(len(Stock)==0):
    return False 
  Stock = Stock[0]
  try:    
      a=datetime.strptime(Start_date, "%d/%m/%Y").date()
  except:
    return False
  df = pd.read_csv(f"C:/Users/RITIK AGRAWAL/Desktop/New folder/{Stock}.csv")
  for i in range(len(df)):
    df["Date"][i]=datetime.strptime(df["Date"][i], "%Y-%m-%d").date()
  temp = df["Date"].values[0]

  if End_date == "":
    if a<temp:
      return False
    return True
  try:    
      b=datetime.strptime(End_date, "%d/%m/%Y")
  except:
    return False
  
  return True
  

@app.route('/show_data', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        vals = request.form.getlist('stocks')
        result = vals
        
    else:
        result = ''

    if request.method == 'POST':
        vals2 = request.form.getlist('startDate')
        result2 = vals2
        print(type(result2[0]))
    else:
        result2 = ''

    if request.method == 'POST':
        vals3 = request.form.getlist('endDate')
        result3 = vals3
        print(result3)
    else:
        result3 = ''
    
    
    if(check(result2[0],result3[0],result)):
       if request.method=='POST':
        try:
          l=fun(result,result2,result3)
          a=l[0]
          b=l[1]
          error=""
        except:
          a="NA"
          b="NA"
          error="ERROR Try to put date in a correct Range"

    else:
      a="N.A."
      b="N.A."
      error="Select Stock Properly or Try Entering date in correct Format"
    return render_template('index.html', result=result, result2=result2,error=error, result3=result3,high=a,low=b)
app.run(debug=True)