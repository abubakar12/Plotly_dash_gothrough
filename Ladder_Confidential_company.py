from dash import Dash, html
from dash import Dash, dash_table
import pandas as pd

df = pd.read_csv(r'C:\Users\hp\Desktop\plotly_dash\Confidential_company\Ladder_confidential_company.csv')

df["Date_of_pred"]=pd.to_datetime(df["TYear"].astype(str)+"-"+\
                                  df["TMonth"].astype(str),format="%Y-%m")

df["Date_pred"]=pd.to_datetime(df["YearOfPrediction"].astype(str)+"-"+\
                                  df["MonthOfPrediction"].astype(str),\
                                      format="%Y-%m") 


    
df.drop(["TYear","TMonth","YearOfPrediction","MonthOfPrediction"],1,inplace=True)

df["Date_of_pred"]=df["Date_of_pred"].astype(str)
df["Date_pred"]=df["Date_pred"].astype(str)

df_copy=pd.pivot_table(df,index="Date_of_pred",values="Projected Sales",\
                       columns="Date_pred").reset_index()
    
app = Dash(__name__)

app.layout = dash_table.DataTable(df_copy.to_dict('records'), \
                                  [{"name": i, "id": i} for i in df_copy.columns])

if __name__ == '__main__':
    app.run_server(debug=False)