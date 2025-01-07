import disnake
from disnake.ext import commands, tasks
from config import DAILY_QUESTION_CHANNEL_ID
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import asyncio
import time


class DailyQuestion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.send_question_of_the_day.start()
        
    @commands.command()
    async def test_question(self, ctx):
        channel = self.bot.get_channel(DAILY_QUESTION_CHANNEL_ID)
        question = await self.fetch_question_of_the_day()
        await channel.send(question)

    async def fetch_question_of_the_day(self):
        url = "https://randomquestionmaker.com/more-tools/question-of-the-day-generator"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        try:
            response = await self.fetch_url(url, headers)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                question_element = soup.find_all('h2', class_='font-source-sans-pro animated fadeInUp visible')[0]
                if question_element:
                    question = question_element.get_text(strip=True)
                    return question
                else:
                    return "Couldn't parse the question of the day."
            else:
                print(f"Debug: Failed to fetch the page, status code {response.status_code}")
                return "Couldn't fetch the question of the day."
        
        except Exception as e:
            print(f"Debug: Exception occurred - {e}")
            return "Couldn't fetch the question of the day."

    async def fetch_url(self, url, headers, retries=3, delay=2):
        loop = asyncio.get_running_loop()

        for attempt in range(retries):
            try:
                response = await loop.run_in_executor(None, lambda: requests.get(url, headers=headers))
                return response
            except requests.exceptions.ConnectionError as e:
                if attempt < retries - 1:
                    print(f"Debug: ConnectionError occurred - {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"Debug: Failed after {retries} attempts. Exception: {e}")
                    raise e
            except Exception as e:
                print(f"Debug: An unexpected exception occurred - {e}")
                raise e

    @tasks.loop(hours=24)
    async def send_question_of_the_day(self):
        await self.bot.wait_until_ready()
        
        now = datetime.now()
        next_run = now + timedelta(days=1)
        next_run = next_run.replace(hour=10, minute=30, second=00, microsecond=0)
        sleep_time = (next_run - now).total_seconds()

        await disnake.utils.sleep_until(next_run)
       
        channel = self.bot.get_channel(DAILY_QUESTION_CHANNEL_ID)
        question = await self.fetch_question_of_the_day()
        await channel.send(question)

def setup(bot):
    bot.add_cog(DailyQuestion(bot))
