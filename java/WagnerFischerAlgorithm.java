import java.util.HashMap;
import java.util.Map;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;

public class WagnerFischerAlgorithm {

    private Map<Integer, String> operations = get_operations();

    public String calculate_all(String source, String destination) {
        String[] source_end = source.trim().toLowerCase().split(" ");
        String[] destination_end = destination.trim().toLowerCase().split(" ");

        return computeDistance_all(source_end, destination_end);
    }


    public String computeDistance_all(Object[] source, Object[] destination) {
        List<Change> changes = computeDistancePath(source, destination);
        String result = "";

        for (Change change : changes)
            if (change.type != Change.KEEP) {
                result += operations.get(change.type) + "," + change.replaced + "," + change.replacement + "\t";
            }

        return result.substring(0, result.length() - 1);
    }

    public double calculate(String source, String destination, String type) {
        String[] source_end = source.trim().split(" ");
        String[] destination_end = destination.trim().split(" ");

        if (type.equals("distance"))
            return computeDistance(source_end, destination_end);
        else if (type.equals("percentage"))
            return computeDistancePercentage(source_end, destination_end);
        else if (type.equals("analyze"))
            return analyzeReplacements(source_end, destination_end);

        return -1;
    }

    public double computeDistance(Object[] source, Object[] destination) {
        List<Change> changes = computeDistancePath(source, destination);
        int result = 0;
        for (Change change : changes)
            if (change.type != Change.KEEP) {
                System.out.println(operations.get(change.type) + "," + change.replaced + "," + change.replacement);
                result++;
            }

        return result;
    }

    public double computeDistancePercentage(Object[] source, Object[] destination) {
        List<Change> changes = computeDistancePath(source, destination);
        int result = 0;
        for (Change change : changes)
            if (change.type != Change.KEEP)
                result++;
        double percentage = ((double) result / changes.size()) * 100;

        return percentage;
    }

    @SuppressWarnings("unchecked")
    public List<Change> computeDistancePath(Object[] source, Object[] destination) {
        // init distance with zero
        int[][] d = new int[source.length + 1][];

        List<Change>[][] paths = new List[source.length + 1][];
        for (int i = 0; i <= source.length; ++i) {
            d[i] = new int[destination.length + 1];

            paths[i] = new List[destination.length + 1];
            for (int j = 0; j <= destination.length; ++j) {
                d[i][j] = 0;
                paths[i][j] = new LinkedList<Change>();
            }
        }

        // removing source prefix cost
        for (int i = 1; i <= source.length; ++i) {
            d[i][0] = i;
            for (int k = 1; k <= i; ++k)
                paths[i][0].add(new Change(Change.DELETE, k - 1, source[k - 1], null));
        }

        // removing destination prefix cost
        for (int j = 1; j <= destination.length; ++j) {
            d[0][j] = j;
            for (int k = 1; k <= j; ++k)
                paths[0][j].add(new Change(Change.ADD_BEFORE, 0, null, destination[k - 1]));
        }

        // filling in the table
        for (int j = 1; j <= destination.length; ++j)
            for (int i = 1; i <= source.length; ++i) {
                boolean matching = (source[i - 1].equals(destination[j - 1]));

                int costDel = d[i - 1][j] + 1;
                int costIns = d[i][j - 1] + 1;
                int costRepl = d[i - 1][j - 1] + (matching ? 0 : 1);

                if (costDel < costIns && costDel < costRepl) {
                    d[i][j] = costDel;
                    List<Change> path = new LinkedList<Change>(paths[i - 1][j]);
                    path.add(new Change(Change.DELETE, i - 1, source[i - 1], null));
                    paths[i][j] = path;
                } else if (costIns < costRepl) {
                    d[i][j] = costIns;
                    List<Change> path = new LinkedList<Change>(paths[i][j - 1]);
                    path.add(new Change(Change.ADD_AFTER, i - 1, null, destination[j - 1]));
                    paths[i][j] = path;
                } else {
                    d[i][j] = costRepl;
                    List<Change> path = new LinkedList<Change>(paths[i - 1][j - 1]);
                    if (matching)
                        path.add(new Change(Change.KEEP, i - 1, source[i - 1], null));
                    else
                        path.add(new Change(Change.REPLACE, i - 1, source[i - 1], destination[j - 1]));
                    paths[i][j] = path;
                }
            }
        //for (Change step:paths[source.length][destination.length])
        //	System.out.println(step);
        return paths[source.length][destination.length];
    }

    public double analyzeReplacements(Object[] source, Object[] destination) {

        List<Change> changes = computeDistancePath(source, destination);
        int result = 0;
        for (Change change : changes) {

            if (!validChange(change)) {
                int a = 1;
            }
        }

        System.out.println("List Size: " + changes.size());

        return 0;
    }

    private boolean validChange(Change change) {

        String source = (String) change.replaced;
        String target = (String) change.replacement;

        if (change.type == Change.REPLACE) {
            // Is it a word?
            if (source.matches("^\\w+") & target.matches("^\\w+")) {
                System.out.println("Change Word: " + source + " | " + target);
                return true;
            }

            // Is it a compound word?
            if (source.matches("^\\w[\\w+-]+") & target.matches("^\\w[\\w+-]+")) {
                System.out.println("Change CWord: " + source + " | " + target);
                return true;
            }
            // System.out.println("Change False: " + source + " | " + target);
        }

        return false;
    }

    public String countOperations(String source, String destination, String type) {

        String[] source_end = source.trim().split(" ");
        String[] destination_end = destination.trim().split(" ");
        List<Change> changes = computeDistancePath(source_end, destination_end);
        String typeResult = "";

        if (type.toLowerCase().equals("simplify")) {
            changes = simplifyOperations(changes);
        }

        typeResult = "";
        int count = 0;
        for (Change change : changes)
            if (change.type != Change.KEEP) {
                typeResult = typeResult + change.type + "-";
                count++;
            }

        return typeResult;
    }

    public List<Change> simplifyOperations(List<Change> changes) {

        List<Change> newChanges = new LinkedList<>();

        for (Change change : changes) {

            if (!change.visited) {
                if (change.type == Change.DELETE || change.type == Change.ADD_AFTER) {
                    Change newChange = searchMatch(change, changes);
                    newChanges.add(newChange);
                } else {
                    newChanges.add(change);
                }
                change.visited = true;
            }
        }

        return newChanges;
    }

    private Change searchMatch(Change change, List<Change> changes) {
        for (int i = 0; i < changes.size(); i++) {
            Change c = changes.get(i);
            if (change.type == Change.DELETE &&
                    c.type == Change.ADD_AFTER &&
                    change.replaced.equals(c.replacement)) {
                Change newChange = new Change(Change.MOVE, change.position, change.replaced, c.replacement);
                c.visited = true;
                return newChange;

            } else if (change.type == Change.ADD_AFTER &&
                    c.type == Change.DELETE &&
                    change.replacement.equals(c.replaced)) {
                Change newChange = new Change(Change.MOVE, change.position, change.replacement, c.replaced);
                c.visited = true;
                return newChange;
            }

        }

        return change;
    }

    private Map<Integer, String> get_operations(){
        Map<Integer, String> operations = new HashMap<Integer, String>();
        operations.put(0, "KEEP");
        operations.put(1, "ADD_BEFORE");
        operations.put(2, "ADD_AFTER");
        operations.put(3, "DELETE");
        operations.put(4, "REPLACE");
        operations.put(5, "MOVE");
        return operations;
    }



}
