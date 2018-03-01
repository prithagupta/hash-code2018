import pandas as pd
from abc import ABCMeta, abstractmethod
import os
import numpy as np
class DataserParser(metaclass=ABCMeta):

    def __init__(self):
        path = os.path.join(os.getcwd(),"data","a_example.in")#
        df = pd.read_csv(path, header=None, sep=" ")
        matrix = df.as_matrix()
        self.rows, self.cols, self.n_vehicles, self.rides, self.bonus, self.steps = matrix[0]
        self.ride_information = np.copy(matrix[1:,:])
        diff = (self.ride_information[:, 5] - self.ride_information[:, 4])[:,None]
        self.ride_information = np.append(self.ride_information, diff, axis=1)

        df = pd.DataFrame(self.ride_information, columns=list('abxysfd'))
        df = df.sort_values(['s', 'd'], ascending=[True, True])
        self.ride_information = df.as_matrix()
        self.ride_index = df.index.get_values()
        self.curr_pos = np.zeros((self.n_vehicles, 2), dtype=int)

    def start(self):
        for i in range(self.steps):
            pass

if __name__ == '__main__':
    dr = DataserParser()
    print(dr.curr_pos)
    print(dr.ride_information)
    print(dr.ride_index)
