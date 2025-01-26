package server;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.util.ArrayList;

import client.Client;

public class ClientHandler implements Runnable {
	public static ArrayList<ClientHandler> clientHandlers = new ArrayList<>();
	private Socket clientSocket;
	private String clientID;
	
	private InputStreamReader inputStreamReader;
	private OutputStreamWriter outputStreamWriter;
	private BufferedReader bufferedReader;
	private BufferedWriter bufferedWriter;
	
	public ClientHandler(Socket clientSocket) throws IOException {
		this.clientSocket = clientSocket;
		clientHandlers.add(this);
		
		//Setting up IO objects for this client
		this.inputStreamReader = new InputStreamReader(this.clientSocket.getInputStream());
		this.outputStreamWriter = new OutputStreamWriter(this.clientSocket.getOutputStream());
		this.bufferedReader = new BufferedReader(this.inputStreamReader);
		this.bufferedWriter = new BufferedWriter(this.outputStreamWriter);		

		this.clientID = this.bufferedReader.readLine(); //corresponds to line 57 in Client
		broadcastMessage("Server: " + this.clientID + " has connected");
	}
	
	@Override
	public void run() {
		try {
			while (this.clientSocket.isConnected()) {
				String clientMessage = this.bufferedReader.readLine();
				
				if (clientMessage.equalsIgnoreCase("bye")) { //TODO: add method in server class to account for terminated client (remove from list of connected clients)
					this.clientSocket.close();
					this.inputStreamReader.close();
					this.outputStreamWriter.close();
					this.bufferedReader.close();
					this.bufferedWriter.close();
					removeClientHandler();
					break;
				} else {
					System.out.println("Client " + this.clientID + ": " + clientMessage);
					broadcastMessage(this.clientID + ": " + clientMessage);
				}
			}
		} catch (IOException e) {
			System.out.println(e.getStackTrace());
		}
	}
	
	public void broadcastMessage(String message) throws IOException {
		for (ClientHandler clientHandler: clientHandlers) {
			if (!clientHandler.clientID.equals(this.clientID)) {
				clientHandler.bufferedWriter.write(message);
				clientHandler.bufferedWriter.newLine();
				clientHandler.bufferedWriter.flush();
			}
		}
	}
	
	public void removeClientHandler() throws IOException {
		clientHandlers.remove(this);
		broadcastMessage("Server: " + this.clientID + "has disconnected.");
	}
}
