# library.py

class Stack:
    """A simple Stack implementation using a Python list."""
    def __init__(self):
        self.items = []

    def push(self, item):
        # Add an item to the top of the stack
        self.items.append(item)

    def pop(self):
        # Remove and return the top item; return None if empty
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        # Return the top item without removing it; return None if empty
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        # Check if the stack has no items
        return len(self.items) == 0

    def size(self):
        # Return the number of items in the stack
        return len(self.items)


class EvaluateExpression:
    """Class to evaluate a mathematical expression in infix notation."""
    def __init__(self, expression):
        # Store the math expression string provided by the user
        self.expression = expression

    def evaluate(self):
        """
        Evaluates the stored infix expression using the two-stack algorithm.
        Supports +, -, *, /, and parentheses ().
        """
        # Helper function to define operator precedence
        def precedence(op):
            if op in ('+', '-'): return 1
            if op in ('*', '/'): return 2
            return 0

        # Helper function to apply an operator to two values
        def apply_operator(operators, values):
            operator = operators.pop()
            right = values.pop()
            left = values.pop()
            
            if operator == '+': values.push(left + right)
            elif operator == '-': values.push(left - right)
            elif operator == '*': values.push(left * right)
            elif operator == '/': values.push(left / right)

        # Initialize our two custom stacks
        values = Stack()
        operators = Stack()
        
        i = 0
        # Remove whitespace to make parsing easier
        tokens = self.expression.replace(" ", "")
        
        while i < len(tokens):
            # If the current character is a number, extract the full number
            if tokens[i].isdigit():
                val = 0
                while i < len(tokens) and tokens[i].isdigit():
                    val = (val * 10) + int(tokens[i])
                    i += 1
                values.push(val)
                i -= 1 # Step back because the outer loop will increment i
            
            # If the current character is an opening parenthesis, push to operators
            elif tokens[i] == '(':
                operators.push(tokens[i])
            
            # If closing parenthesis, solve the inner expression
            elif tokens[i] == ')':
                while not operators.is_empty() and operators.peek() != '(':
                    apply_operator(operators, values)
                operators.pop() # Remove the '(' from the stack
            
            # If the current character is an operator
            elif tokens[i] in "+-*/":
                # Apply higher or equal precedence operators first
                while (not operators.is_empty() and 
                       precedence(operators.peek()) >= precedence(tokens[i])):
                    apply_operator(operators, values)
                operators.push(tokens[i])
                
            i += 1
        
        # Apply remaining operators in the stack
        while not operators.is_empty():
            apply_operator(operators, values)
            
        # The final result is the only item left in the values stack
        return values.pop()