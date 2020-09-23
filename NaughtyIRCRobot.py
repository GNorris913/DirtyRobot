import ssl, socket, time, os, traceback
from dotenv import load_dotenv
import re
import random
import time
"""
BASIC IMPLEMENTATION OF THE SONDERBOT FRAMEWORK
POTTYMOUTH ENABLED ON THIS BOT.
PROVIDED WITHOUT WARRANTY OR REPUTATION
"""
class IRCCON:
    irc = socket.socket()
    read_buffer = ""
    server = ""
    port = ""
    botnick = ""
    botnick2 = ""
    botnick3 = ""
    botnickpass = ""
    channel = ""
    channelList = {}
    users = []
    RPL_NAMESREPLY = '353'
    RPL_ENDOFNAMES = '366'

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.irc = ssl.wrap_socket(self.irc)
        self.irc.setblocking(True)

    def connect(self, server, port, botnick, botnick2, botnick3, botpass, botnickpass):
        self.server = server
        self.port = port
        self.botnick = botnick
        self.botnick2 = botnick2
        self.botnick3 = botnick3
        self.botpass = botpass
        self.botnickpass = botnickpass

        # connect to server
        print("connecting to: " + server)
        self.irc.connect((server, port))

        # Authenticate User
        self.irc.send(bytes("PASS spyfall \n", "UTF-8"))
        # User authentication
        self.irc.send(bytes("USER " + botnick + " " + botnick + " " + botnick + " :SonderBot\n", "UTF-8"))
        self.irc.send(bytes("NICK " + botnick + "\n", "UTF-8"))
        # self.irc.send(bytes("NICKSERV IDENTIFY " + botnickpass + " " + botpass + "\n", "UTF-8"))
        time.sleep(2)

        # self.irc.send(bytes("JOIN " + channel + "n", "UTF-8"))

    def joinchannel(self, channel):
        self.irc.send(bytes("JOIN " + channel + "\n", "UTF-8"))

    def send(self, channel, msg):
        print(channel + " " + msg)
        self.irc.send(bytes("PRIVMSG " + channel + " " + msg + "\n", "UTF-8"))

    def whisper(self, channel, user, msg):
        channel = channel[1:]
        user = user[1:]
        print(channel + " " + user)
        # self.irc.send(bytes("PRIVMSG " + channel + ':/msg ' + user + " " + msg + "\n", "UTF-8"))
        print("PRIVMSG #" + channel + ' :/msg ' + user + " " + msg + "\r\n")
        self.irc.send(bytes("PRIVMSG " + user + " :" + msg + "\r\n", "UTF-8"))

    def echo(self, channel, user, msg):
        channel = channel[1:]
        user = user[1:]

    def get_response(self):
        time.sleep(.1)
        response = ""

        response = self.irc.recv(4096).decode("UTF-8")  # 2040
        if response.find('PING') != -1:
            self.irc.send(bytes('PONG ' + response.split()[1].encode('UTF-8').decode('UTF-8') + '\r\n', "UTF-8"))
            # self.irc.send(bytes("PONG", "UTF-8"))
            print("RESPONSE" + response)

        return response

    def get_names(self, in_channel, firstRun):
        gotNames = False
        if firstRun == False:
            self.irc.send(bytes('NAMES ' + in_channel + '\r\n', "UTF-8"))
        while gotNames == False:
            time.sleep(.3)
            self.read_buffer += self.get_response()
            lines = self.read_buffer.split('\r\n')
            self.read_buffer = lines.pop()
            print(self.read_buffer)
            for line in lines:
                response = line.rstrip().split(' ', 3)
                response_code = response[1]
                if response_code == self.RPL_NAMESREPLY:
                    names_list = response[3].split(':')[1]
                    print(names_list)
                    self.users += names_list.split(' ')
                if response_code == self.RPL_ENDOFNAMES:
                    gotNames = True
        return self.users


class BOTCLIENT:
    #### BOTCLIENT(port,channel,botnick,botnick2,botnick3,botnickpass,botpass) ####
    ##IRC CONFIG###
    botRunning = True
    pottymouth = False
    starttime = 0
    trigger = "!"
    irc = IRCCON()
    accessList = {}
    cwd = ""
    users = []
    channelQueue = []
    whisperQueue = []
    channelList = {}
    appsList = {}

    def __init__(self,
                 server,
                 sslport,
                 channel, botnick, botnick2, botnick3, botnickpasswd, trigger):

        # Accepts connection parameters from .env, can be set manually here
        self.server = server
        self.port = int(sslport)
        self.channel = channel
        self.botnick = botnick
        self.botnick2 = botnick2
        self.botnick3 = botnick3
        self.botnickpass = botnickpasswd
        self.botpass = " "
        self.channelsList = []
        self.trigger = trigger
        # self.functions.add[commands]

        # initiate IRC connection
        self.irc.connect(self.server, self.port, self.botnick,
                         self.botnick2, self.botnick3, self.botpass, self.botnickpass)
        self.irc.joinchannel(self.channel)
        self.cwd = os.getcwd()
        self.users = self.irc.get_names(self.channel, True)

        #############################################################################
        self.bot_running()  # MAIN EVENT LOOP
        #############################################################################

    # *************** MAIN EVENT LOOP ****************************
    def bot_running(self):
        magic_character = "!"
        trigger = magic_character
        #############################################################
        #self.channelQueue.append({"channel":self.channel,"user":self.botnick,"message":pottymouth()})
        time.sleep(2)
        while self.botRunning:
            t = self.irc.get_response()
            # prints chat text to window
            if (len(t)>14):
                print(t)
                self.commands(t)
                self.speak()

    def commands(self, text):
        user = re.match(':.*?!', text)
        if user:
            user = user.group(0)
            user = user[1:-1]

            botName = re.match(self.botnick, user)
            if botName:
                pass
            else:
                command = re.search(r':.*?:', text)  # isolate command in text
                channel = re.search(r'#.*?:', text)  # isolate channel in text
                if channel:
                    channel = channel.group(0)[:-2]
                    #print("CHANNEL" + channel)
                    pottymouthCounter = random.randint(1,300)
                    if pottymouthCounter == 50:
                        self.channelQueue.append({"channel":self.channel,
                                                  "user":self.botnick,
                                                  "message": pottymouth()})
                    if command:
                        newcommand = command.group(0)
                        dirty = re.search(r':!dirty', text)
                        if dirty:
                            print("COMMAND XXX")
                            self.channelQueue.append({"channel": self.channel,
                                                      "user": self.botnick,
                                                      "message": pottymouth()})
                else:
                    channel = user
                    print("WHISPER RECEIVED")

    def speak(self):
        floodLimit = 8
        floodCount = 0
        if floodCount <= floodLimit:
            for chan_msg in self.channelQueue:
                self.irc.send(chan_msg["channel"], chan_msg["message"])
            for whisper in self.whisperQueue:
                self.irc.whisper(whisper["channel"], whisper["user"], whisper["message"])
        else:
            time.sleep(3)
        self.channelQueue.clear()
        self.whisperQueue.clear()

        def shutdown(self):
            self.botRunning = False

def pottymouth(limiter = 10):
    limit = limiter
    with open("PH_Comments.txt", encoding='utf-8') as f:
        dirty = None
        lines = f.readlines()
        z = (random.choice(lines))
        y = eval(z)
        dirty = str(y["comment"])
        if len(dirty) < 10:
            if limit > 0:
                dirty = pottymouth(limit-1)
        return dirty
###########################    MAIN    ############################################
def main():
    errorcount = 0

    while errorcount < 100:
        # Load default connection perameters from .env
        load_dotenv()
        LOG = os.getenv("FONDLEBOT_LOGS")
        BOTNICK = os.getenv("FONDLEBOT_BOTNICK")
        BOTNICK2 = os.getenv("FONDLEBOT_BOTNICK2")
        BOTNICK3 = os.getenv("FONDLEBOT_BOTNICK3")
        CHANNEL = "#wetfish"
        TRIGGER = os.getenv("FONDLEBOT_TRIGGER")
        ACL = os.getenv("FONDLEBOT_ACL")
        SERVER = os.getenv("FONDLEBOT_SERVER")
        PORT = os.getenv("FONDLEBOT_PORT")
        BOTNICKPASSWD = os.getenv("FONDLEBOT_BOTNICKPASSWD")
        try:
            bot = BOTCLIENT(SERVER, PORT, CHANNEL, BOTNICK,
                            BOTNICK2, BOTNICK3, BOTNICKPASSWD, TRIGGER)
        except Exception:
            errorcount = errorcount + 1
            time.sleep(300)
            traceback.print_exc()
            bot = BOTCLIENT(SERVER, PORT, CHANNEL, BOTNICK,
                            BOTNICK2, BOTNICK3, BOTNICKPASSWD, TRIGGER)
            pass


###############
if __name__ == '__main__':
    main()
###########################    MAIN    ############################################