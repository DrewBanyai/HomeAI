import threading
import time
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
        
        # Start a single persistent worker thread for alarm checking
        self.worker_thread = threading.Thread(target=self._worker_loop, name="AlarmCheckThread", daemon=True)
        self.worker_thread.start()

    def _worker_loop(self):
        """Persistent loop that checks for alarms every second."""
        while not self.Exit:
            self.AlarmCheck()
            time.sleep(1.0)
        log_debug_message("AlarmManager", "Alarm worker thread exiting.")

    def AlarmCheck(self):
        # Check if any alarms are going off, and if so, pass that data to the callback
        dt = GetDateTime()
        triggered_alarms = [a for a in self.AlarmList if a.AlarmTime <= dt]
        
        for alarm in triggered_alarms:
            log_debug_message("AlarmManager", f"Alarm triggered: {alarm.AlarmSetting}")
            self.AlarmCallback(alarm.AlarmSetting + " alarm complete")
            
        # Update the list to remove triggered alarms
        self.AlarmList = [a for a in self.AlarmList if a.AlarmTime > dt]

    def SetAlarm(self, alarmSetting, alarmTime):
        log_debug_message("AlarmManager", f"SetAlarm: {alarmTime}")
        self.AlarmList.append(Alarm(alarmSetting, alarmTime))

