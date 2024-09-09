import discord
import requests
import os
import urllib.parse

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Google Custom Search APIの設定
API_KEY = os.getenv('GOOGLE_API_KEY')  # ReplitのSecretsに設定したAPIキー
CX = os.getenv('SEARCH_ENGINE_ID')  # ReplitのSecretsに設定した検索エンジンID

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return  # Bot自身のメッセージは無視

    query = urllib.parse.quote(message.content)  # クエリをURLエンコード
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CX}"

    # Google Custom Search APIを使って検索結果を取得
    response = requests.get(search_url)
    if response.status_code != 200:
        await message.channel.send('Google APIのリクエストに失敗しました。')
        return

    data = response.json()

    # レスポンス全体を表示せず、一部のデータだけ表示
    await message.channel.send(f"検索結果が見つかったよ🐱")

    # JSONデータの一部をデバッグ用に送信（省略されるかもしれませんが）
    await message.channel.send(f"Total Results: {data.get('searchInformation', {}).get('totalResults', '不明')}")

    if 'items' in data and len(data['items']) > 0:
        first_result = data['items'][0]['link']  # 最初の検索結果のリンクを取得
        await message.channel.send(first_result)
    else:
        await message.channel.send('え？無いよ「0」だよ🐶')

def main_function():
    client.run(os.getenv('DISCORD_TOKEN'))

if __name__ == "__main__":
    main_function()
