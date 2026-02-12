"""Service for checking application updates from GitHub."""

import requests
from packaging import version

from app.constants import APP_VERSION


class UpdateService:
    """Checks for new releases on GitHub."""

    GITHUB_API_URL = "https://api.github.com/repos/fikrisyahid/adzanid/releases/latest"
    DOWNLOAD_URL = "https://adzanid.fikrisyahid.my.id/"

    def __init__(self):
        self._latest_version: str | None = None

    def check_for_updates(self) -> dict[str, str | bool]:
        """Check if a newer version is available.

        Returns:
            Dictionary with: 
            - 'update_available': bool
            - 'latest_version': str (if available)
            - 'download_url': str
        """
        result = {
            'update_available': False,
            'latest_version': None,
            'download_url': self.DOWNLOAD_URL,
        }

        try:
            response = requests.get(self.GITHUB_API_URL, timeout=5)
            if response.status_code == 200:
                data = response.json()
                # GitHub tag_name usually has format like "v1.0.0" or "1.0.0"
                tag_name = data.get('tag_name', '').lstrip('v')
                
                if tag_name:
                    self._latest_version = tag_name
                    result['latest_version'] = tag_name
                    
                    # Compare versions
                    try:
                        current = version.parse(APP_VERSION)
                        latest = version.parse(tag_name)
                        result['update_available'] = latest > current
                    except Exception:
                        # If version parsing fails, don't show update
                        pass
                        
        except Exception as e:
            # Silently fail - don't interrupt app startup for update check failures
            print(f"Update check failed: {e}")

        return result
