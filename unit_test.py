# import pytest
import unittest
from dbdbot import *
import sqlite3
# print("conectando")
conn = sqlite3.connect('DB_dbd_Bot_test.db')
# print("pronto")

Cursor = conn.cursor()
# print("pronto2")
discordId = 344257231786868768
nonExistantDiscordId = 1234
steam_name = "SabreLobo"
steamid = 0000
userTable = 'user'
link = 'link.exemplo.com'
code = 123214
avatar = 'avatar.exemplo.com'
db_entry = (steamid, discordId, steam_name, link, code, avatar)
Cursor.execute("INSERT INTO user VALUES (?,?,?,?,?,?)",db_entry)
rankImageLinks()

class TestDiscordBot(unittest.TestCase):

    def test_steam_id_exist(self):
        # print("aaaaa")
        result = getSteamID(userTable, discordId,Cursor)
        self.assertEqual(result, 0000)

    def test_steam_id_non_existant(self):
        with self.assertRaises(Exception):
            result = getSteamID(userTable, nonExistantDiscordId, Cursor)

    def test_get_code(self):
        result = getCode(userTable, discordId,Cursor)
        self.assertEqual(result, 123214)
    
    def test_get_code_non_existant(self):
        with self.assertRaises(Exception):
            result = getCode(userTable, nonExistantDiscordId,Cursor)

    def test_get_link(self):
        result = getLink(userTable, discordId,Cursor)
        self.assertEqual(result, 'link.exemplo.com')
    
    def test_get_link_non_existant(self):
        with self.assertRaises(Exception):
            result = getLink(userTable, nonExistantDiscordId,Cursor)
    
    def test_get_steam_name(self):
        result = getSteamName(discordId,Cursor)
        self.assertEqual(result, 'SabreLobo')

    def test_get_steam_name_non_existant(self):
        with self.assertRaises(Exception):
            result = getSteamName(nonExistantDiscordId, Cursor)
    
    def test_id_exists(self):
        result = id_exists(discordId,Cursor)
        self.assertEqual(result, True)
    
    def test_id_doesnt_exist(self):
        result = id_exists(nonExistantDiscordId,Cursor)
        self.assertEqual(result, False)

    def test_get_avatar(self):
        result = get_avatar(discordId,Cursor)
        self.assertEqual(result, 'avatar.exemplo.com')
    
    def test_get_avatar_non_existant(self):
        with self.assertRaises(Exception):
            result = get_avatar(nonExistantDiscordId,Cursor)

    def test_killer_channel_id_is_correct(self):
        self.assertEqual(getKillerChannelId(),990696291489181810)

    def test_Survivor_channel_id_is_correct(self):
        self.assertEqual(getSurvivorChannelId(),990696291489181810)
        
    def test_Geral_channel_id_is_correct(self):
        self.assertEqual(getGeralChannelId(),990696291489181810)

    def test_Killer_rank_image_link_is_correct(self):
        self.assertEqual(get_rank_image_killer(0),'https://i.imgur.com/gOAR70p.png')
    
    def test_Survivor_rank_image_link_is_correct(self):
        self.assertEqual(get_rank_image_survivor(0),'https://i.imgur.com/3vH3UTW.png')


if __name__ == "__main__":
    unittest.main()   

    