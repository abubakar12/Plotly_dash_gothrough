import dash
import dash_table
import pandas as pd

df = pd.DataFrame(
    {
        "date": ["20210613", "20210614", "20210615"],
        "user": ["A\nB", "C", "D"],
        "machine": [1, 0, 3],
    }
)

app = dash.Dash(__name__)

app.layout = dash_table.DataTable(
    id="table",
    columns=[{"name": i, "id": i} for i in df.columns],
    data=df.to_dict("records"),
    style_cell={"whiteSpace": "pre-line"},
)

if __name__ == "__main__":
    app.run_server(debug=True)