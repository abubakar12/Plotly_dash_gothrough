from dash import Dash, dash_table
import pandas as pd

data = dict(
    [
        ("Date",["2015-01-01", "2015-10-24","2016-05-10"]),
        ("values", ["1\n1.2\n1.3", "2\n2.2\n2.3", "3\n3.2\n3.3"]),
    ]
)


df = pd.DataFrame(data)


def format_cell(cell):
    values = cell.split("\n")
    colors = ["blue", "red", "green"]
    styled = [f"<div style='color: {c}'>{v}</div>" for v, c in zip(values, colors)]
    return "".join(styled)


df["values"] = df["values"].apply(format_cell)


app = Dash(__name__)

app.layout = dash_table.DataTable(
    data=df.to_dict("records"),
    columns=[{"name": i, "id": i, "presentation": "markdown"} for i in df.columns],
    markdown_options={"html": True},
)

if __name__ == "__main__":
    app.run_server(debug=True)