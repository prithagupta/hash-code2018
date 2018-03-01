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

        self.solution = dict()
        for v in range(self.n_vehicles):
            self.solution[v] = [0]

        self.curr_pos = np.zeros((self.n_vehicles, 3), dtype=int)
        self.curr_pos[:,2] = self.curr_pos[:,2] + self.steps

    def start(self):
        while(np.sum(self.curr_pos[:,3]) == 0 ):

            i =  0
            for v in range(self.n_vehicles):
                self.solution[v][0]+=1
                self.n_vehicles[v].append(self.ride_index[i])
                self.ride_information



if __name__ == '__main__':
    dr = DataserParser()
    print(dr.curr_pos)
    print(dr.ride_information)
    print(dr.ride_index)
