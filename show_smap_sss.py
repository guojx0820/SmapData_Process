import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib as mpl
from matplotlib import cm
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap


# np.set_printoptions(threshold=np.inf)
def data_process(file):
    dataset = nc.Dataset(file)
    # print(dataset)
    lon = (dataset.variables['lon'][:])
    lat = (dataset.variables['lat'][:])
    sss = np.array(dataset.variables['sss_smap'][:])
    # sss[np.where(sss == -9999)] = 0
    sss[np.where(sss >= 0) and (sss < 33)] = 33
    sss[np.where(sss > 38)] = 38
    valid_values = np.where(sss > 0)
    sss_min = np.round(np.min(sss[valid_values]))
    sss_mean = np.round(np.mean(sss[valid_values]))
    sss_max = np.round(np.max(sss[valid_values]))
    print(sss[valid_values], sss_min, sss_mean, sss_max)
    # print(lon.shape, lat.shape, sss.shape)
    return lon, lat, sss


def draw_sss_fig(file):
    lon, lat, sss = data_process(file)
    lx, ly = np.meshgrid(lon, lat)
    # sss = np.flip(sss, 1)
    map = Basemap(projection='ortho', resolution='c',
                  lat_0=0, lon_0=l)
    map.drawmapboundary()
    map.fillcontinents(color='darkgray', lake_color='aqua')
    map.drawstates(linewidth=0.25)
    map.drawcoastlines(linewidth=0.25)
    map.drawmeridians(np.arange(-180., 181., 10.), labels=[0, 0, 0, 0], fontsize=12, linestyle='-.', color='k',
                      linewidth=0.5)
    map.drawparallels(np.arange(-90., 91., 10.), labels=[0, 0, 0, 0], fontsize=12, linestyle='-.', color='k',
                      linewidth=0.5)
    x, y = map(lx, ly)
    # plt.figure('Show SSS')
    lvls = np.linspace(33., 38., 300)
    show_sss = map.contourf(x, y, sss, alpha=1.0, cmap=plt.cm.turbo, levels=lvls)
    plt.imshow(sss)
    cbar = map.colorbar(show_sss, 'bottom', ticks=np.arange(33., 38.1, 1.0), format='%.1f', pad='10%')
    cbar.ax.tick_params(labelsize=12)
    font = {'weight': 'normal', 'size': 16}
    # plt.text('Center:(0,180)', fontsize=12, verticalalignment='bottom', horizontalalignment='center')
    plt.title('Global Sea Surface Salinity ' + j, font=font, y=1.02)
    plt.savefig(output_path + k + str(l) + '.jpg', dpi=600)
    plt.show()


if __name__ == '__main__':
    postfix = '.nc'
    # '2020_01', '2020_02', '2020_03', '2020_04', '2020_05', '2020_06', '2020_07', '2020_08', '2020_09',
    # '2020_10', '2020_11', '2020_12', '2021_01', '2021_02',
    prefix = ['2021_03', '2021_04', '2021_05', '2021_06',
              '2021_07', '2021_08', '2021_09']
    # 'Jan.2020', 'Feb.2020', 'Mar.2020', 'Apr.2020', 'May.2020', 'Jun.2020', 'Jul.2020', 'Aug.2020',
    # 'Sept.2020', 'Oct.2020', 'Nov.2020', 'Dec.2020', 'Jan.2021', 'Feb.2021',
title_list = ['Mar.2021', 'Apr.2021',
              'May.2021', 'Jun.2021', 'Jul.2021', 'Aug.2021', 'Sept.2021']
input_path = '/Users/leo/Desktop/MarineTechTest8/Data/'
output_path = '/Users/leo/Desktop/MarineTechTest8/Results/Img2/'
if not os.path.exists(output_path):
    os.mkdir(output_path)
file_list = os.listdir(input_path)
for k, j in zip(prefix, title_list):
    for i in file_list:
        if i.endswith(postfix) and i[24:].startswith(k):
            file = input_path + i
            for l in range(-180, 180, 10):
                print(file, l)
                # input_file = '/Users/leo/Desktop/MarineTechTest8/Data/RSS_smap_SSS_L3_monthly_2020_01_FNL_v04.0.nc'
                draw_sss_fig(file)
