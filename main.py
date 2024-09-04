from DFA import DFA
from MinimizeTable import MinimizeTable

if __name__ == '__main__':
    dfa_filename = input('dfa file> ')
    dfa = DFA()
    dfa.read_file(dfa_filename)
    mt = MinimizeTable(dfa)
    merged = list(mt.analyze())
    print(mt)
    print('States that can be merged:')
    for msn0, msn1 in merged:
        print('    \'{}\' with \'{}\''.format(msn0, msn1))