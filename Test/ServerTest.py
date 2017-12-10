import socket
import sys



print("# Start server..")

# Create TCP/IP socket and start to listen for clients.
server_address = ('192.168.0.106', 8000)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
sock.listen(1)

while True:

    connection, client_address = sock.accept()
    print("# Connected with client.")

    try:
        while True:
            print("# Waiting for data..")
            data = connection.recv(1024)

            if data:
                strData = data.decode('utf-8')

                print >> sys.stderr, 'Data received: "%s"' % strData
                print("# Send data back to client..")
                connection.sendall(data)

            else:
                print("# No more data.")
                break

    except Exception as e:
        print("# Exception:\n", e)

    finally:
        connection.close()
        print("# Connection closed.\n#----------")
