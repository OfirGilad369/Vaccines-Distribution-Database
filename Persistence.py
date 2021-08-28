from Dao import _Logistics, _Suppliers, _Clinics, _Vaccines
from Dto import Logistic, Supplier, Clinic, Vaccine
import sqlite3
import atexit


# The Repository
class _Repository:

    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self._logistics = _Logistics(self._conn)
        self._suppliers = _Suppliers(self._conn)
        self._clinics = _Clinics(self._conn)
        self._vaccines = _Vaccines(self._conn)
        self._next_vaccine_index = 1

    def close(self):
        self._next_vaccine_index = 1
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
        DROP TABLE IF EXISTS 'logistics';
        DROP TABLE IF EXISTS 'suppliers';
        DROP TABLE IF EXISTS 'clinics';
        DROP TABLE IF EXISTS 'vaccines';
        """)
        self._conn.executescript("""
        CREATE TABLE logistics (
            id INTEGER PRIMARY KEY,
            name STRING NOT NULL,
            count_sent INTEGER NOT NULL,
            count_received INTEGER NOT NULL
        );
        
        CREATE TABLE suppliers (
            id INTEGER PRIMARY KEY,
            name STRING NOT NULL,
            logistic INTEGER REFERENCES logistics(id)
        );
        
        CREATE TABLE clinics (
            id INTEGER PRIMARY KEY,
            location STRING NOT NULL,
            demand INTEGER NOT NULL,
            logistic INTEGER REFERENCES logistics(id)
        );
        
        CREATE TABLE vaccines (
            id INTEGER PRIMARY KEY,
            date DATE NOT NULL,
            supplier INTEGER REFERENCES suppliers(id),
            quantity INTEGER NOT NULL
        );
        """)

    def print_all(self):
        print("vaccines")
        self.print_table(self._conn.execute("SELECT * FROM vaccines ORDER BY date ASC"))
        print("suppliers")
        self.print_table(self._conn.execute("SELECT * FROM suppliers"))
        print("clinics")
        self.print_table(self._conn.execute("SELECT * FROM clinics"))
        print("logistics")
        self.print_table(self._conn.execute("SELECT * FROM logistics"))

    @staticmethod
    def print_table(list_of_elements):
        for element in list_of_elements:
            print(element)

    def config_decode(self, config):
        is_first_line = True
        with open(config, 'r') as input_file:
            for line in input_file:
                text_line = line.split(",")
                if is_first_line:
                    vaccines_length = int(text_line[0])
                    suppliers_length = int(text_line[1])
                    clinics_length = int(text_line[2])
                    logistics_length = int(text_line[3])
                    is_first_line = False
                elif vaccines_length > 0:
                    temp = Vaccine(text_line[0], text_line[1], text_line[2], text_line[3])
                    self._vaccines.insert(temp)
                    vaccines_length = vaccines_length - 1
                    if int(temp.id) >= self._next_vaccine_index:
                        self._next_vaccine_index = int(temp.id)
                        self._next_vaccine_index = self._next_vaccine_index + 1
                elif suppliers_length > 0:
                    temp = Supplier(text_line[0], text_line[1], text_line[2])
                    self._suppliers.insert(temp)
                    suppliers_length = suppliers_length - 1
                elif clinics_length > 0:
                    temp = Clinic(text_line[0], text_line[1], text_line[2], text_line[3])
                    self._clinics.insert(temp)
                    clinics_length = clinics_length - 1
                elif logistics_length > 0:
                    temp = Logistic(text_line[0], text_line[1], text_line[2], text_line[3])
                    self._logistics.insert(temp)
                    logistics_length = logistics_length - 1
                else:
                    print("ERROR")

    def find_supplier_by_name(self, supplier_name):
        return self._suppliers.find_by_name(supplier_name)

    def insert_next_vaccine(self, date, supplier_id, amount):
        vaccine_to_insert = Vaccine(self._next_vaccine_index, date, supplier_id, amount)
        self._next_vaccine_index = self._next_vaccine_index + 1
        self._vaccines.insert(vaccine_to_insert)

    def find_logistic_by_id(self, logistic_id):
        return self._logistics.find(logistic_id)

    def update_count_received(self, old_count_received, new_count_received, logistic_id):
        self._logistics.update_count_received(old_count_received, new_count_received, logistic_id)

    def find_by_location_clinic(self, location):
        return self._clinics.find_by_location(location)

    def update_demand(self, old_demand, new_demand, clinic_id):
        self._clinics.update_demand(old_demand, new_demand, clinic_id)

    def update_count_sent(self, old_count_sent, new_count_sent, logistic_id):
        self._logistics.update_count_sent(old_count_sent, new_count_sent, logistic_id)

    def find_next_vaccine(self):
        return self._vaccines.find_next_vaccine()

    def delete_vaccine(self, vaccine_id, next_vaccine_quantity):
        self._vaccines.delete(vaccine_id, next_vaccine_quantity)

    def update_quantity(self, vaccine_id, old_quantity, new_quantity):
        self._vaccines.update_quantity(vaccine_id, old_quantity, new_quantity)

    def total_inventory(self):
        return self._vaccines.total_inventory

    def total_demand(self):
        return self._clinics.total_demand

    def total_received(self):
        return self._logistics.total_received

    def total_sent(self):
        return self._logistics.total_sent


# the repository singleton
repo = _Repository()
atexit.register(repo.close)
