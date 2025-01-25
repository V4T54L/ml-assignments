import argparse
import os

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='a simple application that allows users to extract text from images using OCR')
    parser.add_argument("image_path", help="path of the image to extract text from.")
    args = parser.parse_args()
    image_path: str = args.image_path
    if not os.path.exists(image_path):
        print("\n\t Invalid filepath provided : ", image_path)
        exit(0)
        

    from utils.reader import Reader
    reader = Reader(['en'])

    try:
        result = reader.readtext(image_path)
        print("====== Extracted text ======")
        for detection in result:
            print(detection[1])
        print("============================")

    except ValueError as e:
        print("\n\t Error opening the file : ", e)
    except Exception as e:
        print("\n\t Unhandled error : ", e)
