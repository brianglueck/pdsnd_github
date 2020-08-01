# bikeshare.py - Python code for Brian Glueck's Python project
# for Udacity's "Programming for Data Science with Python" nanodegree program

import time
import pandas as pd
import numpy as np

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']


DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
        'Saturday']

HOURS = ['12 AM', '1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM', '7 AM',
         '8 AM', '9 AM', '10 AM', '11 AM', '12 PM', '1 PM', '2 PM', '3 PM',
         '4 PM', '5 PM', '6 PM', '7 PM', '8 PM', '9 PM', '10 PM', '11 PM']


def choose(choices):
    """
    Prompt user to choose from a list of choices.  Parses the user's
    input until he or she makes a valid choice from the provided list.

    Args:
        (list) choices - list of choices (str) for the user to choose from
    Returns:
        (str) choice - the user's valid choice from the provided list
    """
    while True:
        choice = input('Choose one of [{}]: '.format(', '.join(choices)))
        if choice in choices:
            break
        else:
            print("Sorry, I didn't recognize that choice.  Let's try again.")
    return choice


def full_month(month):
    """
    Expands month from first three letters to full month name, or 'all' if
    month is 'all'

    Args:
        (str) month - first three letters of a month's name or 'all'
    Returns:
        (str) month - full month name or 'all' if month is 'all'
    """
    months = {'Jan': 'January', 'Feb': 'February', 'Mar': 'March',
              'Apr': 'April', 'May': 'May', 'Jun': 'June', 'Jul': 'July',
              'Aug': 'August', 'Sep': 'September', 'Oct': 'October',
              'Nov': 'November', 'Dec': 'December', 'all': 'all'}

    return months.get(month, "Unrecognized month")


def full_day(day):
    """
    Expands day from a simple 1- or 2-letter abbreviation
        Su, M, Tu, W, Th, F, Sa
    to the full day name, or 'all' if day is 'all':
        Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday

    Args:
        (str) day - simple abbreviation of a day's name or 'all'
    Returns:
        (str) day - full day name or 'all' if day is 'all'
    """
    days = {'Su': 'Sunday', 'M': 'Monday', 'Tu': 'Tuesday', 'W': 'Wednesday',
            'Th': 'Thursday', 'F': 'Friday', 'Sa': 'Saturday', 'all': 'all'}

    return days.get(day, "Unrecognized day")


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze (lower case)
        (str) month - name of the month to filter by, or 'all' to apply no month
                      filter
        (str) weekday - name of the day of week to filter by, or 'all' to apply
                        no day filter
    """
    print("Hi! Let's explore some US bike share data together.\n")

    # get user input for which city's data to explore
    print("Which city's data would you like to explore?")
    city = choose(['Chicago', 'New York', 'Washington'])

    # get user input for how to filter the data by month and/or day
    print('\nWould you like to filter the data by month, day, both, or none?')
    filter = choose(['month', 'day', 'both', 'none'])

    # get user input for month to filter by (if requested)
    if filter in ['month', 'both']:
        month = choose(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'])
    else:
        month = 'all'

    # get user input for day to filter by (if requested)
    if filter in ['day', 'both']:
        weekday = choose(['Su', 'M', 'Tu', 'W', 'Th', 'F', 'Sa'])
    else:
        weekday = 'all';

    print('-'*80)
    return city, full_month(month), full_day(weekday)


def load_data(city, month, day):
    """
    Loads data for the specified city, filtered by month and day if applicable.

    Args:
        (str) city - name of city to analyze
        (str) month - name of month to filter by, or 'all' for no filtering
        (str) day - name of day of week to filter by, or 'all' for no filtering
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # give the user a confirmation message about what data will be loaded
    print('Loading bike share data for {} ...'.format(city))
    if month == 'all' and day == 'all':
        print('... unfiltered ...')
    else:
        print('... filtered by month = {}, day = {} ...'.format(month, day))

    start_time = time.time()

    # load data file into a Pandas DataFrame
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day'] = (df['Start Time'].dt.dayofweek + 1) % 7 # Sun = 0, ... Sat = 6
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if requested
    if month != 'all':
        # use the index of the MONTHS list to get the corresponding int
        month = MONTHS.index(month) + 1

        # filter by month to create the new DataFrame
        df = df[df['month'] == month]

    # filter by weekday if requested
    if day != 'all':
        # use the index of the DAYS list to get the corresponding int
        day = DAYS.index(day)

        # filter by weekday to create the new DataFrame
        df = df[df['day'] == day]

    print('\n{} records loaded'.format(len(df.index)))

    print('\n... this took {} seconds to complete'.format(time.time() - start_time))
    print('-'*80)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('Calculating the most frequent times of travel ...\n')
    start_time = time.time()

    # display the most common month(s)
    month_mode = df['month'].mode()
    if month_mode.size == 1:
        print('most frequent month: {}'.format(MONTHS[month_mode[0] - 1]))
    else:
        print('most frequent months:')
        for i in range(month_mode.size):
            print('    {}'.format(MONTHS[month_mode[i] - 1]))

    # display the most common day(s) of week
    day_mode = df['day'].mode()
    if day_mode.size == 1:
        print('\nmost frequent day: {}'.format(DAYS[day_mode[0]]))
    else:
        print('\nmost frequent days:')
        for i in range(day_mode.size):
            print('    {}'.format(DAYS[day_mode[i]]))

    # display the most common start hour(s)
    hour_mode = df['hour'].mode()
    if hour_mode.size == 1:
        print('\nmost frequent start hour: {}'.format(HOURS[hour_mode[0] - 1]))
    else:
        print('\nmost frequent start hours:')
        for i in range(hour_mode.size):
            print('    {}'.format(HOURS[hour_mode[i] - 1]))

    print('\n... this took {} seconds to complete'.format(time.time() - start_time))
    print('-'*80)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating the most popular stations and trip ...\n')
    start_time = time.time()

    # display most commonly used start station(s)
    start_mode = df['Start Station'].mode()
    if start_mode.size == 1:
        print('most popular starting station: {}'.format(start_mode[0]))
    else:
        print('most popular starting stations:')
        for i in range(start_mode.size):
            print('    {}'.format(start_mode[i]))

    # display most commonly used end station(s)
    end_mode = df['End Station'].mode()
    if end_mode.size == 1:
        print('\nmost popular ending station: {}'.format(end_mode[0]))
    else:
        print('\nmost popular ending stations:')
        for i in range(end_mode.size):
            print('    {}'.format(end_mode[i]))

    # display most frequent combination(s) of start station and end station trip
    df['trip'] = df['Start Station'] + ' to ' + df['End Station']
    trip_mode = df['trip'].mode()
    if trip_mode.size == 1:
        print('\nmost popular trip: {}'.format(trip_mode[0]))
    else:
        print('\nmost popular trips:')
        for i in range(trip_mode.size):
            print('    {}'.format(trip_mode[i]))

    print('\n... this took {} seconds to complete'.format(time.time() - start_time))
    print('-'*80)


def hms(n):
    """
    Converts an elapsed time in seconds to hours, minutes and seconds.

    Args
        (int) n - elapsed time in seconds to be converted
    Returns
        (int) hours - number of hours
        (int) minutes - number of minutes from 0 (inclusive) to 60 (exclusive)
        (int) seconds - number of seconds from 0 (inclusive) to 60 (exclusive)
    """
    seconds = int(n % 60)
    minutes = int((n - seconds)/60 % 60)
    hours = int(((n - seconds)/60 - minutes)/60)

    return hours, minutes, seconds


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('Calculating trip duration ...\n')
    start_time = time.time()

    # display total travel time
    hr, min, sec = hms(df['Trip Duration'].sum())
    if hr >= 24:
        print('total trip duration: {} days, {} hours, {} minutes, {} seconds'.format(int(hr/24), hr % 24, min, sec))
    else:
        print('total trip duration: {} hours, {} minutes, {} seconds'.format(hr, min, sec))

    # display mean travel time
    hr, min, sec = hms(df['Trip Duration'].mean())
    if hr == 0:
        print('\naverage trip duration: {} minutes, {} seconds'.format(min, sec))
    else:
        print('\naverage trip duration: {} hours, {} minutes, {} seconds'.format(hr, min, sec))

    print('\n... this took {} seconds to complete'.format(time.time() - start_time))
    print('-'*80)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('Calculating user statistics ...\n')
    start_time = time.time()

    # display counts of user types
    print('User type breakdown:')
    print(df['User Type'].value_counts())

    # display counts of gender
    if 'Gender' in df.columns:
        print('\nGender breakdown:')
        print(df['Gender'].value_counts())
    else:
        print('\nThis data does not include gender')

    # display earliest, most recent, and most common birth year(s)
    if 'Birth Year' in df.columns:
        print('\nBirth years:')
        print('earliest        {}'.format(int(df['Birth Year'].min())))
        print('most recent     {}'.format(int(df['Birth Year'].max())))

        year_mode = df['Birth Year'].mode()
        for i in range(year_mode.size):
            print('most common     {}'.format(int(year_mode[i])))
    else:
        print('\nThis data does not include birth year')

    print('\n... this took {} seconds to complete'.format(time.time() - start_time))
    print('-'*80)


def print_data(df):
    """Print five rows of data at a time as requested by the user"""
    # we will use n to slice the DataFrame from row n to row n+5
    n = 0

    # remove columns that we added to the DataFrame for our analysis
    df.pop('month')
    df.pop('day')
    df.pop('hour')
    df.pop('trip')

    # don't truncate columns, otherwise not much of the data will be visible
    pd.set_option('display.max_columns', None)

    # display 5 rows of data at a time as long as the user wants to see it
    print('Would you like to view individual trip data?')
    response = choose(['yes', 'no'])
    for n in range(0, len(df.index), 5):
        if response != 'yes':
            return
        print(df[n:n+5])
        print('\nWould you like to view more individual trip data?')
        response = choose(['yes', 'no'])

    # we only get here if we've reached the end of the DataFrame df
    print("\nYou've reached the end of the data.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_data(df)

        print('\nWould you like to restart?')
        restart = choose(['yes', 'no'])
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
