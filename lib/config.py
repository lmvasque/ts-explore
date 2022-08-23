COLORS = ["#006BA4", "#FF800E", "#ABABAB", "#595959", "#5F9ED1", "#C85200", "#898989", "#A2C8EC", "#FFBC79", "#CFCFCF"]
CHANGE_PERCENTAGE_LOWER = "token_based_change_percentage.lower_case"
EDIT_OPERATIONS_TYPES_LOWER = "edit_operations_by_type_lower_case"
LEN_DIFF = "sent_length_source_target"
MARKERS = ["v", "s", "o", "*", "P", "X", "<", "D", "p", ">", "^", "|", "_"]
DATA_SPLITS = ["test", "dev", "train"]
RANDOM_SEED = 324

operations = {
    "0": "KEEP",
    "1": "INSERT",
    "2": "INSERT",
    "3": "DELETE",
    "4": "REPLACE",
    "5": "MOVE"
}