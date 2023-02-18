from PIL import Image
import os
import re

# inspect file path is or not is exists
def make_file(path):
    try:
        os.makedirs(path)
    except FileExistsError:
        print("###  File is exist... !")

# resize img
def rescale_imgs(path, size):
    counter = 0
    for img in os.listdir(path):
        if re.findall('\w*.jpg$', img):
            im = Image.open(path + img)
            print(f"##  img --> {img}  --> num:", counter+1)
            print(f"original --> {img}: ", im.format, im.size, im.mode)
            # im.show()  

            img_resized = im.resize(size, Image.ANTIALIAS)
            print(f"draft --> {img}: ", img_resized.format, img_resized.size, img_resized.mode, end = '\n'*2)
            # img_resized.show()
            
            img_resized.save(path[:-1] + '_resized/' + img, "JPEG", quality = 100)
            counter += 1

def main():
    # set img convert size
    resize = (224, 224)

    # get img file
    img_file = 'unsplash_dog_img/'
    file_path = f'/Users/tony/Desktop/Capture_img/{img_file}'
    make_file(file_path[:-1] + '_resized/')

    # resize img
    rescale_imgs(file_path, resize)
    
    # caculate the length of the list of resized images 
    counter = len(os.listdir(file_path[:-1] + '_resized/'))
    print(f"##  Convert  {counter}  Images Size Complete !")

if __name__ == '__main__': 
    import time
    s = time.time()
    main()
    t = time.time()
    print(f"##  ---> Takes {(t-s):.2f} Seconds !")
    




