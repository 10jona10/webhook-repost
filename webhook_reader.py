import discord
import requests

bot_token = "[Insert Bot Token Here]"
destination_webhook_url = "[Discord Webhook URL Here]"

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")

@bot.event
async def on_message(message):
    if message.webhook_id:
        print(f"Webhook Message Content: {message.content}")

        for embed in message.embeds:
            print("Embed Content:")
            if embed.title:
                print(f"Title: {embed.title}")
            if embed.description:
                print(f"Description: {embed.description}")
            if embed.url:
                print(f"URL: {embed.url}")
            for field in embed.fields:
                print(f"Field: {field.name} - {field.value}")
            if embed.footer:
                print(f"Footer: {embed.footer.text}")

        # Post the retrieved message and modified embeds to the destination webhook
        await post_to_destination_webhook(message.content, message.embeds)

async def post_to_destination_webhook(content, embeds):
    filtered_embeds = []
    
    for embed in embeds:
        if embed.fields:
            first_3_fields = embed.fields[:3]  # Take only the first 3 fields
            filtered_embed = discord.Embed(
                title=embed.title,
                description=embed.description,
                url=embed.url,
            )
            for field in first_3_fields:
                filtered_embed.add_field(name=field.name, value=field.value, inline=field.inline)
            if embed.footer:
                filtered_embed.set_footer(text=embed.footer.text)  # Set the footer
            filtered_embeds.append(filtered_embed)

    payload = {
        "content": content,
        "embeds": [embed.to_dict() for embed in filtered_embeds]
    }
    
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(destination_webhook_url, json=payload, headers=headers)
    if response.status_code == 204:
        print("Message posted to destination webhook successfully")
    else:
        print(f"Failed to post message to destination webhook: {response.status_code}")

bot.run(bot_token)
#jona