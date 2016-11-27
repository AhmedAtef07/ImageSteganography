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
        conceal_image(host_image_path, message_image_path, False)


def conceal_image(host_image_path, message_image_path, preview):
    # Validate that the message image can be concealed within the host image
    # Shape (dimensions) of host image should be larger, otherwise crop message image.
    message_img = convert_to_binary_image(message_image_path, preview)
    host_img = cv2.imread(host_image_path)

    _preview_image("To be concealed message image", message_img, keep_open=True)
    _preview_image("Carrier host image", host_img, keep_open=True)

    _conceal(host_img, message_img)

def _conceal(host_img_array, message_img_array):
    # Convert array of int to array of boolean.
    message_img_array_mask = message_img_array == 0
    message_img_01 = message_img_array_mask.astype(int)

    for r, row in enumerate(message_img_01):
        for c, pixel in enumerate(row):
            host_img_array[r][c] += pixel

    _preview_image("Output", host_img_array)

def convert_to_binary_image(image_path, preview):
    img = cv2.imread(image_path)
    if preview: _preview_image("Original message image", img, keep_open=True)

    img_gray = cv2.imread(image_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    if preview: _preview_image("Gray scale message image", img_gray, keep_open=True)

    (thresh, img_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    if preview:  _preview_image("Black & white message image", img_bw)

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
