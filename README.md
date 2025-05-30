## Introduction
This is a web tool to visualize AI-related urban planning document

## Functions
A search box for user to select a category and return a table of relavant documents in format of a table, with information of document filename, match_count (how many chunks are identified as the given subcategory-related) and a link to open the pdf with category-relavant highlights

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

4. (if needed) Update the constant variable SUBCATEGORIES if it's changed, you can get all the unique subcategories by running the following code in a seperate python file
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

### Install Dependencies
Install dependencies from:
If you install other dependencies, run in terminal:
`pip freeze > requirements.txt`

### Deploy it on Fly.io
Sign up for fly.io account at https://fly.io/dashboard

First time launch:
`fly launch`

Whenever you want to update your app
run `fly deploy` in terminal

See instructions details from https://fly.io/docs/reference/fly-launch/

