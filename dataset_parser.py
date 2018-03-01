import os
from abc import ABCMeta

import numpy as np
import pandas as pd
import glob
STEPS = 3
CUR_STEP = 2

class DataserParser(metaclass=ABCMeta):

    def __init__(self, input_file, output_file):
        self.path = input_file#
        self.result = output_file#

        df = pd.read_csv(self.path, header=None, sep=" ")
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

        self.curr_pos = np.zeros((self.n_vehicles, 4), dtype=int)
        self.curr_pos[:, STEPS] = self.curr_pos[:, STEPS] + self.steps

    def start(self):
        rindex = 0
        print("rides {}".format(self.rides))
        # steps_remaining = self.steps
        while (np.sum(self.curr_pos[:, STEPS]) != 0) or rindex != self.rides:
            ride_assigned = False
            for v in range(self.n_vehicles):
                c = self.curr_pos[v, 0:2]
                s = self.ride_information[rindex, 0:2]
                f = self.ride_information[rindex, 2:4]
                distance = np.sum(np.abs(c - s) + np.abs(s - f))
                if self.curr_pos[v, CUR_STEP] < self.ride_information[rindex, 4]:
                    distance = self.ride_information[rindex, 4] - self.curr_pos[v, CUR_STEP]
                # print(c)
                # print(s)
                # print(f)
                # print(distance)
                if distance < self.curr_pos[v, STEPS]:
                    self.solution[v][0] += 1
                    self.solution[v].append(self.ride_index[rindex])
                    self.curr_pos[v, 0:2] = self.ride_information[rindex, 2:4]
                    self.curr_pos[v, CUR_STEP] += distance
                    self.curr_pos[v, STEPS] -= distance
                    rindex +=1
                    ride_assigned=True

            if not ride_assigned:
                rindex+=1

            if rindex == self.rides:
                break
        print(self.solution)
        print(self.curr_pos)
    def save_solution(self):
        file = open(self.result, 'w')
        for k,v in self.solution.items():
            myString = ' '.join([str(x) for x in v])
            myString = myString + "\n"
            file.write(myString)
        file.close()


if __name__ == '__main__':
    for file in glob.glob(os.path.join(os.getcwd(),"data","*.in")):
        output_file = file.replace(".in", ".out")
        print(output_file)
        dr = DataserParser(input_file=file, output_file=output_file)
        dr.start()
        dr.save_solution()
