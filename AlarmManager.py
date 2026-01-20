from threading import Timer
from Helper import GetDateTime, log_debug_message

class Alarm:
    def __init__(self, alarmSetting, alarmTime):
        self.AlarmSetting = alarmSetting
        self.AlarmTime = alarmTime

class AlarmManager:
    def __init__(self, alarmCallback):
        log_debug_message("AlarmManager", "[Alarm Manager] initialized")
        self.AlarmList = []
        self.AlarmCallback = alarmCallback
        self.Exit = False
        timer_thread = Timer(1.0, self.AlarmCheck)
        timer_thread.name = "AlarmCheckThread"
        timer_thread.start()

    def AlarmCheck(self):
        # Check if any alarms are going off, and if so, pass that data to the callback
        dt = GetDateTime()
        for alarm in self.AlarmList:
            if (alarm.AlarmTime <= dt):
                self.AlarmCallback(alarm.AlarmSetting + " alarm complete")
        self.AlarmList = list(filter(lambda a: a.AlarmTime > dt, self.AlarmList))
        if (self.Exit == False):
            timer_thread = Timer(1.0, self.AlarmCheck)
            timer_thread.name = "AlarmCheckThread"
            timer_thread.start()

    def SetAlarm(self, alarmSetting, alarmTime):
        log_debug_message("AlarmManager", f"SetAlarm: {alarmTime}")
        self.AlarmList.append(Alarm(alarmSetting, alarmTime))
