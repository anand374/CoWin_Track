#!/usr/bin/env python
# coding: utf-8
"""@Author - Abhishek Anand
   @Contact - abh.anand@outlook.com
   @Script_Authored_Date - 14th May, 2021
"""
# importing the necessary libraries
import json
import requests
import datetime
import time
import sys
import emailHelper

date='23-05-2021'
DistId = 123
dose1 = True
dose2 = False

baseUrl = 'https://cdn-api.co-vin.in/api/v2'
statesUrl = baseUrl + '/admin/location/states'
districtsUrl = baseUrl + '/admin/location/districts/{0}'

urlByDistOneWeek = baseUrl + '/appointment/sessions/public/calendarByDistrict'

DistPARAMS = {'district_id':DistId,'date':date}

HEADERS = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

curTime = time.time()
lastMailSentAt = curTime - 901

def checkWholeDistrict():
    available = False
    msg = "\nVaccine available for 18+!!!"
    r = requests.get(urlByDistOneWeek,params=DistPARAMS,headers=HEADERS)

    # Transforming the data returned into JSON format
    data = json.loads(r.text)
    #print(data)
    dt = datetime.datetime.now()
    if data['centers'] == []:
        msg = "No data available for {0}. Last Updated on {1}".format(date,dt.strftime("Date: %d/%m/%Y at time: %H:%M:%S"))

    for centre in data['centers']:
        if centre.get('center_id'):
            dist = centre['district_name']
            for session in centre['sessions']:
                if(session != [] and session['min_age_limit']==18 and session['available_capacity']>0):
                    #Check for dose 1 or 2
                    if(dose1 and session.get('available_capacity_dose1') and (session['available_capacity_dose1']>0)):
                        msg += "\n\nFor date {4}, {0} vaccine available at centre {1} for 1st dose with {2} doses left in {5}. Last Updated on {3}".format(session['vaccine'],centre['name'],session['available_capacity'],dt.strftime("Date: %d/%m/%Y at time: %H:%M:%S"),session['date'],dist,)
                        available = True
                    if(dose2 and session.get('available_capacity_dose2') and (session['available_capacity_dose2']>0)):
                        msg += "\n\nFor date {4}, {0} vaccine available at centre {1} for 2nd dose with {2} doses left in {5}. Last Updated on {3}".format(session['vaccine'],centre['name'],session['available_capacity'],dt.strftime("Date: %d/%m/%Y at time: %H:%M:%S"),session['date'],dist,)
                        available = True

    return (available, msg)

def main():
    global lastMailSentAt
    global curTime

    lastErrorMailSentAt = curTime - 901
    while True:
        vaccAvailInDist = False
        isError = False
        try:
            msg = ""

            vaccAvailInDist, message = checkWholeDistrict()

            if(vaccAvailInDist):
                msg += message
            else:
                msg = "No vaccine available!"

                            
        except Exception:
            msg += "\nError in fetching data from CoWin: " + str(sys.exc_info())
            isError = True

        curTime = time.time()
        if(vaccAvailInDist and (curTime - lastMailSentAt)>=900):
            try:
                emailHelper.sendMail(msg)
                print("Email sent successfully!")
                lastMailSentAt = curTime
            except Exception:
                msg += "\nError in sending Email: " + str(sys.exc_info())
                isError = True
        
        if(isError and (curTime - lastErrorMailSentAt) > 900):
            try:
                emailHelper.sendErrorMail(msg)
                print("Error mail sent successfully!")
                lastErrorMailSentAt = curTime
            except Exception:
                msg += "\nError in pushing Error Mail: " + str(sys.exc_info())
        print(msg)

        time.sleep(15)

if __name__=="__main__":
    main()