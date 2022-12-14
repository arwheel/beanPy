from pyexpat import XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE
import numpy as np
import sympy as sym
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator
from math import gamma
from scipy.special import gammainc

class Distribution():
    # This is the generic class that all distributions will inherit from
    def take_sample(self, seed=None):
        '''
        Takes a single sample from a population which follows the given distribution.
        The sample follows a given seed. If no seed is given, it will generate a random seed
        '''
        if self.HasQuantile: #If the function has a defined quantile in beanPy
            if seed is None:
                y = rng_unseeded.random() #Random number in (0,1) using the rng created at the start
            else:
                rng_seeded = np.random.default_rng(seed) #Sets a new seed
                y = rng_seeded.random() #Random number in (0,1) using the seed
            sample = self.find_quantile(y) #Applies that random number to the Quantile function

        else: #If the function takes samples in a different way, such as chi squared
            sample = self._find_sample()
    
        if self.IsDiscrete:
            return(sample)
        
        return( float(sample) )

    def take_multiple_samples(self, num, seed=None):
        '''
        This takes a sample of given size and optional seed.
        '''
        result = [] #Creates a list to be used later
        if seed is None:
            for n in range(num):
                sample = self.take_sample()
                if self.IsDiscrete:
                    result.append(sample)
                else:
                    result.append(float(sample))
        else:
            rng_seeded = np.random.default_rng(seed) #Sets a new seed
            for n in range(num): #This part is very similar to in take_sample
                y = rng_seeded.random()
                sample = self.find_quantile(y)
                if self.IsDiscrete:
                    result.append(sample)
                else:
                    result.append(float(sample))
        
        return(result)

        
    
    def draw_CDF(self, n = 50, safe = False):
        '''
        Draws the CDF graph. 
        It does this by systematically going from 0 - 1 then using that number as the y-axis, plots points for continuous functions.
        For discrete functions, it will plot n + 1 points and stop the graph there.
        The default n is 50, as this ensures a smooth CDF graph for the continuous functions.

        The 'safe' parameter rounds everything in piecewise discrete distributions (such as the uniform discrete distribution) to 6 dp when calculating the x values, and checks the x value rounded to 5 dp against the step rounded to 5 dp. This is to be absolutely safe from floating point errors and will rarely be used.
        Because of the nature of the 'safe' parameter, if it is set to true, the function will not be as good at handling numbers where decimal places after the 5th are significant to the distribution.
        '''
        y_plot = [] #just creating tuples which are later appended to
        x_plot = []
        if not self.IsDiscrete:
            if not self.Piecewise:
                if self.HasQuantile:
                    for i in range(n):
                        y = (i+1)/(n+1) # to ensure an even spread, this will be the y co-ordinate on the graph
                        sample = self.find_quantile(y) #Applies the Quantile function to y, giving the x co-ordinate
                        y_plot.append(y)
                        x_plot.append(sample)
                else: #No Quantile - This method is potentially very slow
                    for i in range(n):
                        x = self.take_sample()
                        x_plot.append(x)
                    x_plot.sort()
                    for i in range(n):
                        y = self.find_CDF(x_plot[i])
                        y_plot.append(y)
            else:
                for i in range(n + 1):
                    y = i / n
                    x = self.find_quantile(y)
                    y_plot.append(y)
                    x_plot.append(x)
            plt.plot(x_plot,y_plot)
        else:
            if not self.Piecewise:
                for i in range(n + 1):
                    x_plot.append(i)
                    y_plot.append(self.find_CDF(i))
            else:
                if safe:
                    for i in range(int(n / self.step + 3)):
                        x_plot.append(round((i * self.step + self.min - 2 * self.step),6))
                        y_plot.append(self.find_CDF(i * self.step + self.min - 2 * self.step, safe = True))
                else:
                    for i in range(int(n / self.step + 3)):
                        x_plot.append(round((i * self.step + self.min - 2 * self.step),10))
                        y_plot.append(self.find_CDF(i * self.step + self.min - 2 * self.step))
            plt.plot(x_plot,y_plot,'o')
        plt.show(block = False)
        
    def draw_PDF(self, n = 50, safe = False):
        '''
        Draws the PDF graph. This takes about twice as long as the CDF graph.
        It does the systematic approach from the CDF, then converts that into an X value, then finds the PDF.
        The default here is 50, as it's a good number for this because it ensures a smooth graph for continuous functions.
        The 'n' input means the same thing as for the CDF

        The 'safe' parameter here is the same as in the draw_CDF function
        '''
        y_plot = []
        x_plot = []
        if not self.IsDiscrete:
            if not self.Piecewise:
                if self.HasQuantile:
                    for i in range(n):
                        a = (i+1)/(n+1) # this ensures an even spread
                        x = self.find_quantile(a) #finds the x co-ordinate like in CDF
                        y = self.find_PDF(x) #finds the y co-ordinate
                        y_plot.append(y)
                        x_plot.append(x)
                else: #No Quantile - This method is potentially very slow
                    for i in range(n):
                        x = self.take_sample()
                        x_plot.append(x)
                    x_plot.sort()
                    for i in range(n):
                        y = self.find_PDF(x_plot[i])
                        y_plot.append(y)
            else:
                for i in range(n + 1):
                    a = (i) * (self.max - self.min) / (n) + self.min
                    x_plot.append(a)
                    y_plot.append(self.find_PDF(a))
            plt.plot(x_plot,y_plot)
        else:
            if not self.Piecewise:
                for i in range(n + 1):
                    x_plot.append(i)
                    y_plot.append(self.find_PDF(i))
            else:
                if safe:
                    for i in range(int(n / self.step + 3)):
                        a = round((i * self.step + self.min - 2 * self.step),6) #for better readability, and it's rounded to 10 to avoid the floating point error
                        x_plot.append(a)
                        y_plot.append(self.find_PDF(a, safe = True))
                else:
                    for i in range(int(n / self.step + 3)):
                        a = round((i * self.step + self.min - 2 * self.step),10) #for better readability, and it's rounded to 10 to avoid the floating point error
                        x_plot.append(a)
                        y_plot.append(self.find_PDF(a))

            plt.plot(x_plot,y_plot,'o')
        plt.show(block = False)
    
    def draw_linear_regression(self,a,b,var,n):
        '''
        Displays a linear regression graph with Y = a + bX + epsilon error with 'var' variance
        The distribution determines the spread of X values, and n values are created
        '''
        Normal_Epsilon = normal_distribution(0,var)
        x_plt = []
        y_plt = []
        for i in range(n):
            X = self.take_sample()
            Y = X * b + a + Normal_Epsilon.take_sample()
            x_plt.append(X)
            y_plt.append(Y)
        plt.plot(x_plt,y_plt,'o')
        plt.show(block = False)
            
        
        

class normal_distribution(Distribution):
    def __init__(self,mean,var):
        '''
        This gives the distribution all the common information. You can call any of these, apart from x of course.
        Calling these attributes gives the value or a formula, depending on which you call
        '''
        self.IsDiscrete = False
        self.Piecewise = False
        self.HasQuantile = True
        self.min = -np.inf
        self.max = np.inf
        self.mean = mean
        self.var = var
        self.sd = var ** (1 / 2) # this is a bit of a cheat I know...
        x = sym.Symbol("x")
        self.pdf = (1 / (self.sd * sym.sqrt(2 * sym.pi))) * sym.exp(-(1 / 2) * ((x - mean) / self.sd) ** 2) 
        self.cdf = (1 / 2) + (1 / 2) * sym.erf((x - mean) / (self.sd * sym.sqrt(2)))
        self.quantile = self.mean + self.sd * sym.sqrt(2) * sym.erfinv(2 * x - 1)
        
    def find_PDF(self,x):
        """
        This finds the distributions probability density function at a given value of x
        """
        return (1 / (self.sd * sym.sqrt(2 * sym.pi))) * sym.exp(-(1 / 2) * ((x - self.mean) / self.sd) ** 2)
    def find_CDF(self, x):
        """
        This finds the distributions cumulative density function at a given value of x
        """
        return ((1 / 2) + (1 / 2) * sym.erf((x - self.mean) / (self.sd * sym.sqrt(2))))
    def find_quantile(self,p):
        """
        This finds the distributions quantile at a given value x
        """
        if p < 0 or p > 1:
            print("Invalid number inputted into the Normal Distribution Quantile Function. This will now return the value 1. The number inputted to the Normal Distribution Quantile Function was: " + str(p))
            return 1
        else:
            return self.mean + self.sd * sym.sqrt(2) * sym.erfinv(2 * p - 1)

class exponential_distribution(Distribution):
    def __init__(self,l):
        '''
        This gives the distribution all the common information. You can call any of these, apart from x of course.
        Calling these attributes gives the value or a formula, depending on which you call
        '''
        self.IsDiscrete = False
        self.Piecewise = False
        self.HasQuantile = True
        self.min = 0
        self.max = np.inf
        self.mean = 1 / l
        self.var = 1 / (l ** 2)
        self.sd = 1 / l
        x = sym.Symbol("x")
        self.pdf = l * sym.exp(- l * x)
        self.cdf = 1 - sym.exp(- l * x)
        self.quantile = -sym.ln(1 - x) / l
        
        '''
        These functions (find_PDF and find_quantile) are technically not needed, as we can just use sympy.subs on the pdf and cdf,
        however the use of these functions causes the graphs to appear a lot quicker.
        '''
    def find_PDF(self,x):
        """
        This finds the distributions probability density function at a given value of x
        """
        if not x > 0:
            return 0
        return (1/self.mean) * sym.exp(- (1/self.mean) * x)
    def find_CDF(self, x):
        """
        This finds the distributions cumulative density function at a given value of x
        """
        if not x > 0:
            return 0
        return (1 - sym.exp(- 1/self.mean * x))
    def find_quantile(self,p):
        """
        This finds the distributions quantile at a given value x
        """
        if p < 0 or p > 1:
            print("Invalid number inputted into the Exponential Distribution Quantile Function. This will now return the value 1. The number inputted to the Exponential Distribution Quantile Function was: " + str(p))
            return 1
        else:
            return -sym.ln(1 - p) * self.mean


class poisson_distribution(Distribution):
    def __init__(self,l):
        '''
        This gives the distribution all the common information. You can call any of these, apart from x of course.
        Calling these attributes gives the value or a formula, depending on which you call
        '''
        self.IsDiscrete = True
        self.Piecewise = False
        self.HasQuantile = True
        self.min = 0
        self.max = np.inf
        self.mean = l
        self.var = l
        self.sd = sym.sqrt(l)
        x = sym.Symbol("x")
        k = sym.Symbol("k")
        self.pdf = l ** x * sym.exp(-l) / sym.factorial(x)
        self.cdf = sym.exp(-l) * sym.summation(((l ** k ) / sym.factorial(k) ),(k,0,sym.floor(x)))

    def find_PDF(self,x):
        """
        This finds the distributions probability density function at a given value of x
        """
        if not x > 0:
            return 0
        return self.mean ** x * sym.exp(-self.mean) / sym.factorial(x)
    def find_CDF(self,x):
        """
        This finds the distributions cumulative density function at a given value of x
        """
        if not x > 0:
            return 0
        k = sym.Symbol("k")
        return sym.exp(-self.mean) * sym.summation(((self.mean ** k ) / sym.factorial(k) ),(k,0,sym.floor(x)))
    def find_quantile(self,p):
        """
        This finds the distributions quantile at a given value x
        """
        Found = False
        n = 0
        if p < 0 or p > 1 or p == 1:
            print("Invalid number inputted into the Poisson Distribution Quantile Function. This will now return the value 1. The number inputted to the Poisson Distribution Quantile Function was: " + str(p))
            return 1
        '''
        This is for discrete and piecewise distributions only. It checks if the given is less than the cdf for n starting 
        from 0 until the end is found. If the given value is 1, this will go on forever.
        '''
        while Found == False:
            if p < self.cdf.subs('x', n):
                Found = True
            else:
                n = n + 1

        return int(n)
        

class continuous_uniform_distribution(Distribution):
    def __init__(self,a,b):
        '''
        This gives the distribution all the common information. You can call any of these, apart from x of course.
        Calling these attributes gives the value or a formula, depending on which you call
        '''
        if not b > a:
            print("Invalid Parameters. The second number must be greater than the first.")
        else:
            self.IsDiscrete = False
            self.Piecewise = True
            self.HasQuantile = True
            self.mean = (a + b) / 2
            self.var = (b - a) / 12
            self.sd = sym.sqrt(self.var)
            self.max = b
            self.min = a
            x = sym.Symbol("x")
        
        '''
        These functions (find_PDF and find_quantile) are technically not needed, as we can just use sympy.subs on the pdf and cdf,
        however the use of these functions causes the graphs to appear a lot quicker.
        '''
    def find_PDF(self,x):
        """
        This finds the distributions probability density function at a given value of x
        """
        if x < self.min:
            return 0
        elif x > self.max:
            return 0
        else:
            return 1 / (self.max - self.min)
    def find_CDF(self,x):
        """
        This finds the distributions cumulative density function at a given value of x
        """
        if x < self.min:
            return 0
        elif x > self.max:
            return 1
        else:
            return (x - self.min) / (self.max - self.min)
    def find_quantile(self,p):
        """
        This finds the distributions quantile at a given value x
        """
        if p < 0 or p > 1:
            print("Invalid number inputted into the Continuous Uniform Distribution Quantile Function. This will now return the value 1. The number inputted to the Exponential Distribution Quantile Function was: " + str(p))
            return 1
        else:
            return ((self.max - self.min) * p + self.min)





class discrete_uniform_distribution(Distribution):
    def __init__(self,min,max,step = 1):
        '''
        This gives the distribution all the common information. You can call any of these, apart from x of course.
        Calling these attributes gives the value or a formula, depending on which you call
        '''
        if not max > min:
            print("The max must be greater than the min!")
        
        self.IsDiscrete = True
        self.Piecewise = True
        self.HasQuantile = True
        self.NumOfSteps = int((max - min) / step) + 1
        self.mean = (max + min) / 2
        self.var = ((self.NumOfSteps) ** 2 - 1) / 12
        self.sd = sym.sqrt(self.var)
        self.min = min
        self.step = step
        self.max = min + (self.NumOfSteps - 1) * step
        x = sym.Symbol("x")
        k = sym.Symbol("k")
        self.pdf = 1 / self.NumOfSteps
        self.cdf = sym.summation((1 / self.NumOfSteps),(k,0,sym.floor(x)))

    def find_PDF(self,x, safe = False):
        """
        This finds the distributions probability density function at a given value of x
        """
        #These if conditions check if the value is a gap or a value
        if sym.floor(round(((x - self.min) / self.step),5)) == round(((x - self.min) / self.step),5) and not x < self.min and not x > self.max and safe:
            return 1 / self.NumOfSteps
        elif sym.floor(round(((x - self.min) / self.step),9)) == round(((x - self.min) / self.step),9) and not x < self.min and not x > self.max:
            return 1 / self.NumOfSteps
        else:
            return 0
    def find_CDF(self,x,safe = False):
        """
        This finds the distributions cumulative density function at a given value of x
        """
        if x < self.min:
            return 0
        elif x > self.max or x == self.max:
            return 1
        elif safe:
            cdf = 0  #Doing this method because summation function is buggy
            for i in range(sym.floor(round((1 + (x - self.min) / self.step),5))): #This long expression is how many steps have been done already
                cdf += self.find_PDF(self.min + self.step * i, safe = True)
            return cdf
        else:
            cdf = 0  #Doing this method because summation function is buggy
            for i in range(sym.floor(round((1 + (x - self.min) / self.step),9))): #This long expression is how many steps have been done already
                cdf += self.find_PDF(self.min + self.step * i)
            return cdf

            
    def find_quantile(self,p):
        """
        This finds the distributions quantile at a given value x
        """
        Found = False
        n = 0
        if p < 0 or p > 1:
            print("Invalid number inputted into the Discrete Uniform Distribution Quantile Function. This will now return the value 1. The number inputted to the Poisson Distribution Quantile Function was: " + str(p))
            return 1
        '''
        This is for discrete and piecewise distributions only. It checks if the given is less than the cdf for n starting 
        from 0 until the end is found. If the given value is 1, this will go on forever.
        '''
        while Found == False:
            if p < n / (self.NumOfSteps):
                Found = True
            else:
                n = n + 1 #This is how many steps it is greater than, -1

        return self.min + (n - 1) * self.step #this fixes the -1 problem

class binomial_distribution(Distribution):
    def __init__(self,n,p):
        self.IsDiscrete = True
        self.Piecewise = False
        self.HasQuantile = True
        self.mean = n * p
        self.var = n * p * (1-p)
        self.sd = sym.sqrt(self.var)
        self.max = n
        self.min = 0
        self.probability = p
        x = sym.Symbol("x")
        k = sym.Symbol("k")
        self.pdf = _choose(n,x) * (p ** x) * ((1 - p) ** (n - x))

    def find_PDF(self,x,safe = False):
        if x < self.min or x > self.max:
            return 0
        if -1 < x and x < self.max + 1 and sym.floor(x) == x:
            result = _choose(self.max,x) * (self.probability ** x) * ((1 - self.probability) ** (self.max - x))
        else:
            result = 0
        return result

    def find_CDF(self,x,safe = False):
        total = 0
        for n in range(sym.ceiling(x + 1)):
            total += self.find_PDF(n)
        return total

    def find_quantile(self,x):
        found = False
        n = 0
        while found == False:
            if x < self.find_CDF(n):
                found = True
            else:
                n += 1
        return n

class chi_squared_distribution(Distribution):
    def __init__(self,k):
        if not sym.floor(k) == k or k<1:
            print("Error: You did not enter a natural number for the degrees of freedom")
        else:
            self.IsDiscrete = False
            self.Piecewise = False
            self.HasQuantile = False
            self.mean = k
            self.var = 2 * k
            self.sd = sym.sqrt(self.var)
            self.max = np.inf
            self.min = 0
            self.dof = k
            x = sym.Symbol("x")
            t = sym.Symbol("t")
            self.pdf = x**(k/2 - 1) * sym.exp(-x/2)/(gamma(k/2)* 2 ** (k/2))
            self.cdf = sym.integrate((t) ** (k/2 - 1) * sym.exp(-t),(t,0,x/2)) / gamma(k/2)

    def find_PDF(self,x):
        z = x ** (self.dof/2 - 1) * np.e ** (-x/2)/(gamma(self.dof/2) * 2 ** (self.dof/2))
        return z

    def find_CDF(self,x):
        z = gammainc(self.dof/2, x/2) / gamma(self.dof/2)
        return z

    def _find_sample(self):
        standard_normal = normal_distribution(0,1)
        result = 0
        for n in range(self.dof):
            z = standard_normal.take_sample()
            z = z ** 2
            result += z
        return result

    #There is no find quantile function as it is too difficult


class joint_distribution():
    def __init__(self,d1,d2):
        x = sym.Symbol("x")
        y = sym.Symbol("y")
        self.x_dist = d1
        self.y_dist = d2
        pdf1 = self.x_dist.pdf
        pdf2 = self.y_dist.pdf
        pdf2 = pdf2.subs(x, y)
        self.pdf = pdf1 * pdf2
        k = sym.integrate(sym.integrate(self.pdf,(x,self.x_dist.min,self.x_dist.max)),(y,self.y_dist.min,self.y_dist.max))
        self.pdf = (self.pdf / k).simplify()

    def find_PDF(self,xval,yval):
        x = sym.Symbol("x")
        y = sym.Symbol("y")
        z = self.pdf.subs(x, xval)
        z = z.subs(y, yval)
        if xval < self.x_dist.min or xval > self.x_dist.max or yval < self.y_dist.min or yval > self.y_dist.max:
            return 0
        return z

    def draw_PDF(self,x_stuff,y_stuff):
        '''
        Draws the joint PDF on a heatmap graph. x_stuff is a 3-tuple whose elements are:
        The lower bound of x to be graphed, the upper bound of x to be graphed, and the number of points in the x-axis to be graphed. (The order is important)
        Similar for y_stuff
        '''
        
        x_step = (x_stuff[1] - x_stuff[0]) / x_stuff[2]
        y_step = (y_stuff[1] - y_stuff[0]) / y_stuff[2]
        z_array = [[0 for n in range(x_stuff[2])] for i in range(y_stuff[2])]
        y_plt = np.linspace(y_stuff[0],y_stuff[1],y_stuff[2])
        x_plt = np.linspace(x_stuff[0],x_stuff[1],x_stuff[2])
        M = np.array([[float(self.find_PDF(x,y)) for x in x_plt] for y in y_plt])
        plt.imshow(M)
        plt.colorbar()
        plt.show()

    def take_sample(self):
        return self.x_dist.take_sample(), self.y_dist.take_sample()




    


            




rng_unseeded = np.random.default_rng()
rng_seeded = np.random.default_rng()

def _choose(n,k):
    '''
    This is here just because I coudn't find a nice to use function on sympy or numpy
    '''
    #if k > n:      This is technically needed for the choose function, but nobody will be using this function because it is locked behing distributions
    #    return 0
    result = sym.factorial(n) / (sym.factorial(k) * sym.factorial(n - k))
    return result