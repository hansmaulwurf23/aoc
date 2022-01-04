def pop = new File('./input.txt').text.tokenize(',')*.toInteger()
def demo = [:].withDefault { 0L }
demo.putAll(pop.countBy { it })
println demo

def dayCycle = {
    def spawners = demo[0]
    def respawners = demo[0]
    (1..8).each {age ->
        demo[age-1] = demo[age]
    }

    demo[8] = spawners
    demo[6] += respawners

}

(1..256).each { day ->
    dayCycle()
    println "day $day - pop size ${demo.values().sum()}"
}