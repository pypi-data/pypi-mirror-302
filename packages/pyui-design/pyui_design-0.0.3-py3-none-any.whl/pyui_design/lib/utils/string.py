def underscore_to_camelcase(s: str) -> str:
    parts = s.split('_')
    # underscore_to_camelcase
    return parts[0].lower() + ''.join(word.capitalize() for word in parts[1:])