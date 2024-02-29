class State:
    def __init__(self, state, transitions, _type):
        self.state_number = state
        self.transition_table = dict(zip(transitions[::2], transitions[1::2]))

        if "S" in _type:
            FSM.start_state = self
        if "E" in _type:
            FSM.end_states.append(self)

    def transition(self, char):
        next_state = self.transition_table.get(char) or self.transition_table.get("*")
        # print("TRANSITIONING FROM", self.state_number, "TO", next_state, "DUE TO", char)
        return FSM.states[next_state]


class FSM:
    states = {}
    start_state = None
    end_states = []

    def __init__(self):
        with open('str.fsm') as lang:
            data = lang.read().splitlines()

        for line in data:
            state, *transitions, _type = line.split()
            if len(transitions) % 2:
                transitions += _type,
                _type = "N"
            FSM.states[state] = State(state, transitions, _type)

    def process(self, chars):
        cur_state = self.start_state
        for char in chars:
            cur_state = cur_state.transition(char)
        return cur_state

    def verify(self, chars):
        state = self.process(chars)
        if state in self.end_states:
            return f"{chars:<3} -> VALID"
        return f"{chars:<3} -> INVALID"


if __name__ == '__main__':
    fsm = FSM()
    print(fsm.verify("0"))
    print(fsm.verify("01"))
    print(fsm.verify("012"))
