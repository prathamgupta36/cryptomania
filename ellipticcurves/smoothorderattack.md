First, factor the order of \\(G\\) into \\(N=p_{1}^{e_{1}}p_{2}^{e_{2}}...p_{n}^{e_{n}}\\), where each \\(p_{i}\\) is a prime and \\(e_{i}\\) is its exponent. Then for each \\(i,\\) take \\(G_{i}=\\left(\\frac{N}{p_{i}^{e_{i}}}\\right)G\\) and \\(H_{i}=\\left(\\frac{N}{p_{i}^{e_{i}}}\\right)H\\). These are valid points on the curve, they're just \\(G\\) and \\(H\\) multiplied by some integer. 

There are 2 facts by which you should check you are convinced:

1. \\(y_{i}G_{i}\\equiv H_{i}\\pmod {p_{i}^{e_{i}}}\\) for some \\(y_{i}\\) is a discrete log problem. Notice also that \\(y_{i}\\) should be "the same" as \\(x\\), but modulo a smaller number.

2. The order of \\(G_{i}\\) (and \\(H_{i}\\)) is \\(p_{i}^{e_{i}}\\).

If we could solve these discrete log subproblems where the order of the base is a power of a prime (instead of an arbitrary composite number), we would get our \\(y_{1},...,y_{n}\\) where each \\(y_{i}\\equiv x \\pmod {p_{i}^{e_{i}}}\\). This relationship reminds me of some kind of... mongolian... leftover lemma?.. I wonder how I would solve this...

But how do we solve \\(y_{i}G_{i}\\equiv H_{i}\\pmod {p_{i}^{e_{i}}}\\)? We will in fact reduce this problem once again, this time from solving the discrete log for a *power of a prime* order to that of simply a *prime* order. 

Here I will drop indices \\(i\\), but know that we have to do this for each of the \\(n\\) prime-exponent pairs. We write \\(y=z_{0}+z_{1}p^{1}+z_{2}p^{2}+...+z_{e-1}p^{e-1}\\). We can do this since we know certainly \\(y<p^{e}\\). Then consider:

\\[
\\begin{align*}
(p^{e-1})H&=(p^{e-1})(y)G\\\\
&= (p^{e-1})(z_{0}+z_{1}p^{1}+z_{2}p^{2}+...+z_{e-1}p^{e-1})G\\\\
&= (p^{e-1})\\bigg( z_{0}+p(z_{1}+z_{2}p+...+z_{e-1}p^{e-2}) \\bigg)G\\\\
&= \\bigg( p^{e-1}(z_{0})G \\bigg)+\\bigg( p^{e}(z_{1}+z_{2}p+...+z_{e-1}p^{e-2})G \\bigg)\\\\
&= z_{0}(p^{e-1}G).
\\end{align*}
\\]

The reduction in line 4 comes from the fact that \\(p^{e}\\) is the order of \\(G\\).

Like previously, observe that we now have the DLP \\(p^{e-1}H=z_{0}(p^{e-1}G)\\), where the order of \\((p^{e-1}G)\\) is just \\(p\\). Solving this lets us recover \\(z_{0}\\). Next, we can perform a similar algebraic manipulation to single out \\(z_{1}\\); we will find \\(z_{0}\\) in that expression, but that's ok since we already know it.

How do we get solve for \\(z_{0}\\), then? Well, there's no trick - we brute force it. We have reduced the composite order DLP to a prime power order DLP to a simple prime DLP. If the primes in question are reasonably small, this is easily done with Babystep-Giantstep algorithm or really just trying all options.