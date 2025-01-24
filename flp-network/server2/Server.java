package server2;

import java.io.IOException;
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

import client2.Client;

public class Server {
    private ServerSocket serverSocket;
    private ArrayList<Socket> connectedClients;

    public Server(ServerSocket serverSocket) {
        this.serverSocket = serverSocket;
        this.connectedClients = new ArrayList<>();
    }

    public void listenForClients(ServerSocket serverSocket, BlockingQueue<Socket> threadPipe) {
        /* Trying thread handler in a seperate method; if aliasing happens or doesnt work, put it
           back in runServer()
        */
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    while (true) {
                        Socket newClient = serverSocket.accept();
                        threadPipe.put(newClient);
                    }
                } catch (IOException | InterruptedException e){
                    e.printStackTrace();
                }
            }
        });
    }

    public void runServer() throws IOException, InterruptedException {
        try {
            BlockingQueue<Socket> threadPipe = new LinkedBlockingQueue<>();        
            this.listenForClients(serverSocket, threadPipe); // Separate thread for receiving incoming clients

            while (!this.serverSocket.isClosed()) {
                /*  This only supports 2 clients. To support n clients:
                    - have a separate thread to listen for incoming connections
                    - study inter-thread communication to be able to send the new connections back to this thread
                      to be dealt with.
                        - Solution: Use a thread-safe queue between the two threads.
                                    Similar to inter-process communication using pipe() fork() in C, 
                                    use a producer/consumer queue between the two threads. 
                */
                Socket newClient = threadPipe.poll(3, TimeUnit.SECONDS); //wait 3 seconds to dequeue
                if (newClient != null) {
                    this.connectedClients.add(newClient); // add new client to list of connected clients
                }

                // loop through clients and retrieve all their changelogs
                for (Socket client: this.connectedClients) {
                    // read pkl data
                    // TODO: implement this
                }


            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            System.out.println('s');
        }
    }
}

