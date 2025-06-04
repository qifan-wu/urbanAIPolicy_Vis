# This is a Flask application that serves a web interface for displaying and highlighting PDF files based on categories.

from flask import Flask, send_from_directory, render_template
from flask import Flask, request, send_file, abort
import fitz  # PyMuPDF
from constants import SUBCATEGORIES
from utils import *
from constants import *


app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def main():
    """
    Home page with searchbox and returned table
    """
    return render_template("/main.html", all_categories=SUBCATEGORIES)

@app.route("/<category>")
def result_table(category):
    '''
    Render the result table for a specific category, including filename, category, count of matches and link to highlighted PDF
    '''
    if category == "All":
        # Combine all categories' results
        all_df = []
        for cat in SUBCATEGORIES:
            df = get_result_by_category(cat)
            df["file_link"] = df["filename"].apply(lambda fname: f"/highlight/{fname}/{cat}")
            df["category"] = cat
            all_df.append(df)

        df_combined = pd.concat(all_df, ignore_index=True)
        data = df_combined.to_dict(orient="records")
        return render_template("/category_table.html", data=data, category="All Categories")

    else:
        df_category = get_result_by_category(category)
        df_category["file_link"] = df_category["filename"].apply(
            lambda fname: f"/highlight/{fname}/{category}"
        )
        df_category["category"] = category
        data = df_category.to_dict(orient="records")
        return render_template("/category_table.html", data=data, category=category)


@app.route("/highlight/<filename>/<category>", methods=["GET"])
def highlight_pdf(filename, category):
    '''
    Highlighted category relevant lines and AI keywords PDF file.
    '''
    doc = read_pdf(filename)

    relevant_lines = get_text_by_file_category(filename, category)

    # Highlight relevant lines and AI keywords
    highlight_lines_forward(doc, relevant_lines, CHUNK_HIGHLIGHT_COLOR)
    highlight_AI_keywords(doc, KEYWORD_HIGHLIGHT_COLOR)

    # Save to in-memory buffer
    output_buffer = io.BytesIO()
    doc.save(output_buffer)
    output_buffer.seek(0)
    doc.close()

    return send_file(
        output_buffer,
        mimetype='application/pdf',
        download_name=f'highlighted_pdf.pdf',
        as_attachment=False)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
