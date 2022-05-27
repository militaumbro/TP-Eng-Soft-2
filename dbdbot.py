import discord
from discord.ext import commands
import discord
from discord.utils import get
import requests
import json
from datetime import datetime
import xml.etree.ElementTree as ET
from random import seed
from random import randint
import sqlite3
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

link_discord = "https://discord.gg/nDTVXbU"

intents = discord.Intents.default()
intents.members = True

conn = sqlite3.connect(dir_path + "/DB_dbd_Bot.db")

Cursor = conn.cursor()

#ids dos canais
assasino_id     = 445248966980927488
sobrevivente_id = 445248966980927488
geral_id        = 445248966980927488

client = commands.Bot(command_prefix='-', intents=intents, help_command=None)

server = client.get_guild(id = 302440660680704001)

roles = ("Iniciante 10 - 200","Aprendiz 200 - 500","Veterano 500 - 1000","Old School 1000 - 3000","Pretty Good Job 3000 - 5000","No Life 5000+")

""" @client.command()
async def help(ctx, args=None):
    help_embed = discord.Embed(title="Nea Bot Help!")
    command_names_list = [x.name for x in client.commands]

    # If there are no arguments, just list the commands:
    if not args:
        help_embed.add_field(
            name="List of supported commands:",
            value="\n".join([str(i+1)+". "+x.name for i,x in enumerate(client.commands)]),
            inline=False
        )

    # If the argument is a command, get the help text from that command:
    elif args in command_names_list:
        help_embed.add_field(
            name=args,
            value=client.get_command(args).help
        )

    # If someone is just trolling:
    else:
        help_embed.add_field(
            name="Nope.",
            value="Don't think I got that command, boss!"
        )
    await ctx.send(embed=help_embed)
 """

#retorna os valores nos formatos corretos de cada User Info do DBD
def get_parameter(parameter):
    if parameter == 0:
        return str(parameter)
    else:
        return str(int(parameter["value"]))

#define imagens para cada rank de Killer
def get_rank_image_killer(i):
    if i in range(0,3): return "https://i.imgur.com/gOAR70p.png"
    elif i in range(3,6): return "https://i.imgur.com/sLtMjaa.png"

    elif i in range(6,10): return "https://i.imgur.com/pc6NL6O.png"
    elif i in range(10,14): return "https://i.imgur.com/8qZCPbz.png"
    elif i in range(14,18): return "https://i.imgur.com/1hEODNS.png"
    elif i in range(18,22): return "https://i.imgur.com/Xf0WdJM.png"
    elif i in range(22,26): return "https://i.imgur.com/qd0Bgxt.png"
    elif i in range(26,30): return "https://i.imgur.com/O9cDxEE.png"

    elif i in range(30,35): return "https://i.imgur.com/63AN9zr.png"
    elif i in range(35,40): return "https://i.imgur.com/Bl74O5o.png"
    elif i in range(40,45): return "https://i.imgur.com/sX2GkML.png"
    elif i in range(45,50): return "https://i.imgur.com/cWTV0YM.png"
    elif i in range(50,55): return "https://i.imgur.com/IRrs3Ob.png"
    elif i in range(55,60): return "https://i.imgur.com/lIQAuXF.png"
    elif i in range(60,65): return "https://i.imgur.com/5mLs5sJ.png"
    elif i in range(65,70): return "https://i.imgur.com/N1l7Vk0.png"
    elif i in range(70,75): return "https://i.imgur.com/yvhexQ5.png"
    elif i in range(75,80): return "https://i.imgur.com/FNTfn0c.png"
    elif i in range(80,85): return "https://i.imgur.com/NRDikmz.png"

    elif i == 85: return "https://i.imgur.com/SrYQhJb.png"
    return "https://i.imgur.com/gOAR70p.png"

#define imagens para cada rank de survivor
def get_rank_image_survivor(i):
    if i in range(0,3): return "https://i.imgur.com/3vH3UTW.png"
    elif i in range(3,6): return "https://i.imgur.com/1MalZLY.png"

    elif i in range(6,10): return "https://i.imgur.com/ZrrmPsT.png"
    elif i in range(10,14): return "https://i.imgur.com/AyA1phE.png"
    elif i in range(14,18): return "https://i.imgur.com/rY9tKbw.png"
    elif i in range(18,22): return "https://i.imgur.com/wPQ5eGs.png"
    elif i in range(22,26): return "https://i.imgur.com/5kmyXe5.png"
    elif i in range(26,30): return "https://i.imgur.com/xUFPcF6.png"

    elif i in range(30,35): return "https://i.imgur.com/WCAdwuU.png"
    elif i in range(35,40): return "https://i.imgur.com/YqgHqFg.png"
    elif i in range(40,45): return "https://i.imgur.com/47lgGVt.png"
    elif i in range(45,50): return "https://i.imgur.com/UBwa4Ga.png"
    elif i in range(50,55): return "https://i.imgur.com/PfGO7vO.png"
    elif i in range(55,60): return "https://i.imgur.com/2QGWh0J.png"
    elif i in range(60,65): return "https://i.imgur.com/st3nsG1.png"
    elif i in range(65,70): return "https://i.imgur.com/JfGvDer.png"
    elif i in range(70,75): return "https://i.imgur.com/aQo9pSU.png"
    elif i in range(75,80): return "https://i.imgur.com/rqoaqWq.png"
    elif i in range(80,85): return "https://i.imgur.com/2jV9Soo.png"

    elif i == 85: return "https://i.imgur.com/hsCEyni.png"
    return "https://i.imgur.com/3vH3UTW.png"


@client.command(name='assassino', pass_context = True, description="Mostra stats de assassino")
async def killer(context, arg = None):
    assassino = client.get_channel(assasino_id)
    if context.message.channel.id == assasino_id:
        r_int = randint(0,9999)
        discordid = context.message.author.id
        steamid = 0
        steam_name = ""

        if arg == None:
            if id_exists(discordid) == False:
                await context.message.channel.send(context.message.author.mention +", você não está registrado no sistema, para se registrar utilize o comando -registro `(link para seu perfil steam)`")
            steam_name = getSteamName(discordid)
            steamid = getSteamID("user", discordid)
        else:
            #checa se é um perfil valido
            if await valid_steam_profile(arg,context,r_int) == False:
                return

            #pega steam name do maluco
            response = requests.get(str(arg) + "?xml="+str(r_int), headers={'Cache-Control': 'no-cache'})
            root = ET.fromstring(response.text)
            steam_name = root.find('steamID').text 
            for element in root.iter():
                if element.tag == "steamID64":
                    steamid = element.text.strip()
                    break

        response = requests.get("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v1/?appid=381210&key=9CB3CFA671EB23758C136E8B5BC6BEA2&steamid=" + str(steamid))
        #response = requests.get("https://dbd.onteh.net.au/api/playerstats?steamid="+arg)
        #data = json.loads(response.content)
        #print(json.dumps(data, indent = 4, sort_keys=True))

        if response.status_code == 200:
            data = json.loads(response.content)
            #print(json.dumps(data["playerstats"]["stats"], indent = 4, sort_keys=True))
            #print(response.content)
            try:
                sacrificed = data["playerstats"]["stats"].get("DBD_SacrificedCampers", 0)
                survivorsgrabbedrepairinggen = data["playerstats"]["stats"].get("DBD_Chapter12_Slasher_Stat1", 0)
                hatchesclosed = data["playerstats"]["stats"].get("DBD_Chapter13_Slasher_Stat1", 0)
                chainsawhits = data["playerstats"]["stats"].get("DBD_ChainsawHit", 0)
                blinkattacks = data["playerstats"]["stats"].get("DBD_SlasherChainAttack", 0)
                hatchetsthrown = data["playerstats"]["stats"].get("DBD_DLC5_Slasher_Stat1", 0)
                evilwithintierup = data["playerstats"]["stats"].get("DBD_SlasherTierIncrement", 0)
                shocked = data["playerstats"]["stats"].get("DBD_DLC4_Slasher_Stat1", 0)
                spirit = data["playerstats"]["stats"].get("DBD_Chapter9_Slasher_Stat2", 0)
                #uncloakattacks = data["playerstats"]["stats"].get("DBD_UncloakAttack", 0)
                oniskill = data["playerstats"]["stats"].get("DBD_Chapter14_Slasher_Stat2",0)
                #dreamstate = data["playerstats"]["stats"].get("DBD_DLC7_Slasher_Stat1", 0) #"Sobreviventes Dormindo com Freddy Krueguer"
                cagesofatonement = data["playerstats"]["stats"].get("DBD_Chapter16_Slasher_Stat1", 0)
                beartrapcatches = data["playerstats"]["stats"].get("DBD_TrapPickup", 0)
                killer_rank = data["playerstats"]["stats"].get("DBD_KillerSkulls", 0)
            except:
                await context.message.channel.send(context.message.author.mention + ", erro na coleta dos dados (tem certeza que este perfil ja jogou DBD? 🤔)")

            embed=discord.Embed(title="<:Clown:799865511117979658> Assassino Stats | Dead by Daylight - Brasil", description="Estatísticas de Assassino de **"+steam_name+"** no Dead by Daylight.", color=0xff1a1a)
            embed.set_thumbnail(url=get_rank_image_killer(int(get_parameter(killer_rank))))
            embed.add_field(name="<:SobreviventesSacrificados:799873355762499584> Sobreviventes Sacrificados", value="`"+get_parameter(sacrificed)+"`", inline=True)
            embed.add_field(name="<:Sobreviventesagarradosnogerador:799870543095791647> Sobreviventes Agarrados no Gerador", value="`"+get_parameter(survivorsgrabbedrepairinggen)+"`", inline=True)
            embed.add_field(name="<:Escotilha:799870542647656448> Escotilhas Fechadas", value="`"+get_parameter(hatchesclosed)+"`", inline=True)
            embed.add_field(name="<:Motoserra:799870543880650772> Acertos com a Motosserra (Billy)", value="`"+get_parameter(chainsawhits)+"`", inline=True)
            embed.add_field(name="<:BlinkNurse:799870543821930507> Acertos de Blink com a Nurse", value="`"+get_parameter(blinkattacks)+"`", inline=True)
            embed.add_field(name="<:ChoqueDoctor:799870544182902846> Acertos de Choque com Doctor", value="`"+get_parameter(shocked)+"`", inline=True)
            embed.add_field(name="<:Armadilha:799870542098333717> Capturas com Armadilhas de Urso", value="`"+get_parameter(beartrapcatches)+"`", inline=True)
            embed.add_field(name="<:BloodFury:802258242394259476> Uso da habilidade do Oni (Blood Fury)", value="`"+get_parameter(oniskill)+"`", inline=True)
            embed.add_field(name="<:MachadoHuntress:799870542743732226> Machados Arremessados com a Huntress", value="`"+get_parameter(hatchetsthrown)+"`", inline=True)
            embed.add_field(name="<:CagePyramid:799870543683780619> Sobreviventes em Cage com Pyramid Head", value="`"+get_parameter(cagesofatonement)+"`", inline=True)
            embed.add_field(name="<:T3MichaelMyers:799870543967944724> Aumentou o nível da Maldade Encarnada do Vulto", value="`"+get_parameter(evilwithintierup)+"`", inline=True)
            embed.add_field(name="<:AfterHaunting:802260069894979594> Sobreviventes derrubados após a habilidade da Spirit (After Haunting)", value="`"+get_parameter(spirit)+"`", inline=True)
            await context.message.channel.send(embed=embed)
        elif response.status_code == 500:
            await context.message.channel.send(context.message.author.mention + ", este perfil na steam está privado. Caso tenha mudado seu perfil para público espere no mínimo 5 minutos e tente de novamente.")
    else:
        await context.message.delete()
        await context.message.channel.send(context.message.author.mention +", utilize este comando `-assassino` apenas no chat " + assassino.mention)

@client.command(name='sobrevivente', pass_context = True, description = "Mostra stats de Sobrevivente")
async def survivor(context, arg = None):
    sobrevivente = client.get_channel(sobrevivente_id)
    if context.message.channel.id == sobrevivente_id:
        r_int = randint(0,9999)
        discordid = context.message.author.id
        steamid = 0
        steam_name = ""

        if arg == None:
            if id_exists(discordid) == False:
                await context.message.channel.send(context.message.author.mention +", você não está registrado no sistema, para se registrar utilize o comando -registro `(link para seu perfil steam)`")
            steam_name = getSteamName(discordid)
            steamid = getSteamID("user", discordid)
        else:
            #checa se é um perfil valido
            if await valid_steam_profile(arg,context,r_int) == False:
                return

            #pega steam name do maluco
            response = requests.get(str(arg) + "?xml="+str(r_int), headers={'Cache-Control': 'no-cache'})
            root = ET.fromstring(response.text)
            steam_name = root.find('steamID').text 
            for element in root.iter():
                if element.tag == "steamID64":
                    steamid = element.text.strip()
                    break

        response = requests.get("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v1/?appid=381210&key=9CB3CFA671EB23758C136E8B5BC6BEA2&steamid=" + str(steamid))
        #steam_name = getSteamName(discordid)
        #response = requests.get("https://dbd.onteh.net.au/api/playerstats?steamid="+arg)
        if response.status_code == 200:
            data = json.loads(response.content)
            try:
                gensrepaired = data["playerstats"]["stats"].get("DBD_GeneratorPct_float", 0)
                survivorshealed = data["playerstats"]["stats"].get("DBD_HealPct_float", 0)
                escaped = data["playerstats"]["stats"].get("DBD_Escape", 0)
                chestssearched = data["playerstats"]["stats"].get("DBD_DLC7_Camper_Stat1", 0)
                itemsdepleted = data["playerstats"]["stats"].get("DBD_Chapter17_Camper_Stat1", 0)
                skillchecks = data["playerstats"]["stats"].get("DBD_SkillCheckSuccess", 0)
                unhookedself = data["playerstats"]["stats"].get("DBD_Chapter9_Camper_Stat1", 0)
                escaped_shoulder = data["playerstats"]["stats"].get("DBD_Chapter12_Camper_Stat1", 0)
                exitgatesopened = data["playerstats"]["stats"].get("DBD_DLC7_Camper_Stat2", 0)
                hookssabotaged = data["playerstats"]["stats"].get("DBD_Chapter10_Camper_Stat1", 0)
                hextotemscleansed = data["playerstats"]["stats"].get("DBD_DLC3_Camper_Stat1", 0)
                saved = data["playerstats"]["stats"].get("DBD_UnhookOrHeal", 0)
                survivor_rank = data["playerstats"]["stats"].get("DBD_CamperSkulls", 0)
            except:
                await context.message.channel.send(context.message.author.mention +", erro na coleta dos dados (tem certeza que este perfil ja jogou DBD? 🤔)")

            embed=discord.Embed(title="<:Dwight:799865511055458325> Sobrevivente Stats | Dead by Daylight - Brasil", description="Estatísticas de Sobrevivente de **"+steam_name+"** no Dead by Daylight.", color=0xfff71a)
            embed.set_thumbnail(url=get_rank_image_killer(int(get_parameter(survivor_rank))))
            embed.add_field(name="<:Gerador:799860276811137065> Geradores Reparados", value="`"+get_parameter(gensrepaired)+"`", inline=True)
            embed.add_field(name="<:Cura:799860276320010242> Sobreviventes Curados", value="`"+get_parameter(survivorshealed)+"`", inline=True)
            embed.add_field(name="<:Fugas:799860276509802538> Total de Fugas", value="`"+get_parameter(escaped)+"`", inline=True)
            embed.add_field(name="<:Bau:799860276966719499> Baús abertos", value="`"+get_parameter(chestssearched)+"`", inline=True)
            embed.add_field(name="<:ItensGastos:799863642560004146> Itens Gastos", value="`"+get_parameter(itemsdepleted)+"`", inline=True)
            embed.add_field(name="<:SkillCheck:799860276681375764> Testes de Perícia", value="`"+get_parameter(skillchecks)+"`", inline=True)
            embed.add_field(name="<:Gancho:799860276668661770> Fugas do Gancho", value="`"+get_parameter(unhookedself)+"`", inline=True)
            embed.add_field(name="<:EscapoudoOmbrodoAssassino:799860276349894668> Escapou do Ombro do Assassino", value="`"+get_parameter(escaped_shoulder)+"`", inline=True)
            embed.add_field(name="<:PortesdeSadaAbertos:799869589663514665> Portões de Saída Abertos", value="`"+get_parameter(exitgatesopened)+"`", inline=True)
            embed.add_field(name="<:GanchosSabotados:799863663539650570> Ganchos Sabotados", value="`"+get_parameter(hookssabotaged)+"`", inline=True)
            embed.add_field(name="<:Totens:799860276727513119> Totens Enfeitiçados Purificados", value="`"+get_parameter(hextotemscleansed)+"`", inline=True)
            embed.add_field(name="<:SobreviventesSalvos:799864463741550602> Sobreviventes Salvos (Caídos no Chão/Gancho)", value="`"+get_parameter(saved)+"`", inline=True)
            
            await context.message.channel.send(embed=embed)
        elif response.status_code == 500:
            await context.message.channel.send(context.message.author.mention +", este perfil na steam está privado. Caso tenha mudado seu perfil para público espere no mínimo 5 minutos e tente de novamente.")
    else:
        await context.message.delete()
        await context.message.channel.send(context.message.author.mention +", utilize este comando `-sobrevivente` apenas no chat " + sobrevivente.mention)

@client.command(name='geral', pass_context = True)
async def geral(context, arg = None):
    geral = client.get_channel(geral_id)
    if context.message.channel.id == geral_id:
        r_int = randint(0,9999)
        discordid = context.message.author.id
        steamid = 0
        avatar = ""
        link = ""
        steam_name = ""
        tempo = 0

        if arg == None:
            try:
                steamid = getSteamID("user",discordid)
                avatar = get_avatar(discordid)
                link = getLink("user",discordid)
                steam_name = getSteamName(discordid)
            except:
                await context.message.channel.send(context.message.author.mention +", você não está registrado no sistema, para se registrar utilize o comando -registro `link para seu perfil steam`")

        else: 
            link = arg
            if await valid_steam_profile(link,context,r_int) == False: 
                return
            
            response = requests.get(str(arg) + "?xml="+str(r_int), headers={'Cache-Control': 'no-cache'})
            root = ET.fromstring(response.text)
            steam_name = root.find('steamID').text 
            for element in root.iter():
                if element.tag == "steamID64":
                    steamid = element.text.strip()
                    break
            for element in root.iter():
                if element.tag == "avatarFull":
                    avatar = element.text.strip()
                    break   
        xml = "/games/?xml="
        response = requests.get(str(link) + xml +str(r_int), headers={'Cache-Control': 'no-cache'})
        root2 = ET.fromstring(response.text)
        try:
            for games in root2.findall('games'):
                for game in games.findall('game'):
                    if(game.find('appID').text.find('381210') > -1):
                        #encontrei dbd
                        tempo = game.find('hoursOnRecord').text.replace(',','.')
                        
        except:
            tempo = 0
            await context.message.channel.send(context.message.author.mention +", as horas deste perfil da Steam estão privadas.")

        response = requests.get("http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v1/?appid=381210&key=9CB3CFA671EB23758C136E8B5BC6BEA2&steamid=" + str(steamid))
        if response.status_code == 200:
            data = json.loads(response.content)
            #print(json.dumps(data, indent = 4, sort_keys=True))
            try:
                perfect_games_killer = data["playerstats"]["stats"].get("DBD_SlasherMaxScoreByCategory", 0)
                if(perfect_games_killer != 0):
                    perfect_games_killer = int(perfect_games_killer['value'])
                    perfect_games_killer = str('{0:,}'.format(perfect_games_killer)).replace(',','.')
            except:
                await context.message.channel.send("Erro na coleta dos dados (tem certeza que este perfil ja jogou DBD? 🤔)")
            
            perfect_games_survivor = data["playerstats"]["stats"].get("DBD_CamperMaxScoreByCategory", 0)
            if(perfect_games_survivor != 0):
                perfect_games_survivor = int(perfect_games_survivor['value'])
                perfect_games_survivor = str('{0:,}'.format(perfect_games_survivor)).replace(',','.')

            bloodpoints =  data["playerstats"]["stats"].get("DBD_BloodwebPoints", 0)
            if(bloodpoints != 0):
                bloodpoints = int(bloodpoints['value'])
                bloodpoints = str('{0:,}'.format(bloodpoints)).replace(',','.')

            embed=discord.Embed(title="<:Feng:799865554512511027> Stats Geral | Dead by Daylight - Brasil", description="Estatísticas Gerais de **"+ str(steam_name) + "** no Dead by Daylight.", color=0x25FC91)
            embed.add_field(name="<:Bloodpoint:799825470102700102>  Pontos de Sangue", value="`"+str(bloodpoints)+"`", inline=True)
            embed.add_field(name="<:Tempodejogo:799865871921184768> Tempo de Jogo", value="`"+str(tempo)+"h`", inline=False)
            embed.add_field(name="<:PartidasperfeitadeAssassinos:799867195148075058> Jogos Perfeitos de Assassino", value="`"+str(perfect_games_killer)+"`", inline=False)
            embed.add_field(name="<:PartidasperfeitadeSobreviventes:799865871182069811> Jogos Perfeitos de Sobrevivente", value="`"+str(perfect_games_survivor)+"`", inline=False)
            embed.set_thumbnail(url = avatar)
            await context.message.channel.send(embed=embed)
        elif response.status_code == 500:
            await context.message.channel.send(context.message.author.mention +", este perfil na steam está privado. Caso tenha mudado seu perfil para público espere no mínimo 5 minutos e tente de novamente.")
    else:
        await context.message.delete()
        await context.message.channel.send(context.message.author.mention +", utilize este comando `-geral` apenas no chat " + geral.mention)
    
def getUserDiscordID(context):
    return context.message.author.id


async def valid_steam_profile(link, context, rInt):
    if link.find("steamcommunity.com") == -1:
        await context.message.channel.send(context.message.author.mention + ", por favor envie um url de perfil da steam Válido.")
        return False
    try:
        res = requests.get(link+"?xml=" + str(rInt))
    except:
        await context.message.channel.send(context.message.author.mention + ", por favor envie um url de perfil da steam Válido.")
        return False
    if res.text.find("The specified profile could not be found") > -1 | res.status_code != 200:
        #perfil invalido
        await context.message.channel.send(context.message.author.mention + ", não foi possível encontrar o seu perfil da steam.")
        return False
    return True

@client.command(name='registro', pass_context = True)
async def registro(context, args = None):
    if args == None:
        await context.message.channel.send(context.message.author.mention + ", também preciso do link do seu perfil steam! Utilize o comando desta forma:\n-registro `(link do seu perfil steam)`")
        return
    if args[-1] != "/":
        args = args + "/"
    #codigo de verificação de identidade para a steam
    verifying_code = randint(100000, 999999)
    rInt = randint(0, 9999)
    discordID = getUserDiscordID(context)
    Cursor.execute("SELECT discordid FROM user WHERE discordid = ?", (discordID,))
    result = Cursor.fetchone()
    #se ja esta registrado negue o pedido e peça o desvinculo
    if result is not None:
        await context.message.channel.send(context.message.author.mention + ", você já está registrado em nosso sistema.")
        return
    #verifica se é um perfil da steam
    if await valid_steam_profile(args, context, rInt) == False:
        return
    #se perfil steam é valido continue
    pos = args.find("/id/") + 4
    #SE id nao foi encontrado entao é um perfil com steamid64 nao personalizado
    if(pos == 3):
        pos = args.find("/profiles/") + 10
        #tem um link da comunidade steam mas não é um perfil
        if pos == 9:
            await context.message.channel.send(context.message.author.mention + ", por favor envie um url de perfil da steam Válido.")
            return
        steamID = args[pos:-1]
    #se é um perfil com link personalizado
    else:
        #utiliza api da steam para pegar o id apartir do steam_name no link personalizado
        steam_name = args[pos:-1]
        response = requests.get("http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key=9CB3CFA671EB23758C136E8B5BC6BEA2&vanityurl="+ steam_name)
        data = json.loads(response.content)
        steamID = data["response"]["steamid"]
        #se perfil com tal link personalizado nao existe
        if data["response"]["success"] != 1:
            await context.message.channel.send(context.message.author.mention + ", por favor envie um url de perfil da steam Válido.")
            return
    response = requests.get(str(args) + "?xml="+str(rInt), headers={'Cache-Control': 'no-cache'})
    root = ET.fromstring(response.text)
    steam_name = root.find('steamID').text
    link = args
    #print("steamID: " + steamID + "\nDiscordID: " + str(discordID) + "\nCodigo de verificação: " + str(verifying_code))
    

    try:
        db_entry_values = (steamID, discordID, verifying_code, link)
        print(db_entry_values)
        Cursor.execute("REPLACE INTO registro VALUES (?,?,?,?)", db_entry_values)
        conn.commit()
    except :
        await context.message.author.send("Ocorreu um erro inesperado na minha conexão com o Sistema de Registro, por favor tente novamente mais tarde.")
        raise 

    embed_imagem1=discord.Embed(title="", description="", color=0xF4F4F4)
    embed_imagem1.set_image(url = "https://i.imgur.com/I26mCuz.jpg")

    embed_imagem2=discord.Embed(title="", description="", color=0xF4F4F4)
    embed_imagem2.set_image(url = "https://i.imgur.com/rZJSaHg.png")

    embed_imagem3=discord.Embed(title="", description="", color=0xF4F4F4)
    embed_imagem3.set_image(url = "https://i.imgur.com/BehbD0c.png")


    embed_inbox=discord.Embed(title="<a:Rainbow:800490718682153050> Registro", description="", color=0xF4F4F4)
    embed_inbox.add_field(name="**<:Register:800499677069312011> Ajuda**", value = "Tentando se registrar como `"+ steam_name +"`, **"+ context.message.author.display_name +"**? Deixa eu te ajudar então.\nPara conseguir acessar suas estatísticas e registrar sua conta no sistema, preciso que coloque o código de verificação no \"resumo\" da sua conta steam, utilize o código de verificação ao lado e execute o comando `-verificar`")
    embed_inbox.add_field(name = "<:Steam:800509342406803486> Código", value = "Este é o seu código de verificação: `"+ str(verifying_code) +"`")

    try:
        await context.message.author.send(embed = embed_imagem1)
    except:
        await context.message.channel.send(context.message.author.mention +", não consigo enviar mensagens no seu privado!")


    await context.message.author.send(embed = embed_imagem2)
    await context.message.author.send(embed = embed_imagem3)
    await context.message.author.send(embed = embed_inbox)
    await context.message.channel.send(context.message.author.mention +", todos os dados para efetuar o seu registro foram enviados para o seu privado.")
    

def getSteamID(table, discordid):
    Cursor.execute("SELECT steamid FROM "+ str(table) +" WHERE discordid = ?",(discordid,))
    return Cursor.fetchone()[0]

def getSteamName(discordid):
    Cursor.execute("SELECT steam_name FROM user WHERE discordid = ?",(discordid,))
    return Cursor.fetchone()[0]

def getCode(table, discordid):
    Cursor.execute("SELECT codigo FROM "+ str(table) +" WHERE discordid = ?",(discordid,))
    return Cursor.fetchone()[0]

def getLink(table, discordid):
    Cursor.execute("SELECT link FROM "+ str(table) +" WHERE discordid = ?",(discordid,))
    return Cursor.fetchone()[0]

def id_exists(discordid):
    Cursor.execute("SELECT discordid FROM user WHERE discordid = ?",(discordid,))
    if Cursor.fetchone() == None:
        return False
    else:
        return True
def get_avatar(discordid):
    Cursor.execute("SELECT avatar FROM user WHERE discordid = ?",(discordid,))
    return Cursor.fetchone()[0]

async def give_role(role_name, server, context ):
    role = discord.utils.get(server.roles, name = role_name)
    member = server.get_member(context.message.author.id)
    if member:
        await member.add_roles(role)
        await context.message.channel.send(context.message.author.mention + ", seu cargo foi atualizado com sucesso.")
        return True
    else:
        await context.message.channel.send(context.message.author.mention + ", você não é um membro da comunidade **Dead by Daylight Brasil**\n Link do convite <:RGB:800490716895510528> https://discord.gg/nDTVXbU")
        return False
async def remove_role(roles, server, context ):
    roles = tuple(get(server.roles, name=n) for n in roles)
    member = server.get_member(context.message.author.id)
    if member:
        await member.remove_roles(*roles)
    #else:
    #    await context.message.channel.send(context.message.author.mention + ", você não é um membro da comunidade **Dead by Daylight Brasil**\n Link do convite <:RGB:800490716895510528> https://discord.gg/nDTVXbU")
    return
@client.command(name='verificar', pass_context = True)
async def verify(context):
    # pega usuario registrado na tabela de dados de registro temporario, e registra ele na tabela user após a verificação
    rInt = randint(1, 9999)
    code = randint(100000, 999999)
    discordid = context.message.author.id
    steamid = 0
    link = ""
    try:
        steamid = getSteamID("registro",discordid)
        code = getCode("registro", discordid)
        link = getLink("registro", discordid)
    except:
        await context.message.channel.send(context.message.author.mention + ", registro não encontrado, por favor se registre utlizando o comando -registro `link para sua conta steam`")
        return
    tempo = 0
    #se steamid nao é nulo entao registro existe na tabela como esperado
    if steamid is not None :
        #checar se discordID ja esta vinculado a uma conta na tabela user
        Cursor.execute("SELECT discordid FROM user WHERE discordid = ?", (discordid,))
        result = Cursor.fetchone()
        #se ja esta registrado negue o pedido e peça o desvinculo
        if result is not None:
            await context.message.channel.send(context.message.author.mention + ", você já está registrado em nosso sistema.")
            return

        #se nao está registrado no user, registre
        response = requests.get(str(link) + "?xml="+str(rInt), headers={'Cache-Control': 'no-cache'})
        root = ET.fromstring(response.text)
        if root.find('summary').text.find(str(code)) > -1:
            #registrar na tabela de user
            steam_name = root.find('steamID').text
            for element in root.iter():
                if element.tag == "avatarFull":
                    avatar = element.text.strip()
                    break
            response = requests.get(str(link) + "/games/?xml="+str(rInt), headers={'Cache-Control': 'no-cache'})
            #pega tempo de jogo
            root2 = ET.fromstring(response.text)
            for games in root2.findall('games'):
                for game in games.findall('game'):
                    if(game.find('appID').text.find('381210') > -1):
                        #encontrei dbd
                        try:
                            tempo = int(game.find('hoursOnRecord').text.replace(',',''))
                        except:
                            tempo = 0
            #definição de cargos baseado nas horas de jogo
            server = client.get_guild(id = 302440660680704001)
            if tempo > 10: 
                if   10   < tempo < 200: 
                    await remove_role(roles, server, context)
                    memb = await give_role("Iniciante 10 - 200",server, context)
                    if memb == False:
                        return
                elif 200  < tempo < 500: 
                    await remove_role(roles, server, context)
                    memb = await give_role("Aprendiz 200 - 500",server, context)
                    if memb == False:
                        return
                elif 500  < tempo < 1000:
                    await remove_role(roles, server, context)
                    memb = await give_role("Veterano 500 - 1000",server, context)
                    if memb == False:
                        return
                elif 1000 < tempo < 3000:
                    await remove_role(roles, server, context)
                    memb = await give_role("Old School 1000 - 3000",server, context)
                    if memb == False:
                        return
                elif 3000 < tempo < 5000:
                    await remove_role(roles, server, context)
                    memb = await give_role("Pretty Good Job 3000 - 5000",server, context)
                    if memb == False:
                        return
                elif tempo > 5000:
                    await remove_role(roles, server, context)
                    memb = await give_role("No Life 5000+",server, context)
                    if memb == False:
                        return
            else: 
                await context.message.channel.send(context.message.author.mention + ", você não atingiu o tempo mínimo de 10 horas ou está com as horas privadas na steam, caso tenha deixado suas horas publicas, basta usar o comando -atualizarhoras")
                await remove_role(roles, server, context)
                memb = await give_role("Iniciante 10 - 200",server, context)
                if memb == False:
                    return
            db_entry = (steamid, discordid, steam_name, link, code, avatar)
            Cursor.execute("DELETE FROM registro WHERE discordid=?",(discordid,))
            Cursor.execute("INSERT INTO user VALUES (?,?,?,?,?,?)",db_entry)
            conn.commit()
            await context.message.channel.send("Registro feito com Sucesso")
            return
        else:
            await context.message.channel.send( context.message.author.mention + ", nenhum código foi encontrado em seu Resumo do seu perfil da steam, coloque o código em seu resumo e digite novamente o comando `-verificar`")
            return
    else: 
        await context.message.channel.send(context.message.author.mention +", seu registro não foi encontrado, por favor se registre utlizando o comando -registro `link para sua conta steam`")
        return

@client.command(name='atualizarhoras', pass_context = True)
async def update_play_time(context):
    rInt = randint(0,9999)

    discordid = context.message.author.id
    try:
        link = getLink("user",discordid)
    except:
        await context.message.channel.send(context.message.author.mention + ", seu registro não foi encontrado, por favor se registre utlizando o comando -registro `link para sua conta steam`")
    response = requests.get(str(link) + "/games/?xml="+str(rInt), headers={'Cache-Control': 'no-cache'})
    tempo = 0
    #pega tempo de jogo
    root2 = ET.fromstring(response.text)
    for games in root2.findall('games'):
        for game in games.findall('game'):
            if(game.find('appID').text.find('381210') > -1):
                #encontrei dbd
                try:
                    tempo = int(game.find('hoursOnRecord').text.replace(',',''))
                except:
                    tempo = 0
    server = client.get_guild(id = 302440660680704001)
    if tempo > 10: 
        if   10   < tempo < 200: 
            await remove_role(roles, server, context)
            await give_role("Iniciante 10 - 200",server, context)
        elif 200  < tempo < 500: 
            await remove_role(roles, server, context)
            await give_role("Aprendiz 200 - 500",server, context)
        elif 500  < tempo < 1000:
            await remove_role(roles, server, context)
            await give_role("Veterano 500 - 1000",server, context)
        elif 1000 < tempo < 3000:
            await remove_role(roles, server, context)
            await give_role("Old School 1000 - 3000",server, context)
        elif 3000 < tempo < 5000:
            await remove_role(roles, server, context)
            await give_role("Pretty Good Job 3000 - 5000",server, context)
        elif tempo > 5000:
            await remove_role(roles, server, context)
            await give_role("No Life 5000+",server, context)
    else: 
        await context.message.channel.send(context.message.author.mention + ", você não atingiu o tempo mínimo de 10 horas ou está com as horas privadas na steam")


@client.command(name='userinfo', pass_context = True)
async def userInfo(context):
    discordid = context.message.author.id
    if id_exists(discordid) == False:
        await context.message.channel.send(context.message.author.mention + ",seu registro não foi encontrado, por favor se registre utlizando o comando -registro `link para sua conta steam`") 
        return
    
    steamid = getSteamID("user",discordid)
    link_do_perfil = getLink("user", discordid)
    steam_name = getSteamName( discordid )
    avatar = get_avatar(discordid)
    
    embed=discord.Embed(title="<a:Rainbow:800490718682153050> Registro do Usuário | Dead by Daylight - Brasil", description="Mostrando registro do usuário: "+ context.message.author.mention + " no Legion Bot.", color=0xF4F4F4)
    embed.add_field(name="<:Discord:800509342192369674> **Discord ID**", value = discordid )
    embed.add_field(name="<:Steam:800509342406803486> **Steam ID64**", value= steamid ) 
    embed.add_field(name="<:Steam:800509342406803486> **Nome Steam**", value= steam_name ) 
    embed.add_field(name="<:Steam:800509342406803486> **Página Steam**", value = link_do_perfil ) 
    embed.set_thumbnail(url= avatar)
    await context.message.author.send(embed = embed)

@client.command(name='desvincular', pass_context = True)
async def desvincular(context):
    discordid = context.message.author.id
    if id_exists(discordid) == False:
        await context.message.channel.send(context.message.author.mention +", você não está registrado no sistema.")
        return
    Cursor.execute("DELETE FROM user WHERE discordid = ?",(discordid,))
    conn.commit()
    if id_exists(discordid) == False:
        await context.message.channel.send(context.message.author.mention +", você foi desvinculado com sucesso.")
        return

client.run('Nzk5MzU0MzIwODA5NzU0NjY0.YACWuQ.jBAquoOOSrDV6cVrvxCQGdT3SU8')