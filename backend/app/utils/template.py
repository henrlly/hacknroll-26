from jinja2 import Template


def render_prompt(raw_template: str, **args) -> str:
    template = Template(raw_template.strip())
    return template.render(args)
