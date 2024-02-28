import time

import streamlit as st
from streamlit_image_select import image_select

import numpy as np
import imageio.v3 as iio
from PIL import Image
import os
import io
import warnings
import shutil
import time
import base64

warnings.simplefilter("ignore")


def image_to_matrix(image_path):
    # Open the image
    img = Image.open(image_path)

    # Convert Image to gray-scale
    img = img.convert("L")

    # Convert to a binary matrix
    width, height = img.size

    matrix = [[0 if img.getpixel((x, y)) == 255 else 1 for x in range(width)] for y in range(height)]
    return np.array(matrix)


def matrix_to_image(matrix, counter, file_name=None):
    scale = 300 // matrix.shape[0]

    matrix = np.repeat(matrix, scale, axis=1)
    matrix = np.repeat(matrix, scale, axis=0)

    height, width = len(matrix), len(matrix[0])

    img = Image.new("RGB", (width, height))

    for y in range(height):
        for x in range(width):
            if matrix[y][x] == 1:
                img.putpixel((x, y), (0, 0, 0))
            elif matrix[y][x] == 0:
                img.putpixel((x, y), (255, 255, 255))
            elif matrix[y][x] == -2:
                img.putpixel((x, y), (0, 0, 255))

            else:
                img.putpixel((x, y), (0, 255, 0))

    img.save(f"{file_name}/{counter}.png", quality=99)


def step(i, j, fn, matrix=None, deep_path=[], final_path=[], end_point=(0, 0)):
    global counter

    if matrix[end_point] > 0:
        return

    if i < 0 or i >= matrix.shape[0] or j < 0 or j >= matrix.shape[1]:
        return

    if (i, j) in deep_path or matrix[(i, j)] > 0:
        return

    deep_path.append((i, j))
    final_path.append((i, j))
    counter += 1
    matrix[(i, j)] = counter
    matrix_to_image(matrix, counter, file_name=fn)

    if (i, j) == end_point:
        st.write(f"This is the deep path: {deep_path}\n")
        st.write(f"\nThis is the final path: {final_path}")
        return


    else:
        step(i + 1, j, fn, matrix, deep_path, final_path, end_point)
        step(i, j - 1, fn, matrix, deep_path, final_path, end_point)
        step(i, j + 1, fn, matrix, deep_path, final_path, end_point)
        step(i - 1, j, fn, matrix, deep_path, final_path, end_point)
        if (i, j) in deep_path or matrix[(i, j)] > 0:
            matrix[(i, j)] = -2
            final_path.pop()
            return


def main():
    st.title("Maze")
    origin_img = ["Maze1.png","Maze2.png"]
    start_end = {'Maze1':[(0, 4),(12, 7)],'Maze2':[(1, 1),(2, 5)]}

    img = image_select(
        label="Select a maze",
        images=["Maze1_resize.png", "Maze2_resize.png"],
        captions=["Maze 1", "Maze 2"],
        use_container_width = False,
        return_value ='index'
    )
    image_path = origin_img[img]

    if st.button("Run Deep Search"):
        maze1 = image_to_matrix(image_path)
        image_name2 = os.path.splitext(os.path.basename(image_path))[0]
        try:
            os.makedirs(image_name2)
        except FileExistsError:
            # directory already exists
            with st.spinner("Erasing previous directory"):
                shutil.rmtree(image_name2)
                time.sleep(2)

            os.makedirs(image_name2)

        start = start_end[image_name2][0]
        end_point = start_end[image_name2][1]

        global counter
        counter = 1
        step(start[0], start[1], fn=image_name2, matrix=maze1, end_point=end_point)

        images = [iio.imread(f'{image_name2}/{i}.png') for i in range(2, counter + 1)]
        # imageio.mimsave(f'{image_name2}/path.gif', images, duration=5.5)

        # instead of saving the file locally, and then loading it,
        # we directly store it in the binary format in memory
        bytes_image = iio.imwrite("<bytes>", images, duration=5.5, extension=".gif")
        frames = iio.imread(bytes_image, index=None)
        byte_stream = io.BytesIO(bytes_image)
        contents = byte_stream.read()

        """### Solution"""
        # file_ = open(f'{image_name2}/path.gif', "rb")
        # contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        # file_.close()

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="path gif">',
            unsafe_allow_html=True,
        )

if __name__ == "__main__":
    main()
