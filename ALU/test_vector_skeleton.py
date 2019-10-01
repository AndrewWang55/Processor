#!/usr/bin/env python
# CS 3410 Artifact
# Written 2/12/19 by Akhil Bhandaru
from random import *

# Maximum 32 bit integer in 2's complement
MAX_INT = 2**31 - 1
MAX_UNSIGNED_INT = 2**32 - 1

# Minimum 32 bit integer in 2's complement
MIN_INT = -1 * (2**31)


# Helper Functions
# =============================================================== #
def to_hex(number, nbits):
    """ Returns hex string with 8 bytes representing hex(number)
    in two's complement binary."""
    return hex((number + (1 << nbits)) % (1 << nbits))


def to_test(A, B, Op, Sa, C, V):
    """ Returns a test vector with above parameters"""
    return "{}\t\t {}\t\t {}\t\t\t {}\t\t\t {}\t\t {}\n".format(
        to_hex(A, 32),
        to_hex(B, 32),
        to_hex(Op, 4),
        to_hex(Sa, 5),
        to_hex(C, 32),
        "{0:b}".format(V)
    )


# Generator Functions
# =============================================================== #
def generate_SLL(channel):
    """ generate_SLL generates a single SLL instruction.
    SLL instructions have an Op[4] code of 0b1010 or 0b1011.
    32 bit number B[32] and 5 bit number Sa[5] are generated
    randomly. """
    Op = randint(10, 11)  # Op can be 10 or 11
    Sa = randint(0, 31)
    B = randint(0, MAX_UNSIGNED_INT)
    C = B << Sa

    # Format: A, B, Op, Sa, C, V
    channel.write(to_test(0, B, Op, Sa, C, 0))


def generate_EQ(channel):
    """ generate_EQ generates a single EQ instruction.
    EQ instructions have an Op[4] code of 0b0010.
    32 bit numbers A[32] and B[32] are generated
    randomly. """
    A = randint(MIN_INT, MAX_INT)
    B = randint(MIN_INT, MAX_INT)
    C = 1 if A == B else 0

    # Format: A, B, Op, Sa, C, V
    channel.write(to_test(A, B, 2, 0, C, 0))


def generate_LT(channel):
    A = randint(MIN_INT, MAX_INT)
    B = randint(MIN_INT, MAX_INT)
    C = 1 if A <= 0 else 0
    channel.write(to_test(A, Bf, 4, 0, C, 0))


def generate_GT(channel):
    A = randint(MIN_INT, MAX_INT)
    B = randint(MIN_INT, MAX_INT)
    C = 1 if A > 0 else 0
    channel.write(to_test(A, B, 6, 0, C, 0))


def generate_NE(channel):
    A = randint(MIN_INT, MAX_INT)
    B = randint(MIN_INT, MAX_INT)
    C = 1 if A != B else 0
    channel.write(to_test(A, B, 0, 0, C, 0))


def generate_ADD(channel):
    A = randint(MIN_INT, MAX_INT)
    B = randint(MIN_INT, MAX_INT)
    Op = randint(8, 9)
    C = A+B
    if (C > MAX_INT or C < MIN_INT):
        V = 1
    else:
        V = 0
    channel.write(to_test(A, B, Op, 0, C, V))


def generate_SUB(channel):
    A = randint(MIN_INT, MAX_INT)
    B = randint(MIN_INT, MAX_INT)
    Op = randint(12, 13)
    C = A-B

    if (C > MAX_INT or C < MIN_INT):
        V = 1
    else:
        V = 0
    channel.write(to_test(A, B, Op, 0, C, V))


def generate_SRA(channel):
    Sa = randint(0, 31)
    B = randint(MIN_INT, MAX_INT)
    C = B >> Sa
    channel.write(to_test(0, B, 15, Sa, C, 0))


def generate_AND(channel):
    A = randint(0, MAX_UNSIGNED_INT)
    B = randint(0, MAX_UNSIGNED_INT)
    C = A & B
    channel.write(to_test(A, B, 3, 0, C, 0))


def generate_OR(channel):
    A = randint(0, MAX_UNSIGNED_INT)
    B = randint(0, MAX_UNSIGNED_INT)
    C = A | B
    channel.write(to_test(A, B, 1, 0, C, 0))


def generate_NOR(channel):
    A = randint(0, MAX_UNSIGNED_INT)
    B = randint(0, MAX_UNSIGNED_INT)
    C = ~(A | B)
    channel.write(to_test(A, B, 5, 0, C, 0))


def generate_XOR(channel):
    A = randint(0, MAX_UNSIGNED_INT)
    B = randint(0, MAX_UNSIGNED_INT)
    C = A ^ B
    channel.write(to_test(A, B, 7, 0, C, 0))


def generate_SRL(channel):
    B = randint(0, MAX_UNSIGNED_INT)
    Sa = randint(0, 31)
    C = B >> Sa
    CString = '{:032b}'.format(C)
    if(Sa >= 1 and CString[0] == 1):
        C = int(CString.replace("1", "0", Sa), 2)
    channel.write(to_test(0, B, 14, Sa, C, 0))


# Main
# =============================================================== #
if __name__ == "__main__":
    """ script.py opens a file called test_vectors.txt,
    and automatically writes 5 EQ or SLL test vectors to it.
    All numbers are written in 8 byte hex."""
    print("What do you want to call your file?")
    file_name = input()

    print("How many tests would you like to generate?")
    num_tests = input()

# Open a file for writing and create one if it does not exist
    channel = open(file_name + ".txt", "w+")

# Add header to test file
    channel.write("## Automatically Generated Tests ##\n")
    channel.write(
        "A[32]\t\t\t B[32]\t\t\t Op[4]\t\t\t Sa[5]\t\t\t C[32]\t\t\t V\n")

# Write tests
    for i in range(int(num_tests)):
        op = randint(0, 12)
        switcher = {
            0: generate_EQ,
            1: generate_SLL,
            2: generate_LT,
            3: generate_GT,
            4: generate_NE,
            5: generate_ADD,
            6: generate_SUB,
            7: generate_SRA,
            8: generate_AND,
            9: generate_OR,
            10: generate_NOR,
            11: generate_XOR,
            12: generate_SRL
        }
    # Get the function from switcher dictionary
        generator = switcher.get(op, lambda x: "Invalid Test Generator")

    # Execute the generator
        generator(channel)

# Print Finished
    print("====================")
    print("Test Generation Complete.")

# Closes file channel
    channel.close()
