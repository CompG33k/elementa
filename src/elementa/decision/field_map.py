from rapidfuzz import fuzz

# Canonical field keys -> common label variants seen in forms
SYNONYMS = {
    "email": ["email", "email address", "e-mail"],
    "phone": ["phone", "mobile", "cell", "telephone"],
    "first_name": ["first name", "given name"],
    "last_name": ["last name", "surname", "family name"],
    "full_name": ["full name", "name"],
    "linkedin": ["linkedin", "linkedin url", "linkedin profile"],
    "github": ["github", "github url", "github profile"],
    "website": ["website", "portfolio", "personal site", "portfolio url"],
    "city": ["city", "town"],
    "state": ["state", "province", "region"],
    "zip": ["zip", "zipcode", "postal code"],
}

DEFAULT_THRESHOLD = 75


def normalize(text: str) -> str:
    if not text:
        return ""
    t = text.lower().strip()
    # remove common noise characters
    for ch in ["*", ":", "(", ")", "[", "]", "{", "}", "\n", "\t"]:
        t = t.replace(ch, " ")
    return " ".join(t.split())


def _best_canonical_key(label_text: str):
    """
    Return (canonical_key, score) based on label text vs SYNONYMS.
    """
    label_n = normalize(label_text)
    best_key = None
    best_score = 0

    for key, variants in SYNONYMS.items():
        for v in variants:
            score = fuzz.partial_ratio(label_n, v)
            if score > best_score:
                best_score = score
                best_key = key

    return best_key, best_score


def best_profile_match(label_text: str, profile: dict, threshold: int = DEFAULT_THRESHOLD):
    """
    Return (profile_key, value, score) best aligned to label_text.

    - Uses synonym matching to map label_text -> canonical key (e.g. "Email Address" -> "email")
    - Then returns the value from profile if present.
    """
    if not label_text or not profile:
        return None, None, 0

    key, score = _best_canonical_key(label_text)
    if not key or score < threshold:
        return None, None, 0

    if key not in profile:
        return None, None, 0

    value = profile.get(key)
    if value is None or str(value).strip() == "":
        return None, None, 0

    return key, str(value), score