import os
import sys
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

def addInputImageToDataFrame(file, df):
    df['Photo'] = file

def runDetection(faceDbDir, inputDir, outfile):
    resultDf = pd.DataFrame()

    for root, dirs, files in os.walk(inputDir):
        for file in files:
            df = facerec \
                .recognizeFaces(os.path.join(root, file), faceDbDir) \
                .filter(like="0", axis=0)

            # TODO: hmm, the line below removes the identity (matched file from db), rather than the zero at the start...
            # ignore first column, which just contains 0 - representing the index for the best matching face
            # df.drop(columns=df.columns[0], axis=1, inplace=True)

            addInputImageToDataFrame(os.path.join(root, file), df)

            if resultDf.empty:
                resultDf = df
            elif not df.empty:
                resultDf = pd.concat([resultDf, df])

    print(resultDf.to_csv())

def main():
    if len(sys.argv) != 4 :
        show_usage()
        exit(1)

    faceDbDir = sys.argv[1]
    inputDir = sys.argv[2]
    outfile = sys.argv[3]

    if not verify_args(faceDbDir, inputDir, outfile):
        exit(2)

    runDetection(faceDbDir, inputDir, outfile)

main()
