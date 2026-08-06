Create a complete SOMatiq module using the structured output schema.

MODULE
ID: {module_id}
TITLE: {title}
SUBTITLE: {subtitle}
DOMAIN: {domain}
CATEGORY: {category}

Requirements:
- General adult reading level.
- At least 8 natural-language customer questions.
- Retrieval summary of approximately 200–350 words.
- At least 8 substantial main sections.
- Each section must stand alone when retrieved in a RAG application.
- Do not use phrases such as "as discussed above."
- Include practical guidance, meaningful safety limitations, misconceptions,
  clinical pearls, key takeaways, glossary terms, related modules, and 3–5
  illustration specifications.
- Do not invent URLs, DOIs, PubMed IDs, authors, or dates.
- Mark reference verification_status as "unverified".
- Use review_status exactly:
  AI draft - scientific, clinical, and editorial review required
