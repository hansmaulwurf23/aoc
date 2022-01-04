def bitsCounter = null

new File('./input.txt').eachLine { l ->
    def bits = l.collect()*.toInteger()
    if (bitsCounter == null) {
        bitsCounter = bits
    } else {
        bits.eachWithIndex { b, idx ->
            bitsCounter[idx] += (b > 0 ? b : -1)
        }
    }
}

bitsCounter = bitsCounter.collect { it > 0 ? 1 : 0 }
def gammaRate = Integer.parseInt(bitsCounter.join(''), 2)
def epsilonRate = Integer.parseInt(bitsCounter.collect { it == 1 ? 0 : 1}.join(), 2)

println "${gammaRate * epsilonRate}"