numTilings = 4
minY = -0.07
maxY = 0.07

minX = -1.2
maxX = 0.5
tilesPerTiling = numTiles = 9
tileWidth = (maxX-minX) / (tilesPerTiling -1)  #0.2125
tileHeight = (maxY-minY) / (tilesPerTiling -1) #0.0175

tilingOffsetX = tileWidth / numTilings #0.6/8
tilingOffsetY = tileHeight / numTilings

"""
The feature vector contains the state(speed, position)
Therefore, the feature vecor that is used is 9X9X4X
"""

def tilecode(in1,in2):

    #print("tilecode: in1:" + str(in1) + " in2: " + str(in2) + " action: " + str(action))
    #The indicie (square) where the value is 1 for each tiling. Do this as an optimiazation rather than storing the entire vector

    if (in1 > maxX or in1 < minX):
        raise Exception("Invalid first parameter (position).  Must be between " + str(minX) + " and " + str(maxX))
    if (in2 > maxY or in2 < minY):
        raise Exception("Invalid second parameter (speed). Must be between " + str(minY) + " and " + str(maxY))
    tileIndices = [0] * numTilings

    #shift the input into positive space since tiles start at 0.
    in1-=minX
    in2-=minY

    for tiling in range(numTilings):

        x = int(in1/tileWidth)
        y = int(in2/tileHeight)
        index = (y*tilesPerTiling + x) + tiling*tilesPerTiling*tilesPerTiling
        #index = index +action*numTiles*numTiles*numTilings
        tileIndices[tiling] = index
        in1+=tilingOffsetX
        in2+=tilingOffsetY
    #print("Tile indices calculated by coder: " + str(tileIndices))
    return tileIndices

    
def printTileCoderIndices(in1,in2, action):

    tileIndices = tilecode(in1,in2,action)
    print('Tile indices for input (',in1,',',in2,', ',action,') are : ', tileIndices)