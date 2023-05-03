class Compiler:
    def compile_input_file(input_file):
        with open(input_file, 'r') as f:
            input_str = f.read()
        return input_str
