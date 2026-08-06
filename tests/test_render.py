from tests.test_schema import sample
from somatiq.render import render_json,render_metadata,render_markdown,render_jsonl,render_docx
def test_renderers(tmp_path):
    m=sample(); funcs=[(render_json,'module.json'),(render_metadata,'metadata.json'),(render_markdown,'module.md'),(render_jsonl,'rag_chunks.jsonl'),(render_docx,'module.docx')]
    for f,n in funcs: f(m,tmp_path/n); assert (tmp_path/n).stat().st_size>0
