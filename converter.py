from PIL import Image
from math import sqrt

def closestDisvisor(n:int)->tuple[int,int]:
    a = round(sqrt(n))
    while n%a > 0 : a-= 1
    return a,n//a

def get_image(filePath:str)->None:
    with open(filePath, mode='rb') as file:
        fileContent = file.read()
        x=''
        for _byte in fileContent:
            x+=bin(_byte).removeprefix('0b').rjust(8,'0')
        cmap = {'0' : 0 , '1' : 255}
        dim = closestDisvisor(len(x))
        data = [cmap[letter] for letter in x]
        image = Image.new('1', dim)
        image.putdata(data)
        image.save("test.png")

def get_file(filePath:str):
    im = Image.open(filePath,'r')
    pixel_values = list(im.getdata())
    data=''
    for i in pixel_values:
        data += "1" if i[0]==255 else "0"
    data = int(data, 2).to_bytes(len(data)//8,byteorder='big')
    with open("original_file",mode='wb') as file:
        file.write(data)

filepath="C:\\Users\\Niraj Patil\\OneDrive\\Documents\\Technical Seminar\\Implementation\\RSA\\Python\\ts\\input.txt"
with open(filepath, mode='rb') as file:
        fileContent = file.read()
        x=''
        for _byte in fileContent:
            x+=bin(_byte).removeprefix('0b').rjust(8,'0')
        print(x)

get_image(filepath)