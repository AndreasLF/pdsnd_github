import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # ----------------------------------------------------------------------------------------------
    # Get city variable from user

    cities_string = ' / '.join(CITY_DATA).title() #Join cities in a string seperated by ' / '
    # loop until a break occurs
    while True:
        #input returns a string so it shouldn't give errors, even if the user inputs a numer
        city_input = input('\nWhich city are you interested in exploring the bike data for?\n ({}) \n'.format(cities_string)).lower()

        if city_input in CITY_DATA: #If the city is defined in CITY_DATA
            city = city_input #set city
            break #break out of loop
        else: #if city is not defined
            print('\nWe don\'t have data for this city. Please enter a valid city\n') #print message and restart loop
    #Show selected city
    print('\nCity selected: {}\n'.format(city).title())

    # ----------------------------------------------------------------------------------------------
    # Ask user how they want to filter the data

    # Define options to filter by
    filter_options = ['none','month','day']

    while True:
        #input returns a string so it shouldn't give errors, even if the user inputs a number
        filter_input = input('\nWould you like to filter the data by \'month\', \'day\' or \'none\' at all?\n').lower()

        if filter_input in filter_options: #If the filter_input is defined in filter_options
            filter = filter_input #set filter
            break #break out of loop
        else:
            print('\nFilter option does not exist. Please enter a valid option\n') #print message and restart loop
    #Show selected filter option
    if filter_input == 'none':
        print('\nYou\'ve chosen not to filter the data\n')
    else:
        print('\nYou\'ve chosen to filter the data by {}\n'.format(filter.title()))

    # ----------------------------------------------------------------------------------------------
    # Get month variable from user


    if filter == 'month':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        months_string = ' / '.join(months).title()

        while True:
            #input returns a string so it shouldn't give errors, even if the user inputs a numer
            month_input = input('\nWhich month are you interested in exploring the bike data for?\n ({}) \n'.format(months_string)).lower()

            if month_input in months: #If the month is defined in months
                month = month_input #set month
                break #break out of loop
            else: #if city is not defined
                print('\nMonth does not exist. Please enter a valid month\n') #print message and restart loop
        #Show selected city
        print('\nMonth selected: {}\n\n'.format(month).title())
    else:
        month = 'all'

    # ----------------------------------------------------------------------------------------------
    # Get day variable from user
    if filter == 'day':
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        days_string = ' / '.join(days).title()

        while True:
            #input returns a string so it shouldn't give errors, even if the user inputs a numer
            day_input = input('\nWhich day are you interested in exploring the bike data for?\n ({}) \n'.format(days_string)).lower()

            if day_input in days: #If the city is defined in CITY_DATA
                day = day_input #set city
                break #break out of loop
            else: #if city is not defined
                print('\nDay does not exist. Please enter a valid day\n') #print message and restart loop
        #Show selected city
        print('\nDay selected: {}\n\n'.format(day).title())
    else:
        day = 'all'

    # print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])

    #convert Start Time Column to a datetime object
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # create new columns contining month (int) and day of the week (int)
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # If month is not set to 'all' a new dataframe will be created only containing rows with the selected month
    if month != 'all':
        #The index is used to convert month to an integer
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

        #New dataframe is created filtered by the month selected
        df = df[df['month']==month]

    # If day is not set to 'all' a new dataframe will be created only containing rows with the selected day
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
        day = days.index(day)
        df =  df[df['day_of_week']==day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Create hour column in DataFrame
    df['hour'] = df['Start Time'].dt.hour
    #Get the modes (most frequent value) of each column
    df_mode = df.mode()

    # ----------------------------------------------------------------------------------------------
    # Display top month

    #Get the top month by only selecting the month column and dropping all NaN values from the mode function
    month = df_mode['month'].dropna()[0] #This comes out as a float
    #Gets the amount of rentals by counting each value in the month column and only picking the top month
    rental_count = df['month'].value_counts()[month]

    #Define a months array to get month name by index later
    month_names = ['january', 'february', 'march', 'april', 'may', 'june']

    month_name = month_names[int(month)-1].title() #Gets the month name from the months array
    print("The most common month for bike rental is {}".format(month_name))
    print("With a total of {} rentals".format(rental_count))

    # ----------------------------------------------------------------------------------------------
    # Display top day

    #Get the top day of the week by only selecting the day_of_week column and dropping all NaN values from the mode function
    day = df_mode['day_of_week'].dropna()[0] #This comes out as a float.
    #Gets the amount of rentals by counting each value in the day_of_week column and only picking the top day
    rental_count = df['day_of_week'].value_counts()[day]

    #Define a days array to get day name by index later
    day_names = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

    day_name = day_names[int(day)].title() #Gets the month name from the months array
    print("The most common day for bike rental is {}".format(day_name))
    print("With a total of {} rentals".format(rental_count))

    # ----------------------------------------------------------------------------------------------
    # Display top hour

    #Get the top hour of the week by only selecting the hour column and dropping all NaN values from the mode function
    hour = df_mode['hour'].dropna()[0] #This comes out as a float
    #Gets the amount of rentals by counting each value in the hour column and only picking the top day
    rental_count = df['hour'].value_counts()[hour]

    print("The most common start hour for bike rental is {}".format(str(hour)))
    print("With a total of {} rentals".format(rental_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Get the modes (most frequent value) of each column
    df_mode = df.mode()

    # ----------------------------------------------------------------------------------------------
    # Display top Start Station

    #Get the top stat station by only selecting the Start Station column and dropping all NaN values from the mode function
    start_station = df_mode['Start Station'].dropna()[0] #This comes out as a float
    #Gets the amount of trips started here by counting each value in the column and only picking the top one
    start_station_count = df['Start Station'].value_counts()[start_station]

    print('The most common Start Stations is {}'.format(start_station))
    print('With a total number of {} trips started here'.format(start_station_count))

    # ----------------------------------------------------------------------------------------------
    # Display top End Station

    end_station = df_mode['End Station'].dropna()[0] #This comes out as a float
    #Gets the amount of trips ended here by counting each value in the column and only picking the top one
    end_station_count = df['End Station'].value_counts()[end_station]

    print('The most common End Stations is {}'.format(end_station))
    print('With a total number of {} trips ended here'.format(end_station_count))

    # ----------------------------------------------------------------------------------------------
    # Display most common trip

    # Get size grouped by Start and End Station. Sort: Descending
    route = df.groupby(['Start Station','End Station']).size().sort_values(ascending=False)
    start = route.index[0][0]
    end = route.index[0][1]
    count = route[0] #Only pick the top value

    print("\nThe most common route starts at {} and ends at {} with a total of {} trips".format(start, end, count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Calculate sum of trip duration
    trip_duration_sum = df['Trip Duration'].sum()
    tds_hours = int(trip_duration_sum / 60**2)
    tds_minutes = int((trip_duration_sum % 60**2) / 60)
    tds_seconds = int((trip_duration_sum % 60**2) % 60)
    print('The total trip duration is {} hours, {} minutes and {} seconds'.format(tds_hours, tds_minutes, tds_seconds))

    # TO DO: display mean travel time
    #Calculate sum of trip duration
    trip_duration_mean = df['Trip Duration'].mean()
    tdm_hours = int(trip_duration_mean / 60**2)
    tdm_minutes = int((trip_duration_mean % 60**2) / 60)
    tdm_seconds = int((trip_duration_mean % 60**2) % 60)
    print('The average trip duration is {} hours, {} minutes and {} seconds'.format(tdm_hours, tdm_minutes, tdm_seconds))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Counts of user types
    df['User Type'] = df['User Type'].fillna('Not defined')
    print("\n - Counts of user types:")
    print(df.groupby(['User Type']).size().sort_values(ascending=False))

    # Counts of gender
    df['Gender'] = df['Gender'].fillna('Not defined')
    print("\n - Counts of gender:")
    print(df.groupby(['Gender']).size().sort_values(ascending=False))

    # Earliest, most recent, and most common year of birth
    desc_year_list = df['Birth Year'].sort_values(ascending=False)
    asc_year_list = df['Birth Year'].sort_values(ascending=True)
    earliest_year = int(asc_year_list[asc_year_list.index[0]])
    latest_year = int(desc_year_list[desc_year_list.index[0]])
    print("\nThe earliest birth year a customer has is {}".format(earliest_year))
    print("The most recent birth year is {}".format(latest_year))

    # Count grouped by Birth year
    count_years = df.groupby(['Birth Year']).size().sort_values(ascending=False)
    common_year = int(count_years.index[0])
    common_year_count = count_years[count_years.index[0]]

    print("\nThe most common birth year is {} with a count of {}".format(common_year,common_year_count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays 5 rows of raw data if the user asks for it"""

    row_count = 0 #To keep track of the rows

    # Loop until a break occurs
    while True:
        user_input = input("Do you want to display 5 rows of data? (yes / no)\n").lower()
        if user_input == 'yes':
            print(df.iloc[row_count:row_count+5])
            row_count += 5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)

        # only print user stats if city is not washington. The washington.csv does not contain that data.
        if city != 'washington':
            user_stats(df)

        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
