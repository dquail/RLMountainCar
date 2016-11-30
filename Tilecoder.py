numTilings = 4
minX = -0.07
maxX = 0.07
minY = -1.2
maxY = 0.5
tilesPerTiling = 9
tileWidth = (maxX-minX) / (tilesPerTiling -1) #0.6
tileHeight = (maxY-minY) / (tilesPerTiling -1)

tilingOffsetX = tileWidth / numTilings #0.6/8
tilingOffsetY = tileHeight / numTilings

"""
The feature vector contains the state(speed, position), and action (0,1,2)
Therefore, the feature vecor that is used is 9X9X4X3
Consider the vecor split up into 3 sections. The first 1/3 is for action 0. The second is for action 1. Third for action 2

"""
#in1 = speed
#in2 = position
def tilecode(in1,in2, action):
    #The indicie (square) where the value is 1 for each tiling. Do this as an optimiazation rather than storing the entire vector
    if not action in (0,1,2):
        raise Exception("Action must be 0, 1, 2")  
    if (in1 > maxX or in1 < minX):
        raise Exception("Invalid first parameter (speed).  Must be between " + str(minX) + " and " + str(maxX))
    if (in2 > maxY or in1 < minY):
        raise Exception("Invalid second parameter (position). Must be between " + str(minY) + " and " + str(maxY))
    tileIndices = [0] * numTilings

    #shift the input into positive space since tiles start at 0.
    in1-=minX
    in2-=minY
    
    for tiling in range(numTilings):
        
        x = int(in1/tileWidth)
        y = int(in2/tileHeight)
        print("X: " + str(x) + ", y: " + str(y))
        print("Tile width: " + str(tileWidth))
        print("Tile height: " + str(tileHeight))
        index = (y*tilesPerTiling + x) + tiling*tilesPerTiling*tilesPerTiling
        index = index * (action + 1)
        tileIndices[tiling] = index
        in1+=tilingOffsetX
        in2+=tilingOffsetY
    return tileIndices
    
def printTileCoderIndices(in1,in2, action):

    tileIndices = tilecode(in1,in2,action)
    print('Tile indices for input (',in1,',',in2,', ',action,') are : ', tileIndices)

"""
printTileCoderIndices(0.1,0.1)
printTileCoderIndices(4.0,2.0)
printTileCoderIndices(5.99,5.99)
printTileCoderIndices(4.0,2.1)
"""