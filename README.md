## Introduction
This is a web tool to visualize AI-related urban planning document,
deployed on https://flyiotest-urban-policy.fly.dev/. # TBD: change to your new fly.io app address


## Functions
A search box for user to select a category and return a table of relavant documents in format of a table, with information of document filename, match_count (how many chunks are identified as the given subcategory-related) and a link to open the pdf with category-relavant highlights

Workflow: 1.find the context and location of chunks classified with specified category using pipeline result; 2.break chunk contend into lines and clean them; 3.loop to find the lines from the pages they're in, using fitz page.search_for and add_highlight_annot functions to find and highlight the relavent lines.


## Code Structure
<pre>```
.
├── Dockerfile  # dockerfile for fly.io launch
├── app.py  # Flask app
└── utils.py    # user functions
├── constants.py    # constants such as folder location, keywords, highlight color
├── fly.toml
├── launch.json     # For dubugging
├── requirements.txt    # All the needed packages
├── static
│   ├── data
│   │   └── ai_policy_analysis_local_0526.db    # Result databse from pipeline
│   └── pdfs    # Original documents in PDF
│   │    ├── license-plate-readers_final-sir.pdf__seattlegov-5ba9b460d8306891aad00231650afb24.
│   │    ├── travel-time-data-collection-handbook.
│   │    └──  ...
│   └── style.css
└── templates   # Templates in html
    ├── main.html
    └── category_table.html
```</pre>

## Steps for setup
### Local database setup
1. Git clone https://github.com/qifan-wu/urbanAIPolicy_Vis.git to local directory, then `git checkout wrapup`

2. Download all the original PDF document from Dropbox source_pdf folder and save it in local folder static/pdfs

3. Download ai_policy_analysis_local.db and save it in
static/data

4. Install Dependencies

Install dependencies using:
`pip install -r requirements.txt`

(optional) Use virtual environment, and if you would like to install new dependencies, run in terminal to update requirements.txt:
`pip freeze > requirements.txt`

5. (if needed) Update the constant variable SUBCATEGORIES if it's changed, you can get all the unique subcategories by running the following code in a seperate python script.
```
conn = sqlite3.connect(RESULT_DB_FILE)
cursor = conn.cursor()
query = """
SELECT DISTINCT subcategory
FROM Classifications
"""
df = pd.read_sql_query(query, conn)
subcategories = df['subcategory'].tolist()
```

6. Run locally with

`python app.py`

## Deploy it on Fly.io
Fly.io a lightweight and cost-effective platform for running backend apps. It supports Flask, SQLite, and file-based workflows, making it ideal for fast, flexible deployment with a public URL.

### Steps to deploy the app on fly.io:
1. Sign up for fly.io account at https://fly.io/dashboard

2. First time launch:
`fly launch`

3. Whenever you want to update your app
run `fly deploy` in terminal

See instructions details from https://fly.io/docs/reference/fly-launch/

