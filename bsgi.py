import MTInterface as mt 
 
direction = 0; 
 
# price was falling, then a doji, then went up 
def isMorningStar(): 
    wasFalling = smaDiff(12, 1) < 0 
    wasDown = (mt.Bars[2].Close - mt.Bars[2].Open) < 0 
    # less than 0.5 pip change 
    wasSmall = abs(mt.Bars[1].Close - mt.Bars[1].Open) < 0.00005 
    wasUp   = (mt.Bars[0].Close - mt.Bars[0].Open) > 0 
    return wasFalling and wasDown and wasSmall and wasUp 
 
# price was rising, then a doji, then fell 
def isEveningStar(): 
    wasRising = smaDiff(12, 1) > 0 
    wasUp = (mt.Bars[2].Close - mt.Bars[2].Open) > 0 
    # less than 0.5 pip change 
    wasSmall = abs(mt.Bars[1].Close - mt.Bars[1].Open) < 0.00005 
    wasDown   = (mt.Bars[0].Close - mt.Bars[0].Open) < 0 
    return wasRising and wasUp and wasSmall and wasDown 
 
# three rising bars in a row 
def isThreeUp(): 
    oneUp   = (mt.Bars[2].Close - mt.Bars[2].Open) > 0 
    twoUp   = (mt.Bars[1].Close - mt.Bars[1].Open) > 0 
    threeUp = (mt.Bars[0].Close - mt.Bars[0].Open) > 0 
    return oneUp and twoUp and threeUp 
 
# three falling bars in a row 
def isThreeDown(): 
    oneDown   = (mt.Bars[2].Close - mt.Bars[2].Open) < 0 
    twoDown   = (mt.Bars[1].Close - mt.Bars[1].Open) < 0 
    threeDown = (mt.Bars[0].Close - mt.Bars[0].Open) < 0 
    return oneDown and twoDown and threeDown 
 
# was trending down, then fell, then rose a small amount, then rose more 
def isThreeInsideUp(): 
    wasFalling = smaDiff(12, 1) < 0 
    wasDown = (mt.Bars[2].Close - mt.Bars[2].Open) < 0 
    wasHalfUp = mt.Bars[1].Close > ((mt.Bars[2].Open + mt.Bars[2].Close)/2) 
    madeRise = mt.Bars[0].Close > mt.Bars[2].Open 
    return wasFalling and wasDown and wasHalfUp and madeRise 
 
# was trending up, then rose, then fell a small amount, then fell more 
def isThreeInsideDown(): 
    wasRising = smaDiff(12, 1) > 0 
    wasUp = (mt.Bars[2].Close - mt.Bars[2].Open) > 0 
    wasHalfDown = mt.Bars[1].Close < ((mt.Bars[2].Open + mt.Bars[2].Close)/2) 
    madeFall = mt.Bars[0].Close < mt.Bars[2].Open 
    return wasRising and wasUp and wasHalfDown and madeFall 
 
# single bar with a long downward shaddow 
def isHammer(): 
    hasLongShaddow = min(mt.Bars[0].Close,mt.Bars[0].Open) - mt.Bars[0].Low > abs(mt.Bars[0].Open - mt.Bars[0].Close) 
    return hasLongShaddow
 
# single bar with a long upward shaddow 
def isShootingStar(): 
    hasLongShaddow = mt.Bars[0].High - max(mt.Bars[0].Close,mt.Bars[0].Open) > abs(mt.Bars[0].Open - mt.Bars[0].Close) 
    return hasLongShaddow 
 
# bar with a very small body (difference in open and close) 
def isDoji(): 
    return abs(mt.Bars[0].Open - mt.Bars[0].Close) < 0.00001 
 
def getDirection(): 
    global direction 
    direction *= 0.9  
    if(isDoji()): 
        direction *= 0.25 
    if(isHammer()): 
        direction += 0.3 
    if(isShootingStar()): 
        direction -= 0.3 
    if(isMorningStar()): 
        direction += 0.8 
    if(isEveningStar()): 
        direction -= 0.8 
    return direction 
 
# rate of change of a simple moving average 
def smaDiff(period, offset): 
    return (mt.Bars[0+offset].Close - mt.Bars[period + offset].Close)/period