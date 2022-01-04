def horizontals = []
def verticals = []
new File('./input.txt').eachLine { l, lineNo ->
    def (from, to) = l.tokenize('->')*.trim()
    def (fx, fy) = from.tokenize(',')*.toInteger()
    def (tx, ty) = to.tokenize(',')*.toInteger()
    //println "$fx,$fy -> $tx,$ty"
    if (fy == ty) {
        horizontals << [from: fx, to: tx, y: fy]
    } else if (fx == tx) {
        verticals   << [from: fy, to: ty, x: fx]
    }
}

def maxX = [horizontals*.from.max(), horizontals*.to.max(), verticals*.x.max()].max()
def maxY = [verticals*.from.max(), verticals*.to.max(), horizontals*.y.max()].max()
println "Creating battle field of x $maxX and y $maxY"
def battleField = []
(0..(maxY+1)).each { y ->
    def row = []
    (0..(maxX+1)).each { x ->
        row << 0
    }
    battleField << row
}

horizontals.each { entry ->
    ((entry.from)..(entry.to)).each { x ->
        battleField[entry.y][x]++
    }
}

verticals.each { entry ->
    ((entry.from)..(entry.to)).each { y ->
        battleField[y][entry.x]++
    }
}

def counter = 0
battleField.each { row ->
    counter += row.findAll { it > 1 }.size()
}

println counter