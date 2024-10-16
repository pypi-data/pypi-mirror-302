import os
from calendar import monthrange
from datetime import datetime, timedelta
import datetime as dt
from dateutil.relativedelta import relativedelta
import calendar
import math


DATE_FORMAT='%Y-%m-%d'
MONTH_FORMAT='%m'
FILE_DATE_FORMAT='%Y%m%d'
DATE_HOUR_FORMAT = "%Y-%m-%d H%H"
TS_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_TIME_FORMAT = "%Y%m%d%H%M%S"
ISO8601_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
ISO8601_FORMAT_ALT = "%Y-%m-%dT%H:%M:%SZ"
DAY_FORMAT = "%d"
HOUR_FORMAT = "%H"
MINUTE_FORMAT = "%M"
SECOND_FORMAT = "%S"
EPOCH_FORMAT = "%s"
WEEK_FORMAT = "%Y%U"
MONTH_FORMAT_PART = "%m"
YEAR_FORMAT = "%Y"
YYMMDD_FORMAT = "%y%m%d"
DATE_NAME="%d %B, %Y"
DATE_FORMAT_2="%d/%m/%Y"


###### ARCHIVO DE AYUDA PARA CENTRALIZAR TODAS LAS FUNCIONES UTILES RELACIONADAS CON LAS FECHAS

def get_dates_difference(dt_from_timestamp, dt_to_timestamp, mode='days'):
    """
    Get difference in days or hours between to dates
    :param dt_from_timestamp: Date from value [Datetime]
    :param dt_to_timestamp: Date to value [Datetime]
    :param mode: Days or hours values allowed [String]
    :return: Difference in days or hours [Integer]
    """
    # deltas
    delta_by_mode = dict()
    delta_by_mode[mode] = 1

    # checking dates
    if dt_from_timestamp > dt_from_timestamp:
        aux = dt_from_timestamp
        dt_from_timestamp = dt_from_timestamp
        dt_to_timestamp = aux

    # calculating shift
    shift = 0
    while dt_from_timestamp <= dt_to_timestamp:
        shift += delta_by_mode[mode]
        dt_from_timestamp = dt_from_timestamp + timedelta(**delta_by_mode)

    return shift

def get_first_day_of_month(date_ts_from):
    """
    Get first day of month by date
    :param date_ts_from: from date [Datetime]
    :return: first_day
    """
    return datetime.strptime(date_ts_from,'%Y-%m-%d').replace(day=1).strftime('%Y-%m-%d')

# def get_first_day_of_previous_month(date_ts_from):
#     """
#     Get first day of month by date
#     :param date_ts_from: from date [Datetime]
#     :return: first_day of previous month
#     """
#     dtObj = datetime.strptime(date_ts_from, '%Y-%m-%d').replace(day=1)
#     return dtObj+relativedelta(months=-1)

def get_first_day_of_previous_month(date_ts_from):
    """
    Get first day of month by date
    :param date_ts_from: from date [Datetime]
    :return: first_day of previous month
    """
    dtObj = datetime.strptime(date_ts_from, '%Y-%m-%d').replace(day=1)
    return (dtObj+relativedelta(months=-1)).strftime('%Y-%m-%d')

def get_first_day_of_previous_previous_month(date_ts_from):
    """
    Get first day of month by date
    :param date_ts_from: from date [Datetime]
    :return: first_day of previous month
    """
    dtObj = datetime.strptime(date_ts_from, '%Y-%m-%d').replace(day=1)
    return (dtObj+relativedelta(months=-2)).strftime('%Y-%m-%d')

def get_last_day_of_month(date_ts_from):
    """
    Get last day of month by date
    :param date_ts_from: from date [Datetime]
    :return: last_day
    """
    tmp = datetime.strptime(date_ts_from,'%Y-%m-%d').replace(day=28) + timedelta(days=4)
    return (tmp + timedelta(days=-1*tmp.day)).strftime('%Y-%m-%d')

def get_last_day_of_previous_month(date_ts_from):
    """
    Get last day of month by date
    :param date_ts_from: from date [Datetime]
    :return: last_day of previous month
    """
    return  get_previous_day(get_first_day_of_month(date_ts_from))

def get_sameday_previous_month(date_ts_from):
    """
    Get same day of the previpus month
    :param date_ts_from: from date [Datetime]
    :return: same day of previous month
    """
    tmp = datetime.strptime(date_ts_from,'%Y-%m-%d')
    return (tmp + relativedelta(months=-1)).strftime('%Y-%m-%d')

def get_previous_day(date_ts_from):
    """
    Get previous day
    :param date_ts_from: from date [Datetime]
    :return: previous day of param
    """
    tmp = datetime.strptime(date_ts_from,'%Y-%m-%d')
    return (tmp - timedelta(days=1)).strftime('%Y-%m-%d')

def get_n_previous_day(date_ts_from, cant):
    """
    Get the that happened N days before
    :param date_ts_from: from date [Datetime]
    :return: previous day of param
    """
    tmp = datetime.strptime(date_ts_from,'%Y-%m-%d')
    return (tmp - timedelta(days=cant)).strftime('%Y-%m-%d')

def get_quarter(dt, delta=0):
    """
    Get quarter by date
    :param dt: date to evaluate
    :param delta: delta quarter
    :return: quarter
    """
    quarter = None
    year = dt.year
    factor = 1

    if delta < 0:
        factor = -1
        delta = abs(delta)

    try:
        q = int(math.ceil(float(dt.month) / 3))
        i = 1
        while i <= delta:
            if factor < 0:
                if q == 1:
                    q = 4
                    year -= 1
                else:
                    q -= 1
            else:
                if q == 4:
                    q = 1
                    year += 1
                else:
                    q += 1
            i += 1

        quarter = 'Q{} [{}]'.format(q, year)
    except Exception as _:
        pass

    return quarter

def get_quarter_range(quarter_year):
    """
    Get range of dates corresponding to a given quarter
    :param quarter_year: quarter of the year in format Q<quarter> [<year>] (Q1 [2019])
    :return: Tuple with from/to range of the quarter
    """
    range = []
    quarter_year = quarter_year.replace('[', '').replace(']', '')
    quarter, year = quarter_year.split()

    try:
        if quarter in ('Q1', 'Q2', 'Q3', 'Q4'):
            if quarter == 'Q1':
                range = [datetime(int(year), 1, 1, 0, 0, 0, 0), datetime(int(year), 3, 31, 23, 59, 59, 999)]
            elif quarter == 'Q2':
                range = [datetime(int(year), 4, 1, 0, 0, 0, 0), datetime(int(year), 6, 30, 23, 59, 59, 999)]
            elif quarter == 'Q3':
                range = [datetime(int(year), 7, 1, 0, 0, 0, 0), datetime(int(year), 9, 30, 23, 59, 59, 999)]
            elif quarter == 'Q4':
                range = [datetime(int(year), 10, 1, 0, 0, 0, 0), datetime(int(year), 12, 31, 23, 59, 59, 999)]
    except Exception as _:
        pass

    return range

def get_week_range(date, deltaweek=0):
    """
    Get week dates range
    :param date: base date [Datetime]
    :param deltaweek: weeks [Integer]
    :return: dates range [Tuple]
    """
    dt = date
    i = 1

    while i <= abs(deltaweek):
        dt = dt - timedelta(days=7)
        i += 1

    week = dt.isocalendar()[1]
    found = False

    while not found:
        prior_dt = dt
        dt = dt + timedelta(days=1)
        if week != dt.isocalendar()[1]:
            found = True
            dt = prior_dt

    date_from = dt - timedelta(days=6, hours=dt.hour, minutes=dt.minute, seconds=dt.second)
    date_to = dt + timedelta(hours=23 - dt.hour, minutes=59 - dt.minute, seconds=59 - dt.second)

    return date_from, date_to

def get_month_range(date, deltamonth=0):
    """
    Get month dates range
    :param date: base date [Datetime]
    :param deltamonth: months [Integer]
    :return: dates range [Tuple]
    """
    dt = date + relativedelta(months=1)
    dt = dt - timedelta(days=dt.day)
    i = 1

    while i <= abs(deltamonth):
        dt = dt - timedelta(days=dt.day)
        i += 1

    date_from = dt - timedelta(days=dt.day - 1, hours=dt.hour, minutes=dt.minute, seconds=dt.second)
    date_to = dt + timedelta(hours=23 - dt.hour, minutes=59 - dt.minute, seconds=59 - dt.second)

    return date_from, date_to

def get_quarter_name(d):
    return "Q%d_%d" % (math.ceil(d.month/3), d.year)

def get_week_range_tax(date):
    """
    Get week dates range
    :param date: base date [Datetime]
    :param deltaweek: weeks [Integer]
    :return: dates range [Tuple]
    """
    dt = date
    if dt.day>=7 and dt.day <= 15:
        ini=dt.strftime(YEAR_FORMAT)+'-'+dt.strftime(MONTH_FORMAT)+'-01'
        end=dt.strftime(YEAR_FORMAT)+'-'+dt.strftime(MONTH_FORMAT)+'-07'
    elif dt.day > 15 and dt.day <= 22:
        ini = dt.strftime(YEAR_FORMAT) + '-' + dt.strftime(MONTH_FORMAT) + '-08'
        end = dt.strftime(YEAR_FORMAT) + '-' + dt.strftime(MONTH_FORMAT) + '-15'
    elif dt.day > 22 and dt.day <= 31:
        ini = dt.strftime(YEAR_FORMAT) + '-' + dt.strftime(MONTH_FORMAT) + '-16'
        end = dt.strftime(YEAR_FORMAT) + '-' + dt.strftime(MONTH_FORMAT) + '-22'
    else:
        dt1=get_last_day_of_previous_month(dt.strftime(DATE_FORMAT))
        ini = datetime.strptime(dt1, DATE_FORMAT).strftime(YEAR_FORMAT) + '-' + datetime.strptime(dt1,DATE_FORMAT).strftime(MONTH_FORMAT) + '-23'
        end = dt1
    date_from = ini
    date_to = end

    return date_from, date_to

def get_decennial_range_tax(date):
    """
    Get week dates range
    :param date: base date [Datetime]
    :param deltaweek: weeks [Integer]
    :return: dates range [Tuple]
    """
    dt = date
    if dt.day>=10 and dt.day <= 20:
        ini=dt.strftime(YEAR_FORMAT)+'-'+dt.strftime(MONTH_FORMAT)+'-01'
        end=dt.strftime(YEAR_FORMAT)+'-'+dt.strftime(MONTH_FORMAT)+'-10'
        decena=1
    elif dt.day > 20 and dt.day <= 31:
        ini = dt.strftime(YEAR_FORMAT) + '-' + dt.strftime(MONTH_FORMAT) + '-11'
        end = dt.strftime(YEAR_FORMAT) + '-' + dt.strftime(MONTH_FORMAT) + '-20'
        decena = 2
    else:
        dt1=get_last_day_of_previous_month(dt.strftime(DATE_FORMAT))
        ini = datetime.strptime(dt1, DATE_FORMAT).strftime(YEAR_FORMAT) + '-' + datetime.strptime(dt1,DATE_FORMAT).strftime(MONTH_FORMAT) + '-21'
        end = dt1
        decena = 3
    date_from = ini
    date_to = end

    return date_from, date_to,decena

def string_formatted(string,dict):
    for key, value in dict.items():
        string = string.replace('{' + key + '}', str(value))
    return string

def generate_date_variables(date_parameter):
    dict_dates = {}
    if date_parameter == '0':
        date_ts_from = str(datetime.now().date())
    else:
        date_ts_from = date_parameter
    dict_dates['current_day'] = datetime.strptime(date_ts_from, DATE_FORMAT).strftime(DATE_FORMAT)
    dict_dates['current_day_2'] = datetime.strptime(date_ts_from, DATE_FORMAT).strftime(DATE_FORMAT_2)
    dict_dates['name_day'] = datetime.strptime(date_ts_from, DATE_FORMAT).strftime('%A')
    dict_dates['month_day'] = datetime.strptime(date_ts_from, DATE_FORMAT).strftime('%B')
    dict_dates['current_day_name'] = datetime.strptime(date_ts_from, DATE_FORMAT).strftime(DATE_NAME)
    dict_dates['is_weekend'] = '0' if datetime.strptime(date_ts_from, DATE_FORMAT).weekday() <= 4 else '1'
    dict_dates['previous_day'] = get_previous_day(date_ts_from)
    year_prev, month_prev, day_prev = get_year_month_day(dict_dates['previous_day'])
    dict_dates['year_prev'] = year_prev
    dict_dates['month_prev'] = month_prev
    dict_dates['day_prev'] = day_prev
    dict_dates['previous_day_name'] = datetime.strptime(dict_dates['previous_day'], DATE_FORMAT).strftime(DATE_NAME)
    dict_dates['same_day_previous_month'] = get_sameday_previous_month(date_ts_from)
    dict_dates['last_day_of_previous_month'] = get_last_day_of_previous_month(date_ts_from)
    year, month, day = get_year_month_day(dict_dates['last_day_of_previous_month'])
    dict_dates['day_part_last_day_of_previous_month'] = day
    dict_dates['month_part_last_day_of_previous_month'] = month
    dict_dates['year_part_last_day_of_previous_month'] = year
    dict_dates['last_day_of_month'] = get_last_day_of_month(date_ts_from)
    dict_dates['first_day_of_previous_previous_month'] = get_first_day_of_previous_previous_month(date_ts_from)
    year, month, day = get_year_month_day(dict_dates['first_day_of_previous_previous_month'])
    dict_dates['day_part_first_day_of_previous_previous_month'] = day
    dict_dates['month_part_first_day_of_previous_previous_month'] = month
    dict_dates['year_part_first_day_of_previous_previous_month'] = year
    dict_dates['first_day_of_previous_month'] = get_first_day_of_previous_month(date_ts_from)
    dict_dates['first_day_of_month'] = get_first_day_of_month(date_ts_from)
    year, month, day = get_year_month_day(dict_dates['first_day_of_month'])
    dict_dates['day_part_first_day_of_month'] = day
    dict_dates['month_part_first_day_of_month'] = month
    dict_dates['year_part_first_day_of_month'] = year
    dict_dates['last_day_of_month'] = get_last_day_of_month(date_ts_from)
    dict_dates['first_day_of_previous_previous_month'] = get_first_day_of_previous_previous_month(date_ts_from)
    year, month, day = get_year_month_day(dict_dates['last_day_of_month'])
    dict_dates['day_part_last_day_of_month'] = day
    dict_dates['month_part_last_day_of_month'] = month
    dict_dates['year_part_last_day_of_month'] = year
    dict_dates['process_date'] = dt.date.today().strftime(DATE_FORMAT)
    dict_dates['partition_date'] = dict_dates['previous_day'] if date_ts_from == dt.date.today().strftime(DATE_FORMAT) else date_ts_from
    dict_dates['file_partition_date'] = datetime.strptime(dict_dates['partition_date'], DATE_FORMAT).strftime(FILE_DATE_FORMAT)
    dict_dates['next_date_from'] = (datetime.strptime(date_ts_from, DATE_FORMAT) + timedelta(days=1)).strftime(
        DATE_FORMAT)
    year_prev, month_prev, day_prev = get_year_month_day(dict_dates['next_date_from'])
    dict_dates['year_next'] = year_prev
    dict_dates['month_next'] = month_prev
    dict_dates['day_next'] = day_prev
    dict_dates['week_day'] = datetime.strptime(date_ts_from, DATE_FORMAT).weekday()
    dict_dates['week'] = datetime.strptime(date_ts_from, DATE_FORMAT).isocalendar()[1]
    dict_dates['week_month'] = (datetime.strptime(date_ts_from, DATE_FORMAT).isocalendar()[1] -datetime.strptime(date_ts_from, DATE_FORMAT).replace(day=1).isocalendar()[1] + 1)
    dict_dates['year'] = datetime.strptime(date_ts_from, DATE_FORMAT).strftime(YEAR_FORMAT)
    dict_dates['month'] = datetime.strptime(date_ts_from, DATE_FORMAT).strftime(MONTH_FORMAT)
    dict_dates['day'] = datetime.strptime(date_ts_from, DATE_FORMAT).strftime(DAY_FORMAT)
    dict_dates['hour'] = datetime.strptime(date_ts_from, DATE_FORMAT).strftime(HOUR_FORMAT)
    dict_dates['minute'] = datetime.strptime(date_ts_from, DATE_FORMAT).strftime(MINUTE_FORMAT)
    dict_dates['second'] = datetime.strptime(date_ts_from, DATE_FORMAT).strftime(SECOND_FORMAT)
    # ultimo dia del mes siguiente
    date_nm = datetime.strptime(date_ts_from, DATE_FORMAT) + relativedelta(months=+1)
    dict_dates['last_day_of_next_month'] = date_nm.replace(
        day=calendar.monthrange(date_nm.year, date_nm.month)[1]).strftime(DATE_FORMAT)
    # Primer dia del mes siguiente
    dict_dates['first_day_of_next_month'] = (
                datetime.strptime(date_ts_from, DATE_FORMAT) + relativedelta(months=1, day=1)).strftime(DATE_FORMAT)
    from_cmfrom, from_cmto = get_month_range(datetime.strptime(date_ts_from, DATE_FORMAT))
    to_cmfrom, to_cmto = get_month_range(datetime.strptime(date_ts_from, DATE_FORMAT))
    dict_dates['month_from'] = from_cmfrom.strftime(DATE_FORMAT)
    dict_dates['month_to'] = to_cmto.strftime(DATE_FORMAT)
    dict_dates['quarter_from'] = get_quarter_range(get_quarter(datetime.strptime(date_ts_from, DATE_FORMAT)))[
        0].strftime(DATE_FORMAT)
    dict_dates['quarter_to'] = get_quarter_range(get_quarter(datetime.strptime(date_ts_from, DATE_FORMAT)))[1].strftime(
        DATE_FORMAT)
    dict_dates['quarter_name'] = get_quarter_name(datetime.strptime(date_ts_from, DATE_FORMAT))
    dict_dates['previous_quarter_from'] = \
    get_quarter_range(get_quarter(datetime.strptime(date_ts_from, DATE_FORMAT), delta=-1))[0].strftime(
        DATE_FORMAT)
    dict_dates['previous_quarter_to'] = \
    get_quarter_range(get_quarter(datetime.strptime(date_ts_from, DATE_FORMAT), delta=-1))[1].strftime(
        DATE_FORMAT)
    dict_dates['previous_quarter_name'] = get_quarter_name(
        datetime.strptime(dict_dates['previous_quarter_from'], DATE_FORMAT))
    dict_dates['previous_week'] = (datetime.strptime(date_ts_from, DATE_FORMAT) - timedelta(days=7)).isocalendar()[1]
    dict_dates['previous_month'] = (datetime.strptime(date_ts_from, DATE_FORMAT) - timedelta(
        days=datetime.strptime(date_ts_from, DATE_FORMAT).day)).strftime(MONTH_FORMAT)
    dict_dates['previous_year'] = int(dict_dates['year']) - 1
    dict_dates['day_15_of_month'] = (
                datetime.strptime(dict_dates['first_day_of_month'], DATE_FORMAT) + timedelta(days=14)).strftime(
        DATE_FORMAT)
    dict_dates['day_15_of_previous_month'] = (
                datetime.strptime(dict_dates['first_day_of_previous_month'], DATE_FORMAT) + timedelta(
            days=14)).strftime(DATE_FORMAT)
    dict_dates['day_16_of_previous_month'] = (
                datetime.strptime(dict_dates['first_day_of_previous_month'], DATE_FORMAT) + timedelta(
            days=15)).strftime(DATE_FORMAT)
    dict_dates['file_last_day_of_previous_month'] = (
        datetime.strptime(dict_dates['last_day_of_previous_month'], DATE_FORMAT)).strftime(FILE_DATE_FORMAT)
    dict_dates['day_tax_forthnightly'] = dict_dates['day_15_of_month'] if datetime.strptime(date_ts_from,DATE_FORMAT).day >= 15 else dict_dates['last_day_of_previous_month']

    from_cwfrom, from_cwto = get_week_range(datetime.strptime(date_ts_from, DATE_FORMAT))
    to_cwfrom, to_cwto = get_week_range(datetime.strptime(date_ts_from, DATE_FORMAT))
    dict_dates['current_week_from'] = from_cwfrom.strftime(DATE_FORMAT)
    dict_dates['current_week_to'] = from_cwto.strftime(DATE_FORMAT)

    pwfrom, pwto = get_week_range(datetime.strptime(date_ts_from, DATE_FORMAT), 1)
    dict_dates['previous_week_from'] = pwfrom.strftime(DATE_FORMAT)
    dict_dates['previous_week_to'] = pwto.strftime(DATE_FORMAT)

    p_two_wfrom, p_two_wto = get_week_range(datetime.strptime(date_ts_from, DATE_FORMAT), 2)
    dict_dates['previous_week-1_from'] = p_two_wfrom.strftime(DATE_FORMAT)
    dict_dates['previous_week-1_to'] = p_two_wto.strftime(DATE_FORMAT)

    p_three_wfrom, p_three_wto = get_week_range(datetime.strptime(date_ts_from, DATE_FORMAT), 3)
    dict_dates['previous_week-2_from'] = p_three_wfrom.strftime(DATE_FORMAT)
    dict_dates['previous_week-2_to'] = p_three_wto.strftime(DATE_FORMAT)

    p_four_wfrom, p_four_wto = get_week_range(datetime.strptime(date_ts_from, DATE_FORMAT), 4)
    dict_dates['previous_week-3_from'] = p_four_wfrom.strftime(DATE_FORMAT)
    dict_dates['previous_week-3_to'] = p_four_wto.strftime(DATE_FORMAT)

    p_five_wfrom, p_five_wto = get_week_range(datetime.strptime(date_ts_from, DATE_FORMAT), 5)
    dict_dates['previous_week-4_from'] = p_five_wfrom.strftime(DATE_FORMAT)
    dict_dates['previous_week-4_to'] = p_five_wto.strftime(DATE_FORMAT)

    pmfrom, pmto = get_month_range(datetime.strptime(date_ts_from, DATE_FORMAT), 1)
    dict_dates['previous_month_from'] = pmfrom.strftime(DATE_FORMAT)
    dict_dates['previous_month_to'] = pmto.strftime(DATE_FORMAT)

    pmfrom_1, pmto_1 = get_month_range(datetime.strptime(date_ts_from, DATE_FORMAT), 2)
    dict_dates['previous_month-1_date_from'] = pmfrom_1.strftime(DATE_FORMAT)
    dict_dates['previous_month-1_date_to'] = pmto_1.strftime(DATE_FORMAT)

    week_ini_tax, week_end_tax = get_week_range_tax(datetime.strptime(date_ts_from, DATE_FORMAT))
    dict_dates['current_week_from_tax'] = week_ini_tax
    dict_dates['current_week_to_tax'] = week_end_tax

    decennial_ini_tax, decennial_end_tax, decennial_month = get_decennial_range_tax(datetime.strptime(date_ts_from, DATE_FORMAT))
    dict_dates['decennial_week_from_tax'] = decennial_ini_tax
    dict_dates['decennial_week_to_tax'] = decennial_end_tax
    dict_dates['decennial_month'] = decennial_month

    #Ints to filter partitions
    dict_filter = {}
    dict_filter = generate_filter_variables(dict_dates)

    dict_final = dict_dates.copy()
    dict_final.update(dict_filter)

    return dict_final

def get_year_month_day(date_parameter):
    """
        Return year,month,date to partition
        :param date_parameter: base date [string]
        :return: year,month,date [Tuple of string]
        """
    year=datetime.strptime(date_parameter, DATE_FORMAT).strftime(YEAR_FORMAT)
    month = datetime.strptime(date_parameter, DATE_FORMAT).strftime(MONTH_FORMAT)
    day= datetime.strptime(date_parameter, DATE_FORMAT).strftime(DAY_FORMAT)
    return year,month,day


def generate_filter_variables(dict):

    new_dict = {}
    for key, value in dict.items():
        try:
            if bool(datetime.strptime(value, DATE_FORMAT)):
                new_value = datetime.strptime(value, DATE_FORMAT)

                new_key_year = 'year_filter_' + key
                new_dict[new_key_year] = new_value.year

                new_key_month = 'month_filter_' + key
                new_dict[new_key_month] = new_value.month

                new_key_day = 'day_filter_' + key
                new_dict[new_key_day] = new_value.day  # int(value.split('-')[-part])

        except:
            pass

    return new_dict

