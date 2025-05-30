RESULT_DB_FILE = 'static/data/ai_policy_analysis_local_0526.db'

CATEGORY_COLORS = {
    "Governance - Fairness, Bias & Transparency Standards": "1 0 0"
    # "Public Service and Citizen Engagement": "0 1 0",
    # "Urban Management and Innovation": "0 0 1",
    # "Prohibited or Restricted AI Use": "1 0 1",
    # 'test': '0 1 0'   # green
}

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