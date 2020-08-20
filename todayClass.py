from datetime import datetime

class todaytime():
    def today(self):
        self.year= str(datetime.now().year)
        if len(str(datetime.now().month)) < 2:
            self.month = "0"+str(datetime.now().month)
            pass
        else:
            self.month = str(datetime.now().month)
            pass
        if len(str(datetime.now().day)) < 2:
            self.day = "0"+str(datetime.now().day)
            pass
        else:
            self.day = str(datetime.now().day)
            pass
        today = self.year+"-"+self.month+"-"+self.day
        return today
