# A simple DFA minimizer using table method

## Usage

Create a file containing list of states and transitions:

A brief description of file format:

1. you have 2 sections *[state]* and *[trans]* for sections and transitions respectively
2. put each definition in a new line
3. state definition contains name and 'f' if it is accepting state
4. transition definition is in a form of 'origin' 'symbol' 'target'

Here is an example:

```
[state]
q0
q1 f
q2 f
q3
q4
q5 f

[trans]
q0 0 q1
q0 1 q2
q1 0 q3
q1 1 q4
q2 1 q3
q2 0 q4
q3 0 q5
q3 1 q5
q4 0 q5
q4 1 q5
q5 0 q5
q5 1 q5

```

When launching your program you will be asked for filename of your DFA. After selecting the file, you will get a table view and a list of states to be merged.