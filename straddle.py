import five_workdays
import input_from_csv
import re




# Input data, nifty fifty or nifty bank? Can be extended in future if required
while True:
    index_type = input('Enter the index you wish to analyze:\n1. Nifty 50\n2. Bank Nifty\n0. Exit\nPlease choose your option: ')
    if index_type == '0':
        exit(0)
    if index_type == '1' or index_type == '2':
        break
    else:
        print('Please select a valid option.')
print('')

############################################## Version 1 code starts, ignore ##########################################################
# print('Please enter H and L of index for past 5 days (space separated): recent first to oldest last')

# def get_h_and_l():
#     hls = []
#     for i in range (5):
#         hl = list(map(lambda x: float(x), input('T - ' + str(i+1) + " day: ").split(' ')))
#         hls.append({'high': hl[0], 'low': hl[1]})
#     print('')
#     return hls

# def get_prev_close():
#     prev_close = float(input('Please enter the previous close of the index: '))
#     print('')
#     return prev_close


# hls = get_h_and_l()


# prev_close = get_prev_close()
# Validate PC data

# pc_valid = False
# while not pc_valid:
#     if prev_close < hls[0]['low'] or prev_close > hls[0]['high']:
#         print("Previous close must be in the range of T-1 day's data.")
#         pc_option = input('Here are your options:\n1. To reenter previous close, press 1\n2. To exit, press 0: ')
#         if pc_option == '0':
#             exit(0)
#         else:
#             prev_close = get_prev_close()
#     else: 
#         pc_valid = True

# print('Validated!')
############################################## Version 1 code ends, ignore ##########################################################

# Compute 5 most recent working days
five_dates_string = []
while True:
    end_date_str = input('Enter the last date out of 5 days in dd-mm-yyyy format. Or just press enter to count from today: ')
    end_date_str = end_date_str.strip()
    if end_date_str == '':
        five_dates_string = five_workdays.return_five_working_days()
        break
    elif re.match('^\d{2}-\d{2}-\d{4}$', end_date_str):
        five_dates_string = five_workdays.return_five_working_days(end_date_str)
        break
    else:
        print('Please re-enter the end date in dd-mm-yyyy format!')


# Read CSV files and get the data
files_missing = []
hls = []
for date in five_dates_string:
    filename = 'data/ind_close_all_{date}.csv'.format(date = date)
    index_map = {
        '1': 'Nifty 50',
        '2': 'Nifty Bank'
    }
    fields = ['High Index Value', 'Low Index Value', 'Closing Index Value']

    data = input_from_csv.read_index_data(filename, index_map[index_type], fields)
    if 'error' in list(data.keys()):
        files_missing.append('ind_close_all_{date}.csv'.format(date = date))
    else:
        hls.append(data)

if len(files_missing) > 0:
    print('Some files are missing. Please check the "data" folder for the following files! Exiting the program.')
    for i in range(len(files_missing)):
        print(str(i) + '. ' + files_missing[i])
    exit(0)


# Validate HL data

hl_valid = False
while not hl_valid:
    hl_valid = True
    for hl in hls:
        if hl['High Index Value'] < hl['Low Index Value']:
            print('High should not be lower than the low')
            hl_option = input('Here are your options:\n1. To reenter the H and L data, press 1\n2. To exit, press 0: ')
            if hl_option == '0':
                exit(0)
            else: 
                hls = get_h_and_l()
                hl_valid = False
                break

print('')

prev_close = hls[0]['Closing Index Value']

pc_valid = False
while not pc_valid:
    if prev_close < hls[0]['Low Index Value'] or prev_close > hls[0]['High Index Value']:
        print("Previous close must be in the range of T-1 day's data.")
        pc_option = input('Here are your options:\n1. To reenter previous close, press 1\n2. To exit, press 0: ')
        if pc_option == '0':
            exit(0)
        else:
            prev_close = get_prev_close()
    else: 
        pc_valid = True

print('')


# Compute averages
h_sum = 0
l_sum = 0
for hl in hls:
    h_sum += hl['High Index Value']
    l_sum += hl['Low Index Value']
h_avg = h_sum / len(hls)
l_avg = l_sum / len(hls)

print('DEBUG: Avg high = {h_avg} and Avg low = {l_avg}'.format(h_avg = h_avg, l_avg = l_avg))

# Find nearest ITM and OTM and print the output
def get_itm_pe_and_otm_ce(prev_close, index_type):
    step_size = 50 if index_type == '1' else 100
    pe = (prev_close // step_size + 1) * step_size
    ce = pe + (2 * step_size)
    target_and_stoploss = 10 * step_size

    return {'pe': pe, 'ce': ce, 'target': target_and_stoploss, 'stoploss': target_and_stoploss}

def get_itm_ce_and_otm_pe(prev_close, index_type):
    step_size = 50 if index_type == '1' else 100
    ce = (prev_close // step_size) * step_size
    pe = ce - (2 * step_size)
    target_and_stoploss = 10 * step_size

    return {'pe': pe, 'ce': ce, 'target': target_and_stoploss, 'stoploss': target_and_stoploss}


if prev_close < l_avg:
    print('The trend is downwards. \nPlease use a nearest ITM PE and OTM CE which is {x} points above PE. That is:'.format(x = 100 if index_type == '1' else 200))
    call_or_put = 'put'
    res = get_itm_pe_and_otm_ce(prev_close, index_type)
    print('Please use {pe} PE and {ce} CE with target at Rs. {target} profit and stoploss at Rs. {stoploss} loss.'.format(pe = res['pe'], ce = res['ce'], target = res['target'], stoploss = res['stoploss']))
elif prev_close > h_avg:
    print('The trend is upwards. \nPlease use a nearest ITM CE and OTM PE which is {x} points below PE. That is:'.format(x = 100 if index_type == '1' else 200))
    call_or_put = 'call'
    res = get_itm_ce_and_otm_pe(prev_close, index_type)
    print('Please use {ce} CE and {pe} PE with target at Rs. {target} profit and stoploss at Rs. {stoploss} loss.'.format(pe = res['pe'], ce = res['ce'], target = res['target'], stoploss = res['stoploss']))
else:
    print('The market is not showing any clear trend, wait for the trend to show up clearly')


