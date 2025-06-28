

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
