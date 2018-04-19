# -*- coding: utf-8 -*-
#---------------------------------------
# Import Libraries
#---------------------------------------
import sys
import io
import json
from os.path import isfile
import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")
from datetime import datetime

#---------------------------------------
# [Required] Script Information
#---------------------------------------
ScriptName = "OwRank"
Website = "https://github.com/lucarin91/overwatch-streamlabs"
Description = "Return the hoster rank on Overwatch."
Creator = "lucarin91"
Version = "2.0.0"

#---------------------------------------
# Set Variables
#---------------------------------------
_command_permission = "everyone"
_command_info = ""
_last_update = None
_responce = None
_battletag = []
_region = 'eu'
_message = "Rank:"
_command = "!owrank"
_cooldown = 10

#---------------------------------------
# [Required] Intialize Data (Only called on Load)
#---------------------------------------
def Init():
    global _last_update, _responce
    settings = 'Services/Scripts/{}/settings.json'.format(ScriptName)
    if isfile(settings):
        with io.open(settings, mode='r', encoding='utf-8-sig') as f:
            string = f.read()
            Parent.Log(ScriptName, 'Load json: {}'.format(string))
            conf = json.loads(string)
            parse_conf(conf)
    
    _responce = build_message()
    _last_update = datetime.today()

#---------------------------------------
# [Required] Execute Data / Process Messages
#---------------------------------------
def Execute(data):
    if data.IsChatMessage():
        if data.GetParam(0).lower() == _command\
           and not Parent.IsOnCooldown(ScriptName, _command)\
           and Parent.HasPermission(data.User, _command_permission, _command_info):
            Parent.SendTwitchMessage(_responce)

#---------------------------------------
# [Required] Tick Function
#---------------------------------------
def Tick():
    global _responce, _last_update
    if (datetime.today() - _last_update).seconds > 30:
        _responce = build_message()
        _last_update = datetime.today()
        Parent.Log(ScriptName, 'update rank! ({})'.format(_responce))

def Unload():
    pass
    
def ReloadSettings(jsonData):
    parse_conf(json.loads(jsonData))

#---------------------------------------
# My functions
#---------------------------------------
def get_rank(username, region='eu'):
    """Return the rank of the username given in input."""
    url = 'https://owapi.net/api/v3/u/{}/stats'.format(username)
    res_raw = Parent.GetRequest(url, {"User-Agent":"Linux/generic"})
    res = json.loads(res_raw)
    status, data = res['status'], json.loads(res['response'])
    if status != 200:
        Parent.Log(ScriptName, 'Request status {}'.format(status))
        return "not placed"
    
    if not data\
       or not region in data\
       or not 'stats' in data[region]\
       or not 'competitive' in data[region]['stats']\
       or not 'overall_stats' in data[region]['stats']['competitive']\
       or not 'comprank' in data[region]['stats']['competitive']['overall_stats']:
        Parent.Log(ScriptName, 'Remote service error.')
        return "not placed"

    rank = data[region]['stats']['competitive']['overall_stats']['comprank']
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
    