from flask import Flask, render_template, jsonify, request
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.offline import plot
import plotly
import json

app = Flask(__name__)

# Wczytanie danych – przy uruchomieniu aplikacji
excel_file = "data/NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx"



df_box = pd.read_excel(excel_file, sheet_name="S4A values", header=2, index_col=0)

def plot_vulacano(file):
    df_volcano = pd.read_excel(file, sheet_name="S4B limma results", header=2, index_col=0)
    df_volcano['neglogP'] = -np.log10(df_volcano['adj.P.Val'])

    fig = px.scatter(
        df_volcano,
        x='logFC',
        y='neglogP',
        hover_name='TargetFullName',
        labels={'logFC': 'log2 Fold Change', 'neglogP': '-log10 Adjusted P-Value'},
        title='Volcano Plot of Differential Protein Expression',
    )

    fig.update_traces(textposition='top center')
    
    return plot(fig, output_type='div', include_plotlyjs=False)

@app.route("/")
def index():
    vulcano_plot = plot_vulacano(excel_file)
    return render_template("main.html", vulcano_plot=vulcano_plot)


if __name__ == "__main__":
    app.run(debug=True)
