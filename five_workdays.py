import input_from_csv
import datetime
from datetime import date
import pytz


def return_five_working_days (end_date_str = None):
    # If file is not passed as argument, consider today as the last day of 5 days
    if not end_date_str:
        ist = pytz.timezone('Asia/Calcutta')
        end_date = datetime.datetime.date(datetime.datetime.now(ist))
        end_date_str = end_date.strftime("%d%m%Y")
    else:
        # Make a datetime object out of date string given as argument
        end_date = datetime.datetime.strptime(end_date_str, "%d-%m-%Y")

    five_dates = []
    i = 5
    today = end_date
    while i > 0:
        # today.weekday() returns day as number. Monday - 0 ... Sunday - 6. If > 5, it's a weekend
        if today.weekday() > 4:
            today = today - datetime.timedelta(days=1)
            continue
        # It's a weekday... yay!
        else:
            five_dates.append(today)
            i -= 1
            today = today - datetime.timedelta(days=1)

    # Return five days as string 
    five_dates_string = []
    for dates in five_dates:
        five_dates_string.append(dates.strftime("%d%m%Y"))
    
    # print(five_dates_string)
    return five_dates_string

# Runs only when the file is run from CLI
if __name__ == "__main__":
    return_five_working_days('25-09-2021')

        
