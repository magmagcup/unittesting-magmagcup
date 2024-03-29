from math import gcd, copysign, inf


class Fraction:
    """A fraction with a numerator and denominator and arithmetic operations.

    Fractions are always stored in proper form, without common factors in 
    numerator and denominator, and denominator >= 0.
    Since Fractions are stored in proper form, each value has a
    unique representation, e.g. 4/5, 24/30, and -20/-25 have the same
    internal representation.
    """
    
    def __init__(self, numerator, denominator=1):
        """Initialize a new fraction with the given numerator
           and denominator (default 1).
        """
        if not isinstance(numerator, int) and not isinstance(denominator,int):
            raise TypeError('Input argument type must be integer.')
        greatest_common_div = gcd(numerator,denominator)
        if greatest_common_div == 0:
            greatest_common_div = 1
        self.numerator = int((numerator/greatest_common_div)
                             / copysign(1, denominator))
        self.denominator = int((denominator/greatest_common_div)
                               / copysign(1, denominator))
        self.sign = copysign(1, self.numerator)
        self.special_value = None
        if self.denominator == 0:
            if self.numerator == 0:
                # The reason why I decide to defined nan(Not A Number)
                # as 'nan' is that nan is not equal to nan.
                self.special_value = 'nan'
            else:
                self.numerator = int(1 * self.sign)
                self.special_value = inf * self.sign

    def __add__(self, frac):
        """Return the sum of two fractions as a new fraction.
           Use the standard formula  a/b + c/d = (ad+bc)/(b*d)
        """
        if self.special_value is None and frac.special_value is None:
            numerator = int((frac.denominator * self.numerator) +
                            (self.denominator * frac.numerator))
            denominator = (self.denominator * frac.denominator)
            return Fraction(numerator, denominator)
        else:
            if self.special_value == 'nan' or frac.special_value == 'nan':
                return Fraction(0, 0)
            elif (self.special_value == -inf and frac.special_value == inf) or \
                    (self.special_value == inf and frac.special_value == -inf):
                return Fraction(0, 0)
            elif self.special_value == inf or frac.special_value == inf:
                return Fraction(1, 0)
            else:
                return Fraction(-1, 0)


    def __mul__(self, frac):
        """
        Return a multiple of 2 fraction.
        :param frac: a fraction
        :return: a new fraction which is the product
        of 2 fraction
        """
        if self.special_value is None and frac.special_value is None:
            numerator = self.numerator * frac.numerator
            denominator = self.denominator * frac.denominator
            return Fraction(numerator, denominator)
        else:
            if self.special_value is 'nan' or frac.special_value is 'nan':
                return Fraction(0, 0)
            elif self.numerator == 0 or frac.numerator == 0:
                # 0 * inf = nan
                return Fraction(0, 0)
            elif self.sign * frac.sign == -1:
                return Fraction(-1, 0)
            else:
                return Fraction(1, 0)

    def __str__(self):
        if self.denominator == 1:
            return str(self.numerator)
        return f'{self.numerator}/{self.denominator}'

    def __sub__(self, frac):
        # __sub__ for f-g
        return self.__add__(frac.__neg__())

    def __gt__(self, frac):
        # __gt__  for f > g
        if self.special_value is None and frac.special_value is None:
            return (self.numerator/self.denominator) > (frac.numerator/frac.denominator)
        else:
            if self.special_value == frac.special_value:
                return False
            elif self.special_value == inf or frac.special_value == inf:
                if self.special_value is None or self.special_value == -inf or self.special_value == 'nan' or frac.special_value == 'nan':
                    return False
                else:
                    return True
            else:
                return False


    def __neg__(self):
        # __neg__ for -f (negation)
        return Fraction(-self.numerator, self.denominator)

    def __eq__(self, frac):
        """Two fractions are equal if they have the same value.
           Fractions are stored in proper form so the internal representation
           is unique (3/6 is same as 1/2).
        """
        # nan != nan according to python math library
        return self.numerator == frac.numerator and self.denominator == frac.denominator
