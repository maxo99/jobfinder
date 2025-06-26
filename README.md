# jobfinder
- Implementation of [JobSpy](https://github.com/speedyapply/JobSpy) 
using [Streamlit](https://streamlit.io/) interface to scrape and manage job listings
- Packaged and mangaed with [uv](https://docs.astral.sh/uv/)
- Initial structure generated with [Claude Sonnet 4](https://www.anthropic.com/claude/sonnet)


### Purpose
- Linkedin etc. often do not have a function to exclude listings.
- Listings scraped with [JobSpy](https://github.com/speedyapply/JobSpy) 
can be managed and analyzed with [Streamlit](https://streamlit.io/).
- Results need to be persistent to be collected over many runs. 
- Add funcationality for user to add context to individual listings. 
- Provide framework for automating evaluation of listings.

## Usage

### Development
#### Setup
`uv add --editable --dev jobfinder`
#### Running
` streamlit run main.py ` 