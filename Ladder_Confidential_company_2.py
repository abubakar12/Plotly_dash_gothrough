from dash import Dash, html
from dash import Dash, dash_table
import pandas as pd
import numpy as np
import dash
import dash_table
import pandas as pd

df = pd.read_csv(
    r'C:\Users\hp\Desktop\plotly_dash\Confidential_company\Ladder_confidential_company.csv')

df["Date_pred"] = pd.to_datetime(df["TYear"].astype(str)+"-" +
                                 df["TMonth"].astype(str), format="%Y-%m")

df["Date_of_pred"] = pd.to_datetime(df["YearOfPrediction"].astype(str)+"-" +
                                    df["MonthOfPrediction"].astype(str),
                                    format="%Y-%m")


df.drop(["TYear", "TMonth", "YearOfPrediction",
        "MonthOfPrediction"], 1, inplace=True)

df["Date_of_pred"] = df["Date_of_pred"].astype(str)
df["Date_pred"] = df["Date_pred"].astype(str)

# df["Projected Sales"]=df["Projected Sales"].astype(str)
# df["Actual Sales"]=df["Actual Sales"].astype(str)
# df["Dawlance Prediction"]=df["Dawlance Prediction"].astype(str)


df = df.fillna(0)

projected_copy = pd.pivot_table(df, index="Date_of_pred",
                                values="Projected Sales",
                                columns="Date_pred")
projected_copy.columns.name=None
projected_copy=projected_copy.reset_index().fillna('')

actual_sales_copy = pd.pivot_table(df, index="Date_of_pred",
                                   values="Actual Sales",
                                   columns="Date_pred")
actual_sales_copy.columns.name=None
actual_sales_copy=actual_sales_copy.reset_index().fillna('') 


dawlance_pred_copy = pd.pivot_table(df, index="Date_of_pred",
                                    values="Dawlance Prediction",
                                    columns="Date_pred")
dawlance_pred_copy.columns.name=None
dawlance_pred_copy=dawlance_pred_copy.reset_index().fillna('') 


new_file = projected_copy.astype(str).set_index("Date_of_pred")+"\n"+actual_sales_copy.astype(str).set_index("Date_of_pred")

new_file = new_file.astype(str)+"\n"+dawlance_pred_copy.astype(str).set_index("Date_of_pred")

new_file=new_file.reset_index()

#______________________________________________________________________

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id="table",
    columns=[{"name": i, "id": i} for i in new_file.columns],
    data=new_file.to_dict("records"),
    style_cell={"whiteSpace": "pre-line"},
)

if __name__ == "__main__":
    app.run_server(debug=True)
