import pandas as pd

BASIC_LIST_TEMPLATE = """# System Instructions
{% for instruction in instructions %}
- {{ instruction.title }}: {{ instruction.content }}
{% endfor %}"""

CATEGORIZED_TEMPLATE = """# System Instructions
{% set categories = instructions | groupby('category') %}
{% for category, items in categories %}
## {{ category }}
{% for instruction in items %}
- **{{ instruction.title }}**: {{ instruction.content }}
{% endfor %}
{% endfor %}"""

PRIORITY_BASED_TEMPLATE = """# System Instructions
{% for instruction in instructions | sort(attribute='priority', reverse=true) %}
{% if instruction.priority >= 3 %}⭐ {% endif %}**{{ instruction.title }}**
{{ instruction.content }}
{% endfor %}"""

DETAILED_FORMAT_TEMPLATE = """# System Instructions
{% for instruction in instructions %}
## {{ instruction.category }}: {{ instruction.title }}
**Instruction ID:** {{ instruction.instruction_id }}
**Priority:** {{ instruction.priority }}/5
**Status:** {{ "Active" if instruction.active else "Inactive" }}
### Content:
{{ instruction.content }}
---
{% endfor %}"""

PRESET_TEMPLATES = {
    "Basic List": BASIC_LIST_TEMPLATE,
    "Categorized": CATEGORIZED_TEMPLATE,
    "Priority Based": PRIORITY_BASED_TEMPLATE,
    "Detailed Format": DETAILED_FORMAT_TEMPLATE,
}



SAMPLE_DATA = pd.DataFrame({
        'instruction_id': ['inst_001', 'inst_002', 'inst_003', 'inst_004', 'inst_005'],
        'category': ['CATEGORY_1', 'CATEGORY_2', 'CATEGORY_3', 'CATEGORY_4', 'CATEGORY_5'],
        'title': ['TITLE_1', 'TITLE_2', 'TITLE_3', 'TITLE_4', 'TITLE_5'],
        'content': [
            'CONTENT_1',
            'CONTENT_2',
            'CONTENT_3',
            'CONTENT_4',
            'CONTENT_5'
        ],
        'priority': [1, 2, 3, 2, 1],
        'active': [True, True, False, True, True]
    })
