from Persistence import repo
from Orders_Execution import _OrderExecution
import sys


def main(args):
    config = args[1]
    orders = args[2]
    output = args[3]
    repo.create_tables()
    repo.config_decode(config)
    print("before orders execution:")
    repo.print_all()
    orders_execute = _OrderExecution(orders, output)
    orders_execute.execute_orders()
    print("after orders execution:")
    repo.print_all()


if __name__ == '__main__':
    main(sys.argv)
