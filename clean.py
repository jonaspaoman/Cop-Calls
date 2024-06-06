# This program was made by Jonas Pao (c) in Spring of 2024
# For questions, please email jonaspaoman@gmail.com

import sys

Violent = {
        'Armed robbery': [],
        'Arson': [],
        'Assault': [],
        'Assault and Battery': [],
        'Assault w/ a deadly weapon': [],
        'Attempted murder': [],
        'Attempted suicide': [],
        'Battery': [],
        'Child abuse': [],
        'Domestic violence': [],
        'Fatal/injury hit and run': [],
        'Kidnapping': [],
        'Murder/homicide': [],
        'Rape': [],
        'Robbery': [],
        'Sex crime': [],
        'Sexual assault': [],
        'Strong arm robbery': [],
        'Suicide': [],
}
Theft = {
        'Appropriate lost property': [],
        'Burglary': [],
        'Checks forgery': [],
        'Commercial burglaries': [],
        'Credit card forgery': [],
        'Embezzlement': [],
        'Financial elder abuse': [],
        'Forgery': [],
        'Fraud': [],
        'Grand theft': [],
        'Identity theft': ['personate to get money'],
        'Petty theft': [],
        'Prowler': [],
        'Residential burglaries': [],
        'Residential burglary attempt': [],
        'Retail theft': [],
        'Shoplifting': [],
        'Theft undefined': [],
}
Drug = {
        'Drinking in public': [],
        'Driving under the influence': ['DUI'],
        'Drug activity': [],
        'Drunk in public': [],
        'Possession of drugs': [],
        'Possession of paraphernalia': ['paraphernalia'],
        'Sale of drugs': [],
        'Sale of liquor to minor': [],
        'Under influence of drugs': [],
}
Vehicle = {
        'Abandoned auto': [],
        'Abandoned bicycle': [],
        'Auto recovery': [],
        'Auto theft': ['take vehicle w/o owners consent/vehicle theft', 'motor vehicle theft'],
        'Bicycle recovery': [],
        'Bicycle theft': [],
        'Driving w/ suspended license': [],
        'Driving without license': [],
        'Display unlawful registration': [],
        'Hit and run': [],
        'Lost/stolen plates': [],
        'Misc traffic': [],
        'Parking/driving violation': ['stored vehicle'],
        'Stolen catalytic converter': [],
        'Theft from auto': [],
        'Theft from auto attempt': [],
        'Theft of vehicle parts': [],
        'Vehicle accident/injury': [],
        'Vehicle accident/mjr. Injury': [],
        'Vehicle accident/mnr. injury': [],
        'Vehicle accident/no injury': ['vehicle accident/non injury'],
        'Vehicle accident/prop. damage': [],
        'Vehicle impound': [],
        'Vehicle tampering': [],
        'Vehicle tow': [],
}
Misc = {
        'APS referral': [],
        'Animal call': [],
        'Be on the lookout': [],
        'Business check': [],
        'Casualty fall': [],
        'Citizen assist': [],
        'Concealed weapon': [],
        'Conspiracy': [],
        'Construction': [],
        'Coroner case': [],
        'Court order violation': [],
        'Courtesy report': [],
        'CPS referral': [],
        'Death unattended': [],
        'Discharge firearm': [],
        'Disorderly conduct': [],
        'Disturbance': [],
        'Disturbing/annoying calls': [],
        'Disturbing the peace': [],
        'Dumping': [],
        'Elder abuse': [],
        'Extortion': [],
        'Failure to register prior sex offender conviction': [],
        'False Tabs': [],
        'Fire call': [],
        'Fireworks': [],
        'Follow up': [],
        'Found property': [],
        'Gang information': [],
        'Gang validation': [],
        'Graffiti abatement': [],
        'Hate incident': [],
        'Hazard': [],
        'Indecent exposure': [],
        'Info case': [],
        'Juvenile problem': [],
        'Located missing person': [],
        'Loitering': [],
        'Lost property': [],
        'Medical assist': [],
        'Man down': [],
        'Meet citizen': [],
        'Mental health crisis': [],
        'Mental health evaluation': [],
        'Misc penal code violation': [],
        'Missing person': [],
        'Noise ordinance violation': [],
        'Non-consensual distribution of intimate images': [],
        'Other/misc': [],
        'Outside assist': [],
        'Outside investigation': [],
        'Outside warrant arrest': [],
        'Manufacture, sale or possession of dangerous weapon': [],
        'Poss. of stolen property': [],
        'Probation violation': [],
        'Property for destruction': [],
        'Psychiatric hold': [],
        'Psychiatric subject': [],
        'Public nuisance': [],
        'Resist arrest': [],
        'Service misc.': [],
        'Solicit lewd act': [],
        'Suspicious circumstances': [],
        'Suspicious person': [],
        'Threats': [],
        'Town ordinance violation': [],
        'Transient failure to register': [],
        'Trespassing': ['trespass'],
        'Unauthorized disabled placard': [],
        'Vandalism': [],
        'Voided case': [],
        'Warrant arrest': [],
        'Warrant/other agency': [],
        'Welfare check': []
    }
categories = [Violent, Theft, Drug, Vehicle, Misc]


def convert_pdf(filename):
    """
    Takes in a pdf and gives a list of the entries of the pdf
    In: PDF — PA police
    Out: LIST — of that data
    >>> convert_pdf('Sample_PDF.pdf')
    0
    >>> convert_pdf('Test_2.pdf')
    0
    """
    from pdfminer.high_level import extract_text
    text = extract_text(filename)
    return text


def count_arrests(text):
    lines = text.split('\n')
    counter = 0
    for element in lines:
        if element == 'M' or element == 'F':
            counter += 1
    return counter


def traverse(lst):
    """
    Takes in list version of PDF and spits out the entries I care about
    In: LIST — un-parsed data
    Out: LIST — parsed data
    """
    updated = []
    for column in lst:
        tpl = tuple(column.split('\n'))
        updated.append(tpl)
    return updated


def go(strs, allowed_letter):
    """
    Take in a string. If it contains a digit or the allowed letter, return True, else return False

    >>> go('hell0', '')
    False
    >>> go('nothing', '-')
    False
    >>> go('24-00686', '-')
    True
    >>> go('24-00686', '/')
    False
    >>> go('3/5/2024 9:34 AM', '/')
    False
    >>> go('3/5/2024', '/')
    True
    >>> go('3/5/2024 1234', '/')
    True
    """
    result = 0
    for ch in strs:
        if ch.isdigit() or ch == allowed_letter or ch == ' ':
            result += 1
    if result == len(strs) and allowed_letter in strs:
        return True
    return False


def identify(strs):
    """
    takes in a string and identifies if it is a crime. Returns T/F
    >>> identify('HeLLo')
    True
    >>> identify('LOST PROPERTY')
    True
    >>> identify('LOCATION')
    False
    >>> identify('123')
    False
    >>> identify('lost property')
    True
    >>> identify('123 Louise Lane')
    True
    >>> identify('123 LOU')
    False
    """
    score = 0
    result = ''
    for ch in strs:
        if ch.isalpha():
            result += ch
    for ch in strs:
        if ch.isupper():
            score += 1
    if score == len(result) and 'PROPERTY' not in strs and 'COURTESY REPORT' not in strs:
        return False
    if 'Outside Warrant/' in strs:
        return False
    if 'www.' in strs:
        return False
    if strs == 'Booked':
        return False
    if strs == 'Cited':
        return False
    if ' VC' in strs:
        return False
    if ' PC' in strs:
        return False
    if ' HS' in strs:
        return False
    if 'Palo Alto Police Department' in strs:
        return False
    if strs == 'Report Log':
        return False
    return True


def it(strs):
    """
    takes in a string and if the string is a location it returns True, otherwise False
    >>> it('Hello this is a test ST')
    True
    """

    if ', ' in strs:
        return False
    if 'ARRESTEE' in strs:
        return False
    if ' AVE' in strs:
        return True
    if ' REAL' in strs:
        return True
    if ' RD' in strs:
        return True
    if ' ST' in strs:
        return True
    if ' WAY' in strs:
        return True
    if ' PL' in strs:
        return True
    if ' DR' in strs:
        return True
    if ' CT' in strs:
        return True
    if ' LN' in strs:
        return True
    if ' BLVD' in strs:
        return True
    return False


def scrape(strs):
    """
    given a string that has a mushing together of street name and crime, just give the street name.
    >>> scrape('this is the test 123 BRYANT ST')
    '123 BRYANT ST'
    >>> scrape('this is the test .123 BRYANT RD')
    '.123 BRYANT RD'
    >>> scrape('this is the test (F) 123 BRYANT ST')
    '123 BRYANT ST'
    """
    i = 0
    if ' AVE' in strs:
        i = strs.find(' AVE') + 3
    if ' REAL' in strs:
        i = strs.find(' REAL') + 4
    if ' RD' in strs:
        i = strs.find(' RD') + 2
    if ' ST' in strs:
        i = strs.find(' ST') + 2
    if ' WAY' in strs:
        i = strs.find(' WAY') + 3
    if ' PL' in strs:
        i = strs.find(' PL') + 2
    if ' DR' in strs:
        i = strs.find(' DR') + 2
    if ' CT' in strs:
        i = strs.find(' CT') + 2
    if ' LN' in strs:
        i = strs.find(' LN') + 2
    if ' BLVD' in strs:
        i = strs.find(' BLVD') + 4
    while i > 0 and (strs[i].isupper() or strs[i].isdigit() or strs[i] == '.' or strs[i] == ' '):
        i -= 1
    result = strs[i + 1:]
    if result[0] == ' ':
        return strs[i + 2:]
    else:
        return result


def clean(lst):
    """
    Take in a list with nested tuples and clean out all the junk
    In: A list with tuples
    Out: A CLEAN list with tuples

    possible bugs — if time is represented as its own string in the list and it is also attached to a date
    """
    codes = []
    dates = []
    times = []
    crimes = []
    locations = []
    # split
    datetime = []
    for tuple in lst:
        for elem in tuple:
            if '\x0c' in elem:
                elem = elem.replace('\x0c', '')
            # codes
            if len(elem) == 8 and '-' in elem and elem[3].isdigit():
                codes.append(elem)
            # dates
            if go(elem, '/'):
                datetime.append(elem)
            # crimes
            if identify(elem):
                crimes.append(elem)
            # locations
            if it(elem):
                if elem.isupper():
                    locations.append(elem)
                else:
                    new = scrape(elem)
                    locations.append(new)
    for elem in datetime:
        if ' ' in elem:
            two = elem.split(' ')
            date = two[0]
            dates.append(date)
            time = two[1]
            times.append(time)
        else:
            dates.append(elem)
    for tuple in lst:
        for elem in tuple:
            if len(elem) == 4 and (not any(ch.isalpha() or ch.isspace() for ch in elem)):
                times.append(elem)
    return crimes, dates, times, codes, locations


def sort(strs):  # SEE TOP
    """
    Takes in a string and sorts it into a standard crime
    >>> sort('Burglary - From motor vehicle (F)')
    'Burglary'
    >>> sort('FOUND PROPERTY')
    'Found property'
    >>> sort('Death Unattended')
    'Death unattended'
    """
    lower = strs.lower()
    for cat in categories:
        for bin in cat.keys():
            if bin.lower() in lower:
                return bin
            for keyword in cat[bin]:
                if keyword.lower() in lower:
                    return bin
    return strs


def printer(crimes):
    """
    Prints a count of each crime and puts it into a bucket.
    If a crime is a felony, it will print crime, date, time, and police code
    """
    dict = {}

    vio = {}
    the = {}
    dru = {}
    veh = {}
    mis = {}
    other = {}
    for crime in crimes:
        out = sort(crime)
        if out in Theft.keys():
            if out not in the:
                the[out] = 0
            the[out] += 1
        elif out in Drug.keys():
            if out not in dru:
                dru[out] = 0
            dru[out] += 1
        elif out in Vehicle.keys():
            if out not in veh:
                veh[out] = 0
            veh[out] += 1
        elif out in Misc.keys():
            if out not in mis:
                mis[out] = 0
            mis[out] += 1
        elif out in Violent.keys():
            if out not in vio:
                vio[out] = 0
            vio[out] += 1
        else:
            if out not in other:
                other[out] = 0
            other[out] += 1
    return vio, the, dru, veh, mis, other


def printed(dictionary):
    """
    takes in a dictionary and spits out a printed version of it
    """
    for key in dictionary.keys():
        print(key, ' — ', dictionary[key])


def follow(strs, crimes, dates, times_c, codes, filenames, times, locations):
    """
    Given a string which will be the name of a crime, follow it and print out the original crime name, time, date etc.
    strs looks like -> 'Burglary'
    """
    counter = 0
    for i in range(len(crimes)):
        crime = crimes[i]
        PDFname = ''
        if strs.lower() in sort(crime).lower():
            for filename in filenames:
                file = convert_pdf(filename)
                if file.find(dates[i]) != -1 and file.find(times[i]) != -1 and file.find(codes[i]) != -1 and file.find(crimes[i]) != -1:
                    PDFname = str(filename)
            if PDFname == '':
                PDFname = 'unknown PDF origin'
            if len(times) != len(locations):
                print(crime + ' — ' + dates[i], times_c[i], codes[i] + ' — ' + PDFname)
                print(codes[i], ' ' + crime + ' — ' + '[check PDF for location]' + ',', dates[i] + ',', times_c[i], ' —  ' + PDFname)
            else:
                print(codes[i], ' ' + crime + ' — ' + locations[i] + ',', dates[i] + ',', times_c[i],  ' —  ' + PDFname)
            counter += 1
    if counter == 0:
        print('Could not find... Did you type — python3 clean.py [PDF NAME(S)] follow [NAME OF CRIME(in quotes?)]')


def file(strs, crimes, dates, times_c, codes, filenames, times, locations):
    for i in range(len(crimes)):
        crime = crimes[i]
        PDFname = ''
        if strs.lower() in sort(crime).lower():
            for filename in filenames:
                file = convert_pdf(filename)
                if file.find(dates[i]) != -1 and file.find(times[i]) != -1 and file.find(codes[i]) != -1 and file.find(crimes[i]):
                    PDFname = str(filename)
            if PDFname == '':
                PDFname = 'unknown PDF origin'
            if len(times) == len(locations):
                print(locations[i] + ', ' + dates[i] + ' at ' + times_c[i] + ' ' + crime + ' [Code:' + codes[i] + ']' + '... ' + PDFname)
            else:
                print('Check ' + '[' + PDFname + ']' + ' for location' + ' , ' + dates[i] + ' at ' + times_c[i] + ' ' + crime + ' [Code:' + codes[i] + ']' + '... ' + PDFname)


def main():
    args = sys.argv[1:]
    if 'follow' in args:
        start = args.index('follow')
        filenames = args[:start]
    elif 'file' in args:
        start = args.index('file')
        filenames = args[:start]
    else:
        filenames = args
    text = ''
    for filename in filenames:
        text += convert_pdf(filename)
    arrests = count_arrests(text) #works
    lst = text.split('\n\n')
    lst = traverse(lst)
    crimes, dates, times, codes, locations = clean(lst)  # all of these elements are lists
    if len(crimes) != len(dates) or len(dates) != len(times) or len(times) != len(codes):
        return print('Error — program can not process these PDFs. The programmer has coded this error function in to prevent possible errors. This means that the program could not identify the correct times, dates, crimes, etc. In this case, resort to hand doing the data and please contact the programmer: Jonas Pao (jonaspaoman@gmail.com)','for debugging purposes: ', 'number of crimes:', len(crimes), 'number of times:', len(times), 'number of dates:', len(dates), 'number of codes:', len(codes))
    times_c = [time[:2] + ':' + time[2:] for time in times]
    if 'follow' in args:
        start = args.index('follow')
        path = ' '.join(args[start + 1:])
        follow(path, crimes, dates, times_c, codes, filenames, times, locations)
    elif 'file' in args:
        start = args.index('file')
        path = ' '.join(args[start + 1:])
        file(path, crimes, dates, times_c, codes, filenames, times, locations)
    else:
        violence, theft, drug, vehicle, misc, uncategorized = printer(crimes)
        print('\nArrests:')
        print('Total People Arrested —', arrests)
        print('\nViolence Related:')
        for crime in violence:
            file(crime, crimes, dates, times_c, codes, filenames, times, locations)
        print('\nTheft Related:')
        printed(theft)
        print('\nAlcohol or Drug Related:')
        printed(drug)
        print('\nVehicle Related:')
        printed(vehicle)
        print('\nMiscellaneous' + ' [' + 'total', str(sum(misc.values())) + ']:')
        printed(misc)
        print('\nUncategorized:')
        printed(uncategorized)


if __name__ == '__main__':
    main()
    # like: '$ python3 clean.py Sample_PDF.pdf' to get pulse section
    # to follow a certain crime type '$ python3 clean.py Sample_PDF.pdf follow '[WHAT YOU WANT TO FOLLOW]''
