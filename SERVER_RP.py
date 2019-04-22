# -*- coding: utf-8 -*-
"""
Created on Tue Apr  2 10:29:46 2019

@author: Gaurav Sharma
"""

import os, time
import re
import threading, UDPComm
from Cryptodome.PublicKey import RSA
from Crypto import Random
from Cryptodome.Cipher import PKCS1_OAEP


#Generate private and public keys
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()
encrypt_str = "encrypted_message="
client_public_key=""

#arr = array.array('
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientPort):
        threading.Thread.__init__(self)
        self.clientAddress=clientAddress
        self.clientPort = clientPort
        print ("New connection added: ", (clientAddress, clientPort))
    def run(self):
        sock = UDPComm.getSock((self.clientAddress, self.clientPort))
        print ("Connection from : ", (self.clientAddress, self.clientPort))
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        UDPComm.sendTo(sock, "Server:Handshake", "", (self.clientAddress, self.clientPort))
        while True:
            data = sock.recv(2048)
            data = data.decode('latin-1')
            #data = unicode(data, errors='ignore')
            msg = data.replace("\r\n", '') #remove new line character
            print ("Server:Message from client", msg)
            if msg=='Client:AckHandshake':
                UDPComm.sendTo(sock, "Server:PublicKey"+str(public_key.exportKey())+"\n", "", (self.clientAddress, self.clientPort))
                print ("Server:Public key sent to client.")
            elif encrypt_str in msg: #Reveive encrypted message and decrypt it.
                msg = msg.replace(encrypt_str, '')
                print ("Received:\nEncrypted message = "+str(msg))
                encrypted = msg
                decryptor = PKCS1_OAEP.new(private_key)
                decrypted = decryptor.decrypt(encrypted)
                print ("Decrypted message = " + decrypted)
                if decrypted=="Client:OK":
                    print("Successfully exchanged keys")
            elif "Client:PublicKey" in msg:
                msg = msg.replace("Client:PublicKey", '')
                msg=msg.replace("\r\n", '')
                client_public_key = RSA.importKey(msg)
                UDPComm.sendTo(sock, "Server:OK", client_public_key, (self.clientAddress, self.clientPort))
            
            elif data == "Client:Terminate": 
                break
                
        print ("Client at ", (self.clientAddress,self.clientPort) , " disconnected...")


def getIPs():    
    myCmd = os.popen('./show_client.sh').read()
    IPs = myCmd.split()
    r = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
    IPs = (filter(r.match, IPs))
    print("Current IPs:", IPs)
    return set(IPs)
    
def getNeighbours():
    global new_list, old_list, hello, byebye
    new_list = getIPs()
    hello = set(new_list) - set(old_list)
    byebye = set(old_list) - set(new_list)
    
    if len(hello)>0 and len(byebye)>0:
        print("The Following IP's joined new\n", hello)
        ip_val = hello
        print("value of Ip\n", new_list)
        print("The Following IP's disconnected new\n", byebye)
        old_list = set(new_list)
    elif len(hello)>0:
        print("The Following IP's joined new\n", hello)
        old_list = set(new_list)
    elif len(byebye)>0:
        print("The Following IP's disconnected new\n", byebye)
        old_list = set(new_list)
    else:
        print("No changes")
    for ips in hello:
        clientAddress=ips
        clientPort=12345
        newthread = ClientThread(clientAddress, clientPort)
        newthread.start()
        
def WifiListener():
    print("WifiListener  started")
    while(True):
        getNeighbours()
        time.sleep(5)

LOCALHOST = "127.0.0.1"
#clientPort = 12345
#clientAddress = '' #used for all communication
PORT= 12345
old_list=set()
new_list=set()
hello=set()
byebye=set()
thread1 = threading.Thread(target = WifiListener)
thread1.start()
#WifiListener()
print("Server started")
print("Waiting for client request..") 
