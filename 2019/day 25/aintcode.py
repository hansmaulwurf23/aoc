from intcode import IntCodeMachine

class NoInputException(Exception):

    def __init__(self):
        super().__init__()


class InteractiveIntCodeMachine(IntCodeMachine):

    def __init__(self, program, initial_in, rel_base=0):
        super().__init__(program, rel_base)
        self.in_queue = initial_in

    def read(self):
        if self.in_queue:
            return self.in_queue.pop(0)
        else:
            raise NoInputException

    def write(self, val):
        self.outputs.append(val)

    def run_to_command(self, inputs):
        self.in_queue.extend(inputs)
        lencm = len('Command?')
        try:
            self._run(lambda: self.prog[self.pc] == 99 or not self.in_queue or (len(self.outputs) >= lencm and self.outputs[-1*len('Command?'):] == 'Command?'))
        except NoInputException:
            pass
        if self.prog[self.pc] == 99:
            self.terminated = True
        res = self.outputs.copy()
        self.outputs = []
        return res
