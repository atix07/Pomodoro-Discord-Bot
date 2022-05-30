import nextcord
from nextcord import FFmpegPCMAudio
from nextcord.ext import commands
from nextcord.ui import View
from dotenv import load_dotenv
from os import getenv
from threading import Event

#initialize
load_dotenv()
bot = commands.Bot(command_prefix='?')
FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
exit = Event()

#Entry
@bot.event
async def on_ready():
    print('Bot: {0.user} is working'.format(bot))

#Functions
async def Timer(min, interaction):
    while not exit.is_set():
        exit.wait(min)
        voice_state = interaction.user.voice
        if voice_state is not None:
            vc = await voice_state.channel.connect()
            vc.play(FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe", source="yay.mp3", **FFMPEG_OPTIONS))

        if not exit.is_set():
            await interaction.user.send('--------------------')
            await interaction.user.send(str(min) + ' minute timer finished!')
            await interaction.user.send('Your 10 minute break timer started. YAY!')
        else:
            await interaction.user.send('--------------------')
            await interaction.user.send(str(min) + ' minute timer finished!')
            await interaction.user.send('You stopped the timer!')
        
        if not exit.is_set():
            exit.wait(10)
            voice_state = interaction.user.voice
            if voice_state is not None:
                vc = await voice_state.channel.connect()
                vc.play(FFmpegPCMAudio(executable="C:/Program Files/ffmpeg/bin/ffmpeg.exe", source="yay.mp3", **FFMPEG_OPTIONS))
        
            if not exit.is_set():
                await interaction.user.send('--------------------')
                await interaction.user.send('10 minute break timer finished!')
                await interaction.user.send('Get back to work! Your ' + str(min) + ' minutes timer started again!')
            else:
                await interaction.user.send('--------------------')
                await interaction.user.send('10 minute break timer finished!')
                await interaction.user.send('You stopped the timer!')
        else:
            await interaction.user.send('--------------------')
            await interaction.user.send('You stopped the timer!')

        
class MinView(View):
    @nextcord.ui.select(
        placeholder='Choose your timer',
        options=[
        nextcord.SelectOption(label='20 min', emoji='⌛', description='Work for 20 minutes and 10 minutes break', value='20'),
        nextcord.SelectOption(label='30 min', emoji='⌛', description='Work for 30 minutes and 10 minutes break', value='30'),
        nextcord.SelectOption(label='40 min', emoji='⌛', description='Work for 40 minutes and 10 minutes break', value='40'),
    ])
    async def select_callback(self, select, interaction):
        select.disabled=True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"{int(select.values[0]) // 60} minute timer started!")
        await Timer(int(select.values[0]), interaction)
    
#Commands
@bot.command()
async def hello(msg):
    await msg.reply('Hello!')

@bot.command()
async def start(msg):
    exit.clear()
    view = MinView()
    await msg.reply('Let\'s setup your timer: ', view=view)

@bot.command()
async def stop(msg):
    exit.set()
    await msg.reply('Timer stopped!')

bot.run(getenv('TOKEN'))