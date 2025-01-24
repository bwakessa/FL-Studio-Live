package client;

import java.io.FileOutputStream;
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

import java.nio.file.*;
import java.util.Scanner;

public class Client {

	private String clientID;
	private Socket clientSocket;
	private String changeLogPath;

	private FileOutputStream fileOutputStream;
	private InputStream inputStream;
	private OutputStream outputStream;
	private BufferedInputStream bufferedInputStream;
	private BufferedOutputStream bufferedOutputStream;
	
	
	public Client(String clientID, Socket clientSocket, String changeLogPath) throws IOException {
		this.clientID = clientID;
		this.clientSocket = clientSocket;
		this.changeLogPath = changeLogPath;

		this.fileOutputStream = new FileOutputStream(this.changeLogPath);
		this.inputStream = this.clientSocket.getInputStream();
		this.outputStream = this.clientSocket.getOutputStream();
		this.bufferedInputStream = new BufferedInputStream(inputStream);
		this.bufferedOutputStream = new BufferedOutputStream(outputStream);
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
		this.bufferedInputStream.close();
		this.bufferedOutputStream.close();
	}
	
	public void startClient(Client client) throws IOException {
		try {
			Scanner in = new Scanner(System.in);
			while (this.clientSocket.isConnected()) {
				String trigger = in.nextLine();

				if (trigger.equalsIgnoreCase("go")) {
					Path path = Paths.get(this.changeLogPath);// TODO: allow the user to designate this path through the UI
					byte[] fileData = Files.readAllBytes(path); // Get pickled changelog data
					
					int byteLength = 8192; //fileData.length
					bufferedOutputStream.write(fileData, 0, byteLength); // Write changelog data to server
					bufferedOutputStream.flush();

					listenForMergedLog(client);
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
			this.terminate();
		}
	}
	
	public void listenForMergedLog(Client client) {
		// Seperate thread for this client to wait and listen for the server to send a merged changelog
		new Thread(new Runnable() {
			@Override
			public void run() {
				byte[] buffer; // 8KB buffer				
				while (clientSocket.isConnected()) {
					try {
						buffer = new byte[8192];
						int bytesRead = bufferedInputStream.read(buffer); // Read merged log from socket input
						if (bytesRead != -1) {
							client.fileOutputStream.write(buffer, 0, bytesRead); // dump log to designated path
						}
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
		Client newClient = new Client(name, s, "C:\\Users\\wbirm\\OneDrive\\Desktop\\changelog.pkl");
		
		//newClient.listenForMergedLog(newClient);
		newClient.startClient(newClient);
	}
}
