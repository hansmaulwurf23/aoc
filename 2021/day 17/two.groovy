def (fx, tx, fy, ty) = new File('./input.txt').text.split(',')*.tokenize('..').flatten()*.replaceAll("[^0-9-]", "")*.toInteger()
if (fy < ty) (fy, ty) = [ty, fy]

// fixme what if y target is not negative
def possVy = [:].withDefault { [] }
def stoppedVy = [:].withDefault { [] }
(0..ty).each { initialVy ->
    def vy = initialVy
    def posY = 0  // since all above is mirrored
    def lastPosY
    def steps = 0
    while (posY >= ty && (lastPosY != posY || initialVy == 0)) {
        lastPosY = posY
        steps++
        posY += vy
        if (posY <= fy && posY >= ty) {
            possVy[steps] << initialVy
            if (initialVy < -1) {
                possVy[(steps+(-1*initialVy*2 - 1))] << (-1 * initialVy - 1)
            }
        }
        vy--
    }

    if (lastPosY <= fy && lastPosY >= ty) {
        stoppedVy[steps] << initialVy
    }
}

//println possVy.collect { k,v -> "[y] $k: ${v.join(',')}"}.join('\n')

// find possible horizontal speeds
// mininum will stop directly at fx -> 1+2+3..+n = n(n+1)/2 >= fx -> n approx sqrt(2*fx)
// maximum is tx
def possVx = [:].withDefault { [] }
def stoppedVx = [:].withDefault { [] }
(((int)(Math.sqrt(2*fx) + 0.5))..(tx)).each { initialVx ->
    def vx = initialVx
    def posX = 0
    def lastPosX
    def steps = 0
    while (posX <= tx && lastPosX != posX) {
        lastPosX = posX
        steps++
        posX += vx
        if (posX >= fx && posX <= tx) possVx[steps] << initialVx
        //print "$posX "
        if (vx > 0) vx--
    }

    if (lastPosX == posX) {
        stoppedVx[steps] << initialVx
        //println "($initialVx)"
    }
}

//println possVx.collect { k,v -> "[x] $k: ${v.join(',')}"}.join('\n')
//println stoppedVx

def launches = [].toSet()
stoppedVx.each { minXsteps, vxs ->
    vxs.each { vx ->
        possVy.findAll { ySteps, vys -> ySteps >= minXsteps }.each { ySteps, vys ->
            launches.addAll(vys.collect { vy -> [vx,vy] })
        }
    }
}

possVx.each { xSteps, vxs ->
    vxs.each { vx ->
        possVy.findAll { ySteps, vys -> ySteps == xSteps }.each { ySteps, vys ->
            launches.addAll(vys.collect { vy -> [vx,vy] })
        }
    }
}

println launches.size()