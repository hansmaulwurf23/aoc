def start = System.currentTimeMillis()
def reg = [:]

def commands = [
    inp: { r, v -> reg[r] = v },
    add: { a, b -> reg[a] += b },
    mul: { a, b -> reg[a] *= b },
    div: { a, b -> reg[a] = (long)(reg[a] / b) },
    mod: { a, b -> reg[a] %= b },
    eql: { a, b -> reg[a] = (reg[a] == b ? 1 : 0) },
]
def monadCommands =[]
new File("./input.txt").eachLine { l ->
    monadCommands << l
}

def resetRegisters = {
    reg = [w:0, x:0, y:0, z:0L]
}

def runMonad = { Long number ->
    resetRegisters()
    List inputs = number.toString().padLeft(14, '0').split('').reverse()
    println inputs
    def zResults = []
    monadCommands.eachWithIndex { cmdString, idx ->
        def splitCmd = cmdString.split(' ')
        def cmdName = splitCmd[0]
        def args = splitCmd[1..-1]

        if (cmdName == 'inp') {
            println "$reg (${zResults.size() - 1})"
            zResults << reg.z
            args << inputs.pop()
        }
        print "[${idx.toString().padLeft(3,' ')}] $cmdName($args)"

        args[1] = (args[1] in reg.keySet() ? reg[args[1]] : args[1].toInteger())
        commands[cmdName].call(args)
        if (reg[splitCmd[-1]] != null) {
            println " ${splitCmd[-1]}=${reg[splitCmd[-1]]} -> ${splitCmd[-2]}=${reg[splitCmd[-2]]}"
        } else {
            println " -> ${splitCmd[-2]}=${reg[splitCmd[-2]]}"
        }
    }
    println zResults.join(' ')
    return reg.z
}

//def testNumber = 12996997829399
//println runMonad(testNumber)

def digitRanges = []
(1..14).each { digitRanges << (1L..9L) }
//r = testNumber.toString().split('')*.toLong().collect { [it] }
//r[0] = [1,2]
def t0 = 0
def tookTime = 0

Long solution
digitRanges[0].find {w0 ->
    def z0 = w0 + 12

digitRanges[1].find { w1 ->
    def z1 = z0 * 26 + w1 + 7

    if (t0) tookTime = System.currentTimeMillis() - t0
    t0 = System.currentTimeMillis()
    println "$w0 $w1 ${tookTime ? tookTime + 'ms (round) ' + (long)(tookTime*81/1000) + 's overall' : ''}"

digitRanges[2].find { w2 ->
    def z2 = z1 * 26 + w2 + 1

digitRanges[3].find { w3 ->
    def z3 = z2 * 26 + w3 + 2
    digitRanges[4] = [(z3 % 26) - 5].find { it > 0 && it <= 9 }

digitRanges[4].find { w4 ->
    def x4 = ((z3 % 26) - 5) == w4 ? 0 : 1
    def z4 = (long)(z3 / 26) * (25 * x4 + 1) + ((w4 + 4) * x4)

digitRanges[5].find { w5 ->
    def z5 = z4 * 26 + w5 + 15

digitRanges[6].find { w6 ->
    def z6 = z5 * 26 + w6 + 11
    digitRanges[7] = [(z6 % 26) - 13].find { it > 0 && it <= 9 }

digitRanges[7].find { w7 ->
    def x7 = ((z6 % 26) - 13) == w7 ? 0 : 1
    def z7 = (long)(z6 / 26) * (25 * x7 + 1) + ((w7+5) * x7)
    digitRanges[8] = [(z7 % 26) - 16].find { it > 0 && it <= 9 }

digitRanges[8].find { w8 ->
    def x8 = ((z7 % 26) - 16) == w8 ? 0 : 1
    def z8 = (long)(z7 / 26) * (25 * x8 + 1) + ((w8+3) * x8)
    digitRanges[9] = [(z8 % 26) - 8].find { it > 0 && it <= 9 }

digitRanges[9].find { w9 ->
    def x9 = ((z8 % 26) - 8) == w9 ? 0 : 1
    def z9 = (long)(z8 / 26) * (25 * x9 + 1) + ((w9+9) * x9)

digitRanges[10].find { w10 ->
    def z10 = z9 * 26 + w10 + 2
    digitRanges[11] = [(z10 % 26) - 8].find { it > 0 && it <= 9 }

digitRanges[11].find { w11 ->
    def x11 = ((z10 % 26) - 8) == w11 ? 0 : 1
    def z11 = (long)(z10 / 26) * (25 * x11 + 1) + ((w11+3) * x11)
    digitRanges[12] = [(z11 % 26)].find { it > 0 && it <= 9 }

digitRanges[12].find { w12 ->
    def x12 = ((z11 % 26)) == w12 ? 0 : 1
    def z12 = (long)(z11 / 26) * (25 * x12 + 1) + ((w12+3) * x12)
    digitRanges[13] = [(z12 % 26) - 4].find { it > 0 && it <= 9 }
    
digitRanges[13].find { w13 ->
    def x13 = ((z12 % 26) - 4) == w13 ? 0 : 1
    def z13 = (long)(z12 / 26) * (25 * x13 + 1) + ((w13+11) * x13)
    if (z13 == 0) {
        solution = Long.parseLong("$w0$w1$w2$w3$w4$w5$w6$w7$w8$w9$w10$w11$w12$w13")
        println "$x4 $x7 $x8 $x9 $x11 $x12 $x13"
        //println "0 $z0 $z1 $z2 $z3 $z4 $z5 $z6 $z7 $z8 $z9 $z10 $z11 $z12 $z13"
        return true
    }
}}}}}}}}}}}}}}

println solution
println "MAX ${solution == 12996997829399}"
println "MIN ${solution == 11841231117189}"
println "took ${System.currentTimeMillis() - start}ms"