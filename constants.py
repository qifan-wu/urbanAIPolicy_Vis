import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDFS_DIR = 'static/pdfs'
# RESULT_DB_FILE = 'static/data/ai_policy_analysis_local_0526.db'
RESULT_DB_FILE = 'static/data/ai_policy_analysis_local_0526_fakepage.db'

CHUNK_HIGHLIGHT_COLOR = (0.8, 0.8, 0.2) # yellow
KEYWORD_HIGHLIGHT_COLOR = (0.7, 0, 0) # red

SUBCATEGORIES = [
    'Application - Fairness, Bias & Transparency Standards',
    'Application - High-Stake & Regulated Public Domain',
    'Application - Public Service and Citizen Engagement',
    'Application - Urban Management and Innovation',
    'Governance - Accountability, '
    'Procurement & Governance Structures',
    'Governance - Data Privacy and Security',
    'Governance - Fairness, Bias & Transparency Standards',
    'Governance - Human Oversight',
    'Governance - Multi-Stakeholder Participation',
    'Governance - Prohibited and Restricted AI Use'
]
AI_KEYWORDS = [
    "Artificial Intelligence",
    "AI ", # trailing space to avoid matching "AI" in "Seattle"
    "AI.",
    "AI,",
    "AI)",
    "Machine Learning",
    "Large Language Model",
    "Natural Language Processing",
    "Computer Vision",
    "Algorithmic Decision",
    "Automated Decision"
]