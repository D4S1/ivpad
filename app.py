from flask import Flask, render_template, jsonify
import utils

app = Flask(__name__)
app.config['ENV'] = 'production'
app.config['DEBUG'] = False
app.config['TESTING'] = False

# Path to the Excel file used for data processing
excel_file = "data/NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx"

# Preprocess values from the Excel file
df_box = utils.preprocess_values(excel_file)


@app.route("/")
def index():
    """
    Renders the index page with the volcano plot and box plot for a specific gene.

    This route loads a volcano plot when the user visits the homepage. 
    It then renders the 'main.html' template and includes the respective plots within the page.

    Returns:
        str: The rendered HTML page generated from the 'main.html' template with the embedded plots.
    """
    vulcano_plot, div_id = utils.plot_vulacano(excel_file)
    return render_template(
        "main.html",
        vulcano_plot=vulcano_plot,
        vulcano_id=div_id,
    )


@app.route("/boxplot/<gene>")
def show_boxplot(gene):
    """
    Renders a box plot for a specified gene.

    This route enables users to view a box plot for a specific gene by providing the gene's name as part of the URL. 
    The box plot for the requested gene will be displayed along with associated publication data.

    Args:
        gene (str): The gene symbol for which the box plot will be displayed.

    Returns:
        json: A JSON response containing the HTML for the box plot of the specified gene and relevant publication information.
    """
    gene_id = int(df_box[df_box.EntrezGeneSymbol == gene].EntrezGeneID)
    return jsonify({
        "boxplot_html": utils.plot_gene(df_box, gene),
        "publication_html": utils.get_publications(gene_id)
    })


if __name__ == "__main__":
    app.run()
