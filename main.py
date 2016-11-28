import argparse

import cv2
import numpy as np

COLOR_LAYER = 0

def main():
    parser = argparse.ArgumentParser(prog="Image Steganography",
                                     description='Hide content within images.')

    parser.add_argument('image',
                        type=argparse.FileType(),
                        help='target image path to play with')

    hide_or_extract_group = parser.add_mutually_exclusive_group(required=True)
    hide_or_extract_group.add_argument('-ce', '--concealandextract',
                                       nargs=1,
                                       type=argparse.FileType(),
                                       help='conceal an image within the passed image (takes another image path)'
                                            'then extract it back while previewing all the changes')
    hide_or_extract_group.add_argument('-c', '--conceal',
                                       nargs=1,
                                       type=argparse.FileType(),
                                       help='conceal an image within the passed image (takes another image path)')
    hide_or_extract_group.add_argument('-e', '--extract',
                                       action="store_true",
                                       help='extract a hidden image from the given image')

    args = parser.parse_args()
    # Validate the given path points to an image

    host_img_path = args.image.name

    if args.conceal:
        message_img_path = args.conceal[0].name  # Validate this path
        conceal_image(host_img_path, message_img_path, False)
    elif args.extract:
        extract(host_img_path)
    elif args.concealandextract:
        message_img_path = args.concealandextract[0].name  # Validate this path
        conceal_and_extract_image(host_img_path, message_img_path, True)


def conceal_and_extract_image(host_img_path, message_img_path, preview):
    concealed_img = conceal_image(host_img_path, message_img_path, preview)

    extracted_img = _extract(concealed_img, COLOR_LAYER)
    _preview_image("Extracted Image", extracted_img)


def conceal_image(host_img_path, message_img_path, preview):
    # Validate that the message image can be concealed within the host image.
    # Shape (dimensions) of host image should be larger, otherwise crop message image.
    message_img = convert_to_binary_image(message_img_path, preview)
    host_img = cv2.imread(host_img_path)

    _preview_image("Message Image", message_img, keep_open=True)
    _preview_image("Carrier Host Image", host_img, keep_open=True)

    concealed_img = _conceal(host_img, message_img, COLOR_LAYER)
    _preview_image("Concealed Image", concealed_img)

    return concealed_img


def _conceal(host_img_array, message_img_array, layer):
    """ Conceal 1's as even red pixels.
        layer: stands for which color to manipulate, RGBA:
            0: for changing the red layer. (1, green), (2, blue), (3, alpha)
    """
    # Convert array of int to array of boolean.

    message_img_array_mask = message_img_array == 0

    for r, row in enumerate(host_img_array):
        if r == message_img_array_mask.shape[0]:
            break
        for c, pixel in enumerate(row):
            if c == message_img_array_mask.shape[1]:
                break
            if (message_img_array_mask[r][c]):
                # Make it even red pixel, it's a 1.
                if pixel[layer] % 2 != 0:
                    pixel[layer] -= 1
            else:
                # Make it odd red pixel, it's a 0.
                if pixel[layer] % 2 == 0:
                    pixel[layer] += 1

    return host_img_array


def extract(host_img_path):
    host_img = cv2.imread(host_img_path)

    extracted_img = _extract(host_img, COLOR_LAYER)
    _preview_image("Extracted Image", extracted_img)

    return extracted_img


def _extract(host_img_array, layer):
    extracted_img = np.zeros(host_img_array.shape[:2], dtype=np.uint8)

    for r, row in enumerate(host_img_array):
        for c, pixel in enumerate(row):
            if pixel[layer] % 2 != 0:
                extracted_img[r][c] = 255

    return extracted_img


def convert_to_binary_image(img_path, preview):
    img = cv2.imread(img_path)
    if preview: _preview_image("Original Message Image", img, keep_open=True)

    img_gray = cv2.imread(img_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
    if preview: _preview_image("Gray Scale Message Image", img_gray, keep_open=True)

    (thresh, img_bw) = cv2.threshold(img_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    if preview:  _preview_image("Black & White Message Image", img_bw)

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
