import socket
import UDPComm
import RSA
import base64

UDP_IP = '0.0.0.0'
UDP_PORT = 12345

private_key , public_key = RSA.generate_keys()
encrypt_str = "encrypted_message="

server_public_key=""
sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #data = unicode(data, errors='ignore')
    data = base64.b64decode(data)
    print ("Received:",data)
    print ("Received from:", addr)
    if data=="Server:Handshake":
        message = "Client:AckHandshake"
        UDPComm.sendTo(sock, message, "", addr)
        break
while True:
    data, addr = sock.recvfrom(1024)
    if len(data)>0:
        #data = data.replace("Server:PublicKey", '')
        #data=data.replace("\r\n", '')
        print("Server pubic key received!")
        server_public_key = RSA.importKey(data)
        message = public_key.exportKey()
        UDPComm.sendTo(sock, message, "key", addr)
        break
while True:
    msg, addr = sock.recvfrom(1024)
    #msg = unicode(msg, errors='replace')
    print("Received:"+msg)
    #msg = base64.b64decode(msg)
    #msg = msg.replace(encrypt_str, '')
    #print ("Received:\nEncrypted message = "+str(msg))
    #decryptor = PKCS1_OAEP.new(private_key)
    #decrypted = decryptor.decrypt(encrypted)
    decrypted = RSA.decrypt_message(msg, private_key)
    decrypted = decrypted.replace(encrypt_str, '')
    print ("Decrypted message = " + decrypted)
    if decrypted=="Server:OK":
        print("Succesfully exchanged keys")
    message = "Client:OK"
    UDPComm.sendTo(sock, message, server_public_key, addr)
        
              
