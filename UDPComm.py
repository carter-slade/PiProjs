import socket
import sys  

from Cryptodome.Cipher import PKCS1_OAEP
encrypt_str = "encrypted_message="

def getSock(ip_port):    
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    
    print ("UDP target IP:", ip_port[0])
    print ("UDP target port:", ip_port[1])
    return sock

def sendTo(sock, message, key, ip_port):
    if str(key)=='':
        message = message.decode('utf-8').encode('utf-8')
        sock.sendto(message, ip_port)
        print("UDPComm:Message sent", message)
    else:
        encryptor = PKCS1_OAEP.new(key)
        encrypted = encryptor.encrypt(message)
        encrypted = (encrypt_str+str(encrypted)).decode('utf-8').encode('utf-8')
        sock.sendto(encrypted, ip_port)
        print("UDPComm:Encrypted Message sent", encrypted)
