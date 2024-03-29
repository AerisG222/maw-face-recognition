import concurrent.futures
import os
import pathlib
import sys
import time
import cv2
import pandas as pd
import facerec

def prefix(s):
    return f"* {s}"

def show_usage():
    print(prefix("A small utility to perform face recognition against photos and a custom face database"))
    print(prefix(""))
    print(prefix("Usage: python main.py <face_database_dir> <input_dir> <outfile> <extract_faces>"))
    print(prefix("Where:"))
    print(prefix("    - face_database_dir: directory containing organized sample images of known people"))
    print(prefix("    - input_dir: directory containing images to try to identify faces"))
    print(prefix("    - outfile: full path to csv to write"))
    print(prefix("    - extract_faces: y or n; will save individual matched faces to facilitate review"))

def verify_args(faceDbDir, inputDir, outfile):
    isValid = True

    if not os.path.exists(faceDbDir):
        print(prefix(f"Face Database Directory [{faceDbDir}] does not exist!  Exiting"))
        isValid = False

    if not os.path.exists(inputDir):
        print(prefix(f"Input image directory [{inputDir}] does not exist!  Exiting"))
        isValid = False

    if os.path.exists(outfile):
        print(prefix(f"* Output file [{outfile}] exists!  Exiting"))
        isValid = False

    return isValid

def addMetadata(file, df):
    height, width, channels = cv2.imread(file).shape

    df['image_height'] = height
    df['image_width'] = width
    df['photo'] = file

def extractFoundFace(series, dir):
    srcFilePart = pathlib.Path(series['photo']).stem
    personPart = pathlib.Path(series['identity']).parts[-2]
    facefile = os.path.join(dir, f"{srcFilePart}_{personPart}_{series['source_x']}.jpg")
    top = series['source_y']
    bottom = series['source_y'] + series['source_h']
    left = series['source_x']
    right = series['source_x'] + series['source_w']

    img = cv2.imread(series['photo'])
    face = img[top:bottom, left:right]
    cv2.imwrite(facefile, face)

def extractFoundFaces(df, dir):
    if not os.path.exists(dir):
        os.mkdir(dir)

    df = df.reset_index()
    print(df.to_csv())
    df.apply(extractFoundFace, axis = 1, args = (dir,))

def runDetection(file, faceDbDir):
    df = facerec \
        .recognizeFaces(file, faceDbDir)

    if df.size == 0:
        return pd.DataFrame()

    addMetadata(file, df)

    # matches with index 0 are the best match
    # we pass [0] rather than 0 to identify the best cases so that when there is
    # only one unique face identified (with potentially many matches), we always return a dataframe
    # which is expected by our caller(s)
    return df.loc[[0]]

def runDetections(faceDbDir, inputDir, outfile, extractFaces):
    for root, dirs, files in os.walk(inputDir):
        print(prefix(f"Processing {len(files)} photos in directory: {root}"))

        resultDf = pd.DataFrame()
        start_time = time.time()
        filenames = list(map(lambda f: f"{root}/{f}", files))
        faceDbArgs = [faceDbDir] * len(filenames)

        # manually testing showed that 2 is optimal:
        #  - 1 worker  -> 29.5s
        #  - 2 workers -> 21.5s
        #  - 3 workers -> 23.2s
        #  - 4 workers -> 26.5s
        #  - 8 workers -> 45.2s
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            for file, df in zip(filenames, executor.map(runDetection, filenames, faceDbArgs)):
                if resultDf.empty:
                    resultDf = df
                elif not df.empty:
                    resultDf = pd.concat([resultDf, df])

        seconds = time.time() - start_time

        print(prefix(f"  Time: {round(seconds, 2)}s, Avg: {round(seconds / len(files), 2)}s/photo"))

        with open(outfile, "w") as csv:
            csv.write(resultDf.to_csv())

        if extractFaces:
            extractFoundFaces(resultDf, outfile.replace(".csv", ""))

if __name__ == '__main__':
    if len(sys.argv) != 5 :
        show_usage()
        exit(1)

    faceDbDir = sys.argv[1]
    inputDir = sys.argv[2]
    outfile = sys.argv[3]
    extractFaces = sys.argv[4]

    if not verify_args(faceDbDir, inputDir, outfile):
        exit(2)

    runDetections(faceDbDir, inputDir, outfile, extractFaces == 'y')
