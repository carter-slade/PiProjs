import socket
import sys  
import RSA
import base64

encrypt_str = "encrypted_message="

def getSock(ip_port):    
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    
    print ("UDP target IP:", ip_port[0])
    print ("UDP target port:", ip_port[1])
    return sock

def sendTo(sock, message, key, ip_port):
    if str(key)=='':
        message = base64.b64encode(message)
        sock.sendto(message, ip_port)
        print("UDPComm:Message sent", message)
    elif str(key)=='key':
        sock.sendto(message, ip_port)
        print("UDPComm:Key sent", message)
    else:
        #encryptor = PKCS1_OAEP.new(key)
        #encrypted = encryptor.encrypt(message)
        #encrypted = encrypted.decode('latin-1').encode('latin-1')
        #encrypted = (encrypt_str+str(encrypted)).encode('latin-1')
        encrypted = RSA.encrypt_message(message , key)
        sock.sendto(b'encrypted_message='+encrypted, ip_port)
        print("UDPComm:Encrypted Message sent", encrypted)
