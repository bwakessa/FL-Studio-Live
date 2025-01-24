//cd eclipse-workspace/FLive/src
//javac client/Client.java server/Server.java server/ClientHandler.java
package server;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

import client.Client;


public class Server {
	private static int initClientID = 1000;
	
	private ServerSocket serverSocket;
	
	private int uniqueClientID; //used to generate unique IDs for clients (basically indefinitely increasing)
	private ArrayList<Client> connectedClients; //list of currently connected clients;; used to keep track of available unique ids
	private Set<Integer> idSet;
	
	public Server(ServerSocket serverSocket) {
		this.serverSocket = serverSocket;
		
		this.uniqueClientID = Server.initClientID; //starting the unique ids at 1000
		this.connectedClients = new ArrayList<Client>();
		this.idSet = new HashSet<>();
	}
	
	public void runServer() {
		/* Starts the server. This method listens to the server socket to accept new clients.
		 * Sends newly connected clients to a client handler to be handled in a new thread 
		 */		
		try {	
			System.out.println("Server is running!\n----------------------------------\n");
			while (!this.serverSocket.isClosed()) {
				Socket clientSocket = this.serverSocket.accept(); //Block until a new client connects
				//Client newClient = new Client(generateUniqueID(), clientSocket); //Create new client
				//this.connectedClients.add(newClient); 
				//this.idSet.add(newClient.getID()); //add to unique clientID set	
				
				ClientHandler clientHandler = new ClientHandler(clientSocket); //instance of class which contains code to be run by Runnable.run() under Thread class
				Thread clientThread = new Thread(clientHandler); //new Thread
				clientThread.start();				
			}
			
		} catch (IOException e) {			
			try {
				this.serverSocket.close();
			} catch (IOException f) {
				f.printStackTrace();
			}				
		}
		
	}
	
	private int generateUniqueID() {
		while (true) {
			int currId = Server.initClientID;
			if (!this.idSet.contains(currId)) {
				return currId;
			} else {
				currId ++;
			}
		}
	}

	public static void main(String[] args) throws IOException {
		ServerSocket serverSocket = new ServerSocket(4999);
		Server server = new Server(serverSocket);
		server.runServer();
	}

}

