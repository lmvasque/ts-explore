//package pl.waw.ipipan.homados.plainification;

public class Change {
    public static final int KEEP = 0;
    public static final int ADD_BEFORE = 1;
    public static final int ADD_AFTER = 2;
    public static final int DELETE = 3;
    public static final int REPLACE = 4;
    public static final int MOVE = 5;

    public int type;
    public int position;
    public boolean visited;
    public Object replaced;
    public Object replacement;
    public String comment;

    public Change(int type, int position, Object old, Object replacement) {
        this.type = type;
        this.position = position;
        this.replaced = old;
        this.replacement = replacement;
        this.visited = false;
    }

    public String toString() {
        switch (type) {
            case KEEP:
                return "Keeping string at position " + position + ": " + replaced;
            case ADD_BEFORE:
                return "Adding string before position 0: " + replacement;
            case ADD_AFTER:
                return "Adding string after position " + position + ": " + replacement;
            case DELETE:
                return "Deleting string at position " + position + ": " + replaced;
            case REPLACE:
                return "Replacing string at position " + position + ": " + replaced + " with: " + replacement;
        }
        return null;
    }
}
