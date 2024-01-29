from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2 #it makes the keys harder to bruteforce

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# 1. simple_key = get_random_bytes(32) #generates a 32 byte random key, which we will use later on for making the salt
#print(simple_key) #generates a random binary string


salt = b'\\q|\xf1\xdeK\xe2<Z\x17\xd9s\x05\xd4"$\xec\xe9\xe7\x15\xb0\xffl\xdc\xeb\tE\x7f\xc5&\xb8\x0b'
# after running the #1 line, we get this output, which we will fix as the salt, otherwise it will change everytime we run the program 

passw = "9954"

key = PBKDF2(passw, salt, dkLen=32) #we need to set the password and salt and set the dkLen as 32 because we mentiones 32 bytes length while making the random bytes, i.e., the present salt
#now we can use this key to encrypt stuff
#NOTE - from the same salt and password, we can generate the same key, so, it is not necessary that the key is unique, the key depends on the initial values


message = b"Hello. This is Indrajit"
#notice that this is Bytes now, this is IMPORTANT!

cipher = AES.new(key, AES.MODE_CBC) #mode cbc sets the cipher as block
#this kinda creates an object

ciphered_data = cipher.encrypt(pad(message, AES.block_size))
#this encrypts the message

print(ciphered_data)

#we can now save the encrypted data in a separate file.
#we can also save the key separately, and then share that to some other person, so that only that person can now read the data, kinda like WhatsApp

with open("encrypted.bin", "wb") as f: #writing the encrypted message
    f.write(cipher.iv)
    f.write(ciphered_data)

with open("key.bin", "wb") as f: #writing the key into a file
    f.write(key)

with open("key.bin", "rb") as f: #reading the key from file
    key = f.read()

with open("encrypted.bin", "rb") as f: #reading the encrypted message
    iv=f.read(16) #iv here is like a metadata, I guess
    decrypt_data=f.read()

cipher = AES.new(key, AES.MODE_CBC, iv=iv) 
original = unpad(cipher.decrypt(decrypt_data), AES.block_size) #this decrypts the data
print(original)