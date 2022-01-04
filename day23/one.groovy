def energy = [1L, 10L, 100L, 1000L]
def rooms = [2, 4, 6, 8]
def startApods = [] // in triples of (loc, room, depth) ordered by A-D

def readApods = [:].withDefault { [] }
new File("./input.txt").eachLine { l, lineNo ->
    if (lineNo in [3,4]) {
        def readPods = l[3..9].split('#')
        readPods.eachWithIndex { r, idx ->
            readApods[r] << [-1, (idx+1) * 2, (lineNo - 2)]
        }
    }
}

readApods.sort { it.key }.each {k, apodsOfType ->
    apodsOfType.each {
        startApods << it
    }
}

println startApods

def apodCharByIndex = { idx ->
    "ABCD"[(int)(idx/2)]
}

def printApods = { apods ->
    println "┌-----------┐"
    print "|"
    def hallway = "...........|".split('')
    apods.eachWithIndex { apod, i ->
        def (loc, room, depth) = apod
        if (loc != -1) {
            hallway[loc] = apodCharByIndex(i)
        }
    }
    println hallway.join('')

    [1, 2].each { depth ->
        depth == 1 ? (print("└-┐")) : (print("  |"))
        rooms.each { room ->
            def found = apods.find { it[1] == room && it[2] == depth }
            if (found) {
                print apodCharByIndex(apods.indexOf(found))
            } else {
                print "."
            }
            if (room < 8) print "|"
        }
        depth == 1 ? println("┌-┘") : println("|")
    }

    println "  └-------┘"
}

def countApodsInTheirRooms = { apods ->
    int i = 0
    apods.findAll { apod ->
        def (loc, room, depth) = apod
        if (room == ((int)(i++ / 2) * 2 + 2)) return true
    }.size()
}

def isWayToDestRoomBlocked = { apods, idx, dest ->
    def (loc, room, depth) = apods[idx]
    loc = [loc, room].max()
    def isBlocked = false

    (0..(apods.size()-1)).each { j ->
        //  j is me  or apod not in hallway
        if (j == idx || apods[j][0] == -1) return

        def outsideLoc = apods[j][0]
        // blocked to the left                        or blocked to the right
        if ((dest <= outsideLoc && outsideLoc <= loc) || (loc <= outsideLoc && outsideLoc <= dest)) {
            //printApods(apods)
            isBlocked = true
        }
    }

    isBlocked
}

def calcNextStates = { state ->
    def (cost, apods) = state
    def nextStates = []

    apods.eachWithIndex { apod, i ->
        def type = (int)(i / 2)
        def (loc, room, depth) = apod
        def partnerIdx = type*2 + (1 - i % 2)
        def partner = apods[partnerIdx]
        def destRoom = (type + 1) * 2

        // am i in a room?
        if (room != -1) {
            // in my room?
            if (room == destRoom) {
                // floor
                if (depth == 2) return

                // or with partner?
                if ([partner[2], depth] in [[1, 2], [2, 1]]) {
                    return
                }
            }
        }

        def costMovingOut = room == -1 ? 0 : depth
        def absoluteLoc = [loc, room].max()
        boolean canMove = true

        // check for blocked exit
        if (room != -1 && depth == 2) {
            (0..(apods.size()-1)).each { j->
                if (i == j) return
                if (apods[j][1] == room && apods[j][2] == 1) {
                    canMove = false
                }
            }
        }

        if (canMove) {
            boolean otherApodsInMyDestRoom = ((0..(apods.size()-1)).find { j ->
                //  not me or my partner      or apod is not in a room
                if (j == i || j == partnerIdx || apods[j][1] == -1) {
                    return false
                } else {
                    return (apods[j][1] == destRoom)
                }
            } != null)

            if (!otherApodsInMyDestRoom) {
                if (!isWayToDestRoomBlocked(apods, i, destRoom)) {
                    def howDeep = (partner[1] == destRoom && partner[2] != 1 ? 1 : 2)
                    def stepCost = energy[type] * (Math.abs(absoluteLoc - destRoom) + howDeep + costMovingOut)
                    def updatedApods = apods.clone()
                    updatedApods[i] = [-1, destRoom, howDeep]
                    nextStates << [cost + stepCost, updatedApods]
                }
            }
        }

        // already moved out into hallway and moving home is handled above
        if (room == -1) {
            return
        }

        // blocking exit of room?
        if (!canMove) {
            return
        }

        // find possible locations to move to
        [0, 1, 3, 5, 7, 9, 10].each { hallwayLoc ->
            def stepCost = energy[type] * (Math.abs(room - hallwayLoc) + (depth))
            if (isWayToDestRoomBlocked(apods, i, hallwayLoc)) return

            def updatedApods = apods.clone()
            updatedApods[i] = [hallwayLoc, -1, -1]
            nextStates << [cost + stepCost, updatedApods]
        }
    }

    return nextStates
}

def previousStateMap = [:]
def cost = [:]
def startState = [0, startApods.clone()]
def minimumCost
def endApods
def curApods
def curCost

printApods(startApods)

def visited = [].toSet()
PriorityQueue pq = new PriorityQueue(1, ([compare: { a, b -> a[0] <=> b[0] }] as Comparator))
pq.add(startState)
while (!pq.empty) {
    (curCost, curApods) = pq.poll()
    //println "${pq.size()} ${countApodsInTheirRooms(curApods)} $curCost"

    if (curApods in visited) continue
    visited << curApods

    cost[curApods] = curCost
    if (countApodsInTheirRooms(curApods) == 8) {
        minimumCost = curCost
        endApods = curApods
        break
    }

    calcNextStates([curCost, curApods]).each { nextState ->
        if (nextState[1] in visited) return
        previousStateMap[nextState[1]] = curApods
        pq.add(nextState)
    }
}

curApods = endApods
while (previousStateMap[curApods]) {
    println cost[curApods]
    printApods(curApods)
    curApods = previousStateMap[curApods]
}

println minimumCost
println "13495!"

