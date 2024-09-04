from Link import Link
from State import State


class DFA:
    def __init__(self):
        self.start = None
        self.states = []
        self.links = []
        self.symbols = []

    def try_add_state(self, state_name, is_final):
        new_state = State(state_name, is_final)
        if new_state not in self.states:
            self.states.append(new_state)
            return True
        return False

    def get_state_by_name(self, state_name):
        for state in self.states:
            if state.state_name == state_name:
                return state
        return None

    def add(self, state_name_from, symbol, state_name_to):
        state_from = self.get_state_by_name(state_name_from)
        state_to = self.get_state_by_name(state_name_to)

        if state_from is None or state_to is None:
            return False

        self.links.append(Link(state_from, state_to, symbol))
        if symbol not in self.symbols:
            self.symbols.append(symbol)
        return True

    def get_state_index(self, state):
        return self.states.index(state)

    def get_link_index(self, link):
        return self.links.index(link)

    def find_link(self, state_from, symbol):
        for link in self.links:
            if link.state_from == state_from and link.symbol == symbol:
                return link
        return None

    def get_state_count(self):
        return len(self.states)

    def read_file(self, filename):
        sections = {
            '[state]': 'states',
            '[trans]': 'links'
        }

        def log_error(msg, text, location):
            print('{}: at line {}\n  \'{}\''.format(msg, text, location))

        section = 'none'
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file.readlines(), 1):
                content = line.strip()
                if content == '':
                    continue

                next_section = sections.get(content, None)
                if next_section is not None:
                    section = next_section
                    continue

                tokens = content.split()
                token_count = len(tokens)
                if section == 'states':
                    if token_count > 2:
                        log_error(
                            'expecting <name> or <name> f for final state '
                            'eg. \'s1 f\'',
                            content, line_number)
                        return False
                    is_final = token_count > 1
                    self.try_add_state(tokens[0], is_final)
                    continue
                if section == 'links':
                    if token_count != 3:
                        log_error(
                            'expecting <from> <symbol> <to> '
                            'eg. \'s1 a s2\'',
                            content, line_number)
                        return False
                    self.add(tokens[0], tokens[1], tokens[2])
                    continue
