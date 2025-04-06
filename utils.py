import pandas as pd
import numpy as np
import plotly.express as px
from plotly.offline import plot


def preprocess_values(excel_file):

    df_box = pd.read_excel(excel_file, sheet_name="S4A values", header=2, index_col=0)

    relevant_idx = list(df_box.columns).index('Set002.H4.OD12.dup')
    samples = [sample for sample in list(df_box.columns)[relevant_idx:] if 'YD' in sample or 'OD' in sample]

    return df_box[["EntrezGeneID", "EntrezGeneSymbol", "Organism"] + samples]


def plot_vulacano(file: str):
    df_volcano = pd.read_excel(file, sheet_name="S4B limma results", header=2, index_col=0)
    df_volcano['neglogP'] = -np.log10(df_volcano['adj.P.Val'])

    fig = px.scatter(
        df_volcano,
        x='logFC',
        y='neglogP',
        hover_name='EntrezGeneSymbol',
        labels={'logFC': 'log2 Fold Change', 'neglogP': '-log10 Adjusted P-Value'},
        title='Volcano Plot of Differential Protein Expression',
    )

    fig.update_traces(textposition='top center')
    
    return plot(fig,
                output_type='div',
                include_plotlyjs=False,
                config={'displayModeBar': False},
                )


def plot_gene(data: pd.DataFrame, gene: str):
    data = data[data.EntrezGeneSymbol == gene].T
    data = data.iloc[3:]

    data["value"] = data.iloc[:, 0].astype(float)
    data["age_group"] = data.index.map(lambda x: "Old" if "OD" in x else "Young")

    fig = px.box(data, x="age_group", y="value", points="all", title=f"Boxplot for {gene} gene")
    fig.update_traces(
        jitter=0.3,
        pointpos=0
    )

    return plot(fig,
                output_type='div',
                include_plotlyjs=False,
                config={'displayModeBar': False},
                )