def template
def rules = [:]
new File('./input.txt').eachLine { l, lineNo ->
    if (lineNo == 1) {
        template = l
    } else if (l.trim()) {
        def (pattern, creation) = l.tokenize('->')*.trim()
        rules[pattern] = creation
    }
}

def demo = [:].withDefault { 0L }
demo.putAll(template.split('').countBy { it })
println demo

def memoize = [:].withDefault { [:] }

// make sure main is withDefault { 0 }
def mapSum = { main, diff ->
    diff.each { k, v ->
        main[k] += v
    }
    return main
}

def grow
grow = { m, n, restSteps ->
    if (restSteps <= 0) {
        return
    } else if (memoize[m+n][restSteps]) {
        return memoize[m+n][restSteps]
    } else {
        def created = rules[m+n]
        def creations = [:].withDefault { 0L }
        creations.put(created, 1)

        mapSum(creations, grow(m, created, restSteps - 1))
        mapSum(creations, grow(created, n, restSteps - 1))

        memoize[m+n][restSteps] = creations

        return creations
    }
}

(0..(template.size() - 2)).each { pos ->
    println template[pos]
    def createds = grow(template[pos], template[pos+1], 40)
    mapSum(demo, createds)
}

def stats = demo.values().sort { it.value }
println (stats[-1] - stats[0])