def (fx, tx, fy, ty) = new File('./input.txt').text.split(',')*.tokenize('..').flatten()*.replaceAll("[^0-9-]", "")*.toInteger()
if (fy < ty) (fy, ty) = [ty, fy]

// fixme what if y target is not negative
def possVy = []
(0..ty).each { initialVy ->
    def vy = initialVy
    def posY = 0  // since all above is mirrored
    def lastPosY
    while (posY >= ty) {
        if (lastPosY == posY) break
        lastPosY = posY
        posY += vy
        vy--
    }

    if (lastPosY <= fy && lastPosY >= ty) {
        possVy << initialVy
    }
}

println possVy
def maxNegVelocity = (possVy.min() * -1) - 1
println (maxNegVelocity*(maxNegVelocity+1)/2)