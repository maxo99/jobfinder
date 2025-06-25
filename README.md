# jobfinder
- Implementation of [JobSpy](https://github.com/speedyapply/JobSpy) using [Streamlit](https://streamlit.io/) interface to scrape and manage job listings
- Initial structure generated with [Claude Sonnet 4](https://www.anthropic.com/claude/sonnet)
    - Prompt Used:
    ``` 
    Create a Python application using streamlit to create a UI to enable:
    1. Trigging the jobspy library to scrape for job listings
    2. Viewing the resulting pandas dataframe and filter out entries marked as viewed
    3. Focusing on individual entries with functionality to mark as viewed and add a note
    ```

## Usage
` streamlit run main.py ` 