RECORDS_WITH_DESCRIPTION = """
- Review the following job listing for comparison against
user reviewed existing records.
- Provided with existing records are the title, pros, cons, score, and description.
- Use the pros of existing records with high scores as positive indicators.
- Use the cons of existing records with low scores as negative indicators.
- If the listing description matches well with high-scoring records, consider it positively.
- If the listing description matches well with low-scoring records, consider it negatively.
- Return a score from -1.0 to 1.0, where -1.0 is the lowest and 1.0 is the highest.
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
- Return a score from -1.0 to 1.0, where -1.0 is the lowest and 1.0 is the highest.
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

SUMMARIZATION_INSTRUCTIONS = """
# Instructions:
- Review one or more job listings for extraction/summarization.
- The goal is to extract qualifications and experience levels from the job listings.
- The response should be a json object with 'summaries' with a json object containing job IDs as keys.
- Each job ID should map to a list of qualifications.
- The qualifications should be extracted from the job listing description.
- The qualifications should be grouped by skill and experience level.
- The experience level should be represented as a string (e.g., "5 years", "2+ years", "N/A").
- The qualifications should be grouped by skill and whether they are required, preferred, or desired.
- The qualifications should be grouped by skill and experience level.
- Each qualification should have the following properties:
    - `skill`: The skill or technology required.
    - `requirement`: Whether the skill is required, preferred, or desired.
    - `experience`: The experience level required for the skill.

"""


SUMMARIZATION_EXAMPLE_RESPONSE = """
## Example Response:
{"summaries":{"job1":[{"skill":"Programming Languages","requirement":"true","experience":"8 years with one or more (e.g., Python, C, C++, Java, JavaScript)"},{"skill":"Master\'s/PhD ","requirement":"preferred","experience":"Engineering, Computer Science, or a related technical field"}]}}


"""


SUMMARIZATION_LISTINGS_TEMPLATE = """
# Job Listings:
{% for record in records %}
## Job Listing
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


_DEFAULT_UPDATE_COLS = [
    "status",
    "score",
    "summarypros",
    "cons",
    "classifier",
    "summarizer",
    "modified",
]
