package server2;

import java.io.IOException;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.nio.channels.SelectionKey;
import java.nio.ByteBuffer;
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;
import java.util.Iterator;

import client2.Client;

public class Server {
    private ServerSocket serverSocket;
    private ArrayList<Socket> connectedClients;

    public Server(ServerSocket serverSocket) throws IOException {
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
                } catch (IOException | InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
    }

    public void runServer() throws IOException, InterruptedException {
        try {
            Selector selector = Selector.open();
            ServerSocketChannel serverChannel = ServerSocketChannel.open();
            // Configure server channel:

            serverChannel.bind(new InetSocketAddress(this.serverSocket.getLocalPort()));
            serverChannel.configureBlocking(false);
            serverChannel.register(selector, SelectionKey.OP_ACCEPT);

            BlockingQueue<Socket> threadPipe = new LinkedBlockingQueue<>();        
            this.listenForClients(serverSocket, threadPipe); // Separate thread for receiving incoming clients

            while (!this.serverSocket.isClosed()) {
                /* - Solution: Use a thread-safe queue between the two threads.
                     Similar to inter-process communication using pipe() fork() in C, 
                     use a producer/consumer queue between the two threads. */
                Socket newClient = threadPipe.poll(2, TimeUnit.SECONDS); //wait 3 seconds to dequeue new client
                if (newClient != null) {
                    SocketChannel clientChannel = SocketChannel.open();
                    clientChannel.bind(new InetSocketAddress(newClient.getPort()));
                    clientChannel.configureBlocking(false);
                    clientChannel.register(selector, SelectionKey.OP_READ);
                    this.connectedClients.add(newClient); // add new client to list of connected clients
                }

                selector.select(); // Use the <select> mechanism to check whether a client has sent new change data.
                Set<SelectionKey> selectedKeys = selector.selectedKeys();
                Iterator<SelectionKey> iterator = selectedKeys.iterator();

                ArrayList<byte[]> changeLogs = new ArrayList<>();

                while (iterator.hasNext()) {
                    SelectionKey key = iterator.next();
                    iterator.remove();

                    if (key.isReadable()) { // data is available to be read from this channel
                        SocketChannel clientChannel = (SocketChannel) key.channel();
                        // read and store pkl data
                        ByteBuffer inputBuffer = ByteBuffer.allocate(16384); //16KB buffer
                        int bytesRead = clientChannel.read(inputBuffer);
                        if (bytesRead > 0) {
                            inputBuffer.flip();
                            changeLogs.add(inputBuffer.array());
                        }
                    } else {
                        ;
                    }
                }

                // Write each byte array to a seperate pickle file in a designated folder
                int merge_number = 0;
                for (byte[] changelog: changeLogs) {
                    FileOutputStream outputStream = new FileOutputStream("C:\\Users\\wbirm\\OneDrive\\Desktop\\premerge\\log" + merge_number);
                    merge_number ++;
                }

                // call the merge algorithm in python
                


            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            System.out.println('s');
        }
    }

    public static void main(String[] args) throws IOException, InterruptedException{
        ServerSocket serverSocket = new ServerSocket(4999);
        Server server = new Server(serverSocket);
        server.runServer();
    }
}

