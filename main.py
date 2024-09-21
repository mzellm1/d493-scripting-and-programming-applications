
class WeatherLoc:
    def __init__(self, mlatitude, mlongitude, month, day, year,
                 maveragetemp, mtempmin, mtempmax, maveragewindspeed,
                 mwindspeedmin, mwindspeedmax, msumprecipitation,
                 mrainmin, mrainmax):
        self.mlatitude = mlatitude
        self.mlongitude = mlongitude
        self.month = month
        self.day = day
        self.year = year
        self.maveragetemp = maveragetemp
        self.mtempmin = mtempmin
        self.mtempmax = mtempmax
        self.maveragewindspeed = maveragewindspeed
        self.mwindspeedmin = mwindspeedmin
        self.mwindspeedmax = mwindspeedmax
        self.msumprecipitation = msumprecipitation
        self.mrainmin = mrainmin
        self.mrainmax = mrainmax
