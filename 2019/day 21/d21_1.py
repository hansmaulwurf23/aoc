import datetime
from intcode import IntCodeMachine
import springscript
begin_time = datetime.datetime.now()


def run_spring_script(script, program):
    vm = IntCodeMachine(program.copy())
    return vm.run(springscript.preprocess_script(script))


with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

script = """
# !(A and B and C) ...
NOT A T
NOT T T
AND B T
AND C T
NOT T J
# ... and D
AND D J
WALK
"""

out = run_spring_script(script, program)
springscript.print_output(out)
print(datetime.datetime.now() - begin_time)
