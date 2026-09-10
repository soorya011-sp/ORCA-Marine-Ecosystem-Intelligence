def detect_language(query):
    query = query.strip()

    if not query:
        return {
            "language": "Unknown",
            "language_code": "unknown",
            "confidence": 0
        }

    language_ranges = {
        "Tamil": (0x0B80, 0x0BFF, "ta"),
        "Malayalam": (0x0D00, 0x0D7F, "ml"),
        "Telugu": (0x0C00, 0x0C7F, "te"),
        "Kannada": (0x0C80, 0x0CFF, "kn"),
        "Hindi": (0x0900, 0x097F, "hi")
    }

    counts = {
        language: 0
        for language in language_ranges
    }

    for character in query:
        code = ord(character)

        for language, (start, end, _) in language_ranges.items():

            if start <= code <= end:
                counts[language] += 1
                break

    detected_language = max(
        counts,
        key=counts.get
    )

    detected_count = counts[
        detected_language
    ]

    total_script_chars = sum(
        counts.values()
    )

    if detected_count == 0:
        return {
            "language": "English",
            "language_code": "en",
            "confidence": 95
        }

    confidence = round(
        (
            detected_count
            / max(total_script_chars, 1)
        ) * 100
    )

    language_code = language_ranges[
        detected_language
    ][2]

    return {
        "language": detected_language,
        "language_code": language_code,
        "confidence": confidence
    }


def normalize_query(query):
    result = detect_language(query)

    normalized_query = (
        query
        .strip()
        .replace("\n", " ")
    )

    normalized_query = " ".join(
        normalized_query.split()
    )

    return {
        "original_query": query,
        "normalized_query": normalized_query,
        "language": result["language"],
        "language_code": result["language_code"],
        "language_confidence": result["confidence"],
        "normalization_complete": True
    }