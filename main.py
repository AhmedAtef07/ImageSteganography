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

    args = parser.parse_args()
    # Validate the given path points to an image

    if args.conceal:
        host_image_path = args.image.name
        message_image_path = args.conceal[0].name  # Validate this path
        conceal_image(host_image_path, message_image_path, True)


def conceal_image(host_image_path, message_image_path, preview):
    message_img_bw = convert_to_binary_image(message_image_path, preview)


def convert_to_binary_image(image_path, preview):
    img = cv2.imread(image_path)
    if preview: _preview_image("Original message image", img, keep_open=True)

    img_gray = cv2.imread(image_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    if preview: _preview_image("Gray scale message image", img_gray, keep_open=True)

    (thresh, img_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    if preview:  _preview_image("Black & white message image", img_bw, keep_open=True)

    return img_bw


def _preview_image(window_name, cv2_image, **kwargs):
    cv2.startWindowThread()
    cv2.namedWindow(window_name)
    cv2.imshow(window_name, cv2_image)
    cv2.waitKey()
    if not 'keep_open' in kwargs:
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
