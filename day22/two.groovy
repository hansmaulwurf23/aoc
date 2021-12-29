def cuboids = []
def states = [ON: 'on', OFF: 'off']

def parseToFromTo = { rangeStr, axis ->
    def tokenized = rangeStr.tokenize('..')*.toInteger()
    return [("f$axis".toString()): tokenized[0], ("t$axis".toString()): tokenized[1] + 1]
}

def parseCuboidCoords = { ranges ->
    def (xR, yR, zR) = ranges.tokenize(',')*.replaceAll(".=", '')
    return parseToFromTo(xR, 'x') + parseToFromTo(yR, 'y') + parseToFromTo(zR, 'z')
}

// is b completely contained in a?
def contains = { a, b ->
    a.fx <= b.fx && a.tx >= b.tx && a.fy <= b.fy && a.ty >= b.ty && a.fz <= b.fz && a.tz >= b.tz;
}

def intersects = { a, b ->
    a.fx <= b.tx && a.tx >= b.fx && a.fy <= b.ty && a.ty >= b.fy && a.fz <= b.tz && a.tz >= b.fz
}

def intersectionCuboids = { c1, c2 ->
    if (contains(c2, c1)) {
        return []
    }

    if (!intersects(c1, c2)) {
        return [c1]
    }

    def xCoords = [c1.fx] + [c2.fx, c2.tx].findAll { x -> c1.fx < x && x < c1.tx } + [c1.tx]
    def yCoords = [c1.fy] + [c2.fy, c2.ty].findAll { y -> c1.fy < y && y < c1.ty } + [c1.ty]
    def zCoords = [c1.fz] + [c2.fz, c2.tz].findAll { z -> c1.fz < z && z < c1.tz } + [c1.tz]

    def res = []
    (0..(xCoords.size() - 2)).each { i ->
        (0..(yCoords.size() - 2)).each { j ->
            (0..(zCoords.size() - 2)).each { k ->
                res << [state: c1.state, fx: xCoords[i], tx: xCoords[i+1], fy: yCoords[j], ty: yCoords[j+1], fz: zCoords[k], tz: zCoords[k+1]]
            }
        }
    }

    res = res.findAll { !contains(c2, it) }

    return res
}

def processCube = { cuboid ->
    println "processing $cuboid (${cuboids.size()})"
    def newCuboids = []
    cuboids.each { existingCuboid ->
        newCuboids.addAll(intersectionCuboids(existingCuboid, cuboid))
    }
    if (cuboid.state == states.ON) newCuboids << cuboid
    cuboids = newCuboids
}


new File('./input.txt').eachLine { l, lineNo ->
    def (state, ranges) = l.tokenize()
    print "$lineNo "
    processCube([state:state] + parseCuboidCoords(ranges))
}

println cuboids.collect { c -> ((c.tx.toBigInteger()-c.fx)*(c.ty-c.fy)*(c.tz-c.fz)) }.sum()
println "> 1536094744"