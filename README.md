This packet can parse results from MongoDb to their original class

    class Pet:
        def __init__(self):
            self.type = "dog"
            self.name = "dogName"
    
        def __dict__(self):
            return {'type': self.type, 'name': self.name}
    
    
    class Human:
        def __init__(self):
            self.age = 42
            self.name = "name"
            self.pet = Pet()
            self.private_attribute = "foo"
    
        def __dict__(self):
            return {'age': self.age, 'name': self.name, 'pet': self.pet}
    
    h = Human()
    client = MongoClientParser('database_name', 'collection_name')
    client.parse_insert_one(h)      # convert attributes from __dict__ to dict and saves them in the database
    

    obj = client.parse_find_one(Human(), {'name': 'name'}, {'pet': Pet})      # obj is instance from Human and not a dict
    # {'pet': Pet} if key == 'pet' value is parsed to Pet


Install with pip

pip install git+https://github.com/Jackson085/DatabaseConnector