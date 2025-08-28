import discord
from discord.ext import commands
import json
import random

# JSONファイルから設定を読み込む
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# JSONファイルからお題を読み込む
with open('themes.json', 'r', encoding='utf-8') as f:
    themes = json.load(f)['themes']

# インテントを設定
intents = discord.Intents.default()
intents.message_content = True

# ボットの設定
bot = commands.Bot(command_prefix='!', intents=intents)

# グローバル変数でゲームの状態を管理
game_state = {
    "is_playing": False,
    "correct_answer": None,
    "channel_id": None
}

# 起動時のイベント
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# メッセージ受信時のイベント
@bot.event
async def on_message(message):
    # ボット自身のメッセージには反応しない
    if message.author == bot.user:
        return

    # ゲームが進行中で、かつそのチャンネルでのメッセージの場合
    if game_state["is_playing"] and message.channel.id == game_state["channel_id"]:
        # メッセージの内容が正解と一致するか判定
        if message.content == game_state["correct_answer"]:
            await message.channel.send(f'🎉おめでとう！「{game_state["correct_answer"]}」が正解です！ゲームを終了します。')
            # ゲームの状態をリセット
            game_state["is_playing"] = False
            game_state["correct_answer"] = None
            game_state["channel_id"] = None
        else:
            await message.channel.send('残念！もう一度！')

    # コマンドを処理
    await bot.process_commands(message)

# ゲーム開始コマンド
@bot.command(name='endless_game')
async def start_endless_game(ctx):
    # 既にゲームが進行中の場合は何もしない
    if game_state["is_playing"]:
        await ctx.send('⚠️既にゲームが進行中です。')
        return

    # ゲームの状態を更新
    game_state["is_playing"] = True
    game_state["correct_answer"] = random.choice(themes)
    game_state["channel_id"] = ctx.channel.id

    await ctx.send(f'🔥「一致するまで終われまテン」スタート！\nお題は、この中に隠されています！\nさあ、見つけ出せるかな？\n\n**ヒント**：お題は{len(game_state["correct_answer"])}文字だよ！')

# ボットを実行
bot.run(config['token'])
