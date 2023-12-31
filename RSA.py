# from google.colab import drive
# drive.mount('/content/drive')


import cv2
import numpy as np
# from google.colab.patches import cv2_cv2.imshow
import matplotlib.pyplot as plt
# %matplotlib inline


# cv2.imshow('',my_img)
# plt.cv2.imshow(my_img, cmap="gray")



#RSA

# STEP 1: Generate Two Large Prime Numbers (p,q) randomly
from random import randrange, getrandbits


def power(a,d,n):
  ans=1
  while d!=0:
    if d%2==1:
      ans=((ans%n)*(a%n))%n
    a=((a%n)*(a%n))%n
    d>>=1
  return ans


def MillerRabin(N,d):
  a = randrange(2, N - 1)
  x=power(a,d,N)
  if x==1 or x==N-1:
    return True
  else:
    while(d!=N-1):
      x=((x%N)*(x%N))%N
      if x==1:
        return False
      if x==N-1:
        return True
      d<<=1
  return False


def is_prime(N,K):
  if N==3 or N==2:
    return True
  if N<=1 or N%2==0:
    return False
  
  #Find d such that d*(2^r)=X-1
  d=N-1
  while d%2!=0:
    d/=2

  for _ in range(K):
    if not MillerRabin(N,d):
      return False
  return True  
  



def generate_prime_candidate(length):
  # generate random bits
  p = getrandbits(length)
  # apply a mask to set MSB and LSB to 1
  # Set MSB to 1 to make sure we have a Number of 1024 bits.
  # Set LSB to 1 to make sure we get a Odd Number.
  p |= (1 << length - 1) | 1
  return p



def generatePrimeNumber(length):
  A=4
  while not is_prime(A, 128):
        A = generate_prime_candidate(length)
  return A

def GCD(a,b):
  if a==0:
    return b
  return GCD(b%a,a)
# Step 4: Find D. 
#For Finding D: It must satisfies this property:-  (D*E)Mod(eulerTotient)=1
#Now we have two Choices
# 1. That we randomly choose D and check which condition is satisfying above condition.
# 2. For Finding D we can Use Extended Euclidean Algorithm: ax+by=1 i.e., eulerTotient(x)+E(y)=GCD(eulerTotient,e)
#Here, Best approach is to go for option 2.( Extended Euclidean Algorithm.)
def gcdExtended(E,eulerTotient):
  a1,a2,b1,b2,d1,d2=1,0,0,1,eulerTotient,E

  while d2!=1:

    # k
    k=(d1//d2)

    #a
    temp=a2
    a2=a1-(a2*k)
    a1=temp

    #b
    temp=b2
    b2=b1-(b2*k)
    b1=temp

    #d
    temp=d2
    d2=d1-(d2*k)
    d1=temp

    D=b2

  if D>eulerTotient:
    D=D%eulerTotient
  elif D<0:
    D=D+eulerTotient

  return D


def generateKeys(length:int):
  P=generatePrimeNumber(length)
  Q=generatePrimeNumber(length)
  #Step 2: Calculate N=P*Q and Euler Totient Function = (P-1)*(Q-1)
  N=P*Q
  eulerTotient=(P-1)*(Q-1)
  #Step 3: Find E such that GCD(E,eulerTotient)=1(i.e., e should be co-prime) such that it satisfies this condition:-  1<E<eulerTotient
  E=generatePrimeNumber(4)
  while GCD(E,eulerTotient)!=1:
    E=generatePrimeNumber(4)
  D=gcdExtended(E,eulerTotient)
  return P,Q,N,eulerTotient,E,D

# P,Q,N,eulerTotient,E,D=generateKeys(5)
def printKeys(n):
  P,Q,N,eulerTotient,E,D=generateKeys(n)
  print(f"\tP={P}\n\tQ={Q}\n\tN={N}\n\teulerTotient={eulerTotient}\n\tE={E}\n\tD={D}")
  return P,Q,N,eulerTotient,E,D

#Step 5: Encryption
def encrypt(image,E,N):
  row,col=image.shape[0],image.shape[1]
  keyMatrix = [[0 for x in range(col)] for y in range(row)]
  for i in range(0,row):
    for j in range(0,col):
      r,g,b=image[i,j]

      if i!=0 and j!=0:
        if j==0:
          _r,_g,_b=image[i-1,-1]
        else:
          _r,_g,_b=image[i,j-1]
        r=r^_r
        g=g^_g
        b=b^_b


      C1=power(r,E,N)
      C2=power(g,E,N)
      C3=power(b,E,N)

      
      keyMatrix[i][j]=[C1//256,C2//256,C3//256]

      C1=C1%256
      C2=C2%256
      C3=C3%256
      image[i,j]=[C1,C2,C3]
  cv2.imwrite('encr.png',image)
  return keyMatrix


#Step 6: Decryption
def decrypt(image,D,N,keyMatrix):
  
  row,col=image.shape[0],image.shape[1]
  for i in range(row-1,-1,-1):
    for j in range(col-1,-1,-1):
      r,g,b=image[i][j]
      C1=r+256*keyMatrix[i][j][0]
      C2=g+256*keyMatrix[i][j][1]
      C3=b+256*keyMatrix[i][j][2]
     
      M1=power(C1,D,N)
      M2=power(C2,D,N)
      M3=power(C3,D,N)

      if i!=0 and j!=0:
        if j==0:
          _M1,_M2,_M3=image[i-1,-1]
        else:
          _M1,_M2,_M3=image[i,j-1]
        M1=M1^_M1
        M2=M2^_M2
        M3=M3^_M3


      image[i,j]=[M1,M2,M3]
  cv2.imwrite('decr.png',image)