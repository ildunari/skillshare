"""
Combine JSON artifacts into a Markdown/HTML research report.
"""
import os
import json
from typing import List, Dict, Any
from jinja2 import Template
from .utils import ensure_out

DEFAULT_TEMPLATE = r"""
# Research Report: {{ title }}

**Generated:** {{ generated }}

## Summary
{{ summary }}

## Findings
{% for section in sections %}
### {{ section.title }}
{{ section.body }}

{% if section.items %}
| Item | Detail |
|------|--------|
{% for k, v in section.items.items() %}
| {{ k }} | {{ v }} |
{% endfor %}
{% endif %}

{% endfor %}

## Sources
{% for s in sources %}
- {{ s.title }} — {{ s.url }} ({{ s.accessed_at }}) {% if s.note %}- {{ s.note }}{% endif %}
{% endfor %}
"""

def load_artifacts(paths: List[str]) -> Dict[str, Any]:
    data = {}
    for p in paths:
        if not os.path.exists(p):
            continue
        with open(p, "r", encoding="utf-8") as f:
            try:
                data[os.path.basename(p)] = json.load(f)
            except Exception:
                data[os.path.basename(p)] = f.read()
    return data

def generate_report(title: str, summary: str, sections: List[Dict[str, Any]], sources: List[Dict[str, str]], out_path: str) -> str:
    ensure_out(os.path.dirname(out_path) or "./out")
    tpl = Template(DEFAULT_TEMPLATE)
    html = tpl.render(title=title, summary=summary, sections=sections, sources=sources, generated=os.environ.get("RDA_GENERATED_AT", ""))
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    return out_path
