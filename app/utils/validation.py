import re

def validate_url(url: str):
    pattern = re.compile (
        r'^(?:https?:\/\/)?(?:www.)?(youtube|linkedin|x|facebook}instagram|tiktok|youtu\.be).*$',
        re.IGNORECASE
    )

    if not bool(pattern.match(url)):
        raise ValueError(f"Url '{url[0:15]}...' is not supported.")

def validate_platform(platform: str):
    supported_platforms = ["youtube", "facebook", "instagram", "x", "twitter", "linkedin", "reddit"]
    if platform.lower() not in supported_platforms:
        raise ValueError(f"Platform '{platform}' is not supported.")