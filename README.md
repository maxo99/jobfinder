# jobfinder

A Streamlit-based job search application that scrapes and manages job listings using JobSpy, with AI-powered evaluation capabilities.

## Features

- **Job Scraping**: Automated job listing collection via JobSpy
- **Persistent Storage**: Results saved across multiple runs
- **User Scoring**: Manual evaluation and weighting of job listings
- **AI Evaluation**: Automated scoring using OpenAI chat completions
- **Modern Tooling**: Built with Streamlit, managed with uv

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd jobfinder

# Install dependencies
uv add --editable --dev jobfinder
```

## Configuration

Create a `.env` file in the root directory:

```env
OPENAI_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4  # or your preferred model
```

## Usage

### Running the Application
```bash
streamlit run main.py
```

### Features
- **Find Jobs**: Use the sidebar to pull job listings with JobSpy
- **Job Details**: Review and score individual listings
- **Manual Scoring**: Add custom pro/con entries for each listing

## Development

Built with:
- [JobSpy](https://github.com/speedyapply/JobSpy) for job scraping
- [Streamlit](https://streamlit.io/) for the web interface
- [uv](https://docs.astral.sh/uv/) for package management
- [Jinja](https://jinja.palletsprojects.com/en/stable/) for templating
- [OpenAI](https://openai.com/) for AI-powered evaluation





### Configuration
- To add additional configurations, create .env in root of repository directory.
- To enable scoring using chat completions model, add to .env:
` OPENAI_KEY = {YOUR_KEY} `
- To set OpenAI chat completions model, add to .env:
` OPENAI_MODEL = {MODEL} `

### Development
#### Setup
`uv add --editable --dev jobfinder`
#### Running
` streamlit run main.py ` 