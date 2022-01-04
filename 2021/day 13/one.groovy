def points = [].toSet()
boolean readPoints = true

def foldX = { x ->
    points.findAll { point -> point[0] > x }.each { point ->
        def diff = point[0] - x
        def newPoint = [x - diff, point[1]]
        points << newPoint
        points.remove(point)
    }
}

def foldY = { y ->
    points.findAll { point -> point[1] > y }.each { point ->
        def diff = point[1] - y
        points << [point[0], y - diff]
        points.remove(point)
    }
}

new File('./input.txt').eachLine { l, lineNo ->
    if (!(l.trim())) {
        println "read ${points.size()} points"
        readPoints = false
        return
    }

    if (readPoints) {
        def (x, y) = l.tokenize(',')*.toInteger()
        points << [x, y]
        return
    }

    def (dir, pos) = l.replace("fold along ", "").tokenize('=')
    if (dir == 'x') foldX(pos.toInteger())
    else            foldY(pos.toInteger())
    println "folding on $dir at $pos -> ${points.size()}"
}

println points.size()