from flask import Flask, send_from_directory, render_template
from flask import Flask, request, send_file, abort
import fitz  # PyMuPDF
import io
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/data/<path:filename>")
# def data_files(filename):
#     return send_from_directory("static/data", filename)

# @app.route("/pdfs/<path:filename>")
# def serve_pdf(filename):
#     return send_from_directory("static/pdfs", filename)

data = {
        'test.pdf':
            {
            'category1':[
                'All City departments. Vendors, contractors, and volunteers who operate on behalf of the City are also subject to this policy',
                'If a technology that has already been approved for use in the City adds or incorporates generative AI capabilities, no additional approval is required to use those capabilities, however all other aspects in this policy apply to said use.'
                ],
            'category2':[
                'Documentation of HITL reviews shall be retained according to the appropriate records retention schedule.'
                ]
            }
        }

CATEGORY_COLORS = {
    'category1': '1 0 0',   # red
    'category2': '0 0 1'    # blue
}

@app.route("/highlight/<file_name>/<category>", methods=["GET"])
def highlight_pdf(file_name, category):
    sentences = data[file_name][category]
    print(sentences)
    color_str = CATEGORY_COLORS.get(category)
    pdf_path = os.path.join(os.path.join('static', 'pdfs'), os.path.basename(file_name))

    if category not in CATEGORY_COLORS:
        return abort(404, description="Category not found for this file.")
    if not os.path.exists(pdf_path):
        return abort(404, description="PDF file not found.")

    doc = fitz.open(pdf_path)
    rgb_color = tuple(map(float, color_str.split()))

    for sentence in sentences:
        for page in doc:
            matches = page.search_for(sentence, quads=True)  # more precise layout match
            for match in matches:
                highlight = page.add_highlight_annot(match)
                highlight.set_colors(stroke=rgb_color)
                highlight.update()

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
    app.run(debug=True, port=8080)
