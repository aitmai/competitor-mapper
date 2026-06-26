"""
Converts threat_level strings to CSS classes and emoji badges
used in the dashboard template.
"""

THREAT_CONFIG = {
    "HIGH": {
        "css_class": "threat-high",
        "badge": "⬛ HIGH",
        "color": "#ff4444",
        "glow": "rgba(255,68,68,0.3)",
        "priority": 3,
    },
    "MEDIUM": {
        "css_class": "threat-medium",
        "badge": "🟨 MEDIUM",
        "color": "#ffaa00",
        "glow": "rgba(255,170,0,0.3)",
        "priority": 2,
    },
    "LOW": {
        "css_class": "threat-low",
        "badge": "🟩 LOW",
        "color": "#00cc66",
        "glow": "rgba(0,204,102,0.3)",
        "priority": 1,
    },
}


def get_threat_config(threat_level: str) -> dict:
    level = str(threat_level).upper().strip()
    return THREAT_CONFIG.get(level, THREAT_CONFIG["MEDIUM"])


def sort_competitors_by_threat(competitors: list) -> list:
    """Sort competitors so HIGH threats appear first."""
    def priority(c):
        return get_threat_config(c.get("threat_level", "MEDIUM"))["priority"]

    return sorted(competitors, key=priority, reverse=True)
