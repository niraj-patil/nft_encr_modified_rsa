from RSA import printKeys,encrypt,decrypt
from converter import get_file,get_image
from numpy import save,load
from IPFS import uploadToIPFS
from Blockchain import mint_nft
from os import getenv
from os.path import getsize
from time import process_time
from cv2 import imread

def main():
    from dotenv import load_dotenv
    load_dotenv()
    ts=process_time()
    print("Generating Keys")
    P,Q,N,eulerTotient,E,D=printKeys(200)
    print(f"\tP={P}\n\tQ={Q}\n\tN={N}\n\teulerTotient={eulerTotient}\n\tE={E}\n\tD={D}")
    print(f"\tTime Taken:{process_time()-ts} seconds")
    ts=process_time()
    print("Encrypting")
    print(f"\tFile Size:{getsize('test.png')} bytes")
    my_img = imread('input.png')
    print("Input Pixel:")
    print(my_img[0,0])
    print(f"\tNumber of Pixels:{int(my_img.size/3)}")
    save("KeyMatrix",encrypt(my_img,E,N))
    my_img = imread('encr.png')
    print("Encrypted Pixel:")
    print(my_img[0,0])

    print(f"\tTime Taken:{process_time()-ts} seconds")
    ts=process_time()
    print("Uploading to IPFS")
    uri=uploadToIPFS("encr.png")
    print(f"\tNFT Data Uploaded at:\n\t\t{uri}")
    print(f"\tTime Taken:{process_time()-ts} seconds")
    ts=process_time()
    print("Minting NFT")
    mint_nft(getenv('ACCOUNT'),uri)
    print(f"\tTrack Transaction at:\n\t\thttps://goerli.etherscan.io/address/0xcabe56cf9a1dc210e47c086fa7dab6b9ac9dd6ee")
    print(f"\tTime Taken:{process_time()-ts} seconds")
    ts=process_time()

    # print("Decrypting")
    # keyMatrix=load('KeyMatrix.npy')
    # my_img = imread('nft.png')
    # print(f"\tNumber of Pixels:{int(my_img.size/3)}")
    # save("KeyMatrix",decrypt(my_img,163,493,keyMatrix))
    # print(f"\tTime Taken:{process_time()-ts} seconds")

if __name__=="__main__":
    main()