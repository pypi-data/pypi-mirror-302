# intervalues
Efficient combining of intervals of numbers for various applications.

## Getting started
To download and install the most recent version, use pip:
`pip install intervalues`. 
Then, consider this simple example for how to use it:

```python

import intervalues as iv

interval_a = iv.BaseInterval(0, 2)  # Interval from 0 to 2
interval_b = iv.BaseInterval(1, 3)  # Another interval, from 1 to 3  
combined = iv.IntervalMeter([interval_a, interval_b])
combined  # -> IntervalMeter:{BaseInterval[0;0.5]: 1, BaseInterval[0.5;1]: 2, BaseInterval[1;1.5]: 1}
combined[1.5]  # -> 2
```
For more extensive examples, see the examples folder (which, admittedly, needs to be improved and extended).

## Motivation
This package will be useful in the following cases:
- If you have too many intervals and can't easily see which value is featured the most across them.
- If you have a large number of integers to keep track of, and you need to do this more memory efficient than a list of 
all individual numbers
- If you have a list of continuous intervals that need to be combined
- If you want to use a collection of intervals for statistical purposes, like sampling a random number from it

## Features
Contains the following classes:
- IntervalSet (optimized towards keeping track of coverage)
- IntervalList (unstructured collection - faster to create, and can apply FIFO-type decisions)
- IntervalCounter (optimized towards tracking counts, integer-valued and positive)
- IntervalMeter (optimized towards tracking values assigned to individual numbers)
- IntervalPdf (normalized IntervalMeter for statistical purposes)

Currently only continuous intervals of floats are supported, for which the distinction between open and closed intervals
is ignored. In the future, this distinction will be taken into account, as well as only considering integers or 
otherwise discrete intervals (only odd numbers, or only multiples of 0.25, etc.)

There is support for using Rust for combining intervals, which reduces runtime roughly by half for bigger datasets. This
is currently optional, and can be used in one of 2 ways:
- Calling `combine_via_rust` with a list of BaseIntervals.
- Creating an IntervalMeter object with a list of BaseIntervals and `use_rust=True`.

Note that both will convert all numbers to Integers by default. In case you want to use floats, you can specify the
number of decimals to keep by supplying the input `nr_digits=..` via either method. Note that numeric issues might occur
so it might be needed to round the numbers again when they come back (or alternatively, just use the Python 
calculations).

In case an IntervalCounter or IntervalSet is requested, the output can be converted to either. There are plans to
also make it possible to directly construct those via Rust (which especially for the set might matter). After the
functionality is more stabilized and better-tested it might become the default.

### Extended future wish list
- As stated above, conversion of continuous intervals to discrete intervals
- As stated above, the distinction between open and closed intervals.
- Allowing for infinity as upper bound (or -infinity as lower bound)
- Sampling from any of these interval collections, where applicable
- Multi-dimensional intervals (e.g. regions, volumes, etc)
- Fully documented and type-hinted code when the codebase is more stable
- Using intervals for more generic (e.g. non-numeric) tracking of properties: [0,2] is green, [1.8,2.5] is sweet, etc.
- IntervalFunctions: getting different functional outputs for different intervals
- Add more examples, and improve the existing ones.