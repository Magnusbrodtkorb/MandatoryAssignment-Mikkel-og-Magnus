import pickle
import socket
from champlistloader import load_some_champs
from core import Match, Team

champions = load_some_champs()


class Server:
    player1 = []
    player2 = []
    SOCKET = socket.socket()
    connections = []

    def __init__(self, PORT) -> None:
        # Inital messages of connection status
        print("Created socket")
        self.SOCKET.bind(("localhost", PORT))
        print(f"Socket binded to localhost with port {PORT}")

        self.SOCKET.listen()
        print("Waiting for connections")
        self.connectionLoop()

    # Connection loop
    def connectionLoop(self):
        while True:
            # Find connections and add to connections list
            con, addr = self.SOCKET.accept()
            self.connections.append(con)
            print(f"Got connection from {addr}")
            # Send message to first player to connect
            match len(self.connections):
                case 1:
                    self.connections[0].send("MESSAGE Waiting for another player to join.".encode())
            # Send start game commands
                case 2:
                    print("MESSAGE All players connected starting game.".encode())
                    self.connections[0].send("MESSAGE All players connected starting game.".encode())
                    self.connections[1].send("MESSAGE All players connected starting game.".encode())
                    self.connections[1].send("GAME Recieved STARTGAME command.".encode())
                    self.connections[0].send("GAME FIRST".encode())

                    break

        self.gameLoop()

    # Method to send message to all Clients
    def sendToAll(self, message):
        for con in self.connections:
            con.send(message.encode())

    # Match summary
    def matchSum(self):
        match = Match(
            Team([champions[name] for name in self.player1]),
            Team([champions[name] for name in self.player2]))

        match.play()
        self.sendToAll("FINISHED ")
        sendmatch = pickle.dumps(match) # Pickle to send match to Clients
        self.connections[0].send(sendmatch)
        self.connections[1].send(sendmatch)

        # Print a summary

    def gameLoop(self):
        # Connect to database
        db = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        db.sendto(" ".encode(), ("localhost", 4000))
        update_champs = db.recv(4000)
        # Send champs to Clinets
        self.champions = pickle.loads(update_champs)
        champion = pickle.dumps(self.champions)
        self.connections[0].send(champion)
        self.connections[1].send(champion)
        while True:
            for i in range(2):
                #Recieve player choices from Client and run matchsum
                msg = self.connections[0].recv(4000).decode()
                msg2 = self.connections[1].recv(4000).decode()
                self.player1.append(msg)
                self.player2.append(msg2)
            self.matchSum()
            self.shutdown()



    # Shutdown Socket
    def shutdown(self):
        self.SOCKET.close()
        print("Server Closed")


if __name__ == "__main__":
    PORT = 4000

    client = Server(PORT)
