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
    monadCommands.eachWithIndex { cmdString, idx ->
        def splitCmd = cmdString.split(' ')
        def cmdName = splitCmd[0]
        def args = splitCmd[1..-1]

        if (cmdName == 'inp') {
            println reg
            args << inputs.pop()
        }
        print "[${idx.toString().padLeft(3,' ')}] $cmdName($args)"

        args[1] = (args[1] in reg.keySet() ? reg[args[1]] : args[1].toInteger())
        commands[cmdName].call(args)
        if (reg[splitCmd[-1]] != null) {
            println " ${splitCmd[-1]} = ${reg[splitCmd[-1]]}"
        } else {
            println ""
        }
    }
    return reg.z
}

(9L..1).find {w0 ->
    def z0 = w0 + 12
(9L..1).find { w1 ->
    def z1 = z0 * 26 + w1 + 7
    println "$w0 $w1"
(9L..1).find { w2 ->
    def z2 = z1 * 26 + w2 + 1
(9L..1).find { w3 ->
    def z3 = z2 * 26 + w3 + 2
(9L..1).find { w4 ->
    def x4 = ((z3 % 26) - 5) == w4 ? 0 : 1
    def z4 = (long)(z3 / 26) * (25 * x4 + 1) + ((w4 + 4) * x4)
    if ((z3 % 26) - 5 != w4) return false
(9L..1).find { w5 ->
    def z5 = z4 * 26 + w5 + 15
(9L..1).find { w6 ->
    def z6 = z5 * 26 + w6 + 11
(9L..1).find { w7 ->
    def x7 = ((z6 % 26) - 13) == w7 ? 0 : 1
    def z7 = (long)(z6 / 26) * (25 * x7 + 1) + ((w7+5) * x7)
    if ((z6 % 26) - 13 != w7) return false

(9L..1).find { w8 ->
    def x8 = ((z7 % 26) - 16) == w8 ? 0 : 1
    def z8 = (long)(z7 / 26) * (25 * x8 + 1) + ((w8+3) * x8)
    if ((z7 % 26) - 16 != w8) return false
(9L..1).find { w9 ->
    if (z8 > (26*26*26*26*26)) return false
    def x9 = ((z8 % 26) - 9) == w9 ? 0 : 1
    def z9 = (long)(z8 / 26) * (25 * x9 + 1) + ((w9+9) * x8)
    if (z0 > 26*26) return false
    //if ((z8 % 26) - 9 != w9) return false
(9L..1).find { w10 ->
    //if (z9 > (26*26*26*26)) return false
    def z10 = z9 * 26 + w10 + 2
    if (z10 > 26*26) return false
(9L..1).find { w11 ->
    def x11 = ((z10 % 26) - 8) == w11 ? 0 : 1
    def z11 = (long)(z10 / 26) * (25 * x11 + 1) + ((w11+3) * x11)
    if (z11 > 26) return false
//    if ((z10 % 26) - 8 != w11) return false
//    println "w11 $w11"
(9L..1).find { w12 ->
    def x12 = ((z11 % 26)) == w12 ? 0 : 1
    def z12 = (long)(z11 / 26) * (25 * x12 + 1) + ((w12+3) * x12)
    if (z12 > 26) return false
    //println "$w0 $w1 $w2 $w3 $w4 $w5 $w6 $w7 $w8 $w9 $w10 $w11 $w12 "
    //if ((z11 % 26) != w12) return false
(9L..1).find { w13 ->
    def x13 = ((z12 % 26) - 4) == w13 ? 0 : 1
    if (x13) return false
    def z13 = (long)(z12 / 26) * (25 * x13 + 1) + ((w13+11) * x13)
    if (z13 == 0) {
        println "$w0 $w1 $w2 $w3 $w4 $w5 $w6 $w7 $w8 $w9 $w10 $w11 $w12 $w13"
return true
}}}}}}}}}}}}}}}

//println runMonad(12345678991234)