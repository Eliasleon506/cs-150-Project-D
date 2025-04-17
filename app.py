import pandas as pd
import plotly.express as px
import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
import reusable_dash_components as rcd
import figures as fig

df1 = pd.read_csv("Forest_Land.csv", skiprows=4)
df2 = pd.read_csv("Agri_Land.csv", skiprows=4)


df1_long = df1.melt(id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
                    var_name="Year", value_name="Forest land %")
df2_long = df2.melt(id_vars=["Country Name", "Country Code", "Indicator Name", "Indicator Code"],
                    var_name="Year", value_name="Agriculture land %")


df1_long["Year"] = pd.to_numeric(df1_long["Year"], errors="coerce")
df2_long["Year"] = pd.to_numeric(df2_long["Year"], errors="coerce")

df1_filtered = df1_long[df1_long["Year"] > 1991]
df2_filtered = df2_long[df2_long["Year"] > 1991]

merged_df = pd.merge(df1_filtered, df2_filtered, on=["Country Name", "Country Code", "Year"], suffixes=("_forest", "_agriculture"))

## Sourced by ChatGPT question ("can you add a row for the global percentage of each")
# Create global averages for each year
year_columns = [col for col in df1.columns if col.isdigit() and int(col) > 1991]

global_forest = merged_df[[col for col in merged_df.columns if "forest" in col]]
global_agriculture = merged_df[[col for col in merged_df.columns if "agriculture" in col]]

# Compute mean percentage (skip NaN)
global_forest_mean = global_forest.mean(numeric_only=True)
global_agriculture_mean = global_agriculture.mean(numeric_only=True)

# Create a new row for global data
global_row = {
    "Country Name": "Global",
    "Country Code": "GLB",
    "Indicator Name_forest": "Forest area (% of land area)",
    "Indicator Code_forest": "AG.LND.FRST.ZS",
    "Indicator Name_agriculture": "Agricultural land (% of land area)",
    "Indicator Code_agriculture": "AG.LND.AGRI.ZS"
}
# Add each year's global average
for year in year_columns:
    global_row[f"{year}_forest"] = global_forest_mean.get(f"{year}_forest", None)
    global_row[f"{year}_agriculture"] = global_agriculture_mean.get(f"{year}_agriculture", None)

# Compute yearly means from long-format data
forest_global = df1_filtered.groupby("Year")["Forest land %"].mean().reset_index()
agri_global = df2_filtered.groupby("Year")["Agriculture land %"].mean().reset_index()

# Merge the two
global_long = pd.merge(forest_global, agri_global, on="Year")
global_long["Country Name"] = "Global"
global_long["Country Code"] = "GLB"

# Reorder to match merged_df structure
merged_df = pd.concat([merged_df, global_long], ignore_index=True)

countries = merged_df["Country Name"].unique()

app = Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col([
                html.H2(

                    "Deforestation: Not an Agricultural Issue",
                    className="text-center bg-primary text-white p-2",
                ),
                html.H4(
                    "Elias Leon",
                    className="text-center"
                ),
                html.H4(
                    "CS-150 : Community Action Computing",
                    className="text-center"
                ),
            ])
        ),
        dbc.Row(
            [
                dbc.Col( rcd.card_component("Controls",[
                        rcd.dropdown_component("Countries","country-dropdown",[{"label": c, "value": c} for c in sorted(countries)],"Global"),
                        rcd.slider_component("year-slider", "Year", int(year_columns[0]), int(year_columns[-2]), 5, 2005)
                ]
                         ), width=12, lg=5, className="mt-4 border"),
                dbc.Col(
                    [
                        html.Div(id="line-chart-container"),
                        html.Div(id="pie-chart"),
                        html.Hr(),
                    ]
                ),
            ]
        ),
    ],
    fluid=True,
)

@dash.callback(
    Output("line-chart-container", "children"),
    Input("country-dropdown", "value")
)
def update_line_chart(selected_country):
    country_df = merged_df[merged_df["Country Name"] == selected_country]
    country_df = country_df.dropna(subset=["Year"])
    years = country_df["Year"].astype(int)

    forest = country_df["Forest land %"].values
    agri = country_df["Agriculture land %"].values

    y_data_dict = {
        "Forest": forest,
        "Agriculture": agri
    }

    return fig.create_line_chart(
        x_data=years,
        y_data_dict=y_data_dict,
        title=f"Forest vs Agriculture Land Use in {selected_country}",
        x_axis_title="Year",
        y_axis_title="% of Land",
        colors=["#228B22", "#FFA500"]
    )

@dash.callback(
    Output("pie-chart", "children"),
    [Input("country-dropdown", "value"),
     Input("year-slider", "value")]
)
def update_pie_chart(selected_country, selected_year):
    row = merged_df[
        (merged_df["Country Name"] == selected_country) &
        (merged_df["Year"] == selected_year)
    ]

    if row.empty:
        return html.Div("No data available.")

    forest_val = row.iloc[0]["Forest land %"]
    agri_val = row.iloc[0]["Agriculture land %"]
    other =  100 - (forest_val + agri_val)
    return fig.create_pie_chart(
        labels=["Forest", "Agriculture", "Other"],
        values=[forest_val, agri_val, other],
        title=f"Land Use in {selected_country} ({selected_year})",
        colors=["#228B22", "#FFA500","gray"]
    )




if __name__ == "__main__":
    app.run(debug=True)
