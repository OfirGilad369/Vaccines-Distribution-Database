from Persistence import repo


class _OrderExecution:
    def __init__(self, orders, output):
        open(output, 'w').close()
        self._orders = orders
        self._output = output

    def execute_orders(self):
        with open(self._orders, 'r') as input_file:
            for line in input_file:
                text_line = line.split(",")
                if len(text_line) == 3:
                    self.receive_shipment_order(text_line)
                elif len(text_line) == 2:
                    self.send_shipment_order(text_line)
                else:
                    print("ERROR")

    def receive_shipment_order(self, order_line):
        name = order_line[0]
        amount = int(order_line[1])
        length = len(order_line[2])
        date = order_line[2][0:length - 1]
        supplier = repo.find_supplier_by_name(name)
        repo.insert_next_vaccine(date, supplier.id, amount)
        logistic = repo.find_logistic_by_id(supplier.logistic)
        new_count_received = logistic.count_received + amount
        repo.update_count_received(logistic.count_received, new_count_received, logistic.id)
        self.print_to_output()

    def send_shipment_order(self, order_line):
        location = order_line[0]
        amount = int(order_line[1])
        clinic = repo.find_by_location_clinic(location)
        new_demand = clinic.demand - amount
        repo.update_demand(clinic.demand, new_demand, clinic.id)
        logistic = repo.find_logistic_by_id(clinic.logistic)
        new_count_sent = logistic.count_sent + amount
        repo.update_count_sent(logistic.count_sent, new_count_sent, logistic.id)
        while amount > 0:
            next_vaccine = repo.find_next_vaccine()
            if amount >= next_vaccine.quantity:
                repo.delete_vaccine(next_vaccine.id, next_vaccine.quantity)
            else:
                new_quantity = next_vaccine.quantity - amount
                repo.update_quantity(next_vaccine.id, next_vaccine.quantity, new_quantity)
            amount = amount - next_vaccine.quantity
        self.print_to_output()

    def print_to_output(self):
        with open(self._output, 'a') as output_file:
            output_file.write(str(repo.total_inventory()) + ",")
            output_file.write(str(repo.total_demand()) + ",")
            output_file.write(str(repo.total_received()) + ",")
            output_file.write(str(repo.total_sent()) + "\n")
