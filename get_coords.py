"""
Click four corners on an image to get coordinates for transform_example.py.
Output is copy-paste ready for: uv run transform_example.py -i <image> -c "<coords>"
"""
from pyimagesearch.transform import four_point_transform
import numpy as np
import argparse
import cv2


def main():
    ap = argparse.ArgumentParser(description="Click 4 corners to get --coords for transform_example.py")
    ap.add_argument("-i", "--image", required=True, help="path to the image file")
    ap.add_argument("--no-preview", action="store_true", help="only print coords, do not show warped window")
    ap.add_argument("-o", "--out", default=None, help="save warped image to file (e.g. warped_preview.png)")
    args = ap.parse_args()

    image = cv2.imread(args.image)
    if image is None:
        raise FileNotFoundError(f"Could not load image: {args.image}")

    points = []
    show_preview = not args.no_preview
    out_path = args.out
    window_name = "get_coords - click 4 corners (r=reset, q=quit)"

    def redraw():
        display = image.copy()
        for i, (x, y) in enumerate(points):
            cv2.circle(display, (int(x), int(y)), 6, (0, 255, 0), 2)
            cv2.putText(display, str(i + 1), (int(x) + 8, int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow(window_name, display)

    def on_mouse(event, x, y, _flags, param):
        if event != cv2.EVENT_LBUTTONDOWN:
            return
        if len(points) >= 4:
            return
        points.append((x, y))
        redraw()
        if len(points) == 4:
            pts = np.array(points, dtype="float32")
            coords_str = str([(int(x), int(y)) for x, y in points])
            print("Coords (copy for -c):")
            print(coords_str)
            warped = four_point_transform(param["image"], pts)
            if param.get("out_path"):
                cv2.imwrite(param["out_path"], warped)
                print(f"Warped image saved to: {param['out_path']}")
            if param.get("show_preview"):
                cv2.imshow("Warped", warped)

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, on_mouse, {"image": image, "show_preview": show_preview, "out_path": out_path})
    redraw()

    print("Click 4 corners of the document/card (any order). Press 'r' to reset, 'q' or ESC to quit.")
    while True:
        k = cv2.waitKey(1) & 0xFF
        if k == ord("r"):
            points.clear()
            redraw()
            print("Reset. Click 4 corners again.")
        elif k == ord("q") or k == 27:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
