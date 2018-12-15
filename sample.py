'''

This is a Project Euler problem with a neat solution that combines efficient design and Python functionality.

I like it how you can do all steps, including generating primes, in one pass.  The Counter object makes the code extra clean.

Simple problem:

Given N <= 1000, find the first triangle number with more than N unique factors.  The kth triangle number is just the sum of 1, 2, ... k.

Helpful Observations:

1.  The k^th triangle number is ( k * (k + 1) ) / 2

2.  Natural numbers have a unique prime factorization.  If a prime number p_i divides natural number x t_i times, each unique factor of x has between 0 and t_i p_i's.  So, the number of unique factors is just the product of (t_i + 1) across i's.

3.  The i^th triangular number is (i * (i + 1))/2 so the (i+1)^th is ( (i+1) * (i+2) )/2.  So, if you factor triangular numbers in order, you will encounter odd natural numbers in order, and (with the exception of 2) consequently primes in order.

4.  Say n if a natural number and p is its smallest prime factor, the prime factorization of n is just {p} + the prime factorization of n/p.  If we're going through triangular numbers in order we'll alread know the factorization of n onces all 2's are removed.  We can save a lot of work by memorizing previous results.

'''

from collections import Counter

def factor(n, ps, d):
    '''
    Takes a natural number n,
    list of found primes ps,
    and a dictionary d of previous results.

    Returns a collection.Counter object of n's prime factorization.

    For example, 12 -> Counter({ 2: 2, 3: 1 }), i.e. two 2s and one 3.
    Updates are potentially made to ps and d.

    Note: Primes need to be encountered in order, or externally supplied.
    '''

    # check if we already have the answer memorized
    if n in d:
        return d[n]

    # iterate through known primes, see if one divides n
    for p in ps:
        if n % p == 0:
            # take advantage of '+' functionality in Counter objects
            d[n] = Counter([p]) + factor(n/p, ps, d)
            return d[n]

    # if nothing divides n, then n is prime
    else:
        ps.append(n)
        d[n] = Counter([n])
        return d[n]


def num_factors(factors):
    '''
    Take a collecton.Counter object giving a prime factorization, factors.
    Returns the number of unique factors.

    If p_i occurs t_i times, calculates as the product of (t_i + 1) across i's.
    '''
    return reduce(lambda x,y: x * (y + 1), factors.values(), 1)


# calculation of x^th triangle number
triangle_number = lambda x : ( x * (x + 1) )/2


# there's more than one test case, so I'll just compute the answer for the max case, and
# memorize along the way, that will give me all the needed answers

max_N = 1000             # biggest case
i = 1                    # the number of triangle number we are on
seek = 1                 # the number of factors we are seeking to exceed
primes = [2]             # running list of discovered primes
mem = {1 : Counter()}    # dictionary : n -> prime factorization; memory of prior results
ans = {}                 # dictionary : n -> first triangle number with > n factors

while seek <= max_N:
    tri = triangle_number(i)
    prime_factors = factor(tri, primes, mem)
    tri_number_factors = num_factors(prime_factors)
    while tri_number_factors > seek:
        ans[seek] = tri
        seek += 1
    i += 1

# now read in the test cases and output results
T = int(raw_input())
for _ in xrange(T):
    N = input()
    print ans[N]
