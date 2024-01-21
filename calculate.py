#!/usr/bin/env python
import math

LUNAR_MONTH = {
    'days': 29,
    'hours': 12,
	'minutes': 44,
    'cholokim': 1
}

LUNAR_CYCLE_TERMS = {
	'days_in_week': 7,
    'days': 29,
    'hours': 24,
	'minutes': 60,
    'cholokim': 48
}

HEBREW_MONTHS = [
    'Nisan',
    'Iyar',
    'Sivan',
    'Tammuz',
    'Av',
    'Elul',
    'Tishrei',
    'Cheshvan',
    'Kislev',
    'Tevet',
    'Shevat',
    'Adar',
    'Adar II'  # In leap years
]

# moved shabbos to 0 position, since modulas correct for it
DAYS_OF_WEEK = [
	'Shabbos',
	'Sunday',
	'Monday',
	'Tuesday',
	'Wednesday',
	'Thursday',
	'Friday',
]

SOLAR_YEAR = {
    'days': 365,
    'hours': 5,
    'cholokim': 48
}

START_DATE = {
	'year': 0,
	'month': 0,
	'days': 0,
	'day_of_week': 3,
	'hours': 6,
	'minutes': 0,
	'cholokim': 0
}

END_DATE = {
	# Get end date dynamically
	# 'cholokim': 0,
	# 'days': 0,
	# 'hours': 0,
	# 'minutes': 0,
	'month': HEBREW_MONTHS.index('Shevat'),
	'year': 5785
}

LAST_MOLAD = {
	'year': 5784,
	'month': 7,
    'days': 30,
	'day_of_week': 0,
    'hours': 18,
	'minutes': 33,
    'cholokim': 1
}

# Shabbos ﴾Oct 14﴿ 6:33 PM + 1 מולד חודש חשון: חלק
# Monday ﴾Nov 13﴿ 7:17 AM + 2 מולד חודש כסלו: חלקים
# Tuesday ﴾Dec 12﴿ 8:01 PM + 3 מולד חודש טבת: חלקי
# Thursday ﴾Jan 11﴿ 8:45 AM + 4 מולד חודש שבט: חלקים
# Friday (Feb 9) 9:29 PM + 5 מולד חודש אדר‐א: חלקים
# Sunday (Mar 10) 10:13 AM + 6 מולד חודש אדר‐ב: חלקים
# Monday ﴾Apr 8﴿ 10:57 PM + 7 מולד חודש ניסן: חלקים
# Wednesday ﴾May 8﴿ 11:41 AM + 8 מולד חודש אייר: חלקי
# Friday ﴾Jun 7﴿ 12:25 AM + 9 מולד חודש סיון: חלקי #####
# Shabbos ﴾Jul 6﴿ 1:09 PM + 10 מולד חודש תמוז: חלקי
# Monday ﴾Aug 5﴿ 1:53 AM + 11 מולד חודש אב: חלקים
# Tuesday ﴾Sep 3﴿ 2:37 PM + 12 מולד חודש אלול: חלקי
# Thursday ﴾Oct 3﴿ 3:21 AM + 13 מולד חודש תשרי: חלקים


def print_dictionary (dictionary):
	for key, value in dictionary.items():
		print(f"{key}: {value}")


""" Format to readable timestamp """
def readable_molad (year, month, days, day_of_week, hours, minutes, cholokim, *rest):
	month_name = HEBREW_MONTHS[month] if not (check_lunar_leap_year(year) and month == 11) else 'Adar I'
	day_of_week_name = DAYS_OF_WEEK[day_of_week]
	time = "{:01}:{:02} {}".format(hours % 12 or 12, minutes, "AM" if hours < 12 else "PM")

	return f"[Molad {month_name} {year}] {day_of_week_name} {time} + {cholokim} cholokim"


def check_lunar_leap_year(hebrew_year):
    year_in_cycle = hebrew_year % 19
    return year_in_cycle in [3, 6, 8, 11, 14, 17, 19]


""" For a given molad, calculate the next molad """
def calculate_molad(year, month, days, day_of_week, hours, minutes, cholokim):
	# deal with `days`
	is_lunar_leap_year = check_lunar_leap_year(year)

	# Add 29 days, 12 hours, 44 minutes and 1 chelek
	new_month = month + 1
	new_day_of_week = day_of_week + (LUNAR_MONTH['days'] % LUNAR_CYCLE_TERMS['days_in_week'])
	new_hour = hours + LUNAR_MONTH['hours']
	new_minute = minutes + LUNAR_MONTH['minutes']
	new_cholokim = cholokim + LUNAR_MONTH['cholokim']

	# Simplify terms
	molad_year = year + 1 if (month < HEBREW_MONTHS.index('Tishrei') and new_month >= HEBREW_MONTHS.index('Tishrei')) else year
	molad_month = new_month % len(HEBREW_MONTHS) if is_lunar_leap_year else new_month % (len(HEBREW_MONTHS) - 1)
	molad_day_of_week = (new_day_of_week + math.floor((new_hour + 1) / LUNAR_CYCLE_TERMS['hours'])) % LUNAR_CYCLE_TERMS['days_in_week']
	molad_hour = (new_hour + math.floor(new_minute / LUNAR_CYCLE_TERMS['minutes'])) % LUNAR_CYCLE_TERMS['hours']
	molad_minute = (new_minute + math.floor(new_cholokim / LUNAR_CYCLE_TERMS['cholokim'])) % LUNAR_CYCLE_TERMS['minutes']
	molad_cholokim = cholokim + LUNAR_MONTH['cholokim'] % LUNAR_CYCLE_TERMS['cholokim']

	return {
		'year': molad_year,
        'month': molad_month,
		# 'month_name': molad_month_name,
		'days': 0,
        'day_of_week': molad_day_of_week,
        'hours': molad_hour,
        'minutes': molad_minute,
        'cholokim': molad_cholokim
    }


def main():
	past_molad = next_molad = LAST_MOLAD
	print(readable_molad(**past_molad))

	while not (past_molad['year'] > END_DATE['year'] or (past_molad['month'] == END_DATE['month'] and past_molad['year'] == END_DATE['year'])):
		next_molad = calculate_molad(**past_molad)
		print(readable_molad(**next_molad))
		past_molad = next_molad

	return


if __name__ == '__main__':
    main()
