def numSeq = null
def fields = []
def currentField = []

new File('./input.txt').eachLine { l, lineNo ->
    if (lineNo == 1) {
        numSeq = l.tokenize(',')*.toInteger()
        return
    }

    if (l.trim()) {
        if (!currentField) {
            currentField = []
            fields << currentField
        }
        currentField << l.tokenize().collect {[val: it.toInteger(), marked: false] }
    } else {
        currentField = []
    }
}

def checkWon = { field ->
    boolean won = false
    field.each { row ->
        if (won) return
        if (row.size() == row.findAll { it.marked }.size()) {
            won = true
        }
    }

    if (won) return won

    def rows = field.size()
    (0..(rows - 1)).each { curIdx ->
        if (won) return
        if (rows == field*.getAt(curIdx).findAll { it.marked }.size()) {
            won = true
        }
    }

    return won
}

def calcWonValue = { field ->
    def val = 0
    field.each { row -> val += (row.findAll { !it.marked }*.val.sum() ?: 0) }
    return val
}

def wonIndexes = []
numSeq.each { curNum ->
    print "\n$curNum "
    fields.eachWithIndex { field, idx ->
        if (!field) return

        print('.')
        field.each { row ->
            row.find { it.val == curNum }?.marked = true
        }
        if (checkWon(field)) {
            wonIndexes << idx
            fields[idx] = []
            print "[${(curNum * calcWonValue(field))}]"
        }
    }
}