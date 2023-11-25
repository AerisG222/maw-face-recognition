import os

for root, dirs, files in os.walk('/facetests'):
    print(root)
    print(dirs)
    print(files)
