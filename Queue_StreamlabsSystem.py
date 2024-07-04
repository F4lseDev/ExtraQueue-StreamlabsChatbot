#---------------------------
#   Import Libraries
#---------------------------
import os
import sys
import json
import random

sys.path.append(os.path.join(os.path.dirname(__file__), "lib")) #point at lib folder for classes / references

import clr
clr.AddReference("IronPython.SQLite.dll")
clr.AddReference("IronPython.Modules.dll")

#   Import your Settings class
from Settings_Module import Settings 
#---------------------------
#   [Required] Script Information
#---------------------------
ScriptName = "ExtraQueue"
Website = "https://www.twitch.tv/falsegr"
Description = "A short plugin for Extra Queues"
Creator = "False"
Version = "0.1"

#---------------------------
#   Define Global Variables
#---------------------------
global SettingsFile
SettingsFile = ""
global ScriptSettings
ScriptSettings = Settings()



#---------------------------
#   Custom Funcs
#---------------------------

Queue = []
open = False
Ticket = []


def StartQueue():
    global open
    open = True
    Parent.SendStreamMessage("Die Queue wurde geoeffnet")
    Parent.Log("ExtraQueue", "Queue opened")

def StopQueue():
    global open
    open = False
    Parent.SendStreamMessage("Die Queue wurde geschlossen")
    Parent.Log("ExtraQueue", "Queue closed")


def DrawQueueAll():
    global Queue
    global Ticket
    players = 4
    if Ticket == []:
        playercount = range(players)
        for x in playercount:
            Parent.Log("ExtraQueue", str(Queue))
            player = random.choice(Queue)
            Parent.SendStreamMessage(player + " wurde gezogen")
            Queue.remove(player)
            Ticket = []
    else:
        TicketInt = len(Ticket)
        players = players - TicketInt
        playercount = range(players)
        for x in playercount:
            Parent.Log("ExtraQueue", str(Queue))
            player = random.choice(Queue)
            Parent.SendStreamMessage(player + " wurde gezogen")
            Queue.remove(player)
        for x in Ticket:
            Parent.SendStreamMessage(x + " ist mit Ticket beigetreten")
            Ticket.remove(x)
            

    
    
    

def DrawQueue():
    global Queue
    Parent.Log("ExtraQueue", str(Queue))
    player = random.choice(Queue)
    Parent.SendStreamMessage(player + " wurde gezogen")
    Queue.remove(player)
    
def ClearQueue():
    global Queue
    Queue = []


#---------------------------
#   [Required] Initialize Data (Only called on load)
#---------------------------
def Init():

    #   Create Settings Directory
    directory = os.path.join(os.path.dirname(__file__), "Settings")
    if not os.path.exists(directory):
        os.makedirs(directory)

    #   Load settings
    SettingsFile = os.path.join(os.path.dirname(__file__), "Settings\settings.json")
    ScriptSettings = Settings(SettingsFile)
    ScriptSettings.Response = "Overwritten Settings"
    return

#---------------------------
#   [Required] Execute Data / Process messages
#---------------------------






def Execute(data):
    if not data.IsChatMessage() or not data.IsFromTwitch():
        return
       
    elif data.Message == ScriptSettings.Command and open == True:
        global Queue
        if data.UserName in Queue:
            Parent.SendStreamMessage("Du bist schon in der Queue")
            return
        elif not data.UserName in Queue and open == True:
            Queue.append(data.UserName)
            Parent.SendStreamMessage( data.UserName + " " + ScriptSettings.Response)
            
        else:
            return
        
    elif "!ticket" in data.Message and data.GetParamCount() == 2 and Parent.HasPermission(data.User, "moderator", "test"):
        Parent.Log("ExtraQueue", "Added " + data.GetParam(1) + " to the tickets")
        Parent.SendStreamMessage("Das Ticket von " + data.GetParam(1) + " wurde angewendet")
        global Ticket
        Ticket.append(data.GetParam(1))
    
    elif "!ticket" in data.Message and data.GetParamCount() == 1 and Parent.HasPermission(data.User, "moderator", "test"):
        Parent.SendStreamMessage("Es muss ein Name angegeben werden nach den !ticket")


    else:
        return
        
    return


    

#---------------------------
#   [Required] Tick method (Gets called during every iteration even when there is no incoming data)
#---------------------------
def Tick():
    return

#---------------------------
#   [Optional] Parse method (Allows you to create your own custom $parameters) 
#---------------------------
def Parse(parseString, userid, username, targetid, targetname, message):
    return parseString

#---------------------------
#   [Optional] Reload Settings (Called when a user clicks the Save Settings button in the Chatbot UI)
#---------------------------
def ReloadSettings(jsonData):
    # Execute json reloading here
    ScriptSettings.__dict__ = json.loads(jsonData)
    ScriptSettings.Save(SettingsFile)
    return

#---------------------------
#   [Optional] Unload (Called when a user reloads their scripts or closes the bot / cleanup stuff)
#---------------------------
def Unload():
    return

#---------------------------
#   [Optional] ScriptToggled (Notifies you when a user disables your script or enables it)
#---------------------------
def ScriptToggled(state):
    return
