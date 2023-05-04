import re

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Lexer:
    def __init__(self, code):
        self.code = code
        self.pos = 0
        self.tokens = []
        self.keywords = ['for', 'if', 'else', 'while', 'do', 'int', 'float', 'char', 'bool']
        
    def tokenize(self):
        while self.pos < len(self.code):
            match = None
            
            match = re.match(r'\s', self.code[self.pos])
            if match:
                self.pos += 1
                continue
            
            match = re.match(r'/\*', self.code[self.pos:])
            if match:
                self.pos += 2
                while self.pos < len(self.code):
                    match = re.match(r'\*/', self.code[self.pos:])
                    if match:
                        self.pos += 2
                        break
                    self.pos += 1
                continue
                
            match = re.match(r'//', self.code[self.pos:])
            if match:
                self.pos += 2
                while self.pos < len(self.code):
                    if self.code[self.pos] == '\n':
                        self.pos += 1
                        break
                    self.pos += 1
                continue
            
            match = re.match(r'\d+\.\d+', self.code[self.pos:])
            if match:
                self.tokens.append(Token('real_literal', match.group(0)))
                self.pos += len(match.group(0))
                continue
            
            match = re.match(r'\d+', self.code[self.pos:])
            if match:
                self.tokens.append(Token('natural_literal', match.group(0)))
                self.pos += len(match.group(0))
                continue
            
            match = re.match(r'(true|false)', self.code[self.pos:])
            if match:
                self.tokens.append(Token('bool_literal', match.group(0)))
                self.pos += len(match.group(0))
                continue
            
            match = re.match(r"'(\\.|[^\\'])'", self.code[self.pos:])
            if match:
                self.tokens.append(Token('char_literal', match.group(0)))
                self.pos += len(match.group(0))
                continue
            
            match = re.match(r'"(\\.|[^\\"])*"', self.code[self.pos:])
            if match:
                self.tokens.append(Token('string_literal', match.group(0)))
                self.pos += len(match.group(0))
                continue
            
            match = re.match(r'[a-zA-Z_]\w*', self.code[self.pos:])
            if match:
                value = match.group(0)
                if value in self.keywords:
                    self.tokens.append(Token(value.upper(), value))
                else:
                    self.tokens.append(Token('IDENTIFIER', value))
                self.pos += len(value)
                continue
            
            match = re.match(r'[+\-*/%]|[=!<>]=?|\|\||&&|!|&|\||\^|\(|\)|{|}|\[|\]|,|;|\.', self.code[self.pos:])
            if match:
                self.tokens.append(Token(match.group(0), match.group(0)))
                self.pos += len(match.group(0))
                continue
            
           
