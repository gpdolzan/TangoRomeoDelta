import socket

# Create a socket object using DGRAM
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Get local machine name
host = socket.gethostname()

# Bastao
bastao = 0

# Open config file
config = open("config", "r")

# From config file read lines until you find the host name then keep info from that line
for line in config:
    if line.startswith(host):
        line = line.split()
        port = int(line[1])
        tHost = line[2]
        tPort = int(line[3])

address = (host, port) # self address
tAddress = (tHost, tPort) # target address

# bind address to socket
s.bind(address)

# transform the string into bytes
if host == "h13":
    bastao = 1

while(1):
    if bastao == 1:
        msg = input("Voce possui o bastao, envie a mensagem: ")
        encoded_msg = msg.encode('ascii')
        s.sendto(encoded_msg, tAddress)
        data, addr = s.recvfrom(1024)
        received_msg = data.decode('ascii')
        # Check if first 2 letters are pb
        if received_msg[:2] == "pb":
            # If size is 14
            if len(received_msg) == 14:
                bastao = 0
        elif msg == received_msg:
            print("Mensagem deu a volta: " + received_msg)
    else:
        data, addr = s.recvfrom(1024)
        received_msg = data.decode('ascii')
        # Check if first 2 letters are pb
        if received_msg[:2] == "pb":
            # If size is 2, get bastao
            if len(received_msg) == 2:
                bastao = 1
            # Concatenate the message with the hostanem at the end
            received_msg = received_msg + "_" + host
            data = received_msg.encode('ascii')
        else:
            print("Recebi uma mensagem: " + received_msg)
        # Recebeu a mensagem, passe a mensagem adiante
        s.sendto(data, tAddress)

# Close the socket
s.close()