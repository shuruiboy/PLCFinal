class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.index = -1
        self.advance()
    
    def advance(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
        else:
            self.current_token = None
    
    def eat(self, token_type):
        if self.current_token is not None and self.current_token.type == token_type:
            self.advance()
        else:
            raise SyntaxError(f"Expected {token_type} but found {self.current_token.type}")
    
    def factor(self):
        token = self.current_token
        if token.type == 'natural_literal':
            self.eat('natural_literal')
            return ('natural_literal', token.value)
        elif token.type == 'real_literal':
            self.eat('real_literal')
            return ('real_literal', token.value)
        elif token.type == 'char_literal':
            self.eat('char_literal')
            return ('char_literal', token.value)
        elif token.type == 'string_literal':
            self.eat('string_literal')
            return ('string_literal', token.value)
        elif token.type == 'bool_literal':
            self.eat('bool_literal')
            return ('bool_literal', token.value)
        elif token.type == 'IDENTIFIER':
            self.eat('IDENTIFIER')
            if self.current_token is not None and self.current_token.type == '(':
                return self.function_call(token.value)
            else:
                return ('IDENTIFIER', token.value)
        elif token.type == '(':
            self.eat('(')
            result = self.expression()
            self.eat(')')
            return result
        elif token.type == '!':
            self.eat('!')
            result = self.factor()
            return ('not', result)
        else:
            raise SyntaxError(f"Expected a factor but found {self.current_token.type}")
    
    def term(self):
        result = self.factor()
        while self.current_token is not None and self.current_token.type in ['*', '/', '%']:
            token = self.current_token
            self.eat(token.type)
            result = ('binary_op', result, token.value, self.factor())
        return result
    
    def expression(self):
        result = self.term()
        while self.current_token is not None and self.current_token.type in ['+', '-']:
            token = self.current_token
            self.eat(token.type)
            result = ('binary_op', result, token.value, self.term())
        return result
    
    def assignment_statement(self):
        identifier_token = self.current_token
        self.eat('IDENTIFIER')
        self.eat('=')
        expr = self.expression()
        return ('assignment', identifier_token.value, expr)
    
    def selection_statement(self):
        self.eat('if')
        self.eat('(')
        condition = self.expression()
        self.eat(')')
        then_block = self.code_block()
        if self.current_token is not None and self.current_token.type == 'else':
            self.eat('else')
            else_block = self.code_block()
            return ('if_else', condition, then_block, else_block)
        else:
            return ('if', condition, then_block)
    
    def loop_statement(self):
        if self.current_token.type == 'while':
            self.eat('while')
            self.eat('(')
            condition = self.expression()
            self.eat(')')
            body = self.code_block()
            return ('while', condition, body)
        elif self.current_token.type == 'do':
            self.eat('do')
            body = self.code
