def is_parseable_hl7(text):
    if not text.startswith("MSH") or len(text) < 9:
        return False
    field_separator = text[3]
    return text[8] == field_separator # must repeat after the delimiters (MSH-1 == MSH-3)
