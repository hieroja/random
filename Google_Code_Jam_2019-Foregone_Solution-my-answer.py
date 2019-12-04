"""
Google Code Jam 2019 qualification round: Foregone Solution - My answer
Author: Jere Liimatainen

Summary:
This is my answer for 2019 Code Jam problem called Foregone Solution.
First, the program asks how many test cases there will be. Then it asks for one
number that contains atleast one number "4". Finally, it converts given number
into two numbers, neither of which contain the number 4. This solution passed
all of the test sets.

================================================================================
PROBLEM
    Someone just won the Code Jam lottery, and we owe them N jamcoins! However,
    when we tried to print out an oversized check, we encountered a problem. The
    value of N, which is an integer, includes at least one digit that is a 4...
    and the 4 key on the keyboard of our oversized check printer is broken.
    Fortunately, we have a workaround: we will send our winner two checks for
    positive integer amounts A and B, such that neither A nor B contains any
    digit that is a 4, and A + B = N. Please help us find any pair of values A
    and B that satisfy these conditions.

INPUT
    The first line of the input gives the number of test cases, T. T test cases
    follow; each consists of one line with an integer N.

OUTPUT
    For each test case, output one line containing Case #x: A B, where x is the
    test case number (starting from 1), and A and B are positive integers as
    described above. It is guaranteed that at least one solution exists. If
    there are multiple solutions, you may output any one of them.

LIMITS
    1 ≤ T ≤ 100.
    Time limit: 10 seconds per test set.
    Memory limit: 1GB.
    At least one of the digits of N is a 4.


Test set 1 (Visible)
    1 < N < 105.

Test set 2 (Visible)
    1 < N < 109.

Solving the first two test sets for this problem should get you a long way
toward advancing. The third test set is worth only 1 extra point, for extra fun
and bragging rights!

Test set 3 (Hidden)
    1 < N < 10100.

SAMPLE
    Input   Output

    3
    4       Case #1: 2 2
    940     Case #2: 852 88
    4444    Case #3: 667 3777

    In Sample Case #1, notice that A and B can be the same. The only other
    possible answers are 1 3 and 3 1.
================================================================================

Source (Visited: 4.12.2019):
https://codingcompetitions.withgoogle.com/codejam/round/0000000000051705/0000000000088231


"""
import sys

def exp(int):
    return len(str(int)) - 1

def no_4s_in(number):
    for index, digit in enumerate(str(number)):
        if digit == str(4):
            return False
    return True

def f(T):

    if T == 4:
        return (2, 2)

    for i in range(exp(T) + 1):
        if str(T)[i] == str(4):
            A = 4 * 10**(exp(T) - i)
            B = T - 4 * 10**(exp(T) - i)
            A -= 1
            B += 1
            break

    if no_4s_in(A) and no_4s_in(B):
        return A, B

    while True:
        for i in range(exp(B) + 1):
            if str(B)[i] == str(4):
                x = 5 * 10 ** (exp(B) - i) - int(str(B)[i:])
                A -= x
                B += x
                if no_4s_in(A) and no_4s_in(B):
                    return A, B

        for i in range(exp(A) + 1):
            if str(A)[i] == str(4) and i != exp(A):
                x = int(str(A)[i:]) - (3 * 10 ** (exp(A) - i) + 9 * 10 ** (
                            exp(A) - i - 1))
                A -= x
                B += x
                if no_4s_in(A) and no_4s_in(B):
                    return A, B

            elif str(A)[i] == str(4) and i == exp(A):
                A -= 1
                B += 1
                if no_4s_in(A) and no_4s_in(B):
                    return A, B


T_amount = int(sys.stdin.readline())
for n in range(1, T_amount + 1):
    T = int(sys.stdin.readline())
    a, b = f(T)

    print("Case #", n, ": ", a, " ", b, sep="")
