# Coppersmith's Method and RSA
## Introduction
The following is a guide for understanding the application of Coppersmith's Theorem to attacks on the RSA cryptosystem. Although many refer to such as Coppersmith's attack, it is actually a class of attacks which can be applied to many relaxed version of the RSA cryptosystem. Coppersmith's thoerm is a statement about finding "small" roots of finite field polynomials. The general class of attacks on RSA involves converting partial information about RSA secrets into polynomials whose "small" roots will be something desireable for us.

## RSA \\(\rightarrow\\) Polynomial
At first glance there is no polynomial to be seen in the RSA equations. We have some practice with this sort of thing already, as its the same principle when we used lattices to crack cryptosystems where there was no lattice present. We can take information present in a cryptosystem and represent it as a polynomial that we can construct using known information, but that we know has small roots at secret information we want. This is analogous to how we construct a lattice basis using public information which we know contains a short, or close vector which represent desireable information.

Recall the primary way to defeat RSA is by factoring the public modulus \\(n = pq\\) where \\(p\\) and \\(q\\) are prime. When we create polynomials, we want to keep their roots as our primary focus. This means they shall evaluate to \\(0\\) when the variables are where we want them. Rearranging the previous equation we get \\(n - pq = 0\\). In other words, the polynomial \\(f(x,y) = n - xy\\) has a roots at \\((1, n), (n, 1), (p, q), (q, p)\\). We have just constructed our first polynomial from the RSA cryptosystem!

Now these methods cannot be used to solve RSA given just the public modulus of course. The most common usecase for a Coppersmith attack would be when we are leaked some bits of secret RSA key material. For example if we are given the \\(k\\) least significant bits of \\(p\\), or the \\(k\\) most significant bits of \\(d\\), etc. So the reason our previous polynomial isn't solveable (in a reasonable amount of time) is that its roots aren't "small" enough. When we say "small", what we really mean is that the size of the root must be significantly lower than the size of the coefficients. In the previous equation our smallest roots where around \\(\sqrt{n}\\). Our coefficient is \\(1\\), so coppersmith isn't going to fly.

## Example
We will start with an example where we have somehow obtained 64% of the MSBs of \\(p\\). Whenever we have some kind of approximation of a value, it is helpfull to write it in some algebraic form. If we have \\(\ell\\) MSBs, then we can say \\(p = 2^\ell b + r\\) where \\(b\\) is known and \\(r\\) is not. Let \\(a = 2^\ell b\\). Now solving \\(r\\) would crack RSA, as then we would know \\(p\\) and could factor \\(n\\). So we want to construct a modular polynomial where when the variable of the polynomial \\(x\\) is what we care about, the polynoamial evaluates to \\(0\\). Without too much time we way think up \\(f(x) = a + x\\). Now when \\(x = r\\), the value we want to find, \\(f(r) = p \equiv 0 \pmod{p}\\). So \\(r\\) is a root of the polynomial \\(f \in \mathbb{F}_p\\).

## Solving the polynomials
Now that we have a polynomail with small roots that we would like to solve, how can we actually do so. Its time to delve a bit more into Coppersmith's Method. We will start by describing Coppersmith's method, and after will arrive at the final statement. This will finally allow us to describe how we know if the roots are "small" enough to work.

The basic idea behind Coppersmith's method is given some modular polynomial \\(f(x)\\), we constrct a new polynomial \\(g(x)\\) over the integers which has the same roots as \\(f(x)\\) under some specific bound \\(X\\). We can then use standard methods to find the roots of \\(g(x)\\) (sage, maple, mathematica, etc.). More rigerously, for some univariate polynomial \\(f(x)\\), for every root \\(x_0 \leq X\\)
\\[
f(x_0) \equiv 0 \pmod{b} \implies g(x_0) = 0 \text{ over }\mathbb{Z}
\\]

Constructing \\(g(x)\\) is a two step process:

1. We pick some \\(m \in \mathbb{Z}\\). We construct a set of polynomials \\(f_1(x), f_2(x), \dots, f_n(x)\\) that all have the same bounded roots \\(x_0\\) modulo \\(b^m\\).

2. Construct integer linear combination \\(g(x) = \sum\limits_{i=1}^na_if_i(x), a_i \in \mathbb{Z}\\) where \\(\left|g(x_0)\right| < b^m\\).

You may see why LLL is useful here, as to get \\(g(x)\\) we want a bounded integer linear combination of other polynomials. In practice we let the coefficient vectors of each \\(f_i\\) be the basis of a lattice. Every point in this lattice then represents an integer linear combination of our polynomials. Applying LLL to this lattice will give us a short vector, hopefully satisfing the requirement that its norm is in the \\(b^m\\) bound. Note that this vector itself represents a polynomial \\(g(x)\\). Since it is a linear combination of polynomials that have \\(x_0 < X\\) as a root modulo \\(b^m\\), this \\(g(x)\\) too must have that root. But we know the norm of \\(g < b^m\\), so \\(x_0\\) will also be a root over the integers, hence we have found our \\(g(x)\\).

Explaining precisely why \\(f_1, \dots, f_n\\) are chosen to work is beyond the depth of this dojo. It is sufficient to understand that the following algorithmic construction will work. Note that here \\(f^n(x)\\) refers to \\((f(x))^n\\) and not function composition.

With polynomial \\(f(x)\\) of degree \\(\delta\\), some \\(N\\) of unknown factorization where \\(b\\) divides \\(N\\) and \\(b \geq N^\beta\\), \\(\epsilon \leq \frac{1}{7}\beta\\)

Pick \\(m = \lceil \frac{\beta^2}{\delta\epsilon} \rceil\\) and \\(t = \lfloor \delta m (\frac{1}{\beta} - 1) \rfloor\\) Define polynomials
\\[
\begin{array}{rcll}
g_{i,j}(x) &=& x^jN^if^{m-i}(x) &\text{ for } i=0, \dots, m, j=0, \dots, \delta-1 \\\\
h_i(x) &=& x^if^m(x) &\text{ for } i=0, \dots, t-1
\end{array}
\\]

Then our bound for the root \\(X\\) can be set as \\(\frac{1}{2}\lceil N^{\frac{\beta^2}{\delta} - \epsilon} \rceil\\). Finally then our final set of polynomials can be made by taking \\(g_{i,j}(xX)\\) and \\(h_i(xX)\\). Its time to try applying this method to our example polynomial \\(f(x) = a + x\\).

## Example cont.
Recall our polynomial \\(f(x) = a + x \pmod{p}\\). So \\(f\\) has degree \\(1\\) and modulus \\(p\\), which is a devisor to \\(n\\), an integer with unknown factorization. So in our example \\(\delta = 1, N = n, b = p\\). For us to apply coppersmith we need a bound on \\(p\\), and because this is RSA, we can say \\(p \geq n^{\frac{1}{2}}\\), so \\(\beta = \frac{1}{2}\\).

Following the procedure we pick \\(\epsilon = \frac{1}{14}, m = \lceil \frac{0.5^2}{\frac{1}{14}} \rceil = 4, t = \lfloor4(\frac{1}{0.5} - 1)\rfloor = 4\\).

This makes our polynomial collection the following:

\\[
\begin{aligned}
g_{0,0}(x) &= f^4(x) = (a + x)^4 \\\\
g_{1,0}(x) &= N \cdot f^3(x) = n(a+x)^3 \\\\
g_{2,0}(x) &= N^2 \cdot f^2(x) = n^2(a+x)^2 \\\\
g_{3,0}(x) &= N^3 \cdot f(x) = n^3(a+x) \\\\
g_{4,0}(x) &= N^4 = n^4 \\\\
h_0(x) &= f^4(x) = (a+x)^4 \\\\
h_1(x) &= xf^4(x) = x(a + x)^4 \\\\
h_2(x) &= x^2f^4(x) = x^2(a + x)^4 \\\\
h_3(x) &= x^3f^4(x) = x^3(a + x)^4 \\\\
\end{aligned}
\\]

There is one duplicate, \\(h_0(x) = g_{0,0}(x)\\), so we can just keep one. In practice we generate these programatically. If you want you can confirm that they all share \\(r\\), the unknown part of \\(p\\), as a root modulo \\(p^4\\). The coefficient vectors of these polynomials will form the basis of our lattice, however to force the lattice to have a short vector caused by a polynomial with small coefficients, we scale using our bound \\(X = \frac{1}{2}\lceil n^{\frac{0.5^2}{1} - \frac{1}{14}} \rceil\\). This in short makes the basis work better with LLL and we can simply undo the scaling on our result. We apply this scaling on \\(x\\), so get get the scaled polynomials we replace \\(x\\) with \\(X\cdot x\\). The end result of this is for every term we multiply the coefficient by \\(X^i\\) where \\(i\\) is the degree of the \\(x\\) in that term. 

The signifigance of this basis is that vectors in the lattice will be coefficient vectors of other polynomials that also have a root at \\(r\\) modulo \\(p^2\\), since they will be integer linear combinations of the polynomials in our collection. Here is our example lattice C where the basis vectors are row vectors. We typically write these in the order that gives us a matrix in lower triangular form. This is part of why we construct the polynomials in this way as it will speed up computation.

\\[
C = 
\begin{bmatrix}
n^4 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\\\
n^3 a & n^3 & 0 & 0 & 0 & 0 & 0 & 0 \\\\
n^2 a^2 & 2n^2 a & n^2 & 0 & 0 & 0 & 0 & 0 \\\\
n a^3 & 3n a^2 & 3n a & n & 0 & 0 & 0 & 0 \\\\
a^4 & 4a^3 & 6a^2 & 4a & 1 & 0 & 0 & 0 \\\\
0 & a^4 & 4a^3 & 6a^2 & 4a & 1 & 0 & 0 \\\\
0 & 0 & a^4 & 4a^3 & 6a^2 & 4a & 1 & 0 \\\\
0 & 0 & 0 & a^4 & 4a^3 & 6a^2 & 4a & 1 \\\\
\end{bmatrix}
\\]

Now we are ready to perform LLL. This will give us a very short vector in this lattice, and by construction after we undo our scaling, it will represent the polynomial with a root at \\(r\\), but because its a short vector, this root holds over the integers and not just modulo \\(p^4\\). Below is some example sage code constructing the lattice and performing LLL on it to output the unscaled short vector.

```python
from sage.all import *
import math

# Define constants and parameters
n=88277897140749381818546469945450221702855591834373937011607754875224048243553082155040593768440731389087460674566334910986337475764238139933259327250982090184795271564342170284349250666577908814359385295818971830994773712012489567890045086845282781657909982803945257994085175685938357628312905049510232608123

a=10352091085765571726579959892312703756563807351327074692644316984517370444496158637132153495719320241563192393183856601303840505985357609010103623689961472

delta = 1
beta = 0.5
epsilon = (1/7)*beta
m = math.ceil(beta**2/(delta*epsilon))
t = math.floor(delta*m*((1/beta)-1))
X = math.ceil(n**(((beta**2)/delta)-epsilon))//2

# Construct Lattice from scaled coefficient vectors
C = Matrix(ZZ, [
    [n**4, 0, 0, 0, 0, 0, 0, 0],
    [n**3*a, n**3*X, 0, 0, 0, 0, 0, 0],
    [n**2*a**2, 2*n**2*a*X, n**2*X**2, 0, 0, 0, 0, 0],
    [n*a**3, 3*n*a**2*X, 3*n*a*X**2, n*X**3, 0, 0, 0, 0],
    [a**4, 4*a**3*X, 6*a**2*X**2, 4*a*X**3, X**4, 0, 0, 0],
    [0, a**4*X, 4*a**3*X**2, 6*a**2*X**3, 4*a*X**4, X**5, 0, 0],
    [0, 0, a**4*X**2, 4*a**3*X**3, 6*a**2*X**4, 4*a*X**5, X**6, 0],
    [0, 0, 0, a**4*X**3, 4*a**3*X**4, 6*a**2*X**5, 4*a*X**6, X**7]
])


# Apply LLL reduction and scale back to unscaled coefficient vector
L = C.LLL()
short_vec = L[0]
unscaled = [val//(X**i) for i, val in enumerate(short_vec)]
print(unscaled)
```

Running this yields a row of exterimely large numbers. Recall that this unscaled vector is the coefficient vector for a polynomial who has a root at \\(r\\) over the integers, ignoring the \\(p^2\\) modulus. There are a few different ways we might try and solve this. In some simpler cases, where we are given much more of \\(p\\), our polynomial is of the form \\(g(x) = x^2 + Bx + A\\). Its a quadratic and so we can just apply the quadratic formula. There a bunch of techniques out there for finding integer roots of many types of polynomials like our 7 degree beast here. Luckily `sage` has a general root finding function which can be applied to finding integer roots since finding roots over the integers without any modulus is well studied and quite fast.

If we have a sage polynomial \\(g\\), we can call `g.roots()`. To construct the sage polynomial from our coefficient vector, we first create a polynomial ring `R` making sure to pass `ZZ` so sage knows its integers only. Then we can do `g = R(vec)` where `vec` is our coefficient vector as a python list. Below is the example to get finish our example and solve for \\(p\\).

 ```python
R = PolynomialRing(ZZ, 'x') # Construct polynomial ring over the integers with variable x
g = R(unscaled) # Get polynomial from coefficient vector vec
roots = g.roots() # returns a list of tuples representing the root and its multiplicity
p_0 = roots[0][0]
p = p_0 + a
q = n // p
assert(p*q == n)
 ```

And with that we can decrypt whatever ciphertext we please as we can recalculate the private key from \\(p\\) and \\(q\\).