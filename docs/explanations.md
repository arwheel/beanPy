# Explanations

## An explanation on how the parameters change the distribution of numbers generated

In a normal distribution with the given parameters $\sigma$, $\mu^2$

$$ X \sim N(\mu, \sigma^2) $$

The probability of each value is given by:

$$ P(X = x) = \frac{1}{\sqrt{2\pi\sigma^2}}e^{\frac{-(x-\mu)^2}{2\sigma^2}} $$

The code picks random values of $0 < x < 1$, and as the equation above weighs the numbers towards the mean μ and the spread around the mean is changed by the variance $\mu^2$. This is similar to all of the other types of distributions but with different equations to calculate the $P(X=x)$ and therefore different steepness of curves and how affected they are by their parameters

This is easily visualized by [plotting a PDF](./tutorials.md#how-to-plot-a-pdf-of-a-distribution-with-given-parameters) of the chosen distribution with the library, however to speed up the plotting the graph is made with systematic choices of x rather than random ones as otherwise it was too slow for large n values

## A brief overview of quantiles

A quantile is a value at which, for any of the distributions X

$$P(X ≤ x) = p\ \text{for}\ 0 < p < 1 $$

This can be visualized as the area under the [PDF curve](./tutorials.md#how-to-plot-a-pdf-of-a-distribution-with-given-parameters), it is useful to think of it that was as when you generate a sample of random numbers with our library, you can say for sure what is the probability that we have so many values less than or equal to a certain value, which can be very useful to know. This is also shown in the [66, 80, 93, 95 rule](https://en.wikipedia.org/wiki/68%E2%80%9395%E2%80%9399.7_rule)

