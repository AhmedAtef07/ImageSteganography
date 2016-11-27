import Image
import argparse
import cv2

def main():
    parser = argparse.ArgumentParser(prog="Image Steganography",
                                     description='Hide content within images.')

    parser.add_argument('image',
                        type=argparse.FileType(),
                        help='target image path to play with')

    hide_or_extract_group = parser.add_mutually_exclusive_group(required=True)
    hide_or_extract_group.add_argument('-c', '--conceal',
                                       nargs=1,
                                       type=argparse.FileType(),
                                       help='conceal an image within the passed image (takes another image path)')
    hide_or_extract_group.add_argument('-e', '--extract',
                                       action="store_true",
                                       help='extract a hidden image from the given image')

    # Samples for add_arguments

    # parser.add_argument('integers', metavar='N', type=int, nargs='+',
    #                     help='an integer for the accumulator')
    #
    # parser.add_argument('--sum', dest='accumulate', action='store_const',
    #                     const=sum, default=max,
    #                     help='sum the integers (default: find the max)')


    args = parser.parse_args()

    # Validate the given path points to an image

    # print args
    # print args.image
    # print type(args.image)
    # print Image.isImageType(args.image)
    # if not Image.isImageType(args.image):
    #     raise Exception("file provided is not an image")
        # raise argparse.ArgumentError(parser, "file provided is not an image")
    # if args.conceal:
    #     if not Image.isImageType(args.conceal):
    #         raise argparse.ArgumentError(parser, "file provided is not an image")
    #
    # print Image.isImageType(args.image)
    # print(args.accumulate(args.integers))

    print args
    host_image_path = args.image.name
    message_image_path = args.conceal[0].name
    cv2.startWindowThread()
    cv2.namedWindow("Preview")

    message_img = cv2.imread(message_image_path)
    cv2.imshow("Preview", message_img)
    cv2.waitKey()

    message_img_gray = cv2.imread(message_image_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    cv2.imshow("Preview", message_img_gray)
    cv2.waitKey()

    (thresh, message_img_bw) = cv2.threshold(message_img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imshow("Preview", message_img_bw)
    cv2.waitKey()

if __name__ == '__main__':
    main()
