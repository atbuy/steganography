# Steganography
This app let's you encode text into  an image.


**All the files you will need to specify, require you to include their extension**

## To encode text:
  1) Select the image to encode the text into
  2) Select the name of the image to output
  3) Write the text to encode inside it
  
  The encoding algorithm creates a new image that changes the bit with the lowest exponent (2^0) according to the bit value of the text you are trying to encode.
  For example, if you want to encode the text "Hello, World" into an image using this algorithm, then the program will follow these steps:
   - Try to open the image
   
       The image has to be in the same directory as the app. *You can not specify a path*.
   - Convert your text to a string of "ones" and "zeroes" and add a delimiter of 64 "ones" to it.
   
       The delimiter is used so the decoding algorithm will know when to stop reading characters from the encoded image.
   - Change the bit value of each pixel to the bit of the text.
       To encode "Hello, World" first you need to convert it to bits. The bit value with the delimiter is: **"0100100001100101011011000110110001101111001011000010000001010111011011110111001001101100011001001111111111111111111111111111111111111111111111111111111111111111"**
       
       The algorithm reads each letter of the message and then appends it's bit value to a string.
       
       Then it changes the bit value of the color of the pixels needed.
       For example if the first pixel of the first row is **[235, 245, 100]** then it converts each of the colors to bits.
       - **235** is **"11101011"**. The last bit (the bit with the lowest power) is "1", but the first bit of our message is "0".
       
         We change it to a *0*. So **235 ("11101011")** becomes **234 ("11101010")**.
       - **245** is **"11110101"**. The last bit is a "1" and the bit we need to write is a "1", so we don't need to change it.
       
       - **100** is **"01100100"**. The last bit is a "0" and the bit we need to write is also a "0", so we don't need to change it.
       
   This happens to all the bits of our message until the message is over. After the message is done, the algorithm just writes the normal values to the image, so nothing is changed.
   
   The bits needed to write can't be bigger than the bytes of the image. Because we can only change 1 bit of every byte, we can only write as many bits as the image has bytes.
   
   An image with 200 bytes can hold 200 bits of text but the algorithm appends a delimiter of 64 bits, leaving you with 136 bits to write.
   
   Most images have more than that though and you should be able to write "lorem ispum" in a small image.
   
   **The files the program creates are made in the same directory of the program.**
   
   **The files you are specifying should also be in the same directory, or the program won't work. You can not specify paths!**
   
   Encoding in small images takes a few seconds. **lena.png** is 512×512 and it takes about 1.5 seconds to encode the message. However a 4k image (3840×2160) took about 41 seconds. 
   
   **Decoding from the image, doesn't have to do with how large the image is, but how large the encoded text is**. Although, decoding from the 4K image, did take longer that decoding from the 512×512 image.
   
## To decode text
  1) Select the image that you know has an encoded message
  2) Select the name of the file you want the output to be written to
  
  The program looks at specific places to decode text from the image. If you encoded the picture in with different algorithm then uses this program to decode it might not work.
  
  **It is also possible that the message you want to send is cut short because the bits you are trying to encode have 64 "1"s in a row**
  
  It doesn't matter how big the image is, it will take the same time to decode if the image is 4K (3840×2160) or 144p (256×144), because the execution time depends on the size of the message and not the image.
  
  The larger in bytes the encoded message is, the longer the execution time.

## Screenshots
- **lena.png**:
  
  ![lena.png](/Screenshots/lena.png)
  
- **encoding a message into _lena.png_**:

  ![encoding](/Screenshots/Encoding1.png)
  
- **output.png**:

  ![output.png](/Screenshots/output.png)
  
- **decoding the message from _output.png_**:

  ![decoding](/Screenshots/Decoding1.png)
  
- **output_text.txt**:

  ![output_text.txt](/Screenshots/output_text.png)
  


- **4k1.jpg**:

  ![4k1.jpg](/Screenshots/4k1.jpg)
  
- **encoding the same message into the _4k1.jpg_ image**:

  ![4k encoding](/Screenshots/4kEncoding1.png)

- **4koutput.png**:

  ![4koutput.png](/Screenshots/4koutput.png)
  
- **decoding the message from _4koutput.png_**:

  ![4k decoding](/Screenshots/4kDecoding1.png)
  
- **4koutput_text.txt**:

  ![4koutput_text.txt](/Screenshots/4koutput_text.png)
