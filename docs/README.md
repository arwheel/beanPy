Tin of beanPy documentation
==================================

This is the official documentation of beanPy, the statistical random number generator. Written for `'Computing for mathematics' coursework <https://vknight.org/cfm/>`_ 

# Tutorial

## How to import our library

Beans can be imported by putting beanPy in your workspace and running

```python
>>> import beanPy as Beans

```

For all of the guides it is implied that you have aready imported the library into your workspace

## How to define a distribution

Beans has an assortment of different distributions to use such as

- **Normal**

This defines a normal distribution given a defined *mean_value* and *variance_value*

```python
our_normal_distribution = Beans.NormalDistribution(mean_value, variance_value)
```
- **Exponential**

This defines an exponential distribution given a defined *lambda_value*

```python
our_exponential_distribution = Beans.ExponentialDistribution(lambda_value)
```
- **Poisson**

This defines an poisson distribution given a defined *lambda_value*

```python
our_poisson_distribution = Beans.PoissonDistribution(lambda_value)
```
- **Continuous uniform**

This defines a continous uniform distribution given a defined *min_value*, *max_value*

```python
our_continous_uniform_distribution = Beans.ContinuousUniformDistribution(min_value, max_value)
```
- **Discrete uniform**

This defines a discrete uniform distribution given a defined *min_value*, *max_value* and an optional *step_value*

```python
our_discrete_uniform_distribution = Beans.DiscreteUniformDistribution(min_value, max_value, [step_value])
```

**Note:**
The default value of *step_value* is 1, so if omitted it will default to *step_value = 1*

The *min_value* is always included in the distribution however if you give a *max_value* and the *step_value* cannot step towards it it will reduce the *max_value* such that the largest number of steps are included

---

**For example:**

```python
>>> mean_value = 0
>>> variance_value = 1
>>> our_normal_distribution = Beans.NormalDistribution(mean_value, variance_value)

```

This will define a standardized normal distribution, of course you could always parse the mean and variance directly into our function

## How to take samples with a chosen distribution

The main use of our library is to take samples of numbers with a given distribution. To do so you must [define a distribution](tutorials.md#How-to-define-a-distribution) and define *number_of_samples* and *seed* then parse

```python
our_chosen_distribution.TakeSample(seed)
```

Or in order to take multiple samples at once you parse

```python
our_chosen_distribution.TakeMultipleSamples(number_of_samples, seed)
```

The seed can be omitted in both of these cases

---

**For example:**

In this tutorial we will see how to use our library, 'Beans' to generate random numbers and draw graphs of probability distributions.

Choosing the required statistical distribution and giving parameters of the distributions where required. In this guide we will be using the normal distribution to show you how our code works.

```python
>>> mean_value = 0
>>> variance_value = 1
>>> our_normal_distribution = Beans.NormalDistribution(mean_value, variance_value)

```

Here we import our library and select our *mean_value*, *variance_value* and distribution which we will later put into our functions to find out data

Depending on what you want to find out you will use Distribution.[function] to do different things, for our guide we will generate a sample of numbers in preportion to the normal distribution

```python
>>> number_of_samples = 1000
>>> seed = 0
>>> our_normal_distribution.TakeMultipleSamples(number_of_samples, seed)

```

This will [output 1000 samples](1000samples.json) of numbers in the preportion of the normal distribution, if the seed is given you can it will output

To test if this has given us a suitable output we can test the samples mean ($\mu$) and variance ($\sigma^2$)

```python
>>> output = our_normal_distribution.TakeMultipleSamples(number_of_samples, seed)
>>> sample_mean = sum(i for i in output) / number_of_samples
>>> #using the equation of variance
>>> sample_variance = sum(i ** 2 for i in output) / number_of_samples - sample_mean
>>> print(f"μ = {sample_mean}, σ² = {sample_variance}")
μ = 0.04904221840834106, σ² = 0.9342589470547096

```

This gives us
> $$\mu = 0.04904221840834106, \sigma^2 = 0.9342589470547096$$

We can now see that this has generated a list of numbers with, approximatley, a mean 0 and a variance 1. Obviously with more samples it will be closer to the desired mean and variance since the sample size would be larger

## How to find quantiles of a defined distribution

For any of the distributions $X$ you can find their quantiles, which is to find the value of $x$ at which the probability of something happening is less than or equal to a probability you parse into it. In other words to find $x$ given $p$

$$P(X ≤ x) = p\ \text{for}\ 0 < p < 1 $$

To do this you must [define a distribution](tutorials.md#How-to-define-a-distribution) and parse

```python
probability_value = p
our_chosen_distribution.FindQuantile(probability_value)
```

---

**For example:**

We will use the standardized normal distribution so that we can check we get the correct value of the quartile

```python
>>> mean_value = 0
>>> variance_value = 1
>>> our_normal_distribution = Beans.NormalDistribution(mean_value, variance_value)

```

First of all we define our standardized normal distribution

```python
>>> our_probability = 0.95
>>> our_normal_distribution.FindQuantile(our_probability)
1.16308715367667*sqrt(2)

```

beanPy uses sympy to compute its functions so it is returned as much of an exact value as it can, obviously when you use this code you may want to just see the decimal value, hence we return the value as a float

```python
>>> float(our_normal_distribution.FindQuantile(our_probability))
1.6448536269514724

```

We can see if this is true by looking at a table of [standardized normal values](https://qualifications.pearson.com/content/dam/pdf/A%20Level/Mathematics/2017/specification-and-sample-assesment/Pearson_Edexcel_A_Level_GCE_in_Mathematics_Formulae_Book.pdf#page=38) you can see that 

```{image} highlightedstatstable.png
:alt: table
:class: bg-primary
:align: center
:width: 400px
```

$$P(X > 1.6449) = 0.05\ \text{and hence}\ P(X ≤ 1.6449) = 0.95$$

And hence we have found the quantile of our defined distribution

## How to plot a PDF of a distribution with given parameters

For all of our supported distributions you can plot them on the graph to have a visualization of how the numbers generated are spread, our library supports being able to change the number of points to draw the graph with - in order to get the required level of accuracy with a speed. To do this you must [define a distribution](tutorials.md#How-to-define-a-distribution) and parse.

```python
number_of_points = 100
our_chosen_distribution.PlotPDF(number_of_points)
```

You can omit *number_of_points* and it will default to 50 points

---

**For example:**

We will use the exponential distribution for this example

```python
>>> lambda_value = 3
>>> our_exponential_distribution = Beans.ExponentialDistribution(lambda_value)

```

For any of the distributions 1000 points is a good balance of speed to accuracy of graph, so we will be using that for ours

```python
>>> number_of_points = 1000
>>> our_exponential_distribution.DrawPDF(number_of_points)

```

```{image} exponentialPDF.png
:alt: PDF
:class: bg-primary
:align: center
:width: 400px
```

# How To Guides

## Modelling a dart player with bivariate distributions

With our sampling techniques you can model a dart player with a distributed probability of hitting certain areas.

In this guide we will model a very good dart player so will have a more accurate horizontal aim but a less accurate vertical aim, such as in real life. To model our samples on a graph we will be using matplotlib so we will need to import it

```python
>>> import matplotlib.pyplot as plt

```

We will be using a normal distribution to model our dart players accuracy as accuracy normally follows a normal distribution, it is also very easy to change a normal distribution to add more spread and change the mean

```python
>>> dart_player_horizontal = Beans.NormalDistribution(0, 0.1)
>>> dart_player_vertical = Beans.NormalDistribution(2, 4)

```

We will now [take our samples](tutorials.md#How-to-take-samples-with-a-chosen-distribution) and add them to tuples to use as our x_values and y_values. We will be using an x_seed and y_seed so you can reproduce the results yourself

```python
>>> number_of_darts = 50
>>> x_seed = 1
>>> y_seed = 2
>>> x_values = dart_player_horizontal.TakeMultipleSamples(number_of_darts, x_seed)
>>> y_values = dart_player_vertical.TakeMultipleSamples(number_of_darts, y_seed)

```

Now we will customize our plot to make it readable and add our dartboard in the centre

```python
>>> draw_dartboard = plt.Circle((0,0), 5, fill=False) #Adds our dartboard
>>> plt.xlim([-9, 9]) #Sets our x axis
>>> plt.ylim([-9, 9]) #Sets our y axis
>>> axes.set_aspect(1) #Keeps the plot in a 1:1 ratio
>>> axes.add_artist(draw_dartboard) #Adds our dartboard to the plot
>>> plt.show() #Shows the plot

```

As you can see we have an empty dart board nice and centred in our plot that has kept its aspect ratio

```{image} circleplot.png
:alt: circleplot
:class: bg-primary
:align: center
:width: 400px
```

Now we will add our darts to the board by adding in our darts before we show the plot

```python
>>> axes.add_artist(draw_dartboard) #Adds our dartboard to the plot
>>> darts = plt.scatter(x_values, y_values) #Adds our darts to the plot
>>> plt.show() #Shows the plot

```

As you can see our dart player went for the triple 20, and was fairly consistent at getting it at the correct horizontal place but strugged with the verticallity

```{image} dartplot.png
:alt: dartplot
:class: bg-primary
:align: center
:width: 400px
```

# Explanations

## An explanation on how the parameters change the distribution of numbers generated

In a normal distribution with the given parameters $\sigma$, $\mu^2$

$$ X \sim N(\mu, \sigma^2) $$

The probability of each value is given by:

$$ P(X = x) = \frac{1}{\sqrt{2\pi\sigma^2}}e^{\frac{-(x-\mu)^2}{2\sigma^2}} $$

Our code picks random values of $0 < x < 1$, and as the equation above weighs the numbers towards the mean μ and the spread around the mean is changed by the variance $\mu^2$. This is similar to all of the other types of distributions but with different equations to calculate the $P(X=x)$ and therefore different steepness of curves and how affected they are by their parameters

This is easily visualized by [plotting a PDF](./tutorials.md#how-to-plot-a-pdf-of-a-distribution-with-given-parameters) of the chosen distribution with our library, however we decided to speed up the plotting by having the graph be made with systematic choices of x rather than random ones as otherwise it was too slow for large n values

## A brief overview of quantiles

A quantile is a value at which, for any of the distributions X

$$P(X ≤ x) = p\ \text{for}\ 0 < p < 1 $$

I like to think of it as the area under the [PDF curve](./tutorials.md#how-to-plot-a-pdf-of-a-distribution-with-given-parameters), it is useful to think of it that was as when you generate a sample of random numbers with our library, you can say for sure what is the probability that we have so many values less than or equal to a certain value, which can be very useful to know

# Testing the code

## Testing the code

To test the code run

```
$ python test_beanPy.py
```

## Testing the documentation

To test the documentation:

```
$ python -m doctest README.md
```

# Bibliography

The wikipedia pages on probability may contain useful information

> <https://en.wikipedia.org/wiki/Probability_density_function>
> <https://en.wikipedia.org/wiki/Cumulative_distribution_function>

For our library it is not strictley nessesary to know what each of the distributions are as all the computations are done for you and you can visualize them with our [PDF function](./tutorials.md#how-to-plot-a-pdf-of-a-distribution-with-given-parameters)