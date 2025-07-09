JOBS_MAPPING = {
        "settings": {"number_of_shards": 1, "number_of_replicas": 0},
        "mappings": {
            "properties": {

                "id": {"type": "keyword"},
                "site": {"type": "keyword"},
                "status": {"type": "keyword"},
                "company": {"type": "keyword"},
                "title": {"type": "keyword"},
                "classifier": {"type": "keyword"},
                "summarizer": {"type": "keyword"},
                
                "is_remote": {"type": "boolean"},
                "date_scraped": {"type": "date"},
                "date_posted": {"type": "date"},
                "modified": {"type": "date"},
                
                "score": {"type": "float"},
                
                "cons": {"type": "text"},
                "pros": {"type": "text"},
                "summary": {"type": "text"},
                "job_url": {"type": "text"},
                "job_url_direct": {"type": "text"},
                "description": {"type": "text"},
                "location": {"type": "text"},

                "job_type": {"type": "text"},
                "salary_source": {"type": "text"},
                "interval": {"type": "text"},
                "min_amount": {"type": "float"},
                "max_amount": {"type": "float"},
                "currency": {"type": "text"},
                "company_industry": {"type": "text"},
                "company_url": {"type": "text"},
                "company_logo": {"type": "text"},
                "company_url_direct": {"type": "text"},
                "experience_range": {"type": "text"},
                "job_level": {"type": "text"},
                "job_function": {"type": "text"},


            }
        },
    }
