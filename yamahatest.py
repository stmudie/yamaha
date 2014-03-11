import socket
import yaml

class yamaha:
    def __init__(self, IP='', port=0):
    
        self.config = {'terminator' : '\r\n', 'port' : 50000, 'timeout' : 3}
    
        try:
            stream = file('config.yml', 'r') 
            self.config.update(yaml.load(stream))
            
        except IOError:
            print "Unable to find configuration file settings.conf, using defaults."
            
        if IP == '':
            IP = self.config['IP']
        
        if port == 0:
            port = self.config['port'] 
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((IP,port))
        except Exception as e:
            print e
            return 'Could not connect'
            
        self.socket.settimeout(self.config['timeout'])

    def playfile(self, source, filename, server=''):
        
        source = source.upper()
        
        if source == 'SERVER':
            if server == '':
                try:
                    server = self.config['server']
                except:
                    pass
                    
                if server == '':
                    print 'No server defined'
                    return 'No server defined'
                
        self.changeinput(source)
        sleep(1.5)
        playing = self.sendmessage('@%s:PLAYBACKINFO=?' % (source,))
        sleep(0.3)
        if playing != Stop:
            self.sendmessage('@%s:PLAYBACK=Stop' % (source,))
            sleep(0.3)
        self.sendmessage('@%s:LISTCURSOR=Return to Home' % (source,))
        sleep(0.3)
        
        maxline = self.sendmessage('@%s:MAXLINE=?' % (source,))
        
        while 1:
            currentline = self.sendmessage('@%s:CURRLINE=?' % (source,))
            if server == self.sendmessage('@%s:LISTINFO=?' % (source,)):
                break
            self.sendmessage('@%s:LISTCURSOR=Down' % (source,))
            sleep(0.3)
            if currentline == maxline:
                return "Server not found"

        
        for i in range(4):
            self.sendmessage('@%s:LISTCURSOR=Sel' % (source,))


        maxline = self.sendmessage('@%s:MAXLINE=?' % (source,))
            
        while 1:
            currentline = self.sendmessage('@%s:CURRLINE=?' % (source,))
            if filename == self.sendmessage('@%s:LISTINFO=?' % (source,)):
                break
            self.sendmessage('@%s:LISTCURSOR=Down' % (source,))
            sleep(0.3)
            if currentline == maxline:
                return "File not found"
        
        self.sendmessage('@%s:LISTCURSOR=Sel' % (source,))
        playing='Play'
        while playing=='Play':
            playing==self.sendmessage('@%s:PLAYBACKINFO=?' % (source,))
            sleep(0.3)

   
    
    def powerstate(self):
        return self.sendmessage('@SYS:PWR=?')

    def currentvol(self):
        return self.sendmessage('@MAIN:VOL=?')

    def changeinput(self, input):
        current = self.currentinput()
        if current != input:
            return self.sendmessage('@MAIN:INP=%s' % (input,))
        return current

    def currentinput(self):
        return self.sendmessage('@MAIN:INP=?')


    def flush(self):
    
        self.socket.settimeout(0.1)
        
        try:
            flush = self.socket.recv(128)
            print flush
        except:
            print 'pass'
                
        self.socket.settimeout(self.config['timeout'])

    def sendmessage(self,message,pretty=True):
        
        #self.flush()
        
        self.socket.sendall("%s%s" % (message,self.config['terminator']))
        data = self.socket.recv(128)
    
        if pretty:
            data = data.split(self.config['terminator'])[0].split('=')[1]
            
        return data

    def __del__(self):
        self.socket.close()

a = yamaha('localhost')
#print a.changeinput('HDMI2')
print a.currentvol()
print a.currentinput()

