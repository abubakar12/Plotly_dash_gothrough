
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

df["Projected Sales"]=df["Projected Sales"].round()
df["Actual Sales"]=df["Actual Sales"].round()
df["Dawlance Prediction"]=df["Dawlance Prediction"].round()

df = df.fillna(0)

material_all=df.Material.unique()
material_all=np.append(material_all,"ALL")
df_copy = (df[(df.Product=='DF')|(df.Material.isin(material_all))])

projected_copy = pd.pivot_table(df_copy, index="Date_of_pred",
                                values="Projected Sales",aggfunc='sum',
                                columns="Date_pred")
projected_copy.columns.name=None
projected_copy=projected_copy.reset_index().fillna('')

actual_sales_copy = pd.pivot_table(df_copy, index="Date_of_pred",
                                   values="Actual Sales",aggfunc='sum',
                                   columns="Date_pred")
actual_sales_copy.columns.name=None
actual_sales_copy=actual_sales_copy.reset_index().fillna('') 


dawlance_pred_copy = pd.pivot_table(df_copy, index="Date_of_pred",
                                    values="Dawlance Prediction",aggfunc='sum',
                                    columns="Date_pred")
dawlance_pred_copy.columns.name=None
dawlance_pred_copy=dawlance_pred_copy.reset_index().fillna('') 


new_file = projected_copy.astype(str).set_index("Date_of_pred")+"\n"+actual_sales_copy.astype(str).set_index("Date_of_pred")

new_file = new_file.astype(str)+"\n"+dawlance_pred_copy.astype(str).set_index("Date_of_pred")

def format_cell(cell):
    values = cell.split("\n")
    colors = ["blue", "red", "green"]
    styled = [f"<div style='color: {c}'>{v}</div>" for v, c in zip(values, colors)]
    return "".join(styled)


new_file=new_file.reset_index()
for column in new_file.columns:
    new_file[column] = new_file[column].apply(format_cell)


app = dash.Dash(__name__)




app.layout = html.Div([
    dash_table.DataTable(
        id="table",
        columns=[{"name": i, "id": i, "presentation": "markdown"} for i in new_file.columns],
        markdown_options={"html": True},
        data=new_file.to_dict("records"),
        style_cell={"whiteSpace": "pre-line"},
    #     style_cell_conditional=[
    # {
    #     'if': {'column_id': 'Region'},
    #     'textAlign': 'left'
    # }
# ]
    ),
    

    dcc.Dropdown(
        list(df["Product"].unique()),
        'DF',
        id='Product-radio',
    ),
    dcc.Dropdown(
        list(material_all),
        'ALL',
        id='Material-radio',
    ),
])

@app.callback(
    Output('table', 'data'),
    Input('Product-radio', 'value'),
    Input('Material-radio', 'value'))
def update_figure(product,material):
    
    if material=="ALL":
        df_copy = (df[(df.Product==product)&(df.Material.isin(material_all))])
    else:   
        df_copy = (df[(df.Product==product)&(df.Material==material)])
 
    
    
    projected_copy = pd.pivot_table(df_copy, index="Date_of_pred",
                                    values="Projected Sales",aggfunc='sum',
                                    columns="Date_pred")
    projected_copy.columns.name=None
    projected_copy=projected_copy.reset_index().fillna('')

    actual_sales_copy = pd.pivot_table(df_copy, index="Date_of_pred",
                                       values="Actual Sales",aggfunc='sum',
                                       columns="Date_pred")
    actual_sales_copy.columns.name=None
    actual_sales_copy=actual_sales_copy.reset_index().fillna('') 


    dawlance_pred_copy = pd.pivot_table(df_copy, index="Date_of_pred",
                                        values="Dawlance Prediction",aggfunc='sum',
                                        columns="Date_pred")
    dawlance_pred_copy.columns.name=None
    dawlance_pred_copy=dawlance_pred_copy.reset_index().fillna('') 


    new_file = projected_copy.astype(str).set_index("Date_of_pred")+"\n"+actual_sales_copy.astype(str).set_index("Date_of_pred")

    new_file = new_file.astype(str)+"\n"+dawlance_pred_copy.astype(str).set_index("Date_of_pred")
    
    new_file=new_file.reset_index()
    for column in new_file.columns:
        new_file[column] = new_file[column].apply(format_cell)

     
    return new_file.to_dict("records")
    

    

if __name__ == "__main__":
    app.run_server(debug=False)


