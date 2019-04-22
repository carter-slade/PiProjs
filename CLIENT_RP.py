import socket
import UDPComm
from Crypto import Random
from Cryptodome.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

UDP_IP = '0.0.0.0'
UDP_PORT = 12345

#Generate private and public keys
random_generator = Random.new().read
private_key = RSA.generate(1024, random_generator)
public_key = private_key.publickey()
encrypt_str = "encrypted_message="

server_public_key=""
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #data = unicode(data, errors='ignore')
    data = data.decode("utf-8")
    print ("Received:",data)
    print ("Received from:", addr)
    if data=="Server:Handshake":
        message = "Client:AckHandshake"
        UDPComm.sendTo(sock, message, "", addr)
    elif  "Server:PublicKey" in data:
        data = data.replace("Server:PublicKey", '')
        data=data.replace("\r\n", '')
        server_public_key = RSA.importKey(data)
        message = "Client:PublicKey"+str(public_key.exportKey())
        UDPComm.sendTo(sock, message, "", addr)
        break
while True:
    msg, addr = sock.recvfrom(1024)
    #msg = unicode(msg, errors='replace')
    print("Received:Server"+msg)
    msg = msg.decode('utf-8')
    msg = msg.replace(encrypt_str, '')
    #print ("Received:\nEncrypted message = "+str(msg))
    encrypted = msg
    decryptor = PKCS1_OAEP.new(private_key)
    decrypted = decryptor.decrypt(encrypted)
    print ("Decrypted message = " + decrypted)
    if decrypted=="Server:OK":
        print("Succesfully exchanged keys")
    message = "Client:OK"
    UDPComm.sendTo(sock, message, server_public_key, addr)
        
              
