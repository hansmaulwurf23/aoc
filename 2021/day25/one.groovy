def map = []
new File("./input.txt").eachLine { l ->
    map << l.split('').collect { it in ['>', 'v'] ? it : null }
}

def maxX = map[0].size() - 1
def maxY = map.size() - 1

printMap = {
    (0..maxY).each { y ->
        (0..maxX).each { x ->
            print (map[y][x] ?: '.')
        }
        println ""
    }
}

def moveLeft = {
    def canMoveCoords = []
    map.eachWithIndex { row, y ->
        row.eachWithIndex{ Object cuc, int x ->
            if (cuc == '>') {
                if (!map[y][(x+1) % (maxX+1)]) canMoveCoords << [x, y]
            }
        }
    }

    canMoveCoords.each { List coord ->
        map[coord[1]][(coord[0]+1) % (maxX+1)] = '>'
        map[coord[1]][coord[0]] = null
    }

    canMoveCoords.size()
}

def moveDown = {
    def canMoveCoords = []
    map.eachWithIndex { row, y ->
        row.eachWithIndex{ Object cuc, int x ->
            if (cuc == 'v') {
                if (!map[(y+1) % (maxY+1)][x]) canMoveCoords << [x, y]
            }
        }
    }

    canMoveCoords.each { List coord ->
        map[(coord[1]+1) % (maxY+1)][coord[0]] = 'v'
        map[coord[1]][coord[0]] = null
    }

    canMoveCoords.size()
}


def step = {
    def moveCounter = moveLeft()
    moveCounter += moveDown()
    moveCounter
}

printMap()
def stepCounter = 1
while(step()) { stepCounter++ }
println stepCounter