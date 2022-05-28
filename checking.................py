
from dash import Dash, dash_table
import pandas as pd
import numpy as np
import pandas as pd
from dash import Dash, dcc, html, Input, Output

from dash import Dash, html
from dash import Dash, dash_table
import pandas as pd
import numpy as np
import dash
import dash_table
import pandas as pd
import re

df = pd.read_csv(
    r'C:\Users\hp\Desktop\plotly_dash\Confidential_company\Ladder_confidential_company.csv')
mapping_material=pd.read_excel(r"C:\Users\hp\Desktop\plotly_dash\Confidential_company\Material_products_mapping.xlsx")
df=pd.merge(df,mapping_material,on="Material",how="left")
df["Date_pred"] = pd.to_datetime(df["TYear"].astype(str)+"-" +
                                 df["TMonth"].astype(str), format="%Y-%m")

df["Date_of_pred"] = pd.to_datetime(df["YearOfPrediction"].astype(str)+"-" +
                                    df["MonthOfPrediction"].astype(str),
                                    format="%Y-%m")


df.drop(["TYear", "TMonth", "YearOfPrediction",
        "MonthOfPrediction"], 1, inplace=True)

df["Date_of_pred"] = df["Date_of_pred"].astype(str)
df["Date_pred"] = df["Date_pred"].astype(str)

df = df.fillna(0)


df_copy = df[df.Product=='DF']

projected_copy = pd.pivot_table(df_copy, index="Date_of_pred",
                                values="Projected Sales",
                                columns="Date_pred")
projected_copy.columns.name=None
projected_copy=projected_copy.reset_index().fillna('')

actual_sales_copy = pd.pivot_table(df_copy, index="Date_of_pred",
                                   values="Actual Sales",
                                   columns="Date_pred")
actual_sales_copy.columns.name=None
actual_sales_copy=actual_sales_copy.reset_index().fillna('') 


dawlance_pred_copy = pd.pivot_table(df_copy, index="Date_of_pred",
                                    values="Dawlance Prediction",
                                    columns="Date_pred")
dawlance_pred_copy.columns.name=None
dawlance_pred_copy=dawlance_pred_copy.reset_index().fillna('') 


new_file = projected_copy.astype(str).set_index("Date_of_pred")+"\n"+actual_sales_copy.astype(str).set_index("Date_of_pred")

new_file = new_file.astype(str)+"\n"+dawlance_pred_copy.astype(str).set_index("Date_of_pred")

new_file=new_file.reset_index()

app = dash.Dash(__name__)

a=new_file.to_dict("records")

for i in a:
    print(i)

a=list(i.values())
a[-1].split('\n')
        

def style_row_by_top_values(df, nlargest=2):
    print(df)
    columns = df.columns
    styles = []
    colors =['red','blue','yellow']
    for i in range(len(df.records)):
        row = df.loc[i, numeric_columns].sort_values(ascending=False)
        i.split('\n') ['a','b','c']
        for j in range(nlargest):
            styles.append({
                'if': {
                    'filter_query': '{{id}} = {}'.format(i), # a
                    'column_id': row.keys()[j]
                },
                'color': {c} for c in colors;
            })
    return styles



app.layout = html.Div([
    dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i} for i in new_file.columns],
        let colors =["red","black"]
        data=new_file.to_dict("records"),
        #style_cell={"color":"blue" },
            style_data_conditional=style_row_by_top_values()
       # style_cell={"whiteSpace": "pre-line" ,"color":"blue" },

    #     style_cell_conditional=[
    # {
    #     'if': {'column_id': 'Region'},
    #     'textAlign': 'left'
    # }
# ]
    ),
    

    dcc.RadioItems(
        list(df["Product"].unique()),
        'DF',
        id='Product-radio',
    ),
])

@app.callback(
    Output('table', 'data'),
    Input('Product-radio', 'value'))
def update_figure(product):
    df_copy = df[df.Product==product]
    
    projected_copy = pd.pivot_table(df_copy, index="Date_of_pred",
                                    values="Projected Sales",
                                    columns="Date_pred")
    projected_copy.columns.name=None
    projected_copy=projected_copy.reset_index().fillna('')

    actual_sales_copy = pd.pivot_table(df_copy, index="Date_of_pred",
                                       values="Actual Sales",
                                       columns="Date_pred")
    actual_sales_copy.columns.name=None
    actual_sales_copy=actual_sales_copy.reset_index().fillna('') 


    dawlance_pred_copy = pd.pivot_table(df_copy, index="Date_of_pred",
                                        values="Dawlance Prediction",
                                        columns="Date_pred")
    dawlance_pred_copy.columns.name=None
    dawlance_pred_copy=dawlance_pred_copy.reset_index().fillna('') 


    new_file = projected_copy.astype(str).set_index("Date_of_pred")+"\n"+actual_sales_copy.astype(str).set_index("Date_of_pred")

    new_file = new_file.astype(str)+"\n"+dawlance_pred_copy.astype(str).set_index("Date_of_pred")

    new_file=new_file.reset_index()
     arr =[]
    print(new_file)

    return new_file.to_dict("records")
    

    

if __name__ == "__main__":
    app.run_server(debug=False)


