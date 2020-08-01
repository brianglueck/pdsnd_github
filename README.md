### Date Created

* GitHub project created 2020-07-31

* README.md file created 2020-07-31

### Bike Share Data Analysis

This project is an interactive Python program for exploring bike share data
from three major cities in the United States: Chicago, New York City and
Washington, DC.  The code imports the data from the city that the user selects,
filters it by month and day of week if requested by the user, calculates and
displays descriptive statistics, and then gives the user the option to step
through the data set 5 rows at a time.

### Files used

* README.md - this file, which replaces README.txt from my Python project

* bikeshare.py - code from my bike share Python project

* chicago.csv - bike share data file for Chicago

* new_york_city.csv - bike share data file for New York City

* washington.csv - bike share data file for Washington, DC

### Credits

In addition to the programming concepts taught as part of the Udacity
Programming for Data Science using Python nanodegree program, I used these
websites as references while writing my code:

1. I used the Pandas `DataFrame.shape` attribute from
[Pandas API reference](https://pandas.pydata.org/docs/reference/frame.html)
as a way to come up with the number of rows in a DataFrame, though I think I
could also have used `len(DataFrame.index)` instead.

2. I used `DataFrame.dt.hour` from
[Pandas API reference](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.hour.html)
although I guessed that it would be available after learning about
`DataFrame.dt.month` and `DataFrame.dt.weekday_name` from the solution to
Practice Problem \#3.

3. I used `DataFrame.dt.dayofweek` instead of `DataFrame.dt.weekday_name` (as
shown in the solution to Practice Problem \#3) because I originally thought
that `weekday_name` returned the name of the day, not a number, and the
documentation for `DataFrame.dt.dayofweek` at
[Pandas API reference](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.dayofweek.html)
clearly showed that it returned a number index for the day of the week.  Later
I caught an error in my code, though, because I assumed that `dayofweek`
returned `Sun = 0, ..., Sat = 6` but it actually returns
`Mon = 0, ..., Sun = 6`, so I had to offset that when I created the `day`
column in my `load_data()` function because I wanted to work with
`Sun = 0, ..., Sat = 6` as the indices for my global list `DAYS` to
convert the day's index to its name.

4. To display five rows of data from my `DataFrame` at a time, I was using
`print()` with a slice of my `DataFrame`, but the columns were so truncated
that the user would really only be able to see a few of them.  I learned about
the option `display.max_columns` and how to set it with
`pd.set_option('display.max_columns', None)` from
[Pandas API reference](https://pandas.pydata.org/pandas-docs/stable/user_guide/options.html).
