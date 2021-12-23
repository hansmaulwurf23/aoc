def riskGrid = []
def templateGrid = []

new File('./input.txt').eachLine { l, lineNo ->
    if (l.trim()) {
        templateGrid << l.split('')*.toInteger()
    }
}

// multiply cols
templateGrid.each { row ->
    def curRow = row
    (1..4).each {offset ->
        curRow += row.collect { (it + offset >= 10 ? it + offset - 9 : it + offset) }
    }
    riskGrid << curRow
}

// multiply rows
def addRows = []
(1..4).each { offset ->
    riskGrid.each { row ->
        addRows << row.collect { (it + offset >= 10 ? it + offset - 9 : it + offset) }
    }
}
riskGrid += addRows

def printGrid = { g ->
    g.each { row ->
        println row.collect { it.toString().padLeft(5) }.join('')
    }
}

printGrid(riskGrid)

def isInGrid = { x, y ->
    (x >= 0 && y >= 0 && x < riskGrid[0].size() && y < riskGrid.size())
}

def maxX = riskGrid[0].size() - 1
def maxY = riskGrid.size() - 1
def memoize = new int[maxY+1][maxX+1]
println "maxX $maxX maxY $maxY"

def calcPath
calcPath = { x, y ->
    def enteringRisk = riskGrid[y][x]
    def alternatives = []

    if (memoize[y][x]) {
        return memoize[y][x]
    }

    if (x < maxX) alternatives << calcPath(x+1, y)
    if (y < maxY) alternatives << calcPath(x, y+1)

    memoize[y][x] = enteringRisk + (alternatives.min() ?: 0)
    return memoize[y][x]
}

calcPath(1,0)
calcPath(0,1)
//printGrid(memoize)

def adjacents = [[0,1], [1,0], [0,-1], [-1,0]]
def stillBetter = true
while(stillBetter) {
    stillBetter = false
    riskGrid.eachWithIndex { row, y ->
        row.eachWithIndex { cellRisk, x ->
            def alternatives = []
            adjacents.each { adj ->
                def (dx, dy) = adj
                if (isInGrid(x+dx, y+dy)) {
                    alternatives << (memoize[y+dy][x+dx] ?: Integer.MAX_VALUE)
                }
            }

            def orgRisk = memoize[y][x]
            def newRisk = ([orgRisk] + alternatives.collect { it != Integer.MAX_VALUE ? it + cellRisk : Integer.MAX_VALUE}).min()
            if (newRisk < orgRisk) {
                //println "$x,$y now better $newRisk / $orgRisk (cellRisk $cellRisk)"
                stillBetter = true
                memoize[y][x] = newRisk
            }
        }
    }
}

println ([calcPath(1, 0), calcPath(0, 1)].min())
