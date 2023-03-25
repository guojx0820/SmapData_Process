import numpy as np
import netCDF4 as nc
import os

# np.set_printoptions(threshold=np.inf)


if __name__ == '__main__':
    postfix = '.nc'
    file_fix = ['200812', '200912', '201012', '201112', '201212', '201312', '201412', '201512', '201612', '201712',
                '201812', '201912', '202012']
    input_path = '/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Data/Dec/'
    input_list = os.listdir(input_path)
    for k in file_fix:
        for i in input_list:
            if i.startswith(k):
                file_name = input_path + i + '/'
    print(file_name)
    # print(file_list)
