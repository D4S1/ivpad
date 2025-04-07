import pandas as pd
import numpy as np
import plotly.express as px
from plotly.offline import plot
import re
import requests


def preprocess_values(excel_file: str) -> pd.DataFrame:
    """
    Preprocess values from an Excel file containing gene expression data.

    Parameters:
    excel_file (str): The path to the Excel file containing the data.

    Returns:
    pd.DataFrame: A DataFrame containing the 'EntrezGeneID', 'EntrezGeneSymbol', 'Organism', 
                  and relevant sample columns that include 'YD' or 'OD' in the sample names.
    """
    df_box = pd.read_excel(excel_file, sheet_name="S4A values", header=2, index_col=0)

    relevant_idx = list(df_box.columns).index('Set002.H4.OD12.dup')
    samples = [sample for sample in list(df_box.columns)[relevant_idx:]
               if 'YD' in sample or 'OD' in sample]

    return df_box[["EntrezGeneID", "EntrezGeneSymbol", "Organism"] + samples]


def plot_vulacano(file: str):
    """
    Generate a volcano plot for differential protein expression from a given Excel file.

    Parameters:
    file (str): The path to the Excel file containing the data.

    Returns:
    tuple: The HTML div of the plot and the div ID.
    """
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

    fig.update_traces(
        marker=dict(size=10, opacity=0.6)
    )

    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=15,
        yaxis_title_font_size=15,
        font=dict(size=14),
        height=600
    )

    fig.update_traces(textposition='top center')

    vulcano = plot(
        fig,
        output_type='div',
        include_plotlyjs=True,
        config={'displayModeBar': False},
    )
    div_id = re.search('<div id="([^"]*)"', vulcano).groups()[0]

    return vulcano, div_id


def plot_gene(data: pd.DataFrame, gene: str):
    """
    Generate a boxplot comparing protein concentrations between young and old age groups for a given gene.

    Parameters:
    data (pd.DataFrame): The dataframe containing protein concentration data.
    gene (str): The gene to plot.

    Returns:
    str: The HTML div of the plot.
    """
    data = data[data.EntrezGeneSymbol == gene].T
    data = data.iloc[3:]

    data["value"] = data.iloc[:, 0].astype(float)
    data["age_group"] = data.index.map(lambda x: "Old" if "OD" in x else "Young")

    fig = px.box(
        data,
        x="age_group",
        y="value",
        points="all",
        color="age_group",
        title=f"Protein Concentration: Young vs. Old for {gene}",
        labels={
            "age_group": "Donor Age Group",
            "value": "Protein Concentration"
        },
    )

    fig.update_traces(
        jitter=0.3,
        pointpos=0,
        hoverinfo='skip',
        marker=dict(opacity=0.6),
        showlegend=False
    )

    fig.update_layout(
        title_font_size=20,
        xaxis_title_font_size=15,
        yaxis_title_font_size=15,
        font=dict(size=14),
        height=600
    )

    return plot(
        fig,
        output_type='div',
        include_plotlyjs=False,
        config={'displayModeBar': False},
    )

def get_publications(gene_id):

    query = f"https://mygene.info/v3/gene/{gene_id}?species=Human&fields=generif&dotfield=false&size=10"
    response = requests.get(query)

    publications = response.json()["generif"][:10]    
    
    publications_html = ""

    for publication in publications:
        publications_html += f'''
        <li class="list-group-item">
        <a href="https://pubmed.ncbi.nlm.nih.gov/{publication["pubmed"]}/">{get_pub_title(publication["pubmed"])}</a><br>
        <small class="text-muted">Pubmed ID: {publication["pubmed"]}</small>
        </li>
        '''
        get_pub_title(publication["pubmed"])
    return publications_html


def get_pub_title(pmid):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    params = {
        "db": "pubmed",
        "id": pmid,
        "retmode": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()

    try:
        return data['result'][str(pmid)]["title"]
    except KeyError:
        return "Title not found"