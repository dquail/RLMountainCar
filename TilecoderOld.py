numTilings = 8
minInput = 0
maxInput = 6
tilesPerTiling = 11
tileSize = (maxInput-minInput) / (tilesPerTiling -1) #0.6
tilingOffset = tileSize / numTilings #0.6/8

def tilecode(in1,in2,tileIndices):
    for tiling in range(numTilings):
        x = int(in1/tileSize)
        y = int(in2/tileSize)
        index = (y*tilesPerTiling + x) + tiling*tilesPerTiling*tilesPerTiling
        tileIndices[tiling] = index
        in1+=tilingOffset
        in2+=tilingOffset
    
def printTileCoderIndices(in1,in2):
    tileIndices = [-1]*numTilings
    tilecode(in1,in2,tileIndices)
    print('Tile indices for input (',in1,',',in2,') are : ', tileIndices)

"""
printTileCoderIndices(0.1,0.1)
printTileCoderIndices(4.0,2.0)
printTileCoderIndices(5.99,5.99)
printTileCoderIndices(4.0,2.1)
"""