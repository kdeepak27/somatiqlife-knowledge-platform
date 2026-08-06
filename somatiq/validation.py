from .schema import ModuleContent

REVIEW_STATUS = 'AI draft - scientific, clinical, and editorial review required'


def validate(module: ModuleContent, expected_id: str, settings: dict) -> None:
    minimums = settings['minimums']
    errors: list[str] = []

    if module.module_id != expected_id:
        errors.append(f'Expected {expected_id}, received {module.module_id}.')
    if len(module.customer_questions) < minimums['customer_questions']:
        errors.append('Too few customer questions.')
    if len(module.sections) < minimums['sections']:
        errors.append('Too few main sections.')
    if len(module.key_takeaways) < minimums['key_takeaways']:
        errors.append('Too few key takeaways.')
    if len(module.illustrations) < minimums['illustrations']:
        errors.append('Too few illustrations.')
    if len(module.retrieval_summary.split()) < minimums['retrieval_summary_words']:
        errors.append('Retrieval summary is too short.')
    if module.review_status != REVIEW_STATUS:
        errors.append('Incorrect review_status.')
    if len({x.heading.strip().lower() for x in module.sections}) != len(module.sections):
        errors.append('Duplicate headings.')
    if len({x.term.strip().lower() for x in module.glossary}) != len(module.glossary):
        errors.append('Duplicate glossary terms.')

    if errors:
        raise ValueError('Validation failed:\n- ' + '\n- '.join(errors))
