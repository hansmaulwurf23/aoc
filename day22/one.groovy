def cubes = new boolean[101][101][101]
def onCounter = 0

def getState = { x, y, z ->
    return cubes[z+50][y+50][x+50]
}

def setState = { x, y, z, state ->
    cubes[z+50][y+50][x+50] = state
}

def setStateAndCount = { x, y, z, state ->
    def oldState = getState(x, y, z)
    if (oldState != state) {
        if (state) onCounter++
        else onCounter--
        setState(x, y, z, state)
    }
}

def parseToRange = { rangeStr ->
    def (from, to) = rangeStr.tokenize('..')*.toInteger()
    return (from..to)
}

def validateRange = { Range r ->
    r.from >= -50 && r.from <= 50 && r.to >= -50 && r.to <= 50
}

def parseToRanges = { ranges ->
    def (xR, yR, zR) = ranges.tokenize(',')*.replaceAll(".=", '')
    return [parseToRange(xR), parseToRange(yR), parseToRange(zR)]
}

def processCommand = { boolean state, xR, yR, zR ->
    xR.each { x ->
        yR.each { y ->
            zR.each { z ->
                setStateAndCount(x, y, z, state)
            }
        }
    }
}

new File('./input.txt').eachLine { l, lineNo ->
    def (state, ranges) = l.tokenize()
    def (xR, yR, zR) = parseToRanges(ranges)
    if (validateRange(xR) && validateRange(yR) && validateRange(zR)) {
        processCommand(state == 'on', xR, yR, zR)
    }
}

println onCounter
