from intcode import IntCodeMachine


class BroadcastException(Exception):

    def __init__(self, vals):
        self.vals = vals


class IOIntCodeMachine(IntCodeMachine):

    def __init__(self, program, network, initial_in, rel_base=0):
        super().__init__(program, rel_base)
        self.in_queue = initial_in
        self.network = network
        self.processed_read = False
        self.empty_reads = 0
        self.idle = False

    def read(self):
        self.processed_read = True
        if self.in_queue:
            self.idle = False
            self.empty_reads = 0
            return self.in_queue.pop(0)
        else:
            self.empty_reads += 1
            if self.empty_reads >= 2:
                self.idle = True
            return -1

    def write(self, val):
        self.outputs.append(val)
        self.idle = False
        self.unserviced_reads = 0

        if len(self.outputs) == 3:
            dest_addr, x, y = self.outputs
            self.outputs = []

            if dest_addr == 255:
                self.pc += 2
                raise BroadcastException([x, y])
            else:
                self.network[dest_addr].in_queue.append(x)
                self.network[dest_addr].in_queue.append(y)

    def run_to_input(self, inputs):
        self.in_queue.extend(inputs)
        self.processed_read = False
        res = self._run(lambda: self.prog[self.pc] == 99 or self.processed_read)
        if self.prog[self.pc] == 99:
            self.terminated = True
        return res
