package day_18_two

class Btree {
    Integer val
    Btree left
    Btree right
    Btree parent

    Btree(List pair, Btree parent) {
        this.left = new Btree(pair[0], this)
        this.right = new Btree(pair[1], this)
        this.parent = parent
    }

    Btree(Integer val, Btree parent) {
        this.val = val.toInteger()
        this.parent = parent
    }

    Btree(Btree left, Btree right) {
        this.left = left
        this.right = right
        this.left.parent = this.right.parent = this
    }

    Btree findLeftMostWithDepth(int curDepth) {
        if (curDepth == 4) {
            if (val == null) {
                return this
            } else {
                return null
            }
        } else {
            def result = left?.findLeftMostWithDepth(curDepth+1)
            if (!result) result = right?.findLeftMostWithDepth(curDepth+1)
            return result
        }
    }

    Btree findLeftMost(Closure clos) {
        if (clos.call(this)) {
            return this
        } else {
            def res = left?.findLeftMost(clos)
            if (!res) res = right?.findLeftMost(clos)
            return res
        }
    }

    def explode() {
        if (val != null) { println "i shall not be a leaf!" }

        findLeftNeighbor()?.add(left.val)
        findRightNeighbor()?.add(right.val)

        left = null
        right = null
        val = 0
    }

    def rightMostChild() {
        right ? right.rightMostChild() : this
    }

    def leftMostChild() {
        left ? left.leftMostChild() : this
    }

    def findLeftNeighbor() {
        def visitor = this
        while (visitor != null && visitor.parent && visitor == visitor.parent.left) {
            visitor = visitor.parent
        }

        // root?
        if (!visitor.parent) return null

        visitor = visitor.parent.left
        return visitor?.rightMostChild()
    }

    def findRightNeighbor() {
        def visitor = this
        while (visitor != null && visitor.parent && visitor == visitor.parent?.right) {
            visitor = visitor.parent
        }

        // root?
        if (!visitor.parent) return null

        visitor = visitor.parent.right
        return visitor?.leftMostChild()
    }

    def split() {
        left = new Btree((int)(val/2), this)
        right = new Btree((int)(val/2 + 0.5), this)
        val = null
    }

    boolean doReduce() {
        Btree fourDepth = findLeftMostWithDepth(0)
        if (fourDepth) {
            fourDepth.explode()
            return true
        }

        def tenVal = findLeftMost { it.val != null && it.val >= 10 }
        if (tenVal) {
            tenVal.split()
            return true
        }

        return false
    }

    def reduce() {
        while (doReduce()) {}
        return this
    }

    def add(int a) {
        val += a
    }

    def add(Btree another) {
        return new Btree(this, another)
    }

    Long magnitude() {
        if (val != null) {
            return val.toLong()
        } else {
            return (3 * left.magnitude()) + (2 * right.magnitude())
        }
    }

    String toString() {
        if (val != null) {
            return val.toString()
        } else {
            return "[${left.toString()},${right.toString()}]"
        }
    }
}

List numbers = []
new File('./input.txt').eachLine { l, lineNo ->
    numbers << evaluate(l)
}

def maxMagnitude = 0
numbers.eachWithIndex{ entry, int idx ->
    numbers.eachWithIndex { another, int i ->
        if (i == idx) return
        def mag = new Btree(entry, null).add(new Btree(another, null)).reduce().magnitude()
        if (mag > maxMagnitude) {
            maxMagnitude = mag
        }
    }
}

println maxMagnitude