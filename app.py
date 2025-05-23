from flask import Flask, send_from_directory, render_template
from flask import Flask, request, send_file, abort
import fitz  # PyMuPDF
import io
import os
from constants import CATEGORY_COLORS
app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def home():
    return render_template("/index.html")

from utils import get_result_by_category, get_text_by_file_category

# http://127.0.0.1:8080/Data%20Privacy%20and%20Security
# http://127.0.0.1:8080/Public%20Service%20and%20Citizen%20Engagement
# http://127.0.0.1:8080/highlight/CTO-Policy-Advisory-Team-on-Generative-AI-Report.pdf__seattlegov-72c2c12bc9b200fd940d82b0d0b2e7fe.pdf/Public%20Service%20and%20Citizen%20Engagement
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
    if category not in CATEGORY_COLORS:
        return abort(404, description="Category not found for this file.")

    # http://127.0.0.1:8080/highlight/City-of-Seattle-Generative-Artificial-Intelligence-Policy.pdf__seattlegov-b6eaf5444e4f4ba7a759bd75016e58bd.pdf/Public%20Service%20and%20Citizen%20Engagement
    # relevant_lines = ['''
    # Acquisition of Generative AI Technology 1.1. Consistent with the City’s standards for Acquisition of Technology Resources, City employees may be authorized to use pre-approved g
    # ''']
    # relevant_lines = ["AI"]

    relevant_lines = get_text_by_file_category(filename, category)

    color_str = CATEGORY_COLORS.get(category)
    rgb_color = tuple(map(float, color_str.split()))

    doc = read_pdf(filename)

    highlight_lines_forward(doc, relevant_lines, rgb_color)

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
    # for line in lines:
    #     for page in doc:
    #         matches = page.search_for(line, quads=True, flags=0)  # case sensitive
    #         for match in matches:
    #             highlight = page.add_highlight_annot(match)
    #             highlight.set_colors(stroke=rgb_color)
    #             highlight.update()

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


# def highlight_pdf(filename, category):
#     if category not in CATEGORY_COLORS:
#         return abort(404, description="Category not found for this file.")

#     # sentences = data[filename][category]
#     relevant_lines = get_text_by_file_category(filename, category)

#     color_str = CATEGORY_COLORS.get(category)
#     rgb_color = tuple(map(float, color_str.split()))

#     doc = read_pdf(filename)

#     for line in relevant_lines:
#         for page in doc:
#             matches = page.search_for(line, quads=True)  # more precise layout match
#             for match in matches:
#                 highlight = page.add_highlight_annot(match)
#                 highlight.set_colors(stroke=rgb_color)
#                 highlight.update()

#     # Save to in-memory buffer
#     output_buffer = io.BytesIO()
#     doc.save(output_buffer)
#     output_buffer.seek(0)
#     doc.close()

#     return send_file(
#         output_buffer,
#         mimetype='application/pdf',
#         download_name=f'highlighted_pdf.pdf',
#         as_attachment=False)


def read_pdf(filename):
    """Reads a PDF file and returns pymupdf.Document."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(BASE_DIR, 'static', 'pdfs', os.path.basename(filename))

    if not os.path.exists(pdf_path):
        return abort(404, description="PDF file not found.")

    doc = fitz.open(pdf_path)

    return doc



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
