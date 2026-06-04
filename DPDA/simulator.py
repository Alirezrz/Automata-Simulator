from dpda import DPDA

GREEN = "\033[92m"
RED   = "\033[91m"
RESET = "\033[0m"

class DPDASimulator:
    
    def run(self, dpda, input_string):
        display_string = input_string if input_string else '(empty)'
        print(f"\nInput string: {display_string}")
        print(f"Acceptance mode: {dpda.acceptance_mode}")
        print()

        current_state = dpda.start_state
        stack = dpda.fresh_stack()
        index = 0 

        print(f"State: {current_state} , Stack: {stack}")

        while True:

            if index < len(input_string):
                current_input = input_string[index]
            
            else:
            
                current_input = 'eps'

            if stack.is_empty():
                break

            stack_top = stack.top()


            transition = dpda.get_transition(current_state, current_input, stack_top)
            if transition is None:
                break

            action  = dpda.describe_action(transition)
            stack  = dpda.apply_transition(stack, transition)
            next_state= transition.to_state

            # only advane input if this was NOT a lambda transition
            if transition.input != 'eps':
                symbol_read = current_input
                index += 1
                
            else:
                symbol_read = 'λ'
                
            print(f"Read {symbol_read} -> {action}")
            print(f"State: {next_state} , Stack: {stack}")
            print()

            current_state = next_state

        input_consumed = (index == len(input_string))
        
        if dpda.acceptance_mode == 'final':
            accepted = input_consumed and dpda.is_accepting_final(current_state)
        else:
            accepted = input_consumed and dpda.is_accepting_empty(stack)

        print(f"Halted at state: {current_state}")
        print(f"Acceptance mode: {dpda.acceptance_mode}")
        if accepted:
            print(f"{GREEN}Result: Accepted{RESET}")
        else:
            print(f"{RED}Result: Rejected{RESET}")
        print()

        return accepted