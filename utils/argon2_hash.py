import os
import psutil
from argon2 import PasswordHasher, exceptions

#By first checking for the current system's hardware capabilities we never risk attempting to use more than it has to
#offer.

#Acquire total number of cores and utilize at most 2 of them for hashing. If, of course the device only has one core,
#we only use one core.
num_cores = os.cpu_count() or 1
used_cores = min(2, num_cores)

#Using psutil we can get our system's total amount of RAM as bytes so we divide it by 1024 to obtain the amount of
#kilobytes. We do this because PasswordHasher expects a value represented as kilobytes.
total_kilobytes_ram = psutil.virtual_memory().total // 1024

#The total amount of RAM to be used for hashing is a minimum between 64 kilobytes and 10% of our system's RAM.
hash_memory = min(65536, total_kilobytes_ram // 10)

#The settings used here are for the sake of speed and ease of testing. Safer settings commented next to each one.
ph = PasswordHasher(
    time_cost=2,                #time_cost is the easiest setting to increase to improve security but also lower performance
    memory_cost=hash_memory,    #Total amount of RAM used should be between 64 and 512 megabytes
    parallelism=used_cores,     #Only a maximum of 2 cores are used, Most devices today have at least 4.
    hash_len=32,
    salt_len=16
)

def hash_password (password: str) -> str:
    return ph.hash(password)

def verify_password(password: str, plaintext: str) -> bool:
    try:
        ph.verify(password, plaintext)
        return True
    except exceptions.VerifyMismatchError:
        return False
    except Exception as e:
        print(f"Unable to verify password: {e}")
        return False