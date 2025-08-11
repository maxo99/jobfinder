# JobFinder Walkthrough

*updates required to descriptions*

*Page documentation needs to be annonomized with images using test data*

## Data Sequence

#### User-Guided Phase

User actions are shown in the red sequnce flow (Upon system maturity these can be automated with higher confidence).

Generative responses are shown in the green sequence flow and should be reviewed by user until large enough corpus of data is available.

Upon system maturity, (user has confidence in the generative responses being returned), the red flow can be automated and reviewing of green flow can be done at discresion.

#### Red (User Operation)

- (1) Setup initial job preferences for to configure Job Search tooling.
- (9) Use summarized jobs to efficiently provide classification of jobs using a score and pros/cons so that it may be used as context for AI tooling to classify larger quantities of job listings autonomously.

#### Green (Generative Response)

- (8) Ensure that the summarization of job descriptions is relevant to qualifications and necessary details for efficient classification without needing to provide entire job descriptions in classification context.

```mermaid
sequenceDiagram
autonumber

%%{init:
{'themeCSS':
'.messageLine0:nth-of-type(1) { stroke: red; }; .messageText:nth-of-type(1) { fill: red; font-size: 20 !important;}; .messageLine0:nth-of-type(7) { stroke: green; }; .messageText:nth-of-type(13) { fill: green; font-size: 20 !important;}; .messageLine0:nth-of-type(8) { stroke: green; }; .messageText:nth-of-type(15) { fill: green; font-size: 20 !important;};  .messageLine0:nth-of-type(9) { stroke: Red; }; .messageText:nth-of-type(17) { fill: Red; font-size: 20 !important;};   .messageLine0:nth-of-type(12) { stroke: Green; }; .messageText:nth-of-type(23) { fill: Green; font-size: 20 !important;}; .messageLine0:nth-of-type(13) { stroke: Green; }; .messageText:nth-of-type(25) { fill: Green; font-size: 20 !important;}; '}
}%%

    actor U as User
    participant JF as JobFinder
    
    Note over U,JF: Initial Job Search
    U->>JF: Submit job search criteria
    
    create participant JS as JobSearch
    JF->>JS: Execute job query
    destroy JS
    JS->>JF: Return raw job listings
    
    JF->>U: Present raw job listings
    
    U->>JF: Select raw job listings for summarization
    
    create participant LLM as AI/LLM
    Note over U,LLM: Job Summarization Phase

    JF->>LLM: Send selected raw job listings
    LLM->>JF: Return summarized jobs
    JF->>U: Display summarized jobs
    
    Note over U,JF: Manual Classification & Training
    U->>JF: Classify summarized jobs manually
    
    Note over U,LLM: AI Auto-Classification
    U->>JF: Request auto-classification for remaining jobs
    JF->>LLM: Send raw jobs + user-classified examples
    destroy LLM
    LLM->>JF: Return AI-classified jobs

    
    JF->>U: Present prioritized job results


```

## Walkthrough Pages

### Records Display

![alt text](records-display.png)

### AI Extraction of Summarization

![alt text](job-summarize.png)

### Bulk Summarization of Jobs

![alt text](bulk-summarize.png)

### Review Jinja2 Template

![alt text](scoring-template.png)

### Populated Template from selections

![alt text](populated-template.png)
