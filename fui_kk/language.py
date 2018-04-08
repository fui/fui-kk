def determine_language(question):
    en_words = ["What ", "How ", "Where ", " the "]
    no_words = ["Hva ", "Hvilken ", "Hvor ", "Hvordan "]
    for word in no_words:
        if word in question:
            return "NO"
    for word in en_words:
        if word in question:
            return "EN"
    return None
