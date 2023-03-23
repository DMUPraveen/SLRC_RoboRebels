class FiniteStateMachine:
    def __init__(self, states, initial_state, actions=None):
        """Create a finite state machine.

        Args:
            states (list): List of states.
            initial_state (str): Initial state.
            actions (dict): Dictionary of actions to execute for each state.
        """
        self.states = states
        self.current_state = initial_state
        self.actions = actions
        self.temp_kwargs = dict()
        self.my_parent = None


    def transition_to(self, state):
        """Transition to a new state."""
        if state not in self.states:
            raise ValueError("Invalid state: {}".format(state))
        self.current_state = state


    def tell_parent_switch(self):
        self.my_parent.transition_to_next()
        pass


    def transition_to_next(self):
        """Transition to a next state."""
        current_state_index = self.states.index(self.current_state)
        print(len(self.states), current_state_index)
        if (current_state_index+1)<len(self.states):
            self.current_state = self.states[current_state_index+1]
        else:
            self.my_parent.transition_to_next()

    def dump_kwargs(self):
        self.temp_kwargs = dict()


    def execute_action(self):
        """Execute the action of the current state."""
        #print('Executing ', self.current_state)
        action = self.actions[self.current_state]
        action(self)

class FiniteStateMachineManager():
    def __init__(self, states, initial_state, children=None):
        
        self.states = states
        self.current_state = initial_state
        self.children = children
        self.my_parent = None
        self.set_children_link()


    def set_children_link(self):
        for keys, child in self.children.items():
            print(child)
            child.my_parent = self


    def tell_parent_switch(self):
        self.my_parent.transition_to_next()
        pass


    def transition_to(self, state):
        """Transition to a new state."""
        if state not in self.states:
            raise ValueError("Invalid state: {}".format(state))
        self.current_state = state


    def transition_to_next(self):
        """Transition to a next state."""
        current_state_index = self.states.index(self.current_state)
        print(len(self.states), current_state_index)
        if (current_state_index+1)<len(self.states):
            self.current_state = self.states[current_state_index+1]
        else:
            self.my_parent.transition_to_next()


    def execute_action(self):
        """Execute the action of the current state."""
        self.children[self.current_state].execute_action()
        #print("Executing %s"%(self.current_state))
        