CURRENT_PATH=$(pwd)
/usr/bin/javac -Xlint:unchecked -classpath "$CURRENT_PATH":py4j0.10.9.1.jar Change.java WagnerFischerAlgorithm.java WagnerFischerAlgorithmEntryPoint.java
/usr/bin/java -Xms2048m -Xmx2048m -classpath "$CURRENT_PATH":py4j0.10.9.1.jar WagnerFischerAlgorithmEntryPoint
