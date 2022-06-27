"""
A functional demo of all possible test cases. This is the format you will want to use with your testing bot.

    Run with:
        python example_tests.py TARGET_NAME TESTER_TOKEN
"""
import asyncio
import sys
from distest import TestCollector
from distest import run_dtest_bot
from discord import Embed, Member, Status
from distest import TestInterface

# The tests themselves

test_collector = TestCollector()
created_channel = None
quick_wait_time = 2
long_wait_time = 6




@test_collector()
async def test_verify_before_register(interface):
    message = await interface.send_message(
        "-verificar"
    )
    await interface.get_delayed_reply(long_wait_time, interface.assert_message_contains, "registro não encontrado, por favor se registre utlizando o comando -registro `link para sua conta steam`")



@test_collector()
async def test_assassino_unregistered(interface):
    message = await interface.send_message(
        "-assassino"
    )
    await interface.get_delayed_reply(quick_wait_time, interface.assert_message_contains, "você não está registrado no sistema, para se registrar utilize o comando -registro `(link para seu perfil steam)`")

@test_collector()
async def test_survivor_unregistered(interface):
    message = await interface.send_message(
        "-sobrevivente"
    )
    await interface.get_delayed_reply(quick_wait_time, interface.assert_message_contains, "você não está registrado no sistema, para se registrar utilize o comando -registro `(link para seu perfil steam)`")


@test_collector()
async def test_assassino_invalid_link(interface):
    message = await interface.send_message(
        "-assassino link_invalido"
    )
    await interface.get_delayed_reply(quick_wait_time, interface.assert_message_contains, "por favor envie um url de perfil da steam Válido")

@test_collector()
async def test_geral_invalid_link(interface):
    message = await interface.send_message(
        "-geral link_invalido"
    )
    await interface.get_delayed_reply(quick_wait_time, interface.assert_message_contains, "por favor envie um url de perfil da steam Válido")

@test_collector()
async def test_survivor_invalid_link(interface):
    message = await interface.send_message(
        "-sobrevivente link_invalido"
    )
    await interface.get_delayed_reply(quick_wait_time, interface.assert_message_contains, "por favor envie um url de perfil da steam Válido")

@test_collector()
async def test_assassino_steamcommunity_invalid_link(interface):
    message = await interface.send_message(
        "-assassino steamcommunity.com"
    )
    await interface.get_delayed_reply(quick_wait_time, interface.assert_message_contains, "por favor envie um url de perfil da steam Válido")

@test_collector()
async def test_geral_steamcommunity_invalid_link(interface):
    message = await interface.send_message(
        "-geral steamcommunity.com"
    )
    await interface.get_delayed_reply(quick_wait_time, interface.assert_message_contains, "por favor envie um url de perfil da steam Válido")

@test_collector()
async def test_survivor_steamcommunity_invalid_link(interface):
    message = await interface.send_message(
        "-sobrevivente steamcommunity.com"
    )
    await interface.get_delayed_reply(quick_wait_time, interface.assert_message_contains, "por favor envie um url de perfil da steam Válido")

# test real link
@test_collector()
async def test_survivor_valid_link_title(interface):
    message = await interface.send_message(
        "-sobrevivente https://steamcommunity.com/id/Sabrelobo/"
    )
    embed = Embed(title=":Dwight: Sobrevivente Stats | Dead by Daylight - Brasil")
    await interface.get_delayed_reply(long_wait_time, interface.assert_embed_equals,embed, ["title"])

@test_collector()
async def test_killer_valid_link_title(interface):
    message = await interface.send_message(
        "-assassino https://steamcommunity.com/id/Sabrelobo/"
    )
    embed = Embed(title=":Clown: Assassino Stats | Dead by Daylight - Brasil")
    await interface.get_delayed_reply(long_wait_time, interface.assert_embed_equals,embed, ["title"])


@test_collector()
async def test_survivor_valid_link_description(interface):
    message = await interface.send_message(
        "-sobrevivente https://steamcommunity.com/id/Sabrelobo/"
    )
    embed = Embed(description="Estatísticas de Sobrevivente de **Sabrelobo** no Dead by Daylight.")
    await interface.get_delayed_reply(long_wait_time, interface.assert_embed_equals,embed, ["description"])

@test_collector()
async def test_killer_valid_link_description(interface):
    message = await interface.send_message(
        "-assassino https://steamcommunity.com/id/Sabrelobo/"
    )
    embed = Embed(description="Estatísticas de Assassino de **Sabrelobo** no Dead by Daylight.")
    await interface.get_delayed_reply(long_wait_time, interface.assert_embed_equals,embed, ["description"])


@test_collector()
async def test_survivor_reply_has_rank_image(interface):
    await interface.assert_reply_has_image("-sobrevivente https://steamcommunity.com/id/Sabrelobo/")

@test_collector()
async def test_killer_reply_has_rank_image(interface):
    await interface.assert_reply_has_image("-assassino https://steamcommunity.com/id/Sabrelobo/")



# Actually run the bot

if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)