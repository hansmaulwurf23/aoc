def octoLevels = []
def totalFlashes = 0

new File('./input.txt').eachLine { l, lineNo ->
    octoLevels << l.collect { it.toInteger() }
}

def maxX = octoLevels[0].size() - 1
def maxY = octoLevels.size() - 1
def totalOctos = (maxY+1)*(maxX+1)

printGrid = {
    octoLevels.each { row ->
        println row.collect { it.toString().padLeft(3) }
    }
}

def adjacentCoords = { x, y ->
    def result = []
    if (x > 0) result << [x-1,y]
    if (x < maxX) result << [x+1,y]
    if (y > 0) result << [x,y-1]
    if (y < maxY) result << [x,y+1]

    if (x > 0 && y > 0) result << [x-1,y-1]
    if (x > 0 && y < maxY) result << [x-1,y+1]
    if (x < maxX && y > 0) result << [x+1,y-1]
    if (x < maxX && y < maxY) result << [x+1,y+1]
    result
}

def cycle = {
    println "cycle... current flashes $totalFlashes"
    def flashes = []
    def unprocessedFlashes = []
    octoLevels.eachWithIndex { row, y ->
        row.eachWithIndex{ level, x ->
            octoLevels[y][x]++
            if (octoLevels[y][x] == 10) {
                unprocessedFlashes << [x,y]
            }
        }
    }

    // find additional flashes
    while(unprocessedFlashes) {
        def curFlash = unprocessedFlashes.pop()
        def (fx,fy) = curFlash
        octoLevels[fy][fx] = 0
        flashes << [fx,fy]
        adjacentCoords(fx,fy).each { ac ->
            def (x,y) = ac
            if ([x,y] in flashes) return
            octoLevels[y][x]++
            if (octoLevels[y][x] == 10) {
                unprocessedFlashes << [x,y]
            }
        }
    }

    totalFlashes += flashes.size()
    flashes.size()
}

def curStep = 0
def curFlashes = 0
while(curFlashes != totalOctos) {
    curFlashes = cycle()
    curStep++
}

println curStep