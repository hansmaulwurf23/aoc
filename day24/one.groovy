def reg = [:]

def twentySixes = [
        0:26,
        1:676,
        2:17576,
        3:456976,
        4:11881376,
        5:308915776,
        6:8031810176,
        7:208827064576
]

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

//def testNumber = 12947997819399L
//println runMonad(testNumber)

def d = false
def r = []
(1..14).each { r << (9L..1) }
//r = testNumber.toString().split('')*.toLong().collect { [it] }

def i0 = r[0]

r[0].find {w0 ->
    def extraDigits = 0
    def z0 = w0 + 12
r[1].find { w1 ->
    def z1 = z0 * 26 + w1 + 7
    println "$w0 $w1"
r[2].find { w2 ->
    def z2 = z1 * 26 + w2 + 1
r[3].find { w3 ->
    def z3 = z2 * 26 + w3 + 2
r[4].find { w4 ->
    def x4 = ((z3 % 26) - 5) == w4 ? 0 : 1
    def z4 = (long)(z3 / 26) * (25 * x4 + 1) + ((w4 + 4) * x4)
    if ((z3 % 26) - 5 != w4) extraDigits = 1

r[5].find { w5 ->
    def z5 = z4 * 26 + w5 + 15
r[6].find { w6 ->
    def z6 = z5 * 26 + w6 + 11
r[7].find { w7 ->
    def x7 = ((z6 % 26) - 13) == w7 ? 0 : 1
    def z7 = (long)(z6 / 26) * (25 * x7 + 1) + ((w7+5) * x7)
    if (x7) {
        if (extraDigits) return false
        else extraDigits = 1
    }
    if (z7 > twentySixes[4]) return false

r[8].find { w8 ->
    def x8 = ((z7 % 26) - 16) == w8 ? 0 : 1
    def z8 = (long)(z7 / 26) * (25 * x8 + 1) + ((w8+3) * x8)
    if (x8) {
        if (extraDigits) return false
        else extraDigits = 1
    }

r[9].find { w9 ->
    //if (z8 > (26*26*26*26*26)) return false
    def x9 = ((z8 % 26) - 8) == w9 ? 0 : 1
    def z9 = (long)(z8 / 26) * (25 * x9 + 1) + ((w9+9) * x9)
    if (x9) {
        if (extraDigits) return false
        else extraDigits = 1
    }

r[10].find { w10 ->
    //if (z9 > (26*26*26*26)) return false
    def z10 = z9 * 26 + w10 + 2
    if (z10 > twentySixes[3]) return false

r[11].find { w11 ->
    def x11 = ((z10 % 26) - 8) == w11 ? 0 : 1
    def z11 = (long)(z10 / 26) * (25 * x11 + 1) + ((w11+3) * x11)
    //if (z11 > 26 * 26) return false
    if (x11) {
        if (extraDigits) return false
        else extraDigits = 1
    }
    if (z11 > twentySixes[2]) return false

r[12].find { w12 ->
    def x12 = ((z11 % 26)) == w12 ? 0 : 1
    def z12 = (long)(z11 / 26) * (25 * x12 + 1) + ((w12+3) * x12)
    //if (z12 > 26) return false
    if (x12) {
        if (extraDigits) return false
        else extraDigits = 1
    }
    if (z12 > twentySixes[1]) return false
    
r[13].find { w13 ->
    def x13 = ((z12 % 26) - 4) == w13 ? 0 : 1
    if (x13) return false
    def z13 = (long)(z12 / 26) * (25 * x13 + 1) + ((w13+11) * x13)
    if (d || z13 == 0) {
        println "$w0$w1$w2$w3$w4$w5$w6$w7$w8$w9$w10$w11$w12$w13"
        println "0 $z0 $z1 $z2 $z3 $z4 $z5 $z6 $z7 $z8 $z9 $z10 $z11 $z12 $z13"
        return true
    }
}}}}}}}}}}}}}}


println "12996997819399 >"
//println runMonad(12345678991234)