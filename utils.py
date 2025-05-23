import sqlite3
import pandas as pd
from constants import RESULT_DB_FILE

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


import re

def get_text_by_file_category(filename, category):
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

    # # Join all the returned chunk_text in a list
    # category_text = df_category["chunk_text"].tolist()

    # examples of row
    # 'Page 3 of 5\n\n6. Public Records & City Records Management\n6.1. All records generated, used, or stored by Generative AI vendors or solutions may be considered\npublic records and must be disclosed upon request.',
    # 'Note: this section refers to exceptions to this policy as it relates to generative AI tools that are\nin use by the City. It does not refer to requests for acquisition of non-standard applications or\ntechnologies. Non-compliance\nThe Chief Technology Officer (CTO) is responsible for compliance with this policy. Enforcement may be\nimposed in coordination with individual division directors and department leaders. Non-compliance may\nresult in department leaders imposing disciplinary action, restriction of access, or more severe penalties\nup to and including termination of employment or vendor contract. Related Standards and Policies\n• City Privacy Policy [POL-202]\n• Acquisition of Technology Resources [STA-209]\n• Information Security Policy [POL-201]\n• Data Classification Guideline [GUI-110]\nResponsibilities\nThe policy will be maintained through the Data Privacy, Accountability and Compliance (DPAC) division,\nowned by the Director of DPAC and City of Seattle Chief Privacy Officer. Their responsibilities include\ncreating and maintaining the generative AI risk and impact criteria and the documents and forms to\nsupport the exception review process for this technology. Document Control\nThis policy shall be effective on 11/1/2023 and shall be reviewed annually. Page 4 of 5\n\nVersion Content Contributors\nv 1.0 Initial Draft Reviewer:\nGreg Smith – Chief Information Security Officer (CISO)\nFinal Approver:\nJim Loter – Interim Chief Technology Officer (CTO)\nPage 5 of 5\n\nApproval Date\n10/23/2023\n10/23/2023']


    # Clean each chunk: split on \n, strip whitespace, collapse internal spaces, drop empty lines
    cleaned_lines = []
    for chunk in df_category["chunk_text"]:
        print(chunk)
        print("===")
        lines = chunk.split('\n')
        for line in lines:
            normalized = re.sub(r'\s+', ' ', line.strip())
            normalized = re.sub(r'-$', '', normalized) #remove trailing -
            if normalized:
                if len(normalized) > 1:
                    cleaned_lines.append(normalized)
    print(len(cleaned_lines))
    return cleaned_lines
    # print(category_text)
    # Save the grouped DataFrame to a CSV file
    # return category_text


if __name__ == "__main__":
    category = "Data Privacy and Security"
    filename = "CTO-Policy-Advisory-Team-on-Generative-AI-Report.pdf__seattlegov-72c2c12bc9b200fd940d82b0d0b2e7fe.pdf"
    # get_result_by_category(category)
    get_text_by_file_category(filename, category)