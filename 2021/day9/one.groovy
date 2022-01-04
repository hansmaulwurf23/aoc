def heightMap = []
new File('./input.txt').eachLine { l, lineNo ->
    heightMap << l.collect { it.toInteger() }
}

def adjacents = { x, y ->
    def result = []
    if (x > 0) result << heightMap[y][x-1]
    if (x < heightMap[y].size() - 1) result << heightMap[y][x+1]
    if (y > 0) result << heightMap[y-1][x]
    if (y < heightMap.size() - 1) result << heightMap[y+1][x]
    result
}

def lowPoint = { x, y ->
    if (y == 99 && x > 95) {
        println adjacents(x,y)
    }
    return (adjacents(x,y).find { it <= heightMap[y][x] } == null)
}

def lowPoints = []
heightMap.eachWithIndex { row, y ->
    println y
    row.eachWithIndex { val, x ->
        if (lowPoint(x, y)) lowPoints << val
    }
}

println lowPoints
println lowPoints.sum()
println lowPoints.size()
println lowPoints.collect { it + 1 }.sum()