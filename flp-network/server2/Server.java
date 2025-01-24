package server2;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

import client2.Client;

public class Server {
    private ServerSocket serverSocket;

    public Server(ServerSocket serverSocket) {
        this.serverSocket = serverSocket;
    }

    public void runServer() throws IOException {
        try {
            while (!this.serverSocket.isClosed()) {
                /*  This only supports 2 clients. To support n clients:
                    - have a separate thread to listen for incoming connections
                    - study inter-thread communication to be able to send the new connections back to this thread
                      to be dealt with.
                        - Solution: Use a thread-safe queue between the two threads.
                                    Similar to inter-process communication using pipe() fork() in C, 
                                    use a producer/consumer queue between the two threads. 
                */
                Socket client1 = this.serverSocket.accept();
                Socket client2 = this.serverSocket.accept();
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            System.out.println('s');
        }
    }
}

