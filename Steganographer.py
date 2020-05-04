import time
import numpy as np
from PIL import Image
from string import digits, ascii_letters


def encode_text(infile, outfile, message):
    # Set the starting time
    start_time = time.time()

    # Open the image to write the text
    img = Image.open(f"{infile}")
    # Get the size of the iamge
    width, height = img.size
    # This is how much data we can write into the image
    able_to_write = width * height * 3

    write = ""
    for letter in message:
        write += "{:08b}".format(ord(letter))
    write += "1111111111111111111111111111111111111111111111111111111111111111"

    # This is how much data we need to write into the image
    need_to_write = len(write)
    # If the message cannot fit inside the image, exit
    if need_to_write > able_to_write:
        print("Unable to write message to image. Text is too large.")
        return

    # if the image's mode is in RGBA continue
    if img.mode in "RGBA":
        # Convert to RGBA just in case
        img.convert("RGBA")
        # Get the image as an array of rows of pixels
        data = np.asarray(img)
        count = 0
        out_data = []
        for row in data:
            cols = []
            for pixel in row:
                temp = []
                for item in pixel:
                    bin_val = "{:08b}".format(item)
                    # If the iterations ar4e larger than the message
                    # then we are done writing the message into the image,
                    # we just write the pixel to the output image
                    if count > len(write) - 1:
                        temp.append(item)
                        continue
                    # if the last bit of the bit value is the same as the message we are trying to encode
                    # then we don't need to change it
                    if bin_val[-1] == write[count]:
                        temp.append(item)
                    else:
                        # Change the last bit of the byte to the next bit of the message
                        to_append = bin_val[:-1] + f"{write[count]}" + bin_val[:0]
                        to_append = int(to_append, 2)
                        temp.append(to_append)
                    count += 1
                cols.append(temp)
            out_data.append(cols)
        # Convert the out_data list to a numpy array
        last_data = np.array(out_data)
        # Create an image from the array
        outimg = Image.fromarray((last_data).astype(np.uint8))
        # Save it
        outimg.save(f"{outfile}")
        img.close()
        print("Completed.")
        # Calculate the execution time
        elapsed_time = time.time() - start_time
        return elapsed_time
    else:
        print("Unable to use format.")
        return


def decode_text(infile, output):
    # Set the starting time
    start_time = time.time()

    # Open the image
    img = Image.open(f"{infile}")

    # If the image mode is in RGBA, then continue
    if img.mode in "RGBA":
        # Convert it just in case
        img.convert("RGBA")
        # Get the pixel array of the image
        data = np.asarray(img)

        # Count how many bytes ended at 1
        # The delimiter set from the encoding algorithm was 64 "ones"
        # So when you find 64 bytes that end with "1" on their bit value
        # Then that is the flag to stop reading characters
        delimiter = 0

        # The bit value of each byte will be written here
        last_8bits = ""
        # This is to append the characters found in the image
        characters = []
        for row in data:
            for pixel in row:
                for item in pixel:
                    # Get the last bit of the byte
                    last_bit = "{:08b}".format(item)[-1]

                    # If we find that the last bit of the byte is 1 we need to know
                    # Because if the delimiter reaches 64 then we need to stop the algorithm
                    if last_bit == "1":
                        delimiter += 1
                    else:
                        delimiter = 0

                    # Stop the execution if the delimiter is found
                    # Write all the characters to a variable and then write the final text in a file
                    if delimiter == 64:
                        text = ""
                        for binary in characters:
                            char = chr(int(binary, 2))
                            text += char
                        with open(f"{output}", "w", encoding="utf-8") as file:
                            file.write(f"{text[:-7]}")

                        # calculate the time the algorithm took
                        elapsed_time = time.time() - start_time
                        return text[:-7], elapsed_time

                    # If we have the last 8 bits of the last 8 bytes we read then we have a character
                    if len(last_8bits) == 8:
                        characters.append(last_8bits)
                        last_8bits = ""
                    last_8bits += last_bit
                    

def main():
    allowed_chars = ascii_letters + digits + ". _-"
    option = input("1) Encrypt Text\n2) Decrypt Text\n\nSelect: ")
    if option == "1":
        infile = input("Image to hide text (include extension, image should be in the same directory): ")
        outfile = input("Name of output image (include extension, usually PNG or JPG): ")
        message = ""
        print("\nDouble-Enter to apply text")
        print("Text to hide:\n\n")
        while True:
            last_message = input()
            if last_message == "":
                break
            else:
                message += last_message + "\n"
        message = message.strip()
        if all([char in allowed_chars for char in infile]) and all([char in allowed_chars for char in outfile]):
            print("Stared encoding...")
            elapsed_time = encode_text(infile, outfile, message)
            print("Elapsed time:", elapsed_time)
        else:
            print("Not allowed character in filename")
    elif option == "2":
        infile = input("Image to decrypt text from (include extension): ")
        outfile = input("Text file to write output (include extension): ")
        if all([char in allowed_chars for char in infile]) and all([char in allowed_chars for char in outfile]):
            print("Started encoding...")
            try:
                result, elapsed_time = decode_text(infile, outfile)
                print("Elapsed time:", elapsed_time)
                print(f"Result:\n\n{result}")
            except TypeError:
                print("Couldn't find text inside image. Maybe it isn't encrypted? Try another one.")

        else:
            print("Not allowed character in filename")
            
            
if __name__ == "__main__":
    main()
