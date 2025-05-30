## Introduction
This is a web tool to visualize AI-related urban planning document

match_count: how many chunks are identified as the given subcategory-related


## Steps for setup
### Local database setup
Download all the original PDF document from Dropbox source_pdf folder and save it in local folder static/pdfs

Download ai_policy_analysis_local.db and save it in
static/data

upload the constant variable SUBCATEGORIES if it's changed, you can get all the unique subcategories by running the following code in a seperate python file
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

### Deploy it on Fly.io
See instructions from

first time launch:
run `fly launch` in terminal
then run `fly deploy`
after code change:
run `fly deploy` in terminal

### Code Structure