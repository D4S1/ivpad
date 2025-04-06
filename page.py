from flask import Flask, render_template, jsonify, request
import utils


app = Flask(__name__)

# Wczytanie danych – przy uruchomieniu aplikacji
excel_file = "data/NIHMS1635539-supplement-1635539_Sup_tab_4.xlsx"
df_box = utils.preprocess_values(excel_file)

utils.plot_gene(df_box, 'STUB1')

@app.route("/")
def index():
    vulcano_plot = utils.plot_vulacano(excel_file)
    return render_template("main.html", vulcano_plot=vulcano_plot)


if __name__ == "__main__":
    app.run(debug=True)
