import logging


from jinja2 import Template

logger = logging.getLogger(__name__)    

def render_jinja(template_str: str, data: dict) -> str:
    try:
        template = Template(template_str)
        return template.render(**data)
    except Exception as e:
        logger.error("Error rendering Jinja template: %s", e)
        raise e