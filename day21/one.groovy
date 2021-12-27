def playerPos = [:]
def playerScore = [:]
def maxPlayerNo = 0
new File("./input.txt").eachLine { l ->
    def (playerNo, startPos) = l.replaceAll(/Player (\d+) starting position: (\d+)/, "\$1:\$2").tokenize(':')*.toInteger()
    playerPos[playerNo] = startPos
    playerScore[playerNo] = 0
    if (playerNo > maxPlayerNo) maxPlayerNo = playerNo
}

def diceRollNo = 1
def curPlayerNo = 1
while (playerScore.values().max() < 1000) {
    3.times {
        playerPos[curPlayerNo] += (diceRollNo++ % 10)
    }

    while (playerPos[curPlayerNo] > 10) {
        playerPos[curPlayerNo] -= 10
    }

    playerScore[curPlayerNo] += playerPos[curPlayerNo]
    println "Player $curPlayerNo now has pos ${playerPos[curPlayerNo]} and points ${playerScore[curPlayerNo]}"
    curPlayerNo = curPlayerNo == maxPlayerNo ? 1 : curPlayerNo+1
}

println (playerScore.values().min() * (diceRollNo-1))