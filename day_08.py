
def count_ones_and_zeroes(layer: str) -> int:
    return layer.count("1") * layer.count("2")


def count_zeroes(layer: str) -> int:
    return layer.count("0")


def main():
    width = 25
    height = 6

    encoded_image = input()

    number_of_layers = len(encoded_image) // (width * height)

    begin_index = 0
    end_index = width * height

    layers = []

    for layer_index in range(number_of_layers):

        layer = encoded_image[begin_index:end_index]

        layers.append(layer)

        begin_index = end_index
        end_index = end_index + (width * height)

    final_image = ""

    for pixel in range(width * height):

        for layer in layers:

            if layer[pixel] == "0":  # black
                final_image += "0"
                break
            if layer[pixel] == "1":  # white
                final_image += "1"
                break

    for i in range(height):
        pixel_row = final_image[i * width:(i*width) + width]

        print(pixel_row.replace("1", "X").replace("0", "."))

if __name__ == "__main__":
    main()
