import py4j.GatewayServer;

import java.util.LinkedList;
import java.util.List;

public class WagnerFischerAlgorithmEntryPoint {

    private WagnerFischerAlgorithm editDistance;

    public WagnerFischerAlgorithmEntryPoint() {
        editDistance = new WagnerFischerAlgorithm();
    }

    public WagnerFischerAlgorithm getEditDistance() {

        return editDistance;
    }

    public static void main(String[] args) {
        GatewayServer gatewayServer = new GatewayServer(new WagnerFischerAlgorithmEntryPoint());
        gatewayServer.start();
        System.out.println("Gateway Server Started");
    }
}