STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "is", "are", "was", "were",
    "in", "on", "at", "to", "for", "of", "with", "by", "as", "that",
    "this", "it", "be", "been", "have", "has", "had", "do", "does",
    "did", "will", "would", "can", "could", "should", "we", "you",
    "i", "he", "she", "they", "them", "his", "her", "their", "our"
}


def clean_text(text: str) -> str:
    text = text.lower()
    words = text.split()
    cleaned_words = [word for word in words if word not in STOPWORDS]
    return " ".join(cleaned_words)