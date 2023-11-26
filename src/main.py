import concurrent.futures
import os
import sys
import time
import cv2
import pandas as pd
import facerec

def show_usage():
    print("A small utility to perform face recognition against photos and a custom face database")
    print("")
    print("Usage: python main.py <face_database_dir> <input_dir> <outfile>")
    print("Where:")
    print("    - face_database_dir: directory containing organized sample images of known people")
    print("    - input_dir: directory containing images to try to identify faces")
    print("    - outfile: full path to csv to write")

def verify_args(faceDbDir, inputDir, outfile):
    isValid = True

    if not os.path.exists(faceDbDir):
        print(f"Face Database Directory [{faceDbDir}] does not exist!  Exiting")
        isValid = False

    if not os.path.exists(inputDir):
        print(f"Input image directory [{inputDir}] does not exist!  Exiting")
        isValid = False

    if os.path.exists(outfile):
        print(f"Output file [{outfile}] exists!  Exiting")
        isValid = False

    return isValid

def addMetadata(file, df):
    height, width, channels = cv2.imread(file).shape

    df['image_height'] = height
    df['image_width'] = width
    df['photo'] = file

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

def runDetections(faceDbDir, inputDir, outfile):
    resultDf = pd.DataFrame()

    print(inputDir)

    start_time = time.time()

    for root, dirs, files in os.walk(inputDir):
        print(f"Processing photos in directory: {root}")

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

    print("--- %s seconds ---" % (time.time() - start_time))

    print(resultDf.to_csv())

if __name__ == '__main__':
    if len(sys.argv) != 4 :
        show_usage()
        exit(1)

    faceDbDir = sys.argv[1]
    inputDir = sys.argv[2]
    outfile = sys.argv[3]

    if not verify_args(faceDbDir, inputDir, outfile):
        exit(2)

    runDetections(faceDbDir, inputDir, outfile)
