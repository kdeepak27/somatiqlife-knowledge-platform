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
- The retrieval summary must contain at least 220 words and no more than 350 words. It must explain the definition, major mechanisms, practical relevance, limitations, and important related concepts.
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
