import MES_Webshop
import MES_Shopfloor
import MES_Analytics
import os
import json
import glob
import time

class MES:
    def __init__(self):
        print(os.getcwd())
        os.chdir('../')
        os.makedirs(os.path.join(os.getcwd(),'Datasheet'), exist_ok=True)
        os.chdir('MES')
        self.orders = MES_Webshop.GetOrders()
        self.list_of_orders = []
        self.move_to_MES_from_orders()
        self.uncraftable = [ 'metal', 'heater', 'motor', 'copper wire',
                             'cpu', 'board', 'LCD', 'pneumatical pump',
                             'small blade', 'handle','blade']
    def move_to_MES_from_orders(self):
        os.chdir('../')
        os.chdir('MES')
        os.chdir('datasheet')
    def move_to_datasheet(self):
        os.chdir('../')
        os.chdir('../')
        os.chdir('Datasheet')
    def move_to_MES_from_datasheet(self):
        os.chdir('../')
        os.chdir('MES')
        os.chdir('datasheet')
    def update(self):
        self.orders = MES_Webshop.GetOrders()

    def ProcessingOrders(self):
        for item in self.orders:
            with open(item,'r') as f:
                data = json.load(f)
                print(f"Processing order with ID: {data['UID']}...")
                self.list_of_orders.append(data)
                self.GetProductFromOrder(data)
    def GetProductFromOrder(self, data: dict):
        self.index = 0
        for product in data['Products']:
            if self.GetStock(product) != 0:
                self.GenerateDatasheet(self.index, data['UID'], product)
    def GenerateDatasheet(self, index, uid, product):
        print(f"Generating Datasheet for product: {product} in order {uid}...")
        time.sleep(2)
        path = os.getcwd()
        file_searcher = glob.glob(os.path.join(path, "*.txt"))
        for file in file_searcher:
            if os.path.basename(file) == (product + '.txt'):
                data = {"UID":f'{uid}', "steps": '', 'materials' : [] }
                with open(os.path.basename(file),'r') as f:
                    list_of_steps = f.read().split(',')
                    for i in range(len(list_of_steps)):
                        if list_of_steps[i][0] == ' ':
                            list_of_steps[i] = list_of_steps[i][1:]
                    self.move_to_datasheet()
                    os.makedirs(os.path.join(os.getcwd(),uid), exist_ok=True)
                    os.chdir(f"{uid}")
                    self.index += 1
                    with open(f"ds_{uid}_{index}.txt",'w') as g:
                        for part in list_of_steps:
                            os.chdir("../")
                            self.move_to_MES_from_datasheet()
                            with open("components.txt", 'r') as h:
                                json_data = json.load(h)
                                item = part.split(' ')
                                if len(item) == 2 and item[1] not in self.uncraftable:
                                    for i in json_data[f"{item[1]}"]:
                                        data['materials'].append(i)
                                elif len(item) == 3:
                                    data['steps'] += f"do {item[1]} {item[2]}, "
                                    for i in json_data[f"{item[1]} {item[2]}"]:
                                        data['materials'].append(i)
                                elif len(item) == 2 and item[1] in self.uncraftable:
                                    data['materials'].append(f"{item[0]} {item[1]}")
                        data['steps'] += f'assembly {product}'
                        print("Datasheet generated successfully.")
                        print()
                        MES_Shopfloor.SendDatasheet()
                        MES_Analytics.SendDatasheet()
                        time.sleep(2)
                        json.dump(data,g)
                        print("Datasheet sent successfully.")
                        print()

                    os.chdir("../")
                    self.move_to_MES_from_datasheet()
    def GetStock(self, item):
        return MES_Analytics.AskForItem(item)