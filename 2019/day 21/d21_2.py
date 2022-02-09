import datetime
from intcode import IntCodeMachine
import springscript
begin_time = datetime.datetime.now()


def run_spring_script(script, program):
    vm = IntCodeMachine(program.copy())
    return vm.run(springscript.preprocess_script(script))


with open('./input.txt') as f:
    program = [int(x) for x in f.readlines()[0].split(',')]

# see notes.txt
# (!A OR ((!B OR !C) AND H) AND D
script = """
# (!B OR !C)
NOT B J
NOT C T
OR T J
# ((..) AND H)
AND H J
# (!A OR (..))
NOT A T
OR T J
# (..) AND D
AND D J
RUN
"""

out = run_spring_script(script, program)
springscript.print_output(out)
print(datetime.datetime.now() - begin_time)
