import socket
from emoji import demojize
from apscheduler.schedulers.background import BackgroundScheduler


class TwitchControl:
    # define relevant constants here
    

    def __init__(self):
        self.server = 'irc.chat.twitch.tv'
        self.port = 6667
        self.nickname = 'yourtwitchusername'
        self.token = 'oauth:youroauthkeyhere'
        self.channel = '#yourtwitchchannel'
        
        
        
        self.sched = BackgroundScheduler()
            
        self.sock = socket.socket()
        self.sock.connect((self.server,self.port))
        self.sock.send(f"PASS {self.token}\n".encode('utf-8'))
        self.sock.send(f"NICK {self.nickname}\n".encode('utf-8'))
        self.sock.send(f"JOIN {self.channel}\n".encode('utf-8'))
        
       

        self.voteDict = {"null": 0, "fwd" : 0, "rev" : 0, "left" : 0, "right" : 0}


        self.sched.add_job(self.voteCount, 'interval', seconds=2)
        self.sched.start()

    
    def loop(self):
                
        while True:
            resp = self.sock.recv(2048).decode('utf-8')
            if resp.startswith('PING'):
                self.sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                respClean = demojize(resp)
                print(respClean)
                msgComponents=respClean.split(" ",3)

                msgUser=msgComponents[0]                    #get username from message
                msgUser = msgUser[msgUser.find(':')+1: msgUser.find('!')]
                msgContent=msgComponents[3]                             #print message content
                
                if msgContent.find("FLAG") >=0:
                    print("Wave the flag!")
                    donorUser=(msgContent[1 : msgContent.find(' ')])    
                    subprocess.call('espeak -v +f3  -s 140 "Thank you for the donation "' + donorUser + ' 2>/dev/null', shell=True)
                

                if msgContent.find("FWD") >=0:
                    self.voteDict["fwd"] = self.voteDict["fwd"] +1
                if msgContent.find("REV") >=0:
                    self.voteDict["rev"] = self.voteDict["rev"] +1
                if msgContent.find("LEFT") >=0:
                    self.voteDict["left"] = self.voteDict["left"] +1
                if msgContent.find("RIGHT") >=0:
                    self.voteDict["right"] = self.voteDict["right"] +1
                    
    def voteCount(self): 			#function responsible for checking votes and executing commands
        print('Counting votes and executing command')
        voteWinner = max(self.voteDict, key=self.voteDict.get)
        print("biggest vote:" + voteWinner)
        nullCheck=all(x==0 for x in self.voteDict.values())
        
        if nullCheck:
            print('doing a nullo')
            
        elif voteWinner=="fwd":
            print('going Forward')
            #code to go forward here
        elif voteWinner=="rev":
            print('going Reverse')
            #code to go reverse here
        elif voteWinner=="left":
            print('going  Left')
            #code to go left here
        elif voteWinner=="right":
            print('going Right')
            #code to go right here
        self.voteDict = {"null" : 0, "fwd" : 0, "rev" : 0, "left" : 0, "right" : 0} #reset votes to 0
    
                
    def close(self):
        print('closing I think')
        self.sched.shutdown()

    def __enter__(self):
        return self

    def __exit__(self, *_, **__):
        self.close()

def main(argv=None):
    TwitchControl().loop()
    
main()
