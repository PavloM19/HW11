from collections import UserDict
from datetime import datetime
import re


class AddressBook(UserDict):
    quant_iter = 5 # генератор за записами AddressBook за одну ітерацію повертає представлення для N записів
    current_index = 0
    def __iter__(self):
        return self

    def __next__(self): 
        out_dict = {}
        if self.current_index < len(self):
            for i, record in enumerate(self.data.items()):
                if i < self.current_index:
                    continue
                elif self.current_index <= i < self.current_index + self.quant_iter:
                    out_dict[record[0]] = record[1]
                else:
                    break
            
            self.current_index += self.quant_iter
            return out_dict
        
        else:
            raise StopIteration

    def add_record(self, record):
        self.data[record.name.value] = record

    def del_record(self, name):
        if name in self:
            self.data.pop(name)
        else:
            print('bot>> Error. This record does not exist!')

    def show_all_names(self):
        print(f'bot>> {list(self.data)}')


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return str(self.__value)

    def __repr__(self):
        return self.__str__()    

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    def __init__(self, name):
        super().__init__(name)
    

class Phone(Field):
    def __init__(self, phone):
        if phone.isdigit():
            self.phone = phone
        else:
            self.phone = None
            print('bot>> Error, phone must contain only digits')
        super().__init__(self.phone)

    # @Field.value.setter
    # def value(self, value: str):
    #     if value.isdigit():
    #         self.__value = value
    #         print('Field.value.setter ',value, self.value)
    #     else:
    #         self.__value = None
    #         print('bot>> Error, phone must contain only digits')


class Birthday(Field):
    def __init__(self, birthday: str):  #format: 'dd.mm.YYYY or dd/mm/YYYY or dd-mm-YYYY'
        super().__init__(birthday)

    @Field.value.setter
    def value(self, birthday: str):
        self.data_str = re.sub(r'[/-]', '.', birthday.strip())
        try:
            data = datetime.strptime(self.data_str, '%d.%m.%Y')
        except ValueError as err:
            print('bot>> Error, ' + str(err))
        else:
            self.__value = data            

    def __str__(self):
        return self.data_str


class Record:
    def __init__(self, name: Name, phone=None, birthday=None): 
        self.name = name
        
        if phone:
            if type(phone) is Phone:
                self.phones = []
                if phone.value:
                    self.phones.append(phone)
            else:
                print('bot>> Error. phone must be an object of class Phone!')

        if birthday:
            if type(birthday) is Birthday:
                self.birthday = birthday
            else:
                print('bot>> Error. birthday must be an object of class Birthday!')

    def __str__(self):
        return f'{self.phones} ({self.birthday})'

    def __repr__(self):
        return self.__str__()
    
    def add_new_phone(self, new_phone):
        if not phone:
            self.phones = []
            self.phones.append(new_phone)
        else:
            self.phones.append(new_phone)

    def del_phone(self, phone=''):
        if not phone:
            self.phones.pop()  #delete the last
        else:
            if phone in self.phones:
                self.phones.remove(phone)
            else:
                print('bot>> Error. This phone does not exist!')

    def days_to_birthday(self):
        current = datetime.now()
        date_cut = self.birthday.split('.')
        d = int(date_cut[0])
        m = int(date_cut[1])
        next_bd = datetime(year=current.year, month=m, day=d+1)
        delta = next_bd - current
        if delta.days < 0:
            next_bd = datetime(year=current.year+1, month=m, day=d)
            delta = next_bd - current
            
        return delta.days
        

if __name__ == "__main__":
    pass
