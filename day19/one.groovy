def scans = []
def curScan
new File('./input.txt').eachLine { l, lineNo ->
    if (l.startsWith("---")) {
        if (curScan) scans << curScan
        curScan = [].toSet()
        return
    }

    if (!l.trim()) return

    curScan << l.split(',')*.toInteger()
}
scans << curScan

def vector = { Iterable a, Iterable b ->
    [b[0] - a[0], b[1] - a[1], b[2] - a[2]]
}

def vectorAdd = { Iterable a, Iterable b ->
    [a[0] + b[0], a[1] + b[1], a[2] + b[2]]
}

def directions = [
    { x, y, z -> [x, y, z] },
    { x, y, z -> [x, -y, -z] },
    { x, y, z -> [x, -z, y] },
    { x, y, z -> [-y, -z, x] },
    { x, y, z -> [-x, -z, -y] },
    { x, y, z -> [y, -z, -x] }
]

def flip = { n, coords ->
    coords.collect { directions[n].call(it[0], it[1], it[2]) }
}

def orientations = [
    { x, y, z -> [x, y, z] },
    { x, y, z -> [-y, x, z] },
    { x, y, z -> [-x, -y, z] },
    { x, y, z -> [y, -x, z] }
]

def rotate = { n, coords ->
    coords.collect { orientations[n].call(it[0], it[1], it[2]) }
}

def relativeTo = { point, coords ->
    coords.collect { c ->
        [c[0] - point[0], c[1] - point[1], c[2] - point[2]]
    }
}

def matches = { scan0, scan1 ->
    def matchingVector
    scan0.find { a ->
        scan1.find { b ->
            def v = vector(b, a)
            int matches = 0
            scan0.eachWithIndex { m, idx ->
                if (matches + scan0.size() - idx < 12) return
                if (matchingVector) return
                scan1.each { n ->
                    if (matchingVector) return
                    if (vectorAdd(n, v) == m) matches++
                    if (matches >= 12) matchingVector = v
                }
            }
            matchingVector
        }
    }
    return matchingVector
}

def beaconCoords = [].toSet()
beaconCoords.addAll(scans[0])
def finishedScanners = [0]
def otherScannerPositions = [[0,0,0]] + ([null] * (scans.size() - 2))
def todos = [0]
while (finishedScanners.size() < scans.size()) {
    println "\nnext round"
    (1..scans.size()-1).findAll { !(it in finishedScanners) }.each { scannerIdx ->
        print "\n$scannerIdx"
        def freshFinisheds = []

        (0..orientations.size()-1).find { o ->
            (0..directions.size()-1).find { d ->
                print "."
                todos.find { finishedScannerIdx ->
                    def pos = matches(scans[finishedScannerIdx], rotate(o, flip(d, scans[scannerIdx])))
                    if (pos) {
                        println "$finishedScannerIdx -> $scannerIdx  rot($o) flip($d) v: $pos $finishedScanners"
                        // flip and rotate in org data
                        scans[scannerIdx] = rotate(o, flip(d, scans[scannerIdx]))

                        def relToScanner0 = vectorAdd(pos, otherScannerPositions[finishedScannerIdx])
                        otherScannerPositions[scannerIdx] = relToScanner0
                        beaconCoords.addAll(scans[scannerIdx].collect { n -> vectorAdd(n, relToScanner0) })

                        freshFinisheds << scannerIdx
                        return true
                    }
                }

                freshFinisheds
            }
        }

        finishedScanners.addAll(freshFinisheds)
    }
    todos = finishedScanners - todos
}

//println beaconCoords
println beaconCoords.size()
println "306!"