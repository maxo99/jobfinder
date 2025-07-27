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
### Title: {{ listing.title }}
### Description: {{ listing.description }}
### Existing Records:
{% for record in records %}
    ### Title: {{ record.title }}
    ### Summary: {{ record.summary }}
    ### Pros: {{ record.pros }}
    ### Cons: {{ record.cons }}
    ### Score: {{ record.score }}
{% endfor %}

"""

SUMMARIZATION_INSTRUCTIONS = """
# Instructions:
- Review one or more job listings for extraction/summarization.
- The goal is to extract qualifications and experience levels from the job listings.
- Each returned qualification **must** have a jobID that exactly matches one of the jobIDs provided in the listings below.
- **Do not invent or hallucinate jobIDs. Only use jobIDs from the provided listings.**
- The qualifications should be extracted from the job listing description respective of the jobID it belongs to.
- The qualifications should be grouped by skill and experience level.
- The experience level should be represented as a string (e.g., "5 years", "2+ years", "N/A").
- The qualifications should be grouped by skill and whether they are required, preferred, or desired.
"""

# SUMMARIZATION_EXAMPLE_RESPONSE = """
# ## Example Response:
# {"summaries":[{"id":"{{JOB_ID}}","skill":"Programming Languages","requirement":"true","experience":"8 years with one or more (e.g., Python, C, C++, Java, JavaScript)"},{"id":"{{JOB_ID}}","skill":"Master\'s/PhD ","requirement":"preferred","experience":"Engineering, Computer Science, or a related technical field"}]}

# """


SUMMARIZATION_LISTINGS_TEMPLATE = """
## Job Listings:
{% for record in records %}
### Job Listing
    #### jobID: {{ record.id }}
    #### Description: {{ record.description }}
{% endfor %}

# Instruction Reminder:
**the only valid jobIDs:**
REMEMBER: Do not invent or hallucinate jobIDs. Use only the jobIDs are listed above.

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

DEFAULT_COLS = [
    "modified",
    "date_posted",
    "company",
    "title",
    "site",
    "status",
    "summarizer",
    "classifier",
    "score",
    # "is_remote",
    "job_type",
]
EXTRA_COLS = ["id", "pros", "cons", "summary"]

# JOBSPY_COLS = [
#     "id",
#     "job_url",
#     "job_url_direct",
#     "location",
#     "salary_source",
#     "interval",
#     "min_amount",
#     "max_amount",
#     "currency",
#     "job_level",
#     "job_function",
#     "description",
#     "company_industry",
#     "company_url",
#     "listing_type",
#     "emails",
#     "company_logo",
#     "company_url_direct",
#     "company_addresses",
#     "company_num_employees",
#     "company_revenue",
#     "company_description",
#     "skills",
#     "experience_range",
#     "company_rating",
#     "company_reviews_count",
#     "vacancy_count",
#     "work_from_home_type",
# ]

DISPLAY_COLS = [
    *DEFAULT_COLS,
    #   *JOBSPY_COLS,
    *EXTRA_COLS,
]


SCORING_UTIL_DESCRIPTION = """
    Select a listing to use for evaluation.
    Select records to populate as prompt context using Jinja2 templates.
"""


EMBEDDINGS_DIMENSION = 768

NEW = "new"
VIEWED = "viewed"
EXCLUDED = "excluded"
APPLIED = "applied"
STATUS_TYPES = {NEW, VIEWED, EXCLUDED, APPLIED}
USER = "User"
AI = "AI"
NA = "N/A"
USER_TYPES = {USER, AI, NA}


DEFAULT_STATUS_FILTERS = [s for s in STATUS_TYPES if s != EXCLUDED]

DEFAULT_PAGE_DESCRIPTION = """
        ### Getting Started:
        1. **Configure your search** in the sidebar
        2. **Select a job site** (Indeed, LinkedIn)
        3. **Enter search terms** and location
        4. **Click 'Scrape Jobs'** to start collecting job listings
        5. **View and manage** your jobs in the tabs above
        ### Features:
        - 🔍 **Job Scraping**: Collect jobs from multiple sites
        - 📊 **Overview**: View all jobs with filtering options
        - 📋 **Details**: Focus on individual jobs with notes
        - ✅ **Tracking**: Mark jobs as viewed and add personal notes
        - 💾 **Persistence**: Data is automatically saved between sessions
        """
