from threading import Timer
from Helper import GetDateTime

class Alarm:
    def __init__(self, alarmSetting, alarmTime):
        self.AlarmSetting = alarmSetting
        self.AlarmTime = alarmTime

class AlarmManager:
    def __init__(self, alarmCallback):
        print("[Alarm Manager] initialized")
        self.AlarmList = []
        self.AlarmCallback = alarmCallback
        Timer(1.0, self.AlarmCheck).start()

    def AlarmCheck(self):
        # Check if any alarms are going off, and if so, pass that data to the callback
        dt = GetDateTime()
        for alarm in self.AlarmList:
            if (alarm.AlarmTime <= dt):
                self.AlarmCallback(alarm.AlarmSetting + " alarm complete")
        self.AlarmList = list(filter(lambda a: a.AlarmTime > dt, self.AlarmList))
        Timer(1.0, self.AlarmCheck).start()

    def SetAlarm(self, alarmSetting, alarmTime):
        print("SetAlarm", alarmTime)
        self.AlarmList.append(Alarm(alarmSetting, alarmTime))
