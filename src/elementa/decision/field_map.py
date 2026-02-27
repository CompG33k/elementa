from rapidfuzz import fuzz


def best_profile_match(label_text: str, profile: dict):
    """Return the profile key, value, and match score that best aligns with the
    provided label text.

    A simple fuzzy‑matching strategy is used so that fields like "Email Address"
    will match against a profile key such as ``email``.  If the profile is
    empty the result will be ``(None, None, 0)``.
    """

    best_key = None
    best_value = None
    best_score = 0

    # iterate through the provided profile mapping and keep the highest scoring
    # key/value pair. ``token_sort_ratio`` ignores word order which works well
    # for short label strings.
    for key, value in profile.items():
        score = fuzz.token_sort_ratio(label_text, key)
        if score > best_score:
            best_score = score
            best_key = key
            best_value = value

    return best_key, best_value, best_score
