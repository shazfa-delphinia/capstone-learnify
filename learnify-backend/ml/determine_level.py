def determine_json_level_from_percent(percent_correct):
    if percent_correct is None:
        return "Menengah"
    if percent_correct <= 20:
        return "Dasar"
    elif percent_correct <= 40:
        return "Pemula"
    elif percent_correct <= 60:
        return "Menengah"
    elif percent_correct <= 80:
        return "Mahir"
    else:
        return "Profesional"
