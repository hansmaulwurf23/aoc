def pop = new File('./input.txt').text.tokenize(',')*.toInteger()
def demo = [:].withDefault { 0 }
demo.putAll(pop.countBy { it })
println demo

def calcFuel = { int pos ->
    demo.collect { x, popSize ->
        Math.abs(x - pos) * popSize
    }.sum()
}

def fuelByPos = [:]
((demo.keySet().min())..(demo.keySet().max())).each { pos ->
    fuelByPos[pos] = calcFuel(pos)
}

def minFuel = fuelByPos.values().min()
println "min fuel $minFuel at ${fuelByPos.findAll { pos, fuel -> fuel == minFuel}}"