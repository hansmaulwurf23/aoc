import os

import imageio
from PIL import Image, ImageDraw
from PIL.ImageFont import truetype


class Ascii2Gif:

    def __init__(self, folder):
        self.folder = folder

    def render(self, in_memory = False, only_frames = False, gifname = 'render.gif'):
        images = []
        W, H = (800, 800)
        rows, w, h = None, None, None
        fontSize = 12
        font = truetype("DejaVuSansMono.ttf", fontSize)

        files = os.listdir(self.folder)
        file_count = len(files)
        prog = 0
        for fi, f in enumerate(sorted(files)):
            if not f.endswith(".txt"):
                continue

            if int(fi / file_count * 100) != prog:
                prog = int(fi / file_count * 100)
                print(f'{prog}%')
            ascii_text = open(os.path.join(self.folder, f), 'r').read()

            if rows is None:
                lines = ascii_text.splitlines()
                rows = len(lines)
                im = Image.new("RGBA", (W, H), "black")
                draw = ImageDraw.Draw(im)
                w = draw.textlength(lines[0], font=font)
                h = (1.35 * fontSize) * rows
                W, H = int(w + 20), int(h + 20)

            # Draw text to image
            im = Image.new("RGBA", (W, H), "black")
            draw = ImageDraw.Draw(im)

            # draws the text in the center of the image
            draw.text(((W - w) / 2, (H - h) / 2), ascii_text, font=font, fill="white")

            # Save Image
            if in_memory:
                images.append(im)
            else:
                im.save(os.path.join(self.folder, f'{f[0:-4]}.png'))

        if in_memory:
            images[0].save(os.path.join(self.folder, gifname),
                       save_all=True, append_images=images[1:], optimize=False, duration=40, loop=0)
        elif not only_frames:
            with imageio.get_writer(os.path.join(self.folder, gifname), mode='I') as writer:
                for f in sorted(os.listdir(self.folder)):
                    if not f.endswith(".png"):
                        continue
                    image = imageio.imread(os.path.join(self.folder, f))
                    writer.append_data(image)
                    os.remove(os.path.join(self.folder, f))

