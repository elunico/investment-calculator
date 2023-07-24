import argparse
from functools import total_ordering
from typing import Union


def ordered(cls):

    def equals(self, other):
        if type(self) is not type(other):
            return NotImplemented

        for key in self.__dict__:
            if getattr(self, key) != getattr(other, key):
                return False
        return True

    setattr(cls, '__eq__', equals)
    return total_ordering(cls)


@ordered
class InterestRate:
    def __init__(self, decimal: float):
        self.decimal = decimal

    @classmethod
    def frompercentage(cls, percentage: float):
        return cls(percentage / 100)

    @property
    def value(self) -> float:
        return self.decimal

    def __str__(self) -> str:
        return '{}%'.format(100 * self.value)

    def __lt__(self, other: 'InterestRate') -> bool:
        if not type(other) is InterestRate:
            return NotImplemented
        return self.value < other.value


@ordered
class TimeUnit:
    def __init__(self, name: str, monthly_conversion_factor: float) -> None:
        self.name = name
        self.monthly_conversion_factor = monthly_conversion_factor

    def __lt__(self, other: 'TimeUnit') -> bool:
        if not type(other) is TimeUnit:
            return NotImplemented
        return self.months(1) < other.months(1)

    def months(self, amount: float) -> float:
        return amount * self.monthly_conversion_factor

    def __str__(self) -> str:
        return '{}'.format(self.name)

    def __repr__(self) -> str:
        return 'TimeUnit[{}]'.format(str(self))


DAY = TimeUnit('days', 30.4368)
WEEK = TimeUnit('weeks', 4.345)
FORTNIGHT = TimeUnit('fortnight', 2.1726)
MONTH = TimeUnit('months', 1)
BIMONTH = TimeUnit('bimonth', 1/2)
QUARTER = TimeUnit('quarter', 1/4)
YEAR = TimeUnit('years', 1/12)


@ordered
class Contribution:
    def __init__(self, amount: float, unit: TimeUnit):
        self.amount = amount
        self.unit = unit

    @property
    def montly_amount(self) -> float:
        return self.unit.months(self.amount)

    def __lt__(self, other: 'Contribution') -> bool:
        if not type(other) is Contribution:
            return NotImplemented

        return self.montly_amount < other.montly_amount


@ordered
class DollarAmount:
    def __init__(self, dollars: int, cents: int, fractions: int) -> None:
        self.dollars = dollars
        self.cents = cents
        self.fractions = fractions

    @classmethod
    def fromfloat(cls, value: float) -> 'DollarAmount':
        dollars = int(value)
        cents = int((value - dollars) * 100)
        fraction = value - dollars - cents
        return DollarAmount(dollars, cents, fraction)

    @property
    def value(self) -> float:
        return self.dollars + self.cents / 100 + self.fractions

    def __str__(self) -> str:
        return '${:,.2f}'.format(self.dollars+(self.cents/100))

    def __repr__(self) -> str:
        return 'DollarAmount({}, {}, {})'.format(self.dollars, self.cents, self.fractions)

    def __lt__(self, other: Union['DollarAmount', float]) -> bool:
        if not type(other) is DollarAmount and not type(other) is float and not type(other) is int:
            return NotImplemented
        return self.value < other.value


def calculate_return(principle: float, rate: InterestRate, contribution: Contribution, years: int, compound_frequency: TimeUnit = MONTH) -> DollarAmount:
    compound_factor = int(compound_frequency.monthly_conversion_factor * 12)
    balance = principle
    for i in range(years * compound_factor):
        balance = balance * (1 + (rate.value / (compound_factor)))
        balance += (contribution.montly_amount * (12 / compound_factor))

    return DollarAmount.fromfloat(balance)


def unit_for(num):
    return {'1': DAY, '2': WEEK, '3': MONTH, '4': YEAR}[num]


def run_with_inputs(amount, percent, frequency, contribution, years):
    interest_rate = InterestRate.frompercentage(percent) if percent is not None else None

    starting_amount = float(input("Enter the starting balance: ")) if amount is None else amount
    interest_rate = InterestRate.frompercentage(float(input("Enter the interest percentage: "))) if interest_rate is None else interest_rate

    if frequency is None and contribution is None:
        frequency = unit_for(input('Enter the frequency of contribution (1) daily | (2) weekly | (3) monthly | (4) yearly: '))
        contribution = DollarAmount.fromfloat(float(input("Amount of contributions: ")))
    elif frequency is None:
        frequency = unit_for(input('Enter the frequency of contribution (1) daily | (2) weekly | (3) monthly | (4) yearly: '))
        contribution = DollarAmount.fromfloat(contribution)
    elif contribution is None:
        frequency = unit_for(frequency)
        contribution = DollarAmount.fromfloat(float(input("Amount of contributions: ")))
    else:
        frequency = unit_for(frequency)
        contribution = DollarAmount.fromfloat(contribution)

    years = int(float(input("Years to allow growth: "))) if years is None else years

    print(f'\nAfter {years} years at {interest_rate} starting with {DollarAmount.fromfloat(starting_amount)} and contributing {contribution} every {frequency}, you will have')
    print(calculate_return(starting_amount, interest_rate, Contribution(contribution.value, frequency), years))


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('-a', '--amount', help='Starting balance of the investment', type=float)
    ap.add_argument('-p', '--percent', help='The interest rate percentage for the investment', type=float)
    ap.add_argument('-f', '--frequency', help='Frequency of contribution (1) daily | (2) weekly | (3) monthly | (4) yearly')
    ap.add_argument('-c', '--contribution', help='Amount of money to contribute repeatedly to the account', type=float)
    ap.add_argument('-y', '--years', help='Number of years to allow the investment to be active', type=int)

    return ap.parse_args()


def main():
    options = parse_args()

    run_with_inputs(options.amount, options.percent, options.frequency, options.contribution, options.years)

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
