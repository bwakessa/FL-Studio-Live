package server;

// IO IMPORTS
import java.io.IOException;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedReader;
// INTER-THREAD COMMUNICATION IMPORTS
import java.nio.channels.ServerSocketChannel;
import java.nio.channels.Selector;
import java.nio.channels.SocketChannel;
import java.nio.channels.SelectionKey;
import java.nio.ByteBuffer;

// SOCKET IMPORTS
import java.net.InetSocketAddress;
import java.net.ServerSocket;
import java.net.Socket;

// JAVA UTIL IMPORTS
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;

import java.util.HashMap;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Set;
import java.util.Iterator;

public class Server {
    private ServerSocket serverSocket;
    private ArrayList<Socket> connectedClients;

    public Server(ServerSocket serverSocket) throws IOException {
        this.serverSocket = serverSocket;
        this.connectedClients = new ArrayList<>();
    }

    private void listenForClients(BlockingQueue<Socket> threadPipe) {
        /* - Solution: Use a thread-safe queue between the two threads.
                     Similar to inter-process communication using pipe() fork() in C, 
                     use a producer/consumer queue between the two threads. 
        
        Trying thread handler in a seperate method; if aliasing happens or doesnt work, put it
        back in runServer()
        */
        new Thread(new Runnable() {
            @Override
            public void run() {
                try (ServerSocketChannel listeningChannel = ServerSocketChannel.open()) { 
                    //listeningChannel.configureBlocking(false);
                    listeningChannel.bind(new InetSocketAddress(5000));    
                    listeningChannel.configureBlocking(false);
                    Selector listeningSelector = Selector.open();
                    listeningChannel.register(listeningSelector, SelectionKey.OP_ACCEPT);
                    while (true) {
                        listeningSelector.select(); //Block this thread to wait for a new client connection  
                        for (SelectionKey key : listeningSelector.selectedKeys()) {
                            if (key.isAcceptable()) {
                                SocketChannel clientChannel = listeningChannel.accept();
                                Socket newClient = clientChannel.socket();
                                threadPipe.put(newClient); //Send new client through the thread queue
                            }
                        }               
                    }
                } catch (IOException | InterruptedException e) {
                    e.printStackTrace();                    
                }
            }
        }).start();
    }

    private void handleClient(Socket clientSocket, byte[] mergedLog) {
        /*  TODO: figure out how to return an error to <broadcastToClients> incase the client fails
                  to receive the merged log.
        */ 
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    //BufferedOutputStream bos = new BufferedOutputStream(clientSocket.getOutputStream());
                    //bos.write(mergedLog);
                   // bos.flush();

                    SocketChannel clientChannel = clientSocket.getChannel();

                    ByteBuffer mergelogbuffer = ByteBuffer.wrap(mergedLog);
                    //System.out.println("got here 1");
                    while (mergelogbuffer.hasRemaining()) {
                       // System.out.println("got here 2");
                        clientChannel.write(mergelogbuffer);
                       // System.out.println("got here 3");
                    }

                } catch (IOException e) {
                    e.printStackTrace();
                } 
            }
        }).start();        
    }

    private void broadcastToClients(byte[] mergedLog) {
        /*For each client in <connectedClients>, create a new thread handler to send the merged log to it, so that 
         * it doesn't block in the server's process and potentially cause problems to succeeding clients if a 
         * preceding client fails.
         */
        for (Socket clientSocket: this.connectedClients) {
            handleClient(clientSocket, mergedLog);
        }
    }

    public void runServer() throws IOException, InterruptedException {        
        try {
            Selector selector = Selector.open(); 

            ServerSocketChannel serverChannel = this.serverSocket.getChannel(); // Create and configure server channel for selector
            //serverChannel.bind(this.serverSocket.getLocalSocketAddress());
            //serverChannel.configureBlocking(false);
            serverChannel.register(selector, SelectionKey.OP_ACCEPT);

            BlockingQueue<Socket> threadPipe = new LinkedBlockingQueue<>(); // Thread pipe for inter-thread communication
            this.listenForClients(threadPipe); // Separate thread for receiving incoming clients

            while (!this.serverSocket.isClosed()) {                
                Socket newClient = threadPipe.poll(5, TimeUnit.SECONDS); //wait 2 seconds to dequeue new client
                if (newClient != null) {
                    SocketChannel clientChannel = newClient.getChannel();//SocketChannel.open();
                    //clientChannel.bind(new InetSocketAddress(newClient.getPort()));
                    clientChannel.configureBlocking(false);
                    clientChannel.register(selector, SelectionKey.OP_READ);
                    this.connectedClients.add(newClient); // add new client to list of connected clients
                }
                
                System.out.println("There are " + connectedClients.size() + " clients");
                //TimeUnit.SECONDS.sleep(2);

                if (connectedClients.size() >= 1) {
                    selector.select(); // Use the <select> mechanism to check whether a client has sent new change data.
                    System.out.println("there are " + selector.selectedKeys().size() + " keys");
                    Set<SelectionKey> selectedKeys = selector.selectedKeys();
                    Iterator<SelectionKey> iterator = selectedKeys.iterator();

                    //ArrayList<byte[]> changeLogs = new ArrayList<>();
                    HashMap<byte[], Integer> changeLogs = new HashMap<>();
                    while (iterator.hasNext()) {
                        SelectionKey key = iterator.next();
                        iterator.remove();

                        if (key.isReadable()) { // data is available to be read from this channel
                            SocketChannel clientChannel = (SocketChannel) key.channel();
                            // read and store pkl data
                            ByteBuffer inputBuffer = ByteBuffer.allocate(67108864); //64MB buffer
                            
                            int bytesRead = clientChannel.read(inputBuffer);
                            while (bytesRead > 0) {
                                bytesRead = clientChannel.read(inputBuffer);
                            }
                            
                            if (bytesRead >= 0) {
                                int bufferPosition = inputBuffer.position();
                                inputBuffer.flip();
                                changeLogs.put(inputBuffer.array(), bufferPosition);
                                //changeLogs.add(inputBuffer.array());
                            }
                        } else {;}
                    }

                    System.out.println("There are " + changeLogs.size() + " changelogs...");
                    //TimeUnit.SECONDS.sleep(2);

                    if (changeLogs.size() > 0) {
                        // Write each byte array to a seperate pickle file in a designated folder
                        int merge_number = 0;
                        for (byte[] changelog: changeLogs.keySet()) {
                            
                            System.out.println("Writing changelog " + merge_number + " to pc");
                            //TimeUnit.SECONDS.sleep(2);

                            FileOutputStream outputStream = new FileOutputStream("C:\\Users\\wbirm\\OneDrive\\Desktop\\premerge\\log" + merge_number + ".pkl");
                            outputStream.write(changelog, 0, changeLogs.get(changelog));
                            merge_number ++;
                            outputStream.close();
                        }
                        
                        System.out.println("Calling the python merge algorithm in 2 seconds...");
                        //TimeUnit.SECONDS.sleep(2);

                        // call the merge algorithm in python
                        String[] args = {"python", "C:\\Users\\wbirm\\FL-Studio-Live\\flp_parser\\merge_logs.py"};
                        Process mergeAlgorithm = Runtime.getRuntime().exec(args);

                        System.out.println("Merge algorithm called; Now waiting for merge algorithm to finish...");

                        int exitCode = mergeAlgorithm.waitFor();
                        
                        if (exitCode != 0) {
                            System.out.println("Merge Algorithm finished with code: " + exitCode);
                            BufferedReader errorReader = mergeAlgorithm.errorReader(); 
                            String errline = errorReader.readLine();
                            while (errline != null) {
                                System.out.println("Error: " + errline);
                                errline = errorReader.readLine();
                            }
                        }
                        System.out.println("Merge Algorithm finished with code: " + exitCode);

                        // retrieve the merged log, and broadcast it to all clients
                        FileInputStream inputStream = new FileInputStream("C:\\Users\\wbirm\\OneDrive\\Desktop\\merged_log.pkl");
                        //FileInputStream inputStream = new FileInputStream("C:\\Users\\wbirm\\OneDrive\\Desktop\\premerge\\log0.pkl");
                        byte[] mergedLogBuffer = new byte[67108864]; //64MB buffer;
                        int bytesRead = inputStream.read(mergedLogBuffer);
                        if (bytesRead > 0) {// broadcast merged log to all clients
                            this.broadcastToClients(Arrays.copyOfRange(mergedLogBuffer, 0, bytesRead));
                        }
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            System.out.println('s');
        }
    }

    public static void main(String[] args) throws IOException, InterruptedException{
        ServerSocketChannel serverChannel = ServerSocketChannel.open();
        serverChannel.configureBlocking(false);
        serverChannel.bind(new InetSocketAddress(4999));

        ServerSocket serverSocket = serverChannel.socket();
        Server server = new Server(serverSocket);
        server.runServer();
    }
}

