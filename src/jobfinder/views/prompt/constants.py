import pandas as pd


PROMPT_V1 = """# 
Review the following job listing for comparison against 
user reviewed existing records. 
## Listing:
### Title: {{listing.title}}
### Company: {{listing.company}}
### Description: {{listing.description}}

### Existing Records:
{% for record in records %}
### Title: {{record.title}}
### Company: {{record.company}}
### Description: {{record.description}}
### Pros: {{record.pros}}
### Cons: {{record.cons}}
### Score: {{record.score}}
{% endfor %}

"""

PRESET_TEMPLATES = {
    "Prompt V1": PROMPT_V1,
}



SAMPLE_DATA = pd.DataFrame({
        'instruction_id': [
            'inst_001', 
            'inst_002', 
            'inst_003', 
            'inst_004', 
            'inst_005',
            'inst_006',
            'inst_007',
            ],
        'category': [
            'CATEGORY_1', 
            'CATEGORY_2',
            'CATEGORY_3',
            'CATEGORY_4', 
            'CATEGORY_5',
            'CATEGORY_6',
            'CATEGORY_7',
            ],
        'title': [
            'TITLE_1',
            'TITLE_2',
            'TITLE_3',
            'TITLE_4',
            'TITLE_5',
            'TITLE_6',
            'TITLE_7',
            ],
        'content': [
            'CONTENT_1',
            'CONTENT_2',
            'CONTENT_3',
            'CONTENT_4',
            'CONTENT_5',
            'CONTENT_6',
            'CONTENT_7'
        ],
        'priority': [1, 2, 3, 2, 1, 3, 4],
        'active': [True, True, False, True, True, False, True]
    })



TEMPLATE_HELP_MD = """
            **Available Variables:**
            - `instructions`: List of selected instruction objects
            **Object Properties:**
            - `instruction.instruction_id`: Unique identifier
            - `instruction.category`: Category name
            - `instruction.title`: Instruction title
            - `instruction.content`: Instruction content
            - `instruction.priority`: Priority level (1-5)
            - `instruction.active`: Boolean active status
            **Example Templates:**
            ```jinja2
            {% for instruction in instructions %}
            ## {{ instruction.title }}
            {{ instruction.content }}
            {% endfor %}
            ```
            **Conditional Logic:**
            ```jinja2
            {% for instruction in instructions %}
            {% if instruction.priority >= 3 %}
            ⭐ HIGH PRIORITY: {{ instruction.title }}
            {% endif %}
            {{ instruction.content }}
            {% endfor %}
            ```
            """
