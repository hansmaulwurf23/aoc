class IntCodeMachine:

    def __init__(self, program, rel_base=0):
        self.prog = program.copy()
        self.pc = 0
        self.rel_base = rel_base
        self.terminated = False

    def reset(self, program):
        self.prog = program.copy()
        self.pc = 0
        self.rel_base = 0
        self.terminated = False

    def read_op(self, addr, mode):
        real_addr = addr if mode == 1 else self.prog[addr] + (self.rel_base * (mode // 2))
        return self.prog[real_addr] if len(self.prog) > real_addr else 0

    def write_res(self, addr, mode, val):
        real_addr = addr if mode == 1 else self.prog[addr] + (self.rel_base * (mode // 2))
        if len(self.prog) <= real_addr:
            while len(self.prog) <= real_addr:
                self.prog.append(0)
        self.prog[real_addr] = val

    def run_to_output(self, inputs):
        res = self._run(inputs, lambda outputs: self.prog[self.pc] == 99 or len(outputs) >= 1)
        if self.prog[self.pc] == 99 and len(res) < 1:
            self.terminated = True
        return res[0] if len(res) >= 1 else None

    def run(self, inputs):
        res = self._run(inputs, lambda outputs: self.prog[self.pc] == 99)
        self.terminated = True
        return res

    def _run(self, inputs, halt):
        outputs = []

        # while self.prog[self.pc] != 99:
        while not halt(outputs):
            raw = self.prog[self.pc]
            opcode = raw % 10
            param_mode1 = (raw // 100) % 10
            param_mode2 = (raw // 1000) % 10
            param_mode3 = (raw // 10000) % 10

            # add
            if opcode == 1:
                op1 = self.read_op(self.pc + 1, param_mode1)
                op2 = self.read_op(self.pc + 2, param_mode2)
                self.write_res(self.pc + 3, param_mode3, op1 + op2)
                self.pc += 4
            # mul
            elif opcode == 2:
                op1 = self.read_op(self.pc + 1, param_mode1)
                op2 = self.read_op(self.pc + 2, param_mode2)
                self.write_res(self.pc + 3, param_mode3, op1 * op2)
                self.pc += 4
            # read
            elif opcode == 3:
                self.write_res(self.pc + 1, param_mode1, inputs.pop(0))
                self.pc += 2
            # write
            elif opcode == 4:
                op1 = self.read_op(self.pc + 1, param_mode1)
                outputs.append(op1)
                self.pc += 2
            # jump-if-true
            elif opcode == 5:
                op1 = self.read_op(self.pc + 1, param_mode1)
                op2 = self.read_op(self.pc + 2, param_mode2)
                self.pc = op2 if op1 != 0 else self.pc + 3
            # jump-if-false
            elif opcode == 6:
                op1 = self.read_op(self.pc + 1, param_mode1)
                op2 = self.read_op(self.pc + 2, param_mode2)
                self.pc = op2 if op1 == 0 else self.pc + 3
            # less than
            elif opcode == 7:
                op1 = self.read_op(self.pc + 1, param_mode1)
                op2 = self.read_op(self.pc + 2, param_mode2)
                self.write_res(self.pc + 3, param_mode3, 1 if op1 < op2 else 0)
                self.pc += 4
            # equals
            elif opcode == 8:
                op1 = self.read_op(self.pc + 1, param_mode1)
                op2 = self.read_op(self.pc + 2, param_mode2)
                self.write_res(self.pc + 3, param_mode3, 1 if op1 == op2 else 0)
                self.pc += 4
            elif opcode == 9:
                if param_mode1 == 1:
                    self.rel_base += self.prog[self.pc + 1]
                else:
                    self.rel_base += self.prog[self.prog[self.pc + 1] + (self.rel_base * (param_mode1 // 2))]
                self.pc += 2
            else:
                print(f'unknown op code! {opcode}')
                break

        return outputs
