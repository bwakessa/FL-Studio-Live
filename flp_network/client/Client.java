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

		this.fileOutputStream = new FileOutputStream("C:\\Users\\wbirm\\OneDrive\\Desktop\\merged_changelog.pkl");
		this.inputStream = this.clientSocket.getInputStream();
		this.outputStream = this.clientSocket.getOutputStream();
		this.bufferedInputStream = new BufferedInputStream(this.inputStream);
		this.bufferedOutputStream = new BufferedOutputStream(this.outputStream);
	}

    public String getID() {
		return this.clientID;
	}
	
	public Socket getClientSocket() {
		return this.clientSocket;
	}
	
	public BufferedInputStream getBufferedInputStream() throws IOException {
		return this.bufferedInputStream;
	}
	
	public BufferedOutputStream getBufferedOutputStream() throws IOException {
		return this.bufferedOutputStream;
	}
	
	public void terminate() throws IOException {
		this.clientSocket.close();
		this.bufferedInputStream.close();
		this.bufferedOutputStream.close();
	}

    public void startClient() throws IOException {
        try {
            Scanner in = new Scanner(System.in);
            while (this.clientSocket.isConnected()) {
                String trigger = in.nextLine();
                if (trigger.equalsIgnoreCase("go")) {
                    // ---------- WRITE CHANGELOG TO SERVER ---------- //  
                    Path path = Paths.get(this.changeLogPath); // TODO: allow the user to designate this path through the UI
                    byte[] fileData = Files.readAllBytes(path); // Read pickled changelog data

                    this.bufferedOutputStream.write(fileData, 0, fileData.length); 
                    this.bufferedOutputStream.flush();

                    // ------ READ MERGED CHANGELOG FROM SERVER ------ //
                    byte[] inputBuffer = new byte[67108864]; //64Mb buffer
                    int bytesRead = this.bufferedInputStream.read(inputBuffer); //blocking call
                    if (bytesRead != -1) {
                        this.fileOutputStream.write(inputBuffer, 0, bytesRead); // dump to file
                        System.out.println("get");
                    } else {
                        System.out.println("failed");
                    }
                } else {
                    this.terminate();
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) throws IOException {
        Scanner in = new Scanner(System.in);

        //String ip = "192.168.2.20"; // home ip address
        String ip = "192.168.2.122"; // newman centre ip address
        //String ip = "10.0.0.253"; // boras place
        Socket s = new Socket(ip, 5000);

        // System.out.println("Enter username: ");
        // String name = in.nextLine();
        Client newClient = new Client("poop", s, "C:\\Users\\wbirm\\OneDrive\\Desktop\\changelog.pkl");

        newClient.startClient();        		
    }
}
