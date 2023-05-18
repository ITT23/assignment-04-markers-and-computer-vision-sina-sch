import argparse
 
def  get_parsed_arguments():
    parser = argparse.ArgumentParser()
 
    # data related arguments
    parser.add_argument(
        "-input", help="Specify the path to the image."
    )
 
    parser.add_argument(
        "-output", help="Specify the path for saving the image.'"
    )
 
    # specify the resolution of the image
    parser.add_argument(
        "-width", help="Specify the width of the image.", type=int
    )

    parser.add_argument(
        "-height", help="Specify the height of the image.", type=int
    )

    return parser.parse_args()
 
