import sqlite3
import pandas as pd
from constants import *
import os
import fitz  # PyMuPDF
import io
import re

def read_pdf(filename):
    """Reads a PDF file and returns pymupdf.Document."""

    pdf_path = os.path.join(BASE_DIR, PDFS_DIR, os.path.basename(filename))

    if not os.path.exists(pdf_path):
        return abort(404, description="PDF file not found.")

    doc = fitz.open(pdf_path)

    return doc

def get_result_by_category(category):
    '''
    Get filename, occurance of chunks relavant to the given category from the database.

    Parameters
    ----------
    category : str
        e.g. "Data Privacy and Security"
    Returns
    -------
    df_category : pd.DataFrame
        DataFrame containing the filename and count of chunks relevant to the given category.
    '''

    conn = sqlite3.connect(RESULT_DB_FILE)
    cursor = conn.cursor()

    query = """
    SELECT Documents.filename, COUNT(*) as match_count
    FROM Classifications
    JOIN Chunks ON Classifications.chunk_id = Chunks.chunk_id
    JOIN Documents ON Classifications.doc_id = Documents.doc_id
    WHERE Classifications.subcategory = ?
    GROUP BY Documents.filename
    ORDER BY match_count DESC, Documents.filename
    """

    # Execute the query with the user-provided category
    df_category = pd.read_sql_query(query, conn, params=(category,))

    # Close the connection
    conn.close()

    # # Group chunk_texts by filename
    # grouped_df = df_category.groupby("filename")["chunk_text"].agg(list).reset_index()
    return df_category

def get_text_by_file_category(filename, category):
    '''
    Get all chunks text of category-relevant in a given document.

    filename(str): e.g. 'Q3-2022-CTO-Quarterly-Surveillance-Technology-Determination-Report.pdf__seattlegov-063a1ef3fafa3e91b84441ab73a730ff.pdf'
    category (str): e.g. "Governance - Fairness, Bias & Transparency Standards"

    Returns
    -------
    cleaned_lines (list of str):
        List of cleaned lines from the chunks relevant to the given category in the specified document.
        Each line is stripped of leading/trailing whitespace, internal spaces are collapsed, and empty lines are dropped.
    '''
    conn = sqlite3.connect(RESULT_DB_FILE)
    cursor = conn.cursor()

    query = """
    SELECT Chunks.chunk_text
    FROM Classifications
    JOIN Chunks ON Classifications.chunk_id = Chunks.chunk_id
    JOIN Documents ON Classifications.doc_id = Documents.doc_id
    WHERE Documents.filename = ?
    AND Classifications.subcategory = ?
    """

    # Execute the query with the user-provided category
    df_category = pd.read_sql_query(query, conn, params=(filename, category,))

    # Close the connection
    conn.close()

    # Clean each chunk: split on \n, strip whitespace, collapse internal spaces, drop empty lines
    cleaned_lines = []
    for chunk in df_category["chunk_text"]:
        # print(chunk)
        # print("===")
        lines = chunk.split('\n')
        for line in lines:
            normalized = re.sub(r'\s+', ' ', line.strip())
            normalized = re.sub(r'-$', '', normalized) #remove trailing -
            if normalized:
                if len(normalized) > 1:
                    cleaned_lines.append(normalized)
    # print(len(cleaned_lines))

    return cleaned_lines

def highlight_lines_forward(doc, lines, rgb_color):
    '''
    Highlight lines in the PDF document

    doc (fitz.Document): The PDF document to highlight lines in.
    lines (list of str): List of lines to highlight in the document.
    rgb_color (tuple): RGB color for the highlights, e.g. (1, 0, 0) for red.

    Returns
    -------
    None
    '''

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

def highlight_AI_keywords(doc, rgb_color):
    '''
    Highlight AI-related keywords in the PDF document.

    Returns
    -------
    None
    '''
    for ai_keyword in AI_KEYWORDS:
        for page in doc:
            matches = page.search_for(ai_keyword, quads=True)
            for match in matches:
                highlight = page.add_highlight_annot(match)
                highlight.set_colors(stroke=rgb_color)
                highlight.update()


if __name__ == "__main__":
    category = "Governance - Fairness, Bias & Transparency Standards"
    filename = "Q3-2022-CTO-Quarterly-Surveillance-Technology-Determination-Report.pdf__seattlegov-063a1ef3fafa3e91b84441ab73a730ff.pdf"
    # get_result_by_category(category)
    # get_text_by_file_category(filename, category)
