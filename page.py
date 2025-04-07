from flask import Flask, render_template
import utils

app = Flask(__name__)

excel_file = "data/NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx"
df_box = utils.preprocess_values(excel_file)


@app.route("/")
def index():
    """
    Renders the index page with the volcano plot and box plot for a given gene.

    This route loads the volcano plot and the box plot for the gene 'STUB1' when the user visits the home page.
    It then renders the 'main.html' template with the respective plots.

    Returns:
    str: The HTML page generated from the 'main.html' template with embedded plots.
    """
    vulcano_plot, div_id = utils.plot_vulacano(excel_file)
    box_plot = utils.plot_gene(df_box, 'STUB1')
    return render_template(
        "main.html",
        vulcano_plot=vulcano_plot,
        vulcano_id=div_id,
        box_plot=box_plot
    )


@app.route("/boxplot/<gene>")
def show_boxplot(gene):
    """
    Renders a box plot for a specified gene.

    This route allows the user to view a box plot for any given gene by passing the gene's name in the URL.
    
    Parameters:
    gene (str): The gene for which the box plot will be displayed.

    Returns:
    str: The HTML div of the box plot for the specified gene.
    """
    gene_id = df_box[df_box.EntrezGeneSymbol == gene].EntrezGeneID
    utils.get_publications(gene_id)
    return utils.plot_gene(df_box, gene)


if __name__ == "__main__":
    app.run(debug=True)
