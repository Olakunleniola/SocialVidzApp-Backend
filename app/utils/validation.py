import re

def validate_url(url: str):
    pattern = re.compile (
        r'^(?:https?:\/\/)?(?:www.)?(?:web\.)?(youtube|linkedin|x|facebook|fb|instagram|tiktok|youtu\.be).*$',
        re.IGNORECASE
    )

    match = pattern.match(url)

    if not bool(match):
        raise ValueError(f"Url '{url[0:25]}...' is not supported.")
    
    return match[1]

def validate_platform(platform: str):
    supported_platforms = ["youtube", "facebook", "instagram", "x", "twitter", "linkedin", "reddit"]
    if platform.lower() not in supported_platforms:
        raise ValueError(f"Platform '{platform}' is not supported.")