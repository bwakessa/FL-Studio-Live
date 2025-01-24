package client;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.Socket;
import java.util.Scanner;

public class Client {

	private String clientID;
	private Socket clientSocket;
	
	private InputStreamReader inputStreamReader;
	private OutputStreamWriter outputStreamWriter;	
	private BufferedReader bufferedReader;
	private BufferedWriter bufferedWriter;
	
	
	public Client(String clientID, Socket clientSocket) throws IOException {
		this.clientID = clientID;
		this.clientSocket = clientSocket;
		this.inputStreamReader = new InputStreamReader(this.clientSocket.getInputStream());
		this.outputStreamWriter = new OutputStreamWriter(this.clientSocket.getOutputStream());
		this.bufferedReader = new BufferedReader(inputStreamReader);
		this.bufferedWriter = new BufferedWriter(outputStreamWriter);
	}

	public String getID() {
		return this.clientID;
	}
	
	public Socket getClientSocket() {
		return this.clientSocket;
	}
	
	public InputStream getInputStream() throws IOException {
		return this.clientSocket.getInputStream();
	}
	
	public OutputStream getOutputStream() throws IOException {
		return this.clientSocket.getOutputStream();
	}
	
	public void terminate() throws IOException {
		this.clientSocket.close();
		this.bufferedReader.close();
		this.bufferedWriter.close();
	}
	
	public void startClient() throws IOException {
		try {
			this.bufferedWriter.write(this.clientID); //Corresponds to line 33 in ClientHandler
			this.bufferedWriter.newLine();
			this.bufferedWriter.flush();
			
			Scanner in = new Scanner(System.in);
			while (this.clientSocket.isConnected()) {
				String msg = in.nextLine();
				
				bufferedWriter.write(msg);
				bufferedWriter.newLine();
				bufferedWriter.flush();
			}
		} catch (IOException e) {
			e.printStackTrace();
			this.terminate();
		}
	}
	
	public void listenForMessage() {
		new Thread(new Runnable() {
			@Override
			public void run() {
				String message;
				
				while (clientSocket.isConnected()) {
					try {
						message = bufferedReader.readLine();
						System.out.println(message);
					} catch (IOException e) {
						try {
							terminate();
						} catch (IOException e1) {
							e1.printStackTrace();
						}
						e.printStackTrace();
						break;
					}
				}
			}
		}).start();
	}
	
	public static void main(String[] args) throws IOException {
		Scanner in = new Scanner(System.in);
		Socket s = new Socket("localhost", 4999);
		
		System.out.println("Enter a username: ");
		String name = in.nextLine();
		Client newClient = new Client(name, s);
		
		newClient.listenForMessage();
		newClient.startClient();
	}
}
