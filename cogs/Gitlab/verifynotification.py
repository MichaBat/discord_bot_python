import disnake  # instead of discord if you're using Disnake
from disnake.ext import commands, tasks
import requests

class GitLabIssueNotifier(commands.Cog):  # Inheriting from commands.Cog
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = 1304430671716159508  # Your Discord channel ID
        self.gitlab_token = "nzSdFS8sUvU6TCaTbaKy"  # GitLab private token
        self.project_id = 47998  # GitLab project ID
        self.verified_issues = set()  # Track issues with the 'verify' tag
        self.check_issues.start()  # Start the task loop

    def fetch_issues(self):
        headers = {
            "PRIVATE-TOKEN": self.gitlab_token
        }
        url = f"https://gitlab.fdmci.hva.nl/api/v4/projects/{self.project_id}/issues"
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch issues: {response.status_code}")
            return []

    @tasks.loop(minutes=10)  # Check every 10 minutes
    async def check_issues(self):
        issues = self.fetch_issues()
        for issue in issues:
            if "verify" in [label.lower() for label in issue.get("labels", [])]:
                issue_id = issue["id"]
                if issue_id not in self.verified_issues:
                    self.verified_issues.add(issue_id)
                    await self.notify_issue(issue)

    async def notify_issue(self, issue):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send(
                f"Issue **{issue['title']}** has been tagged with 'verify'.\n"
                f"Link: {issue['web_url']}"
            )

    @check_issues.before_loop
    async def before_check_issues(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.check_issues.cancel()  # Stop the loop when the cog is unloaded

# Required setup function for loading the cog
def setup(bot):
    bot.add_cog(GitLabIssueNotifier(bot))
