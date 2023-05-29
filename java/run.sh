#!/usr/bin/env bash
CURRENT_PATH=$(pwd)
/usr/bin/javac -Xlint:unchecked -classpath "$CURRENT_PATH":py4j0.10.9.1.jar Change.java WagnerFischerAlgorithm.java WagnerFischerAlgorithmEntryPoint.java
/usr/bin/java -Xms5120m -Xmx5120m -classpath "$CURRENT_PATH":py4j0.10.9.1.jar WagnerFischerAlgorithmEntryPoint
