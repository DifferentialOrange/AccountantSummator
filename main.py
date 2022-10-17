import decimal

from tkinter import Tk
from tkinter.filedialog import askopenfilename

import xmltodict


def to_eng_number(s):
    return s.replace(',', '.')

class Result():
    def __init__(self, category):
        self.category = category
        self.sum = 0
        self.count = 0
        self.examples = []
        self.examples_count = 10

    def __str__(self):
        return f"Выплаты для категории {self.category} " + \
               f"(первые {self.examples_count} выплат: " + \
               f"{', '.join(self.examples)}): сумма {self.sum}, " + \
               f"количество {self.count}"

    __repr__ = __str__

    def add(self, amount_str):
        if len(self.examples) < self.examples_count:
            self.examples.append(amount_str)

        amount = decimal.Decimal(to_eng_number(amount_str))

        self.sum = self.sum + amount
        self.count = self.count + 1

def compute(filename):
    xml_data = open(filename, 'r').read()
    xml_dict = xmltodict.parse(xml_data)
    elements = xml_dict['ns6:data']['package']['elements']['fact']
    
    result = {}    
    for el in elements:
        category = el['ns2:categoryId']
        if category not in result:
            result[category] = Result(category)

        amount_str = el['ns2:assignmentInfo']['ns2:monetaryForm']['ns2:amount']
        result[category].add(amount_str)

    return '\n'.join([str(item) for item in result.values()])

if __name__ == '__main__':
    Tk().withdraw()

    filetypes = (
        ('XML files', '*.xml'),
        ('All files', '*.*'),
    )

    filename = askopenfilename(filetypes=filetypes)
    print(compute(filename))
