class State:
    def __init__(self, state_name, is_final):
        self.state_name = state_name
        self.is_final = is_final
        self.count_in = 0
        self.count_out = 0

    def __eq__(self, other):
        return (self.state_name == other.state_name and
                self.is_final == other.is_final)
