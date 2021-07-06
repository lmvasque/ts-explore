import org.junit.Test;
import org.junit.Assert;

import static org.junit.Assert.*;

public class WagnerFischerAlgorithmTest {

    private WagnerFischerAlgorithm engine;

    private double calculate(String source, String destination, String type) {
        engine = new WagnerFischerAlgorithm();
        return engine.calculate(source, destination, type);
    }

    private String countOperations(String source, String destination, String type) {
        engine = new WagnerFischerAlgorithm();
        return engine.countOperations(source, destination, type);
    }

    @Test
    public void computeDistance_0change_NOP() {

        // TurkCorpus Test, Edit distance: 0.0
        String source = "their eyes are quite small , and their visual acuity is poor .";
        String destination = "their eyes are quite small , and their visual acuity is poor .";

        assertEquals(0, calculate(source, destination, "distance"), 0);
    }

    @Test
    public void computeDistance_1change_DELETE() {
        // TurkCorpus Test, Edit distance: 0.058823529411764705
        // DELETE
        String source = "addiscombe is a suburb in the london borough of croydon , england .";
        String destination = "addiscombe is a suburb in london borough of croydon , england .";

        assertEquals(1, calculate(source, destination, "distance"), 0);

    }

    @Test
    public void computeDistance_1change_REPLACE() {
        // TurkCorpus Test, Edit distance: 0.08064516129032258, interred => buried
        // REPLACE
        String source = "he is interred in the restvale cemetery in alsip , illinois .";
        String destination = "he is buried in the restvale cemetery in alsip , illinois .";
        assertEquals(1, calculate(source, destination, "distance"), 0);
    }

    @Test
    public void computeDistance_1change_INSERT_REPLACE() {
        // TurkCorpus Test, Edit distance: 0.1111111111111111, lies => is located
        // ADD_AFTER, REPLACE
        String source = "geography the town lies in the limmat valley between baden and zürich .";
        String destination = "geography the town is located in the limmat valley between baden and zürich .";
        assertEquals(2, calculate(source, destination, "distance"), 0);

    }

    @Test
    public void computeDistance_6changes_human_passive_voice() {
        // From https://www.espressoenglish.net/passive-voice-examples-exercises-present-past/
        // REPLACE (4), DELETE (2)
        // Edit distance = 6 / 41 = 0.14
        String source = "The house was painted last week by John .";
        String destination = "John painted the house last week .";

        assertEquals(6, calculate(source, destination, "distance"), 0);


    }

    @Test
    public void computeDistance_13changes_MULTIPLE() {
        // Wiki Auto Train, Edit distance: 0.6666666666666666,
        // DELETE (4), REPLACE (9)

        String source = "Since 1994 , most agree that the photo was an elaborate hoax .";
        String destination = "The image was revealed as a hoax in 1994";
        assertEquals(13, calculate(source, destination, "distance"), 0);

    }

    @Test
    public void computeDistance_21_changes_SPLIT() {
        // HSplit dataset
        // REPLACE (21)
        String source = "prior to the arrival of the storm , the national park service closed visitor centers and campgrounds along the outer banks .";
        String destination = "the National Park Service closed visitor centers and campgrounds along the Outer Banks . it anticipated the arrival of the storm .";
        assertEquals(21, calculate(source, destination, "distance"), 0);
    }

    @Test
    public void computeDistance_25changes_MULTIPLE() {
        // Wiki Manual, Change Percentage: 96.15384615384616
        // REPLACE (20), DELETE (4), REPLACE (1)
        String source = "In government and other administrative systems, \"meritocracy\" refers to a system under which advancement within the system turns on \"merits\", like performance, intelligence, credentials, and education.";
        String destination = "A meritocracy is the condition where people who deserve to can go up in rank, as opposed to a system like nepotism.";
        assertEquals(25, calculate(source, destination, "distance"), 0);
    }

    @Test
    public void computeDistance_common_approach() {
        String source = "prior to the arrival of the storm ,";
        String destination = " it anticipated the arrival of the storm .";
        assertEquals(3, calculate(source, destination, "distance"), 0);
    }

    @Test
    public void countOperations_1_INSERT_1_DELETE() {
        String source = "in computing , kivio is free diagramming software that is part of koffice , an integrated office suite for kde .".toLowerCase();
        String destination = "in computing , kivio is a free diagramming software that is part of koffice , an office suite for kde .".toLowerCase();
        String result = countOperations(source, destination, "simplify");
        assertEquals("2-3-", result);

    }

    @Test
    public void countOperations_2_INSERT_4_REPLACE() {
        String source = "the bells of lüdinghausen allegedly chimed by themselves , whenever liudger entered the town .".toLowerCase();
        String destination = "the bells of lüdinghausen were said to chime by themselves , whenever liudger came to town .".toLowerCase();
        String result = countOperations(source, destination, "simplify");
        assertEquals("2-2-4-4-4-4-", result);
    }

    @Test
    public void countOperations_2_INSERT_5_REPLACE_2_DELETE() {
        String source = "it peaked at # 3 in the uk singles chart .".toLowerCase();
        String destination = "the song was the third most popular in the uk .".toLowerCase();
        String result = countOperations(source, destination, "simplify");
        assertEquals("1-1-4-4-4-4-4-3-3-", result);
    }


    @Test
    public void countOperations_4_DELETE_4_MOVE_3_INSERT() {
        String source = "prior to the arrival of the storm , the national park service closed visitor centers and campgrounds along the outer banks".toLowerCase();
        String destination = " the national park service closed visitor centers and campgrounds along the outer banks . it anticipated the arrival of the storm.".toLowerCase();
        String result = countOperations(source, destination, "simplify");
        assertEquals("3-3-5-5-5-5-3-3-2-2-2-5-2-", result);
    }

    @Test
    public void countOperations_8_DELETE_8_INSERT() {
        String source = "prior to the arrival of the storm , the national park service closed visitor centers and campgrounds along the outer banks".toLowerCase();
        String destination = " the national park service closed visitor centers and campgrounds along the outer banks . it anticipated the arrival of the storm.".toLowerCase();
        String result = countOperations(source, destination, "default");
        assertEquals("3-3-3-3-3-3-3-3-2-2-2-2-2-2-2-2-", result);
    }

}

