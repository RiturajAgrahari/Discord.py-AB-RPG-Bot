import discord
import string

KOEN_EMOJI = '<:Koen:1211589943147892756>'
EVENT_WORD = 'ARENA BREAKOUT'

async def help_embed(name, avatar):
    embed = discord.Embed(
        title='AB RPG',
        description='Players can gain discord koens by claiming it once a day with the command /daily.'
                    ' A player can use their discord koens at events by using the command /events,'
                    ' letter event.',
        color=discord.Color.blue()
    )
    embed.add_field(
        name="</daily:1210461850144346152>",
        value="Claim your daily discord koens",
        inline=False
    )
    embed.add_field(
        name="* Reset [00:00:00 UTC+0]",
        value="After reset you will be able to get another drop from the above command",
        inline=False
    )
    embed.add_field(
        name="</inventory:1210461850144346153>",
        value="List the items you have in your inventory.",
        inline=False
    )
    embed.add_field(
        name="</events:1210461850144346154>",
        value="Use discord koens to play events and earn rewards!",
        inline=False
    )
    # embed.set_author(name=name, icon_url=avatar)
    embed.set_footer(text='Arena Breakout')
    return embed


async def daily_koen_embed(interaction, koens):
    embed = discord.Embed(
        title='',
        description=f'{interaction.user.mention}, you got {koens}{KOEN_EMOJI} today!',
        colour=discord.Color.blue()
    )
    return embed


async def letter_event_embed(interaction, letter, owned):
    refund = 0
    reword = False
    win = False

    progress = {}
    new_word = EVENT_WORD.replace(' ', '')
    for i in range(0, len(new_word)):  # {0: 'A', 1: 'R', 2: 'E', 3: 'N', 4: 'A', 5: 'B', 6: 'R', 7: 'E', 8: 'A'...}
        progress[i] = new_word[i]

    if owned is None:
        inventory = ['']
    else:
        inventory = owned.split(',')  # ['R', '']

    embed = discord.Embed(
        title="Letter Box :mailbox:",
        description=f"Collect all the letter of '{EVENT_WORD}' and get 10,000{KOEN_EMOJI}",
        colour=discord.Colour.green()
    )

    embed.set_thumbnail(
        url='https://cdn.discordapp.com/attachments/1171092440233541632/1176439824622833764/Untitled.png?ex=656edff7&is=655c6af7&hm=3e2cd8767c426187fbfc3171749ccf0158152f94a9b64f5acb3ae0a868a907c5&'
    )

    if letter in string.ascii_uppercase:
        embed.add_field(
            name=f":regional_indicator_{str(letter).lower()}:",
            value=f'you got the letter {letter}',
            inline=False
        )
    else:
        embed.add_field(
            name=f':cyclone:',
            value=f'WOW! You got a magical word! :magic_wand:\nThis magical word will randomly transform into any of'
                  f' the word that is left for your event!',
            inline=False
        )

    for i in range(0, len(inventory) - 1):
        # {0: 'O', 1: 'N', 2: 'C', 3: 'E', 4: ':regional_indicator_h:', 5: 'U', 6: 'M', 7: 'A', 8: 'N'}
        if list(progress.values()).index(inventory[i]) in progress.keys():
            progress[list(progress.values()).index(inventory[i])] = \
                f":regional_indicator_{str(progress[list(progress.values()).index(inventory[i])]).lower()}:"
        else:
            print(False)

    msg = ''

    if letter in EVENT_WORD:
        if letter in progress.values():
            progress[list(progress.values()).index(letter)] = \
                f":regional_indicator_{str(progress[list(progress.values()).index(letter)]).lower()}:"
            print(f'progress: {progress}')
            reword = letter
        else:
            msg = f'You already got this letter earlier'
            refund += 25

    elif letter == '#':
        for key, value in progress.items():
            if value in string.ascii_uppercase:
                progress[list(progress.values()).index(value)] = \
                    f":regional_indicator_{str(progress[list(progress.values()).index(value)]).lower()}:"
                print(f'progress: {progress}')

                embed.add_field(
                    name=f":regional_indicator_{str(value).lower()}:",
                    value=f':magic_wand:your magical word transformed into the letter \'{value}\'',
                    inline=False
                )
                msg = f'You got 100% refund on getting a :magic_wand:magical word!'
                refund += 100
                reword = value
                break
            else:
                pass

    else:
        msg = f'This letter is not in \'{EVENT_WORD}\''
        refund += 10

    if refund == 0:
        pass
    else:
        embed.add_field(
            name=msg,
            value=f'You got {refund} {KOEN_EMOJI} back for this letter',
            inline=False
        )

    for LETTER in EVENT_WORD:
        if LETTER in progress.values():
            break
        else:
            pass
    else:
        win = True

    if win is True:
        embed.add_field(
            name=f':confetti_ball: CONGRATULATIONS :confetti_ball:',
            value=f'You got all the words in \'{EVENT_WORD}\'',
            inline=False
        )
        embed.add_field(
            name=f'Reward',
            value=f'10,000{KOEN_EMOJI}',
            inline=False
        )
    else:
        pass

    result = ''
    for key, value in progress.items():
        result += f" {value}"

    embed.add_field(
        name=f'Your progress',
        value=f'{result}',
        inline=False
    )
    embed.set_footer(text=f'Opened by {interaction.user}')
    return embed, refund, reword, win


async def inventory_embed(koens, inventory, achievement, avatar_url, username, event):
    embed = discord.Embed(
        title=f'Discord Koens',
        description='',
        colour=None
    )
    embed.set_author(name=username, icon_url=avatar_url)
    embed.add_field(name=f'{KOEN_EMOJI} {koens}', value='', inline=False)
    if inventory is not None:
        embed.add_field(name='Inventory', value=inventory, inline=False)
    if achievement is not None:
        embed.add_field(name='Achievement', value=achievement, inline=False)
    if event is not None:
        # embed.add_field(name='Event Storage', value=event, inline=False)
        inventory = event.split(' ')
        progress = {}
        new_word = EVENT_WORD.replace(' ', '')
        for i in range(0, len(new_word)):  # {0: 'A', 1: 'R', 2: 'E', 3: 'N', 4: 'A', 5: 'B', 6: 'R', 7: 'E', 8: 'A'...}
            progress[i] = new_word[i]

        for i in range(0, len(inventory) - 1):
            if list(progress.values()).index(inventory[i][len(inventory[i])-2].upper()) in progress.keys():
                progress[list(progress.values()).index(inventory[i][len(inventory[i])-2].upper())] = \
                    f"{inventory[i]}"
            else:
                print(False)

        result = ''
        for key, value in progress.items():
            result += f" {value}"

        embed.add_field(
            name=f'Your Word Event progress',
            value=f'{result}',
            inline=False
        )
    return embed
