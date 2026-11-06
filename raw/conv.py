from PIL import Image
import glob, os
for p in sorted(glob.glob(r"C:\Users\HXY\assist\ant-fund-proposal\figures_test\m*.png")):
    im = Image.open(p)
    print(os.path.basename(p), im.format, im.size)
    if im.format != "PNG":
        im.convert("RGB").save(p, "PNG")
