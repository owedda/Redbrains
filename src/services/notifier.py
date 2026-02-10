import requests
import logging
from src.config import settings

logger = logging.getLogger("Notifier")

def send_discord_alert(lead_obj):
    """
    Sends a formatted Embed to Discord via Webhook.
    """
    if not settings.DISCORD_WEBHOOK_URL:
        logger.warning("No Discord Webhook URL set. Skipping notification.")
        return

    # Color logic: Green for high score, Orange for medium
    color = 0x57F287 if lead_obj.lead_score > 85 else 0xE67E22

    payload = {
        "embeds": [{
            "title": f"🎯 Lead Detected: Score {lead_obj.lead_score}/100",
            "url": lead_obj.url,
            "description": lead_obj.title[:200], # Truncate long titles
            "color": color,
            "fields": [
                {
                    "name": "Why?",
                    "value": lead_obj.ai_analysis,
                    "inline": False
                },
                {
                    "name": "Draft Reply",
                    "value": f"```{lead_obj.draft_reply}```",
                    "inline": False
                }
            ],
            "footer": {
                "text": f"ID: {lead_obj.id}"
            }
        }]
    }

    try:
        response = requests.post(settings.DISCORD_WEBHOOK_URL, json=payload)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"Failed to send Discord alert: {e}")