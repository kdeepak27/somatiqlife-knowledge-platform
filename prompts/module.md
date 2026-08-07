Create a complete SOMatiq knowledge module using the structured output schema.

MODULE
ID: {module_id}
TITLE: {title}
SUBTITLE: {subtitle}
DOMAIN: {domain}
CATEGORY: {category}

Requirements:
- At least 12 distinct natural-language customer questions.
- Retrieval summary of 250-400 words covering definition, mechanisms, practical
  relevance, major synonyms, limitations, and safety.
- At least 10 substantial main sections.
- Every main section must stand alone for RAG retrieval; never rely on
  "as described above", "as discussed earlier", or neighboring sections.
- Cover definitions, mechanisms, physiology, evidence, practical application,
  limitations, misconceptions, and safety where relevant.
- At least 8 key takeaways.
- Useful glossary with both scientific and common-language terminology.
- 3-5 illustration specifications.
- Related modules using stable SOMatiq IDs when known.
- References must never be invented. Mark generated references as unverified.
- Use review_status exactly:
  AI draft - scientific, clinical, and editorial review required
