from typing import TYPE_CHECKING
from collections.abc import Sequence
from maspy.learning.core import Model
from maspy.learning.space import Box
from itertools import product
import numpy as np

if TYPE_CHECKING:
    from maspy.environment import Environment, Percept

groups = ["interval", "sequence", "combination", "listed"]

class EnvModel(Model):
    def __init__(self, env: 'Environment') -> None:
        useful_percepts: list[Percept] = []
        percepts = env.perception()
        for _, percept_set in percepts[env._my_name].items():
            for percept in percept_set:
                if percept.group in groups:
                    useful_percepts.append(percept)
                    
        states: dict = {}
        low_states = []
        high_states = []
        for percept in useful_percepts:
            match percept.group:
                case 'combination':
                    ranges = [range(i) for i in percept.args]
                    states[percept.key] = list(product(*ranges))
                case 'listed':
                    assert isinstance(percept.args, Sequence), f"Expected Sequence of values (list/tuple), got {type(percept.args)}"
                    states[percept.key] = percept.args
                case 'interval':
                    assert len(percept.args) == 2, f"Expected 2 values (low, high) for interval, got {len(percept.args)}"
                    assert isinstance(percept.args[0], (int, float)) and isinstance(percept.args[1], (int, float)), f"Expected numeric values, got {type(percept.args[0])} and {type(percept.args[1])}"
                    low_states.append(percept.args[0])
                    high_states.append(percept.args[1])
        if len(low_states) > 0 and len(high_states) > 0 and len(low_states) == len(high_states):
            low = np.array(low_states, dtype=np.float32)
            high = np.array(high_states, dtype=np.float32)
            states['space'] = Box(low, high, (len(low_states),), dtype=np.float32)
            
        actions = env._actions.copy()
        all_actions = []
        for action in actions:
            for arg in action.data:
                all_actions.append(arg)
        state: dict = {}
        keys = states.keys()
        value_lists = states.values()
        all_states = list(product(*value_lists))
            
        self.P: dict = {
            state: {action: [] for action in all_actions}
            for state in all_states
        }
        
        for combination in all_states:
            for key, val in zip(keys, combination):
                state[key] = val
            for action in actions:
                if action.type == 'listed':
                    for args in action.data:
                        if len(action.data) == 1:
                            results = action.func(env,state)
                        else:
                            results = action.func(env,state, args)
                        
                        assert isinstance(results, tuple)
                        new_state: tuple = tuple(results[0].values())
                        reward: float | int = results[1]
                        probability: float = 1.0
                        terminated: bool = False
                        
                        for result in results[2:]:
                            if isinstance(result, float):
                                probability = result
                            elif isinstance(result, bool):
                                terminated = result
                              
                        self.P[combination][args].append((probability, new_state, reward, terminated))
                elif action.type == 'single':
                    
                    pass
                else:
                    print(f"Unsupported action type: {action.type}")
        