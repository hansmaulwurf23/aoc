def heightMap = []
new File('./input.txt').eachLine { l, lineNo ->
    heightMap << l.collect { it.toInteger() }
}

def height = { x, y ->
    heightMap[y][x]
}

def adjacentCoords = { x, y ->
    def result = []
    if (x > 0) result << [x-1,y]
    if (x < heightMap[y].size() - 1) result << [x+1,y]
    if (y > 0) result << [x,y-1]
    if (y < heightMap.size() - 1) result << [x,y+1]
    result
}

def adjacentHeights = { x, y ->
    adjacentCoords(x,y).collect { height(it) }
}

def lowPoint = { x, y ->
    if (adjacentHeights(x,y).find { it <= height(x,y) } == null) {
        return [x,y]
    }
}

def calcBasinSize

calcBasinSize = { x, y, basinCoords ->
    if (height(x,y) >= 9) return 0
    def size = 0
    if (!([x,y] in basinCoords)) {
        size++
        basinCoords << [x,y]
    }

    adjacentCoords(x,y).findAll { !(it in basinCoords) }.each { coords ->
        size += calcBasinSize(coords[0], coords[1], basinCoords)
    }

    return size
}

def basins = [:]
heightMap.eachWithIndex { row, y ->
    println y
    row.eachWithIndex { val, x ->
        if (lowPoint(x, y)) {
            basins[[x,y]] = calcBasinSize(x,y, [])
        }
    }
}

sortedBasinSizes = basins*.value.sort().reverse()
println sortedBasinSizes[0] * sortedBasinSizes[1] * sortedBasinSizes[2]