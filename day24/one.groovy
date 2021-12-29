def reg = [:]

def commands = [
    inp: { r, v -> reg[r] = v },
    add: { a, b -> reg[a] += b },
    mul: { a, b -> reg[a] *= b },
    div: { a, b -> reg[a] = (int)(reg[a] / b) },
    mod: { a, b -> reg[a] %= b },
    eql: { a, b -> reg[a] = (reg[a] == b ? 1 : 0) },
]
def monadCommands =[]
new File("./input.txt").eachLine { l ->
    monadCommands << l
}

def resetRegisters = {
    reg = [w:0, x:0, y:0, z:0]
}

def runMonad = { Long number ->
    resetRegisters()
    List inputs = number.toString().padLeft(14, '0').split('').reverse()
    println inputs
    monadCommands.eachWithIndex { cmdString, idx ->
        def splitCmd = cmdString.split(' ')
        def cmdName = splitCmd[0]
        def args = splitCmd[1..-1]

        if (cmdName == 'inp') args << inputs.pop()
        println "[${idx.toString().padLeft(3,' ')}] $cmdName($args)"

        args[1] = (args[1] in reg.keySet() ? reg[args[1]] : args[1].toInteger())
        commands[cmdName].call(args)
    }
    return reg.z
}

println runMonad(12345678991234)