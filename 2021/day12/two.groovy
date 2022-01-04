def graph = [:].withDefault { [] }
new File('./input.txt').eachLine { l, lineNo ->
    def (from,to) = l.tokenize('-')*.trim()
    if (from == 'end' || to == 'start') graph[to] << from
    else {
        graph[from] << to
        graph[to] << from
    }
}

def isBigCave = { String c ->
    def x = c[0].toCharacter()
    x.isLetter() && x.isUpperCase()
}

println graph
def paths = []
def createPath
createPath = { from, List thisPath = [] ->
    //println "creating paths from $from ($thisPath)"
    graph[from].each { to ->
        def newPath = thisPath.clone()

        if (to == 'end') {
            newPath << to
            paths << newPath
            return
        }

        if (to == 'start') return

        // do not enter small caves twice
        if (!isBigCave(to) && to in thisPath) {
            if (thisPath[0] != '_') {
                // add marker for small cave revisited
                newPath.add(0, '_')
            } else {
                //println "not reentering $to ($thisPath)"
                return
            }
        }

        newPath << to
        createPath(to, newPath)
    }
}

createPath('start', ['start'])
println paths.size()