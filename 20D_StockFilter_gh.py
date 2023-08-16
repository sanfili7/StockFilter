#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 22:26:01 2018

@author: jaspersanfilippo
"""

### Alpha Vantage API Key: XXXXXXXXXXXXXXXX

import urllib.request
from bs4 import BeautifulSoup
import requests
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys

# Returns users selected item as the most current available as a float in USD
def statement_func(sheet, item, companySymbol):
    sheet = sheet.replace(' ', '-')
    sheet = sheet.lower()

    # Make sheet readable for showing the user if necessary
    statementSheet = sheet
    statementSheet = statementSheet.title()
    statementSheet = statementSheet.replace('-', ' ')

    # If looking for Income Statement, url is actually 'financials'
    if sheet == 'income-statement':
        sheet = 'financials'

    # Puts item into a nice format incase user needs to check the financial statement
    item = item.title()

    companySymbol = companySymbol.upper()

    # Inserts user input into the yahoo finance url for str of data of users desired statement
    yahooSheet_url = 'https://finance.yahoo.com/quote/' + companySymbol + \
        '/' + sheet + '?p=' + companySymbol

    # Converts webpage html into text
    req = urllib.request.Request(yahooSheet_url)
    with urllib.request.urlopen(req) as response:
        html = response.read()

    soup = BeautifulSoup(html, "lxml")

    for script in soup(["script", "style"]):
        script.extract()

    websiteText = soup.get_text()

    runFunction = True

    error_bool = False

    error = 'An error has occured.'

    # Check if substring exists
    exists = websiteText.find(item)

    if exists == -1:
        valueUSD = 0
        runFunction = False

    else:
        # Finds the index point to start analyzing values from
        item_len = len(item)
        item_index = websiteText.index(item) + item_len
        item_str = websiteText[item_index:]

        start_index = 0
        finish_index = 1

           # Quickly tells if the value is 0 by seeing in the item_str two dashes together
           # It will know that the first dash is not a negative sign
        valueZero_str = item_str[1:2]

        if valueZero_str == '-':
            valueUSD = 0

        else:
            # Variable that finds the first character after 'item'
            itemTest_str = item_str[start_index:finish_index]

            # Number to find the comma or the dot depending on the value
            separaterNumber = 3

            negative_item = False

            if itemTest_str == '-':
                separaterNumber += 1

                negative_input = input('Enter value for ' + item + ' for ' + companySymbol \
                    + ' as it appears on the ' + statementSheet + ': ')

                if negative_input == '-':
                    negative_value = 0

                else:
                    negativeValue = negative_input
                    negative_item = True

            separater_index = item_str.index(',')

            while error_bool == False:

                # If there is no comma it looks for the index number of the decimal
                if separater_index > separaterNumber:
                    separater_index = item_str.index('.')

                    if separater_index > separaterNumber:
                        print('Check the ' + statementSheet + ' for ' + item)
                        print('There may be small numbers, or no values at all... ')

                        usersInput = input('Enter the value for ' + item + ' as shown: ')
                        levelsValue = usersInput

                        negativeQualifier = usersInput[0:1]

                        if levelsValue == '-':
                            levelsValue = 0
                            negative_item = False

                        elif negativeQualifier == '-':
                            negative_item = True

                        else:
                            negative_item = False

                        runFunction = False

                    #except ValueError:
                     #   print('There are likely no values for ' + companySymbol + '.')

                while runFunction == True:

                    if separater_index == 1:
                        start_index = 0
                        finish_index = 1
                        itemlvl01 = item_str[start_index:finish_index]
                        start_index += 1
                        finish_index += 1

                    if separater_index == 2:
                        start_index = 0
                        finish_index = 2
                        itemlvl01 = item_str[start_index:finish_index]
                        start_index += 2
                        finish_index += 1

                    if separater_index == 3:
                        start_index = 0
                        finish_index = 3
                        itemlvl01 = item_str[start_index:finish_index]
                        start_index += 3
                        finish_index += 1

                    if separater_index == 4:
                        start_index = 0
                        finish_index = 4
                        itemlvl01 = item_str[start_index:finish_index]
                        start_index += 4
                        finish_index += 1

                    end_var = True

                    while end_var == True:
                        # Setup for Level Two
                        itemTest_str = item_str[start_index:finish_index]

                        if itemTest_str != ',':
                            if itemTest_str == '.':
                                finish_index += 3
                                dotValue = item_str[start_index:finish_index]
                                levelsValue = itemlvl01 + dotValue
                                end_var = False
                                break

                            else:
                                levelsValue = itemlvl01
                                end_var = False
                                break

                        # Level Two
                        if itemTest_str == ',':
                            start_index += 1
                            finish_index += 3
                            itemlvl02 = item_str[start_index:finish_index]
                            start_index += 3
                            finish_index += 1

                        # Setup for Level Three
                        itemTest_str = item_str[start_index:finish_index]

                        if itemTest_str != ',':
                            if itemTest_str == '.':
                                finish_index += 3
                                dotValue = item_str[start_index:finish_index]
                                levelsValue = itemlvl01 + itemlvl02 + dotValue
                                end_var = False
                                break

                            else:
                                levelsValue = itemlvl01 + itemlvl02
                                end_var = False
                                break

                        # Level Three
                        if itemTest_str == ',':
                            start_index += 1
                            finish_index += 3
                            itemlvl03 = item_str[start_index:finish_index]
                            start_index += 3
                            finish_index += 1

                        # Setup for Level Four
                        itemTest_str = item_str[start_index:finish_index]

                        if itemTest_str != ',':
                            if itemTest_str == '.':
                                finish_index += 3
                                dotValue = item_str[start_index:finish_index]
                                levelsValue = itemlvl01 + itemlvl02 + itemlvl03 + dotValue
                                end_var = False
                                break

                            else:
                                levelsValue = itemlvl01 + itemlvl02 + itemlvl03
                                end_var = False
                                break

                        # Level Four
                        if itemTest_str == ',':
                            start_index += 1
                            finish_index += 3
                            itemlvl04 = item_str[start_index:finish_index]
                            start_index += 3
                            finish_index += 1

                        # Setup for Level Five
                        itemTest_str = item_str[start_index:finish_index]

                        if itemTest_str != ',':
                            if itemTest_str == '.':
                                finish_index += 3
                                dotValue = item_str[start_index:finish_index]
                                levelsValue = itemlvl01 + itemlvl02 + itemlvl03 + itemlvl04 \
                                    + dotValue
                                end_var = False
                                break

                            else:
                                levelsValue = itemlvl01 + itemlvl02 + itemlvl03 + itemlvl04
                                end_var = False
                                break

                        # Level Five
                        if itemTest_str == ',':
                            start_index += 1
                            finish_index += 3
                            itemlvl05 = item_str[start_index:finish_index]
                            start_index += 3
                            finish_index += 1

                        # Final Setup
                        itemTest_str = item_str[start_index:finish_index]

                        if itemTest_str != ',':
                            if itemTest_str == '.':
                                finish_index += 3
                                dotValue = item_str[start_index:finish_index]
                                levelsValue = itemlvl01 + itemlvl02 + itemlvl03 + itemlvl04 \
                                    + itemlvl05 + dotValue
                                end_var = False
                                break

                            else:
                                levelsValue = itemlvl01 + itemlvl02 + itemlvl03 + itemlvl04 \
                                    + itemlvl05
                                end_var = False
                                break

                    runFunction = False

                if negative_item == True:
                    #value = levelsValue[1:]
                    value_float = float(negativeValue) * 1000

                else:
                    value_float = float(levelsValue) * 1000

                ##### Exchanges item into USD if necessary #####

                exchangeQualifier_index = websiteText.index('All numbers in thousands') - 2
                exchangeQualifier = websiteText[exchangeQualifier_index]

                if exchangeQualifier == '.':
                    # Do a conversion from starting currency to USD
                    exchange_index = websiteText.index('. All numbers in thousands') - 3

                    startCurrency_index = exchange_index
                    finishCurrency_index = exchange_index + 3
                    currency_str = websiteText[startCurrency_index:finishCurrency_index]

                    exchange_url = 'https://api.exchangerate-api.com/v4/latest/' + \
                        currency_str

                    response = requests.get(exchange_url)
                    data = response.json()

                    rates_dict = data['rates']
                    usdConversion_float = float(rates_dict['USD'])

                    valueUSD_raw = value_float * usdConversion_float
                    valueUSD = round(valueUSD_raw, 3)

                else:
                    valueUSD = value_float

                # Just to get the error loop to stop running
                break

    return valueUSD

# Returns "Shares Outstanding" as a float
def sharesOutstanding_func(companySymbol):
    # Pulls up Yahoo Finance statistics page as a string
    yahooStatistics_url = 'https://finance.yahoo.com/quote/' + companySymbol \
        + '/key-statistics?p=' + companySymbol

    # Converts webpage html into text
    req = urllib.request.Request(yahooStatistics_url)
    with urllib.request.urlopen(req) as response:
        html = response.read()

    soup = BeautifulSoup(html, "lxml")

    for script in soup(["script", "style"]):
        script.extract()

    yahooStatistics_str = soup.get_text()

    # Creates new string from the website text after "Shares Outstanding"
    so_index = yahooStatistics_str.index('Shares Outstanding 5') + 20
    so_str = yahooStatistics_str[so_index:]

    # Find first value to make sure Shares Outstanding isn't N/A
    soDisqualifier_str = so_str[0:1]

    if soDisqualifier_str == 'N':
        sharesOutstanding_int = 0
        return sharesOutstanding_int

    else:

        #Finds and changes "Shares Outstanding" to a float
        sharesOutstanding_index = so_str.index('Float') - 1
        so_float = float(so_str[:sharesOutstanding_index])

        # Finds and determines the multiple for "Shares Outstanding" as defined
        # by the letter after the end of the number
        mqStart_index = so_str.index('Float') - 1
        mqFinish_index = so_str.index('Float')
        multiplicationQualifier_str = so_str[mqStart_index:mqFinish_index]

        if multiplicationQualifier_str == 'B':
            sharesOutstanding_float = so_float * 1000000000

        if multiplicationQualifier_str == 'M':
            sharesOutstanding_float = so_float * 1000000

        if multiplicationQualifier_str == 'k':
            sharesOutstanding_float = so_float * 1000

        return sharesOutstanding_float

def marketCap_func(companySymbol):

    yahooSummary_url = 'https://finance.yahoo.com/quote/' + companySymbol \
        + '?p=' + companySymbol

    # Converts webpage html into text
    req = urllib.request.Request(yahooSummary_url)
    with urllib.request.urlopen(req) as response:
        html = response.read()

    soup = BeautifulSoup(html, "lxml")

    for script in soup(["script", "style"]):
        script.extract()

    yahooSummary_str = soup.get_text()

    # Finds the number for Market Cap
    marketCapStart_index = yahooSummary_str.index('Market Cap') + 10
    marketCapFinish_index = yahooSummary_str.index('Beta') - 1

    marketCap_str = yahooSummary_str[marketCapStart_index:marketCapFinish_index]
    marketCap_float = float(marketCap_str)

    # Finds the multiplier for Market Cap
    multiplierStart_index = yahooSummary_str.index('Beta') - 1
    multiplierFinish_index = yahooSummary_str.index('Beta')

    multiplier_str = yahooSummary_str[multiplierStart_index:multiplierFinish_index]

    if multiplier_str == 'B':
        MarketCapitalization = marketCap_float * 1000000000

    if multiplier_str == 'M':
        MarketCapitalization = marketCap_float * 1000000

    return MarketCapitalization

# Returns "Share Price" as a float
def sharePrice_func(companySymbol):
    # Uses the API from Alpha Vantage
    API_URL = 'https://www.alphavantage.co/query'

    data = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": companySymbol,
        "interval": "1min",
        "outputsize": "compact",
        "datatype": "json",
        "apikey": "JEHP1MJQWTU5QIQW",
        }

    response = requests.get(API_URL, data)
    allData_dict = response.json()

    nested01_dict = allData_dict['Meta Data']
    lastRefreshed_key = nested01_dict['3. Last Refreshed']

    nested02_dict = allData_dict['Time Series (1min)']

    nested03_dict = nested02_dict[lastRefreshed_key]

    sharePrice_float = float(nested03_dict['4. close'])

    return sharePrice_float

# Handles user inputs and makes them work for the program
def handleInputs_func(companySymbol, userInput):
    # Remove commas and make the users input a float

    userInput_float = float(userInput) * 1000
    
    sheet = 'balance-sheet'

    companySymbol = companySymbol.upper()

    # Inserts user input into the yahoo finance url for str of data of users desired statement
    yahooSheet_url = 'https://finance.yahoo.com/quote/' + companySymbol + \
        '/' + sheet + '?p=' + companySymbol

    # Converts webpage html into text
    req = urllib.request.Request(yahooSheet_url)
    with urllib.request.urlopen(req) as response:
        html = response.read()

    soup = BeautifulSoup(html, "lxml")

    for script in soup(["script", "style"]):
        script.extract()

    websiteText = soup.get_text()

    ##### Exchanges item into USD if necessary #####

    exchangeQualifier_index = websiteText.index('All numbers in thousands') - 2
    exchangeQualifier = websiteText[exchangeQualifier_index]

    if exchangeQualifier == '.':
        # Do a conversion from starting currency to USD
        exchange_index = websiteText.index('. All numbers in thousands') - 3

        startCurrency_index = exchange_index
        finishCurrency_index = exchange_index + 3
        currency_str = websiteText[startCurrency_index:finishCurrency_index]

        exchange_url = 'https://api.exchangerate-api.com/v4/latest/' + \
            currency_str

        response = requests.get(exchange_url)
        data = response.json()

        rates_dict = data['rates']
        usdConversion_float = float(rates_dict['USD'])

        valueUSD_raw = userInput_float * usdConversion_float
        valueUSD = round(valueUSD_raw, 3)

    else:
        valueUSD = userInput_float

    return valueUSD

# Shows the user the url to copy and paste for pertinent information
def url_func(companySymbol):
    
    sheet = 'balance-sheet'

    companySymbol = companySymbol.upper()

    # Inserts user input into the yahoo finance url for str of data of users desired statement
    yahooSheet_url = 'https://finance.yahoo.com/quote/' + companySymbol + \
        '/' + sheet + '?p=' + companySymbol

    return yahooSheet_url

###############################################################################
#                              ACTUAL PROGRAM                                 #
###############################################################################

runAgain = True

while runAgain == True:

    # Prompt user to input company ticker symbol
    tickerSymbol = input("Enter the company ticker symbol... ")

    # Program currently tailored for me
    #userStatement = input("Enter the desired statement you want information on... ")

    # Program currently tailored for me
    #userItem = input("Enter the item of that statement you want to calculate... ")

    # Run functions to find Net Tangible Assets and Shares Outstanding
    NetTangibleAssets = statement_func('balance sheet', 'net tangible assets', tickerSymbol)
    SharesOutstanding = sharesOutstanding_func(tickerSymbol)

    if SharesOutstanding == 0:
        print('There is no data for Shares Outstanding.')

    else:
        # Calculate, round and show Net Tangible Asset Value per Share
        ntaPerShare = round(NetTangibleAssets / SharesOutstanding, 3)
        nta_perShare_str = str(ntaPerShare)
        print(nta_perShare_str + " ---> Net Tangible Assets / Share")

        # Find and show Share Price
        SharePrice = sharePrice_func(tickerSymbol)
        sharePrice_str = str(SharePrice)
        print(sharePrice_str + ' ---> Share Price')

        discount_int = round((SharePrice / ntaPerShare) * 100, 2)
        discount_str = str(discount_int)

        print('---> ' + discount_str + '% <--- Discount, or premium as a percentage')

        discount_float = round((SharePrice / ntaPerShare), 3)
        if 0 < discount_float < 1:
            # Finds the Current Ratio
            url = url_func(tickerSymbol)
            print("---")
            print("Copy URL for the below: " + url)
            print("---")

            TotalCurrentAssets_input = input("Enter 'Current Assets' as shown with no commas... ")
            TotalCurrentLiabilities_input = input("Enter 'Current Liabilities' as shown with no commas... ")

            TotalCurrentAssets = handleInputs_func(tickerSymbol, TotalCurrentAssets_input)
            TotalCurrentLiabilities = handleInputs_func(tickerSymbol, TotalCurrentLiabilities_input)

            if TotalCurrentLiabilities == 0:
                print('Current Liabilities may be 0.')
                ## Note: maybe add a part allowing the user to check and enter the values for current assets and current liabilities...
                print('The Current Ratio cannot be calculated.')

            else:
                CurrentRatio = round((TotalCurrentAssets / TotalCurrentLiabilities), 3)
                currentRatio_str = str(CurrentRatio)
                print(currentRatio_str + ' ---> Current Ratio')

                if CurrentRatio >= 1.5:
                    # Finds Total Debt / Net Working Capital
                    TotalDebt = statement_func('balance sheet', 'total debt', tickerSymbol)
                    NetWorkingCapital = TotalCurrentAssets - TotalCurrentLiabilities

                    if NetWorkingCapital == 0:
                        print('Net Working Capital is 0.')
                        print('Total Debt / Net Working Capital cannot be calculated.')

                    else:
                        TD_NWC = round(((TotalDebt / NetWorkingCapital) * 100), 3)

                        td_nwc_str = str(TD_NWC)
                        print(td_nwc_str + ' ---> Total Debt / Net Working Capital')

                        if TD_NWC <= 110:
                            # Finds Market Capitalization / Net Tangible Assets
                            MarketCapitalization = marketCap_func(tickerSymbol)
                            # Theoretically already have a value for Net Tangible Assets

                            resultingValue = round(((MarketCapitalization / NetTangibleAssets) * 100), 3)

                            mc_nta_str = str(resultingValue)
                            print(mc_nta_str + ' ---> Market Capitalization / Net Tangible Assets')

                            if NetTangibleAssets == 0:
                                print('Net Tangible Assets is 0.')
                                print('Market Capitalization / Net Tangible Assets cannot be calculated.')

                            else:
                                if resultingValue <= 120:
                                    print('PERHAPS A PRUDENT INVESTMENT!!!')
                                    print('Look into ' + tickerSymbol + ' for further details.')

                                else:
                                    print('Missed on Market Capitalization / Net Tangible Assets...')

                        else:
                            print('Missed on Total Debt / Net Working Capital...')

                else:
                    print('Missed on Current Ratio...')

        else:
            print('Missed on Net Tangible Asset value per share...')

    # Asks user if they would like to run the program again
    # This line is not subject to indentation
    userPrompt_input = input('Run again? [y/n]: ')
    userPrompt_str = userPrompt_input.lower()

    if userPrompt_str == 'y':
        print(" ")
        print("+++++++++++++++++")
        print(" ")
        runAgain = True

    else:
        runAgain = False
