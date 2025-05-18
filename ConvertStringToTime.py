from datetime import datetime, timedelta

from Pronunciation import PRONUNCIATION_WORDS_TO_NUMBERS

#  NOTE: This class takes in a string and then generates whether it succeeded, the datetime of the time generated (if successful) and an error if one exists
class ConvertStringToTime:
    def __init__(self, string):
        self.SuccessMessage = ""
        self.DateTime = datetime.now()
        self.DeltaTime = timedelta()
        self.TimeSetting = None
        self.Error = None

        try:
            if (string == None or len(string) == 0):
                self.Error = "No string provided, or string of zero length provided."
                return
            
            string_parts = string.split(" ")
            part_count = len(string_parts)
            if (string_parts == None or part_count == 0):
                self.Error = "No string provided, or string of zero length provided."
                return
        
            #  First potential case: The string is a number or collection of numbers and then AM or PM to signify a specific time
            if ((part_count > 1) and (string_parts[0] in PRONUNCIATION_WORDS_TO_NUMBERS)):
                self.TimeSetting = " ".join(string_parts)
                last_part = string_parts[part_count - 1]
                if last_part in [ "am", "pm" ]:
                    number_parts = string_parts[0:part_count-1]
                    if (len(number_parts) == 1):
                        hour = PRONUNCIATION_WORDS_TO_NUMBERS[number_parts[0]]
                        if (hour > 12):
                            self.Error = "Failure occurred: Could not utilize the given hour, as it was not between 1 and 12"
                            return
                        hour24 = self.ConvertHourTo24Hour(hour, last_part)

                        self.DateTime = self.GetDateTimeFromTimeHourMinute(h=hour24)
                        self.DeltaTime = self.DateTime - datetime.now()
                        return
                    else:
                        convert = self.ConvertNumberGroupToTime(number_parts, last_part)
                        if (self.Error != None):
                            return
                        elif (convert[0] == False):
                            self.Error = "Unknown failure occurred. Failed to convert string to time."
                            return
                        else:
                            self.DateTime = convert[1]
                            self.DeltaTime = self.DateTime - datetime.now()
                            return
            
            #  Second potential case: The string is a count of units (hours, minutes, seconds)
            if (string_parts[part_count - 1] in [ "hours", "hour", "minutes", "minute", "seconds", "second" ]):
                string_parts = list(filter(lambda a: a not in ["and", "in"], string_parts))
                self.TimeSetting = " ".join(string_parts)

                # Determine the number of hours
                hours = 0
                minute_begin = 0
                if ("hours" in string_parts or "hour" in string_parts):
                    hour_numbers = []
                    for i in range(part_count):
                        if (string_parts[i] == "hours" or string_parts[i] == "hour"):
                            minute_begin = i + 1
                            break
                        hour_numbers.append(string_parts[i])
                    for x in hour_numbers:
                        hours += PRONUNCIATION_WORDS_TO_NUMBERS[x]
                    print("Hours: " + str(hours))

                # Determine the number of minutes
                minutes = 0
                second_begin = minute_begin
                if ("minutes" in string_parts[minute_begin:part_count] or "minute" in string_parts[minute_begin:part_count]):
                    minute_numbers = []
                    for i in range(part_count):
                        if (i < minute_begin):
                            continue
                        if (string_parts[i] == "minutes" or string_parts[i] == "minute"):
                            second_begin = i + 1
                            break
                        minute_numbers.append(string_parts[i])
                    for x in minute_numbers:
                        minutes += PRONUNCIATION_WORDS_TO_NUMBERS[x]
                    print("Minutes: " + str(minutes))

                # Determine the number of minutes
                seconds = 0
                if ("seconds" in string_parts[second_begin:part_count] or "second" in string_parts[second_begin:part_count]):
                    second_numbers = []
                    for i in range(part_count):
                        if (i < second_begin):
                            continue
                        if (string_parts[i] == "seconds" or string_parts[i] == "second"):
                            break
                        second_numbers.append(string_parts[i])
                    for x in second_numbers:
                        seconds += PRONUNCIATION_WORDS_TO_NUMBERS[x]
                    print("Seconds: " + str(seconds))

                self.DateTime = self.GetDateTimeFromDelta(h=hours, m=minutes, s=seconds)
                self.DeltaTime = self.DateTime - datetime.now()
                return

            self.Error = "Unknown failure occurred. Failed to convert string to time."
            return
        except Exception as e:
            print(e)
            self.Error = "Unknown error occurred. Failed to convert string to time."
            return
        

    def ConvertNumberGroupToTime(self, number_parts, last_part):
        #  A converted number group must be of size 2 or 3
        if ((len(number_parts) != 2) and (len(number_parts) != 3)):
            return (False, datetime.now())
        
        for n in number_parts:
            if (n not in PRONUNCIATION_WORDS_TO_NUMBERS):
                return (False, datetime.now())
        
        hour = PRONUNCIATION_WORDS_TO_NUMBERS[number_parts[0]]
        if (hour > 12):
            self.Error = "Failure occurred: Could not utilize the given hour, as it was not between 1 and 12"
            return (False, datetime.now())
        
        minute = PRONUNCIATION_WORDS_TO_NUMBERS[number_parts[1]]
        if (len(number_parts) == 3):
            minute += PRONUNCIATION_WORDS_TO_NUMBERS[number_parts[2]]
        if (minute >= 60):
            self.Error = "Failure occurred: Could not utilize the given minute, as it was not between 1 and 59"
            return (False, datetime.now())
        
        hour24 = self.ConvertHourTo24Hour(hour, last_part)
        dt = self.GetDateTimeFromTimeHourMinute(h=hour24, m=minute)
        return (True, dt)

            
    def GetDateTimeFromTimeHourMinute(self, h=0, m=0, s=0):
        dt = datetime.now()
        dt = dt.replace(hour=h, minute=m, second=s, microsecond=0)
        if (dt < datetime.now()):
            dt += timedelta(days=1)
        return dt
    
    def GetDateTimeFromDelta(self, h=0, m=0, s=0):
        dt = datetime.now()
        dt += timedelta(hours=h, minutes=m, seconds=s)
        return dt
            
        
    def GetDeltaString(self):
        deltaH = int(self.DeltaTime.seconds / 3600)
        deltaM = int((self.DeltaTime.seconds - (deltaH * 3600)) / 60)
        deltaS = int((self.DeltaTime.seconds - (deltaH * 3600) - (deltaM * 60)))
        return "Alarm set for " + str(self.DeltaTime.days) + " days, " + str(deltaH) + " hours, " + str(deltaM) + " minutes, " + str(deltaS) + " seconds from now"


    def ConvertHourTo24Hour(self, hour, ap):
        return hour - (12 if (hour == 12) else 0) + (0 if (ap == "am") else 12)