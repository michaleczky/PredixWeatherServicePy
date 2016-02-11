import simplejson as json
from lib import database
from settings import MIN_DATE, MAX_DATE

class JSONSerializable(object):
    def to_json(self):
        return self.__dict__
       
class Place(JSONSerializable):
    """Place model class."""
        
    cache = None

    def __init__(self, row):        
        if row:
            self.Id = row['Id']
            self.Name = row['Name']
            self.CoordLon = row['CoordLon']
            self.CoordLat = row['CoordLat']
            self.Country = row['Country']
        else:
            self.Id = -1
    
    @staticmethod
    def get_by_id(id):
        if not Place.cache: Place.get_all()
        for place in Place.cache:
            if place.Id == id: return place

    @staticmethod
    def get_all():
        if not Place.cache:
            SQL_GET_ALL = "SELECT Id, Name, CoordLon, CoordLat, Country FROM Place"
            Place.cache = [Place(row) for row in database.query(SQL_GET_ALL)]
        return Place.cache
    
    @staticmethod
    def load_measurement_counts(places):
        if places.count > 0:
            params = [place.Id for place in places]
            meta = ''
            for id in params: meta = meta + ',?'
            SQL_MEASUREMENT_COUNT = 'SELECT Place, COUNT(Value) FROM Measurement WHERE Place IN (%s) GROUP BY Place' % meta[1:]
            result = database.query(SQL_MEASUREMENT_COUNT, params)
            for mc in result:
                for place in places:
                    if place.Id == mc[0]: place.MeasurementCount = mc[1]
            return True            

class Measurement(JSONSerializable):
    """Measurement model class."""

    def __init__(self, row):
        if row:
            self.Time = row['Time']
            self.PlaceId = row['PlaceId']
            self.TypeId = row['TypeId']
            self.Value = row['Value']
            self.Type = None
            self.Place = None
    
    @staticmethod
    def get_all(place_id = None, from_date = None, to_date = None, type_id = None):
        params = ()
        SQL = 'SELECT Time, Place as PlaceId, Type as TypeId, Value FROM Measurement WHERE 1=1'
        if place_id:
            SQL = SQL + ' AND Place = ?'
            params = params + (place_id,)
        if type_id:
            SQL = SQL + ' AND Type = ?'
            params = params + (type_id,)
        if from_date > MIN_DATE:
            SQL = SQL + ' AND Time >= ?'
            params = params + (from_date,)
        if to_date < MAX_DATE:
            SQL = SQL + ' AND Time < ?'
            params = params + (to_date,)
        print SQL
        return [Measurement(row) for row in database.query(SQL, params)]
  
    @staticmethod
    def load_types(measurements):
        for m in measurements:
            m.Type = MeasurementType.get_by_id(m.TypeId)

    @staticmethod
    def load_places(measurements):
        for m in measurements:        
            m.Place = Place.get_by_id(m.PlaceId)

    def to_json(self):
        dict = super(Measurement, self).to_json()
        if self.Type: 
            dict['Type'] = self.Type.to_json()
        if self.Place:
            dict['Place'] = self.Place.to_json()
        return dict

class MeasurementType(JSONSerializable):
    """Measurement Type model class."""

    cache = None

    def __init__(self, row):
        if row:
            self.Id = row['Id']
            self.Name = row['Name']
            self.Unit = row['Unit']        

    @staticmethod
    def get_by_id(id):
        if not MeasurementType.cache:
            MeasurementType.get_all()
        for type in MeasurementType.cache:
            if type.Id == id: return type        

    @staticmethod
    def get_all():
        if not MeasurementType.cache:
            SQL = 'SELECT Id, Name, Unit FROM MeasurementType'
            MeasurementType.cache = [MeasurementType(row) for row in database.query(SQL)]
        return MeasurementType.cache