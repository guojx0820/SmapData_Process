import numpy as np
import netCDF4 as nc
import os
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def anomaly_value(sst):
    # print(sst, sst.shape, sep='\n')
    sst_month_mean = np.mean(sst, 0)
    # print(sst_month_mean)
    ssta = sst - sst_month_mean
    # print(ssta, ssta.shape, sep='\n')
    return ssta


def min_mean_max(data):
    normal_value = data[np.where(data <= 3.) and np.where(data >= -6)]
    data_min = np.round(np.min(normal_value))
    data_mean = np.round(np.mean(normal_value))
    data_max = np.round(np.max(normal_value))
    # print(normal_value, data_min, data_mean, data_max, sep='\n')
    return data_min, data_mean, data_max


def ssta_ninoIndex(ssta):
    # print(ssta.shape)
    ssta_nino34 = ssta[226:322, 85:95, 190:240]
    ssta_nino12 = ssta[226:322, 90:100, 270:280]
    ssta_nino3 = ssta[226:322, 85:95, 210:270]
    ssta_nino4 = ssta[226:322, 85:95, 160:210]

    ssta_nino34_list = []
    ssta_nino12_list = []
    ssta_nino3_list = []
    ssta_nino4_list = []
    for i in range(len(ssta_nino34)):
        # print(nino34_region[i])
        ssta_nino34_mean = np.round(np.mean(ssta_nino34[i] * 100))
        ssta_nino12_mean = np.round(np.mean(ssta_nino12[i] * 100))
        ssta_nino3_mean = np.round(np.mean(ssta_nino3[i] * 100))
        ssta_nino4_mean = np.round(np.mean(ssta_nino4[i] * 100))
        ssta_nino34_list.append(ssta_nino34_mean)
        ssta_nino12_list.append(ssta_nino12_mean)
        ssta_nino3_list.append(ssta_nino3_mean)
        ssta_nino4_list.append(ssta_nino4_mean)
    # print(ssta_nino34_list, len(ssta_nino34_list), sep='\n')
    return ssta_nino34_list, ssta_nino12_list, ssta_nino3_list, ssta_nino4_list


def cycle_data_read(file_list):
    lon_all = []
    lat_all = []
    ssha_all = []
    for f in file_list:
        if f.endswith(postfix):
            # print(file_name)
            input_data = file_path + f
        dataset = nc.Dataset(input_data)
        # print(dataset)
        lon = dataset.variables['lon'][:]
        lat = dataset.variables['lat'][:]
        ssha = dataset.variables['ssha'][:]
        # (ssha[np.where((ws >= 1)]) = 10 * (ws[np.where((ws > 0) & (ws <= 250))]) + 50
        ssha[np.where(ssha >= 10)] = 0.
        # print(ssha)
        lon_all = np.append(lon_all, lon)
        lat_all = np.append(lat_all, lat)
        ssha_all = np.append(ssha_all, ssha)
    ssha_min, ssha_mean, ssha_max = min_mean_max(ssha_all)
    # print(ssha_min, ssha_mean, ssha_max, sep='\n')
    # ssha_all[np.where(ssha_all >= 10.)] = ssha_min
    # print(ssha_all, ssha_all.shape)

    lx = np.arange(0., 360., 1)
    ly = np.arange(-90., 90., 1)
    X, Y = np.meshgrid(lx, ly)
    # ssha_all_mat = np.mat(ssha_all).T
    lat_all_mat = np.mat(lat_all).T
    lon_all_mat = np.mat(lon_all).T
    pos = np.concatenate([lon_all_mat, lat_all_mat], axis=1)
    # print(lon_all.shape, lat_all.shape, lon_all_mat.shape, lat_all_mat.shape, sep='\n')

    ssha_grid = griddata(pos, ssha_all, (X, Y), method='linear')
    data_min, data_mean, data_max = min_mean_max(ssha_grid)
    # print(ssha_grid, ssha_grid.shape, data_min, data_mean, data_max, sep='\n')
    return ssha_grid


def reg_plot(data_frame):
    sns.set(color_codes=True)
    np.random.seed(sum(map(ord, "regression")))
    print(data_frame[0:8])
    R34 = data_frame[0:8].corr()
    R12 = data_frame[8:16].corr()
    R3 = data_frame[16:24].corr()
    R4 = data_frame[24:32].corr()
    print('R-Region-Nino3.4：', R34)
    print('R-Region-Nino1+2：', R12)
    print('R-Region-Nino3：', R3)
    print('R-Region-Nino4：', R4)
    sns.lmplot(x="SSTA", y="SSHA", hue="Region Nino Index", palette='husl', data=data_frame, aspect=1.5,
               markers=['o', 'x', 's', 'D'], legend=True)
    plt.text(-3.0, 0.24, 'R-3.4 = ' + str(round(R34.SSHA.SSTA, 3)), color='r')
    plt.text(-3.0, 0.22, 'R-1+2 = ' + str(round(R12.SSHA.SSTA, 3)), color='r')
    plt.text(-3.0, 0.20, 'R-3 = ' + str(round(R3.SSHA.SSTA, 3)), color='r')
    plt.text(-3.0, 0.18, 'R-4 = ' + str(round(R4.SSHA.SSTA, 3)), color='r')
    plt.title('Regrassion of SSTA & SSHA for Different Nino Index Region - Nov.', fontsize=14, y=1.02)
    plt.xlabel('SSTA(K)')
    plt.ylabel('SSHA(m)')
    # plot.map_lower(corrfunc)
    plt.savefig(outputfile + 'Regrass11.png', dpi=300,
                bbox_inches='tight')
    plt.show()


if __name__ == '__main__':

    # SSHA data
    postfix = '.nc'
    file_fix = ['200811', '200911', '201011', '201111', '201211', '201311', '201411', '201511']
    input_path = '/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Data/Months/11/'
    input_list = os.listdir(input_path)
    ssha_nino34_list = []
    ssha_nino12_list = []
    ssha_nino3_list = []
    ssha_nino4_list = []
    for k in file_fix:
        for i in input_list:
            if i.startswith(k):
                file_path = input_path + i + '/'
                # print(file_path)
                file_list = os.listdir(file_path)
                print(file_list)
                ssha_grid = cycle_data_read(file_list)
                print(ssha_grid.shape)
                ssha_nino34 = ssha_grid[85:95, 190:240]
                ssha_nino12 = ssha_grid[90:100, 270:280]
                ssha_nino3 = ssha_grid[85:95, 210:270]
                ssha_nino4 = ssha_grid[85:95, 160:210]
                ssha_nino34_mean = np.round(np.mean(ssha_nino34 * 100))
                ssha_nino12_mean = np.round(np.mean(ssha_nino12 * 100))
                ssha_nino3_mean = np.round(np.mean(ssha_nino3 * 100))
                ssha_nino4_mean = np.round(np.mean(ssha_nino4 * 100))
                # print(ssha_nino34_mean)
                ssha_nino34_list.append(ssha_nino34_mean)
                ssha_nino12_list.append(ssha_nino12_mean)
                ssha_nino3_list.append(ssha_nino3_mean)
                ssha_nino4_list.append(ssha_nino4_mean)
    # print(ssha_nino34_list, ssha_nino12_list, ssha_nino3_list, ssha_nino4_list)
    ssha_nino_index = ssha_nino34_list + ssha_nino12_list + ssha_nino3_list + ssha_nino4_list
    print(ssha_nino_index)

    # SSTA Data
    file = '/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Data/X222.195.148.75.342.1.52.22.nc'
    outputfile = '/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Img/Regrassion/'
    dataset = nc.Dataset(file)
    # print(dataset)
    lon = dataset.variables['lon'][:]
    lat = dataset.variables['lat'][:]
    sst = dataset.variables['sst'][:]
    # print(lon.shape, lat.shape, len(sst), sep='\n')
    ssta = anomaly_value(sst)
    # print(ssta, ssta.shape, sep='\n')
    ssta_nino34_list, ssta_nino12_list, ssta_nino3_list, ssta_nino4_list = ssta_ninoIndex(ssta)
    # print(ssta_nino34_list, len(ssta_nino34_list))
    ssta_nino34_list1 = []
    ssta_nino12_list1 = []
    ssta_nino3_list1 = []
    ssta_nino4_list1 = []
    for n in range(0, len(ssta_nino34_list), 12):
        # print(ssta_nino34_list[n])
        ssta_nino34_list1.append(ssta_nino34_list[n])
        ssta_nino12_list1.append(ssta_nino12_list[n])
        ssta_nino3_list1.append(ssta_nino3_list[n])
        ssta_nino4_list1.append(ssta_nino4_list[n])
    # print(ssta_nino34_list1, ssta_nino12_list1, ssta_nino3_list1, ssta_nino4_list1, sep='\n')
    ssta_nino_index = ssta_nino34_list1 + ssta_nino12_list1 + ssta_nino3_list1 + ssta_nino4_list1
    print(ssta_nino_index, len(ssta_nino_index), sep='\n')
    region_list = ['Region-Nino3.4', 'Region-Nino3.4', 'Region-Nino3.4', 'Region-Nino3.4', 'Region-Nino3.4',
                   'Region-Nino3.4', 'Region-Nino3.4', 'Region-Nino3.4',
                   'Region-Nino1+2', 'Region-Nino1+2', 'Region-Nino1+2', 'Region-Nino1+2', 'Region-Nino1+2',
                   'Region-Nino1+2', 'Region-Nino1+2', 'Region-Nino1+2',
                   'Region-Nino3', 'Region-Nino3', 'Region-Nino3', 'Region-Nino3', 'Region-Nino3', 'Region-Nino3',
                   'Region-Nino3', 'Region-Nino3',
                   'Region-Nino4', 'Region-Nino4', 'Region-Nino4', 'Region-Nino4', 'Region-Nino4', 'Region-Nino4',
                   'Region-Nino4', 'Region-Nino4']
    x = np.array(ssta_nino_index) / 100.
    y = np.array(ssha_nino_index) / 100.
    data_frame = pd.DataFrame({'SSTA': x,
                               'SSHA': y,
                               'Region Nino Index': region_list})
    print(data_frame)
    reg_plot(data_frame)
