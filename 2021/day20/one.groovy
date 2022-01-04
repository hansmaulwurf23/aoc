def enhancement = []
def img = [].toSet()
def enhancementRun = 0
boolean test = false

new File("./${test ? 'test' : ''}input.txt").eachLine { l, lineNo ->
    if (lineNo == 1) {
        enhancement = l.split('')
    } else if (l.trim()) {
        l.split('').eachWithIndex { c, i ->
            if (c == '#') {
                img << [i, lineNo-3]
            }
        }
    }
}

def getMinMax = {
    return [img*.getAt(0).min(), img*.getAt(1).min(), img*.getAt(0).max(), img*.getAt(1).max()]
}

def (minX, minY, maxX, maxY) = getMinMax()

def printImage = { ->
    (minX..maxY).each { y ->
        (minY..maxX).each { x ->
            print "${[x,y] in img ? '#' : '.'} "
        }
        println ""
    }
}

def enhance = {
    enhancementRun++
    def enhancedImg = [].toSet()
    ((minY-1)..(maxY+1)).each { y ->
        ((minX-1)..(maxX+1)).each { x ->
            int enhanceIndex = 0
            (-1..1).each { yOffset ->
                (-1..1).each { xOffset ->
                    def (px, py) = [x+xOffset, y+yOffset]
                    enhanceIndex = enhanceIndex << 1
                    if ([px,py] in img) {
                        enhanceIndex |= 1
                    } else if ((px < minX || py < minY || px > maxX || py > maxY) && enhancement[0] == '#' && enhancementRun % 2 == 0) {
                        enhanceIndex |= 1
                    }
                }
            }

            if (enhancement[enhanceIndex] == '#') enhancedImg << [x,y]
        }
    }
    img = enhancedImg
    (minX, minY, maxX, maxY) = getMinMax()
}

if (test) printImage()
2.times {
    println "enhancing... img ($maxY x $maxX)"
    enhance()
    if (test) printImage()
}
println img.size()