import os
import requests
from datetime import datetime, timedelta

# GitHub API setup
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
USERNAME = 'Centinol-alt'
headers = {'Authorization': f'token {GITHUB_TOKEN}'}

# Fetch commits from the last 24 hours
since = (datetime.utcnow() - timedelta(hours=24)).isoformat() + 'Z'
url = f'https://api.github.com/users/{USERNAME}/events'
response = requests.get(url, headers=headers)
events = response.json()

# Count commits (you can adjust this logic for other metrics like issues)
commit_count = sum(1 for event in events if event['type'] == 'PushEvent')

# Calculate chaos level (0-100%)
# Example: 0 commits = 0%, 10+ commits = 100%
chaos_level = min(commit_count * 10, 100)  # Adjust multiplier as needed
chaos_width = (chaos_level / 100) * 180  # Scale for SVG bar (180px max)

# Determine chaos bar color based on level
if chaos_level <= 20:
    bar_color = "#55ff55"  # Green for low chaos
    chaos_text = "All systems green"
    tooltip_text = "Everything's under control... for now."
elif chaos_level <= 60:
    bar_color = "#ffff55"  # Yellow for medium chaos
    chaos_text = "Things are heating up"
    tooltip_text = "I might've forgotten a semicolon somewhere."
else:
    bar_color = "#ff5555"  # Red for high chaos
    # More chaotic messages for high chaos
    if chaos_level <= 80:
        chaos_text = "Send coffee!"
        tooltip_text = "I broke prod again!"
    else:
        chaos_text = "Regex betrayed me!"
        tooltip_text = "I trusted regex, and now I'm paying for it."

# Update SVG file with color, tooltip, custom message, and percentage below the bar
svg_content = f"""<svg width="200" height="60" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="20" width="180" height="20" fill="#444" rx="10"/>
  <rect x="10" y="20" width="{chaos_width}" height="20" fill="{bar_color}" rx="10" id="chaos-bar">
    <title>{tooltip_text}</title>
  </rect>
  <text x="100" y="15" font-size="12" fill="#fff" text-anchor="middle" id="chaos-text">Chaos: {chaos_text}</text>
  <text x="100" y="45" font-size="12" fill="#fff" text-anchor="middle" id="chaos-percentage">{int(chaos_level)}%</text>
</svg>"""

with open('chaos-meter/chaos-meter.svg', 'w') as f:
    f.write(svg_content)
