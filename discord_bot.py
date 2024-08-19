import json
import requests
import discord
from discord import ApplicationContext, Bot, Message, DMChannel, PartialMessageable


def run(bot: Bot):
    # 在这里添加你的 bot.run('YOUR_BOT_TOKEN')
    token = ""
    bot.run(token)


def main():
    url = "https://api.studio.thegraph.com/query/86661/token_vis/version/latest"
    body = """ 
        {
          approvals(first: 5) {
            id
            owner
            spender
            value
          }
          ownershipTransferreds(first: 5) {
            id
            previousOwner
            newOwner
            blockNumber
          }
        }
        """

    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }

    bot = discord.Bot(intents=discord.Intents.all())

    @bot.event
    async def on_ready():
        print(f"{bot.user} is ready and online!")

    @bot.slash_command(name="get_top5_approval", description="")
    async def get_top5_approval(ctx: ApplicationContext):
        response = requests.request("POST", url, headers=headers, json={"query": body})
        response_json = json.loads(response.text)
        approvals_list = response_json["data"]["approvals"]
        for approval in approvals_list:
            id1 = approval["id"]
            owner = approval["owner"]
            spender = approval["spender"]
            value = approval["value"]
            print(id1, owner, spender, value)
            await ctx.respond(f'transaction id: {id1}\n'
                              f'owner: {owner}\n'
                              f'permit\n'
                              f'spender: {spender}'
                              f'\nto spent {value}')

    run(bot)


if __name__ == '__main__':
    main()


