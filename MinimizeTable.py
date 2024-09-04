class MinimizeTable:
    def __init__(self, dfa):
        width = dfa.get_state_count() - 1
        if width <= 1:
            raise ValueError('Too small DFA')

        self.dfa = dfa
        self.table = [0] * MinimizeTable.get_table_size(width)
        self.width = width

    def get_tile_index(self, state_0, state_1):
        row = self.dfa.get_state_index(state_0)
        col = self.dfa.get_state_index(state_1)
        if col == row:
            return None
        if col > row:
            row, col = col, row

        row_offset = 0
        for r in range(1, row):
            row_offset += r

        return col + row_offset

    def get_next_tiles(self, state_0, state_1, symbol):
        link_0 = self.dfa.find_link(state_0, symbol)
        link_1 = self.dfa.find_link(state_1, symbol)

        if link_0 is None or link_1 is None:
            return None

        return link_0.state_to, link_1.state_to

    def get_tile(self, state_from, state_to):
        index = self.get_tile_index(state_from, state_to)
        if index is None:
            return 0
        return self.table[index]

    def set_tile(self, state_from, state_to, value):
        index = self.get_tile_index(state_from, state_to)
        if index is not None:
            self.table[index] = value

    def get_pairs(self):
        width = 1
        for i in range(self.width):
            for j in range(width):
                yield i + 1, j
            width += 1

    def analyze(self):
        for pair in self.get_pairs():
            i0, i1 = pair
            s0 = self.dfa.states[i0]
            s1 = self.dfa.states[i1]

            if ((s0.is_final and not s1.is_final) or
                    (not s0.is_final and s1.is_final)):
                self.set_tile(s0, s1, 1)

        pass_index = 1
        was_set = False

        while True:
            pass_index += 1
            was_set = False
            for pair in self.get_pairs():
                i0, i1 = pair
                s0 = self.dfa.states[i0]
                s1 = self.dfa.states[i1]
                if self.get_tile(s0, s1) == 0:
                    for symbol in self.dfa.symbols:
                        if self.get_tile(*self.get_next_tiles(s0, s1, symbol)) > 0:
                            was_set = True
                            self.set_tile(s0, s1, pass_index)
            if not was_set:
                break

        for pair in self.get_pairs():
            i0, i1 = pair
            s0 = self.dfa.states[i0]
            s1 = self.dfa.states[i1]
            if self.get_tile(s0, s1) == 0:
                yield s0.state_name, s1.state_name


    def __str__(self):
        out = ''
        width = 1
        index = 0
        for row in range(self.width):
            row_state = self.dfa.states[row + 1]

            out += '----+{}\n'.format('-----+' * width)
            out += '{:3} |'.format(row_state.state_name)
            for col in range(width):
                out += ' {:3} |'.format(self.table[index])
                index += 1

            out += '\n'
            width += 1

        out += '----+{}\n'.format('-----+' * (width - 1))

        out += '    |'
        for col in range(width - 1):
            col_state = self.dfa.states[col]
            out += ' {:3} |'.format(col_state.state_name)

        out += '\n'
        return out

    @staticmethod
    def get_table_size(width):
        return sum(i for i in range(width + 1))