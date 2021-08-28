from Dto import Vaccine
from Dto import Supplier
from Dto import Clinic
from Dto import Logistic


class _Vaccines:
    total_inventory = 0

    def __init__(self, conn):
        self._conn = conn
        _Vaccines._total_inventory = 0

    def insert(self, vaccine):
        _Vaccines.total_inventory = _Vaccines.total_inventory + int(vaccine.quantity)
        
        self._conn.execute("""
            INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
            """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, date, supplier, quantity FROM vaccines WHERE id = ?
            """, [vaccine_id])

        return Vaccine(*c.fetchone())

    def update_quantity(self, vaccine_id, vaccine_quantity_old_value, vaccine_quantity_new_value):
        quantity_to_add = vaccine_quantity_new_value - vaccine_quantity_old_value
        _Vaccines.total_inventory = _Vaccines.total_inventory + quantity_to_add

        c = self._conn.cursor()
        c.execute("""
            UPDATE vaccines SET quantity = (?) WHERE id = (?)
            """, [vaccine_quantity_new_value, vaccine_id])

    def find_next_vaccine(self):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM vaccines ORDER BY date ASC
            """)

        return Vaccine(*c.fetchone())
    
    def delete(self, vaccine_id, vaccine_quantity):
        _Vaccines.total_inventory = _Vaccines.total_inventory - vaccine_quantity
        
        self._conn.execute("""
                    DELETE FROM vaccines WHERE id = (?)
                    """, [vaccine_id])


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
            INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
            """, [supplier.id, supplier.name, supplier.logistic])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, logistic FROM suppliers WHERE id = ?
            """, [supplier_id])

        return Supplier(*c.fetchone())

    def find_by_name(self, supplier_name):
        c = self._conn.cursor()
        c.execute("""
                    SELECT id, name, logistic FROM suppliers WHERE name = ?
                    """, [supplier_name])

        return Supplier(*c.fetchone())


class _Clinics:
    total_demand = 0

    def __init__(self, conn):
        self._conn = conn
        _Clinics.total_demand = 0

    def insert(self, clinic):
        _Clinics.total_demand = _Clinics.total_demand + int(clinic.demand)

        self._conn.execute("""
            INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
            """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find(self, clinic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, location, demand, logistic FROM clinics WHERE id = ?
            """, [clinic_id])

        return Clinic(*c.fetchone())

    def find_by_location(self, clinic_location):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, location, demand, logistic FROM clinics WHERE location = ? 
            """, [clinic_location])

        return Clinic(*c.fetchone())

    def update_demand(self, clinic_demand_old_value, clinic_demand_new_value, clinic_id):
        demand_to_add = clinic_demand_new_value - clinic_demand_old_value
        _Clinics.total_demand = _Clinics.total_demand + demand_to_add

        c = self._conn.cursor()
        c.execute("""
            UPDATE clinics SET demand = (?) WHERE id = (?)
            """, [clinic_demand_new_value, clinic_id])


class _Logistics:
    total_sent = 0
    total_received = 0

    def __init__(self, conn):
        self._conn = conn
        _Logistics.total_sent = 0
        _Logistics.total_received = 0

    def insert(self, logistic):
        _Logistics.total_sent = _Logistics.total_sent + int(logistic.count_sent)
        _Logistics.total_received = _Logistics.total_received + int(logistic.count_received)

        self._conn.execute("""
            INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
            """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, logistic_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT id, name, count_sent, count_received FROM logistics WHERE id = ?
            """, [logistic_id])

        return Logistic(*c.fetchone())

    def update_count_sent(self, logistic_count_sent_old_value, logistic_count_sent_new_value, logistic_id):
        count_to_add = logistic_count_sent_new_value - logistic_count_sent_old_value
        _Logistics.total_sent = _Logistics.total_sent + count_to_add

        c = self._conn.cursor()
        c.execute("""
            UPDATE logistics SET count_sent = (?) WHERE id = (?)
            """, [logistic_count_sent_new_value, logistic_id])

    def update_count_received(self, logistic_count_received_old_value, logistic_count_received_new_value, logistic_id):
        count_to_add = logistic_count_received_new_value - logistic_count_received_old_value
        _Logistics.total_received = _Logistics.total_received + count_to_add

        c = self._conn.cursor()
        c.execute("""
            UPDATE logistics SET count_received = (?) WHERE id = (?)
            """, [logistic_count_received_new_value, logistic_id])
