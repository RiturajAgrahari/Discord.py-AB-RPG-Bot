import discord
import random
from database import select_query, update_query
from embed import letter_event_embed

KOEN_EMOJI = '<:Koen:1211589943147892756>'

async def letter_event(uid, interaction):
    Choices = 'ABCDEFGHIJKLMNOPQRSTUVWXY#'

    koen = await select_query(column='koens', table='inventory', condition_column='uid', condition_value=int(uid))

    if koen[0][0] >= 100:
        await update_query(table='inventory', key_value={'koens': 100}, condition_column='uid', condition_value=int(uid), operation='subtraction')
        randomletter = random.choice(Choices)
        # print(randomletter)
        items = await select_query(column='storage', table='events', condition_column='uid', condition_value=int(uid))
        embed, refund, reword, win = await letter_event_embed(interaction, randomletter, items[0][0])
        # print(refund, reword, win)
        if refund:
            await update_query(table='inventory', key_value={'koens': refund}, condition_column='uid', condition_value=int(uid), operation='addition')

        if reword:
            if items[0][0] is None:
                await update_query(table='events', key_value={'storage': f'{reword},'}, condition_column='uid', condition_value=int(uid))
            else:
                letters = items[0][0]
                letters += f'{reword},'
                await update_query(table='events', key_value={'storage': letters}, condition_column='uid',
                                   condition_value=int(uid))


        await interaction.response.send_message(embed=embed)

        if win is True:
            await update_query(table='inventory', key_value={'koens': 10000}, condition_column='uid', condition_value=int(uid), operation='addition')
            await update_query(table='events', key_value={'letter_event': 'won'}, condition_column='uid', condition_value=int(uid))
            await update_query(table='events', key_value={'storage': None}, condition_column='uid',
                               condition_value=int(uid))
            await update_query(table='inventory', key_value={'achieveent': '🏅'}, condition_column='uid', condition_value=int(uid))
        else:
            pass
    else:
        await interaction.response.send_message(f'You need 100 {KOEN_EMOJI} to open a letter box, use'
                                                f' </daily:1210461850144346152> to get discord koens',
                                                ephemeral=True)