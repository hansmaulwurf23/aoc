def possibleDiceSumCounts = [:].withDefault { 0 }
(1..3).each { a ->
    (1..3).each { b ->
        (1..3).each { c ->
            possibleDiceSumCounts[a+b+c]++
        }
    }
}

def wins = [0L, 0L]
def nextRound
nextRound = { positions, scores, player, sameUniverseCounter ->
    possibleDiceSumCounts.each { diceSum, count ->
        def newPositions = positions.clone()
        def newScores = scores.clone()

        newPositions[player] += diceSum
        if (newPositions[player] > 10) newPositions[player] -= 10

        newScores[player] += newPositions[player]

        if (newScores[player] < 21) {
            nextRound(newPositions, newScores, (player+1)%2, sameUniverseCounter*count)
        } else {
            wins[player] += (sameUniverseCounter*count)
        }
    }
}

def playerPos = []
new File("./input.txt").eachLine { l ->
    def (playerNo, startPos) = l.replaceAll(/Player (\d+) starting position: (\d+)/, "\$1:\$2").tokenize(':')*.toInteger()
    playerPos << startPos
}
nextRound(playerPos, [0, 0], 0, 1L)
println wins.max()