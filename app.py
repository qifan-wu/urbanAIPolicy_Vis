from flask import Flask, send_from_directory, render_template
from flask import Flask, request, send_file, abort
import fitz  # PyMuPDF
from constants import SUBCATEGORIES
from utils import *
from constants import *


app = Flask(__name__, static_folder="static", template_folder="templates")


@app.route("/")
def main():
    return render_template("/main.html", all_categories=SUBCATEGORIES)

# @app.route("/selectbox")
# def selectbox():
#     return render_template("/selectbox.html", all_categories=SUBCATEGORIES)

@app.route("/<category>")
def result_table(category):
    df_category = get_result_by_category(category)
    df_category["file_link"] = df_category["filename"].apply(
        lambda fname: f"/highlight/{fname}/{category}"
    )
    df_category["category"] = category
    data = df_category.to_dict(orient="records")
    return render_template("/category_table.html", data=data, category=category)


@app.route("/highlight/<filename>/<category>", methods=["GET"])
def highlight_pdf(filename, category):

    # http://127.0.0.1:8080/highlight/City-of-Seattle-Generative-Artificial-Intelligence-Policy.pdf__seattlegov-b6eaf5444e4f4ba7a759bd75016e58bd.pdf/Public%20Service%20and%20Citizen%20Engagement
    # relevant_lines = ['''
    # Acquisition of Generative AI Technology 1.1. Consistent with the City’s standards for Acquisition of Technology Resources, City employees may be authorized to use pre-approved g
    # ''']
    # relevant_lines = ["AI"]

    relevant_lines = get_text_by_file_category(filename, category)

    doc = read_pdf(filename)

    highlight_lines_forward(doc, relevant_lines, CHUNK_HIGHLIGHT_COLOR)
    highlight_AI_keywords(doc, relevant_lines, KEYWORD_HIGHLIGHT_COLOR)

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

def highlight_lines_forward(doc, lines, rgb_color):
    # brute force
    # for line in lines:
    #     for page in doc:
    #         matches = page.search_for(line, quads=True, flags=0)  # case sensitive
    #         for match in matches:
    #             highlight = page.add_highlight_annot(match)
    #             highlight.set_colors(stroke=rgb_color)
    #             highlight.update()

    # forward search to reduce time
    page_index_current = 0
    num_pages = len(doc)

    # search in page forward direction
    for line in lines:
        for p_i in range(page_index_current, num_pages):
            page = doc[p_i]
            matches = page.search_for(line, quads=True)
            if matches:
                for match in matches:
                    highlight = page.add_highlight_annot(match)
                    highlight.set_colors(stroke=rgb_color)
                    highlight.update()
                p_index_current = p_i
                break

def highlight_AI_keywords(doc, lines, rgb_color):
    for ai_keyword in AI_KEYWORDS:
        for page in doc:
            matches = page.search_for(ai_keyword, quads=True)
            for match in matches:
                highlight = page.add_highlight_annot(match)
                highlight.set_colors(stroke=rgb_color)
                highlight.update()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
