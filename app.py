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
            'ai_associated':[
                'All City departments. Vendors, contractors, and volunteers who operate on behalf of the City are also subject to this policy',
                'If a technology that has already been approved for use in the City adds or incorporates generative AI capabilities, no additional approval is required to use those capabilities, however all other aspects in this policy apply to said use.'
                ],
            'ai_associated_fuzzy':[
                'All City departments. vendors, contractors and volunters for the city should also obbey this policy',
                ],
            'ai_vendors':[
                'Documentation of HITL reviews shall be retained according to the appropriate records retention schedule.'
                ],
            'ai_general':[
                '''1. Acquisition of Generative AI Technology
                1.1. Consistent with the City’s standards for Acquisition of Technology Resources, City employees may be authorized to use pre-approved generative AI software tools or they may request a nonstandard acquisition of generative AI software through Seattle IT’s current request process.
                1.2. Seattle IT shall review exception requests according to its current risk and impact methodology,
                which shall include specific review criteria for generative AI technology. Seattle IT shall either
                approve or deny a request according to its criteria.
                1.3. The City’s standard for technology acquisition applies to all technology, including free-to-use
                software or software-as-a-service tools.
                '''
            ],
            'test': [
                '''prior to the use of a Generative AI tool, especially uses that will

                analyze datasets or be used to inform decisions or policy. As per the objectives of the RSJ
                program, the RET should document the steps the department will take to evaluate AI-generated

                content to ensure that its output is accurate and free of discrimination and bias against
                protected classes.
                '''
            ]
            }
        }

CATEGORY_COLORS = {
    'ai_associated': '1 0 0',   # red
    'ai_associated_fuzzy': '1 0 0',   # red
    'ai_vendors': '0 0 1',    # blue
    'ai_general': '0 1 0',   # green
    'test': '0 1 0'   # green
}


@app.route("/highlight/<file_name>/<category>", methods=["GET"])
def highlight_pdf(file_name, category):
    if category not in CATEGORY_COLORS:
        return abort(404, description="Category not found for this file.")

    sentences = data[file_name][category]
    color_str = CATEGORY_COLORS.get(category)
    rgb_color = tuple(map(float, color_str.split()))

    doc = read_pdf(file_name)

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


def read_pdf(file_name):
    """Reads a PDF file and returns pymupdf.Document."""
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    pdf_path = os.path.join(BASE_DIR, 'static', 'pdfs', os.path.basename(file_name))

    if not os.path.exists(pdf_path):
        return abort(404, description="PDF file not found.")

    doc = fitz.open(pdf_path)

    return doc

@app.route("/highlight_fuzzy/<file_name>/<category>", methods=["GET"])
def highlight_fuzzy_pdf(file_name, category):
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


RESULT_DB_FILE = 'ai_policy_analysis_local.db'
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
