import random
import discord
from embed import inventory_embed
from database import select_query, creating_main_profile, create_inventory, update_query, create_events


async def check_profile(interaction: discord.Interaction):
    output = await select_query(column='uid', table='profile', condition_column='discord_id', condition_value=str(interaction.user.mention))
    if not output:
        print(f'creating {interaction.user.name} profile')
        await creating_main_profile(interaction)
        uid = await check_profile(interaction)
        return uid
    else:
        output_inv = await select_query(column='uid', table='inventory', condition_column='uid', condition_value=output[0][0])
        if not output_inv:
            print(f'creating {interaction.user.name} inventory')
            await create_inventory(output[0][0])
            print(f'creating {interaction.user.name} event table')
            await create_events(output[0][0])
            return output[0][0]
        else:
            return output[0][0]


async def daily_claim(uid):
    output = await select_query(column='status', table='inventory', condition_column='uid', condition_value=int(uid))
    print(output)
    if output[0][0] == 'not_claimed':
        koens = random.randint(50, 101)
        await update_query(table='inventory', key_value={'koens': koens, 'status': 'claimed'}, condition_column='uid', condition_value=int(uid), operation='addition')
        return koens
    return None


async def check_inventory(uid, interaction, avatar_url):
    koens = await select_query(column='koens', table='inventory', condition_column='uid', condition_value=int(uid))
    inventory = await select_query(column='storage', table='inventory', condition_column='uid', condition_value=int(uid))
    achievement = await select_query(column='achievement', table='inventory', condition_column='uid', condition_value=int(uid))
    storage = ''
    for i in range(len(str(inventory[0][0]).split(',')) - 1):
        storage += f":regional_indicator_{str(inventory[0][0]).split(',')[i].lower()}: "
    embed = await inventory_embed(koens[0][0], inventory[0][0], achievement[0][0], avatar_url, interaction.user.name, storage)
    await interaction.response.send_message(embed=embed)


async def reset_status():
    await update_query(table='inventory', key_value={'status': 'not_claimed'})
