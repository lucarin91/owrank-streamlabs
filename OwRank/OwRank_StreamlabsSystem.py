# -*- coding: utf-8 -*-
#---------------------------------------
# Import Libraries
#---------------------------------------
import sys
import io
import json
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
import datetime

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "OwRankCommand"
Website = "https://github.com/lucarin91/overwatch-streamlabs"
Description = "Return the hoster rank on Overwatch."
Creator = "lucarin91"
Version = "1.0.0"

#---------------------------------------
# Set Variables
#---------------------------------------
_command_permission = "everyone"
_command_info = ""
_battletag = []
_region = 'eu'
_message = "Rank:"
_command = "!owrank"
_cooldown = 10

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
    with io.open('Services/Scripts/OwRank/settings.json', mode='r', encoding='utf-8-sig') as f:
        string = f.read()
        Parent.Log(ScriptName, 'Load json: {}'.format(string))
        conf = json.loads(string)
        parse_conf(conf)

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    if data.IsChatMessage():
        if data.GetParam(0).lower() == _command\
           and not Parent.IsOnCooldown(ScriptName, _command)\
           and Parent.HasPermission(data.User, _command_permission, _command_info):
            responce = build_message()
            Parent.SendTwitchMessage(responce)

#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
    pass

def Unload():
    pass
    
def ReloadSettings(jsonData):
    parse_conf(json.loads(jsonData))

#---------------------------------------
# My functions
#---------------------------------------
def get_rank(username, region='eu'):
    """Return the rank of the username given in input."""
    url = 'http://ow-api.herokuapp.com/profile/pc/{}/{}'.format(region, username)
    res_raw = Parent.GetRequest(url, {})
    res = json.loads(res_raw)
    status, data = res['status'], json.loads(res['response'])
    if status != 200:
        Parent.Log(ScriptName, 'Request status {}'.format(status))
        return
    
    Parent.Log(ScriptName, '{} - {} - {}'.format(status, type(data), data))  # debug

    if 'competitive' not in data or 'rank' not in data['competitive']:
        Parent.Log(ScriptName, 'Remote service error.')
        return

    rank = data['competitive']['rank']
    return rank if rank is not None else "not placed"

def parse_conf(conf):
    """Set the configuration variable."""
    global _battletag, _region, _message, _command, _cooldown
    _battletag = [b.strip() for b in conf['battletag'].split(',')]
    _region = conf['region']
    _message = conf['message']
    _command = conf['command']
    _cooldown = conf['cooldown']
    Parent.Log(ScriptName, 'Load conf: {}'.format((_battletag, _region, _message, _command, _cooldown)))

def build_message():
    """Build the message with the rank to sent to the chat."""
    ranks = [(user.split('-')[0], get_rank(user, _region)) for user in _battletag]
    responce = "{} {}".format(_message, ', '.join(['{}->{}'.format(u, r) for u, r in ranks]))
    return responce

def ShowRank():
    """Send the rank to the chat."""
    Parent.Log(ScriptName, 'Send rank to chat!')
    responce = build_message()
    Parent.SendTwitchMessage(responce)
    