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


@test_collector()
async def test_assassino_bad_link(interface):
    message = await interface.send_message(
        "-assassino link_invalido"
    )
    await interface.get_delayed_reply(5, interface.assert_message_contains, "por favor envie um url de perfil da steam Válido")




# @test_collector()
# async def test_delayed_reply(interface):
#     message = await interface.send_message(
#         "Say some stuff, but at 4 seconds, say 'yeet'"
#     )
#     await interface.get_delayed_reply(5, interface.assert_message_equals, "yeet")

# Actually run the bot

if __name__ == "__main__":
    run_dtest_bot(sys.argv, test_collector)