def graph = [:].withDefault { [] }
new File('./input.txt').eachLine { l, lineNo ->
    def (from,to) = l.tokenize('-')*.trim()
    if (from == 'end' || to == 'start') graph[to] << from
    else {
        graph[from] << to
        graph[to] << from
    }
}

def isBigCave = { c ->
    c == c.toUpperCase()
}

println graph
def paths = []
def createPath
createPath = { from, thisPath = [] ->
    //println "creating paths from $from ($thisPath)"
    graph[from].each { to ->
        if (to == 'end') {
            def newPath = thisPath.clone()
            newPath << to
            paths << newPath
            return
        }

        // do not enter small caves twice
        if (!isBigCave(to) && to in thisPath) {
            println "not reentering $to ($thisPath)"
            return
        }

        def newPath = thisPath.clone()
        newPath << to
        createPath(to, newPath)
    }
}

createPath('start', ['start'])
println paths*.join('-').join('\n')
println paths.size()