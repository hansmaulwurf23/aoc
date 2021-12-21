def horizontals = []
def verticals = []
def diagonals = []
new File('./input.txt').eachLine { l, lineNo ->
    def (from, to) = l.tokenize('->')*.trim()
    def (fx, fy) = from.tokenize(',')*.toInteger()
    def (tx, ty) = to.tokenize(',')*.toInteger()
    //println "$fx,$fy -> $tx,$ty"
    if (fy == ty) {
        horizontals << [from: fx, to: tx, y: fy]
    } else if (fx == tx) {
        verticals   << [from: fy, to: ty, x: fx]
    } else {
        diagonals << [fx: fx, tx: tx, fy: fy, ty: ty]
    }
}

def maxX = [
        horizontals*.from.max(),
        horizontals*.to.max(),
        verticals*.x.max(),
        diagonals*.fx.max(),
        diagonals*.tx.max()
].max()
def maxY = [
        verticals*.from.max(),
        verticals*.to.max(),
        horizontals*.y.max(),
        diagonals*.fy.max(),
        diagonals*.ty.max()
].max()

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

diagonals.each { entry ->
    def dx = entry.fx < entry.tx ? 1 : -1
    def dy = entry.fy < entry.ty ? 1 : -1
    def curX = entry.fx
    def curY = entry.fy
    while(dx > 0 ? curX <= entry.tx : curX >= entry.tx) {
        battleField[curY][curX]++
        curX += dx
        curY += dy
    }
}

def counter = 0
battleField.each { row ->
    counter += row.findAll { it > 1 }.size()
}

println counter