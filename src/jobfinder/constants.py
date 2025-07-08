RECORDS_WITH_DESCRIPTION = """
- Review the following job listing for comparison against 
user reviewed existing records. 
- Provided with existing records are the title, pros, cons, score, and description.
- Use the pros of existing records with high scores as positive indicators.
- Use the cons of existing records with low scores as negative indicators.
- If the listing description matches well with high-scoring records, consider it positively.
- If the listing description matches well with low-scoring records, consider it negatively.
- Return a score from 0.0 to 10.0, where 0.0 is the lowest and 10.0 is the highest.
- Return pros and cons from the listing description to support your score.
- Pros and cons should be a single string response of bullet points.
- Format the response as json with keys: score, pros, cons.
## Listing:
### Title: {{listing.title}}
### Description: {{listing.description}}
### Existing Records: 
# {% for record in records %}
    ### Title: {{record.title}}
    ### Pros: {{record.pros}}
    ### Cons: {{record.cons}}
    ### Score: {{record.score}}
    ### Description: {{record.description}}
{% endfor %}

"""

RECORDS_NO_DESCRIPTION = """
- Review the following job listing for comparison against 
user reviewed existing records. 
- Provided with existing records are the title, pros, cons, score, and description.
- Use the pros of existing records with high scores as positive indicators.
- Use the cons of existing records with low scores as negative indicators.
- If the listing description matches well with high-scoring records, consider it positively.
- If the listing description matches well with low-scoring records, consider it negatively.
- Return a score from 0.0 to 10.0, where 0.0 is the lowest and 10.0 is the highest.
- Return pros and cons from the listing description to support your score.
- Pros and cons should be a single string response of bullet points.
- Format the response as json with keys: score, pros, cons.
## Listing:
### Title: {{listing.title}}
### Description: {{listing.description}}
### Existing Records:
{% for record in records %}
    ### Title: {{record.title}}
    ### Summary: {{record.summary}}
    ### Pros: {{record.pros}}
    ### Cons: {{record.cons}}
    ### Score: {{record.score}}
{% endfor %}

"""


SUMMARIZATION_TEMPLATE = """
- Review the following job listing and summarize the qualifications and responsibilities.
- Return json with single json list element 'summaries' where each object represents a provided job listing description.
- For each object in the list there should be a string id and a 'summary' which should be a single string response of bullet points.

{% for record in records %}
# Record
    ### ID: {{record.id}}
    ### Description: {{record.description}}
{% endfor %}
"""

PRESET_TEMPLATES = {
    "v1_records_no_description": RECORDS_NO_DESCRIPTION,
    "v1_records_with_description": RECORDS_WITH_DESCRIPTION,
}


TEMPLATE_HELP_MD = """
            **Available Variables:**
            - `listing`: Job listing
            **Object Properties:**
            - `listing.title`: Job Title
            - `listing.description`: Description from job listing
            
            - `records`: List of selected record objects
            **Object Properties:**
            - `record.title`: Job Title
            - `record.pros`: Pros
            - `record.cons`: Cons
            - `record.score`: Score
            **Example Templates:**
            ```
            """
