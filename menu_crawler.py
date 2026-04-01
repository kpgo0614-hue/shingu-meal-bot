import os, requests, datetime, urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_today_meal():
    url = "https://www.shingu.ac.kr/cms/FR_CON/index.do?MENU_ID=1630"
    try:
        res = requests.get(url, verify=False, timeout=10)
        soup = BeautifulSoup(res.text, 'html.parser')
        weekday = datetime.datetime.today().weekday()
        if weekday > 4: return "오늘은 주말입니다! 😊"
        rows = soup.select('table.menu-table tbody tr')
        items = [row.find_all('td')[weekday+1].get_text(separator="\n").strip() for row in rows if len(row.find_all('td')) > weekday+1]
        return "🍱 【신구대 오늘의 식단】\n\n" + "\n\n---\n\n".join(items)
    except Exception as e: return f"❌ 오류: {e}"

if __name__ == "__main__":
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if token and chat_id:
        requests.get(f"https://api.telegram.org/bot{token}/sendMessage", params={'chat_id': chat_id, 'text': get_today_meal()})
