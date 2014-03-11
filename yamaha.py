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
            return
            
        self.socket.settimeout(self.config['timeout'])

          
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

