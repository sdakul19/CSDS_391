class puzzle_state:

    def __init__(self):
        self.puzzle_config = ["0", "1", "2", "3", "4", "5", "6", "7", "8"]
        self.empty_pos = 0
        self.parent_node = None
        self.prev_move = None

    