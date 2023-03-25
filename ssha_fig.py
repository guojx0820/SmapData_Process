import netCDF4 as nc
from matplotlib.colors import LinearSegmentedColormap as LSColormap
from matplotlib import cm
import os
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


# np.set_printoptions(threshold=np.inf)
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
    print(normal_value, data_min, data_mean, data_max, sep='\n')
    return data_min, data_mean, data_max


def cycle_data_read(file_list):
    lon_all = []
    lat_all = []
    ssha_all = []
    for file_name in file_list:
        if file_name.endswith(postfix):
            # print(file_name)
            input_data = input_path + file_name
        dataset = nc.Dataset(input_data)
        # print(dataset)
        lon = dataset.variables['lon'][:]
        lat = dataset.variables['lat'][:]
        ssha = dataset.variables['ssha'][:]
        # (ssha[np.where((ws >= 1)]) = 10 * (ws[np.where((ws > 0) & (ws <= 250))]) + 50
        ssha[np.where(ssha >= 3)] = 0.
        # print(ssha)
        lon_all = np.append(lon_all, lon)
        lat_all = np.append(lat_all, lat)
        ssha_all = np.append(ssha_all, ssha)
    # print(ssha_all, ssha_all.shape)
    ssha_min, ssha_mean, ssha_max = min_mean_max(ssha_all)
    print(ssha_min, ssha_mean, ssha_max, sep='\n')
    return lon_all, lat_all, ssha_all


def draw_fig(lon_all, lat_all, ssha_all):
    fig, axes = plt.subplots(2, 1)
    axes[0].set_title('Sea Sursace Height Anomaly of 2011/12 (Unit:m)', fontsize=10)
    map = Basemap(projection='cyl', resolution='l', llcrnrlat=-30., urcrnrlat=30., llcrnrlon=60., urcrnrlon=301.,
                  ax=axes[0],
                  lon_0=-180.,
                  lat_0=0.)
    map.drawcoastlines(linewidth=0.25)
    map.drawstates(linewidth=0.25)
    map.fillcontinents(color='darkgray', lake_color='aqua')
    parallels = np.arange(-90., 91., 10)
    map.drawparallels(parallels, labels=[1, 0, 0, 0], fontsize=8, color='k', linewidth=0.5)
    meridians = np.arange(-180., 181., 30)
    map.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=8, color='k', linewidth=0.5)
    # rgb = colorbar()
    lx = np.arange(0., 360., 1)
    ly = np.arange(-90., 90., 1)
    X, Y = np.meshgrid(lx, ly)
    # ssha_all_mat = np.mat(ssha_all).T
    lat_all_mat = np.mat(lat_all).T
    lon_all_mat = np.mat(lon_all).T
    pos = np.concatenate([lon_all_mat, lat_all_mat], axis=1)
    # print(lon_all.shape, lat_all.shape, lon_all_mat.shape, lat_all_mat.shape, sep='\n')

    data = griddata(pos, ssha_all, (X, Y), method='linear')
    data_min, data_mean, data_max = min_mean_max(data)
    print(data, data.shape, data_min, data_mean, data_max, sep='\n')
    cmap_lev = np.linspace(-0.4, 0.4, 80)
    show_ssha = map.contourf(X, Y, data, 10, alpha=1.0, cmap=plt.cm.jet, levels=cmap_lev)
    show_curve = map.contour(X, Y, data, 10, colors='darkgray', linewidths=0.75)
    cbar = map.colorbar(show_ssha, 'bottom', ticks=np.arange(-0.4, 0.41, 0.05), pad='20%', format='%.2f')
    plt.clabel(show_curve, inline=True, fontsize=6, inline_spacing=3)
    # plt.xlabel('Sea Sursace Height Anomaly of 2015/12 (Unit:m)', labelpad=60)
    cbar.ax.tick_params(labelsize=8)
    plt.imshow(data)

    axes[1].set_title('Sea Sursace Temperature Anomaly of 2011/12 (Unit:K)', fontsize=10)
    map = Basemap(projection='cyl', resolution='l', llcrnrlat=-30., urcrnrlat=30., llcrnrlon=60., urcrnrlon=301.,
                  ax=axes[1],
                  lat_0=0,
                  lon_0=-180)
    map.drawmapboundary()
    map.fillcontinents(color='darkgray', lake_color='aqua')
    map.drawstates(linewidth=0.25)
    map.drawcoastlines(linewidth=0.25)
    map.drawmeridians(np.arange(-180., 181., 30.), labels=[0, 0, 0, 1], fontsize=8, color='k', linewidth=0.5)
    map.drawparallels(np.arange(-90., 91., 10.), labels=[1, 0, 0, 0], fontsize=8, color='k', linewidth=0.5)
    lx, ly = np.meshgrid(lon, lat)
    x, y = map(lx, ly)
    ssta_min, ssta_mean, ssta_max = min_mean_max(ssta)
    print(ssta_min, ssta_mean, ssta_max, sep='\n')
    cmap_lev = np.linspace(-4., 4., 80)
    show_ssta = map.contourf(x, y, ssta[251], 10, alpha=1.0, cmap=plt.cm.jet, levels=cmap_lev)
    show_curve = map.contour(x, y, ssta[251], 10, colors='darkgray', linewidths=0.75)
    cbar = map.colorbar(show_ssta, 'bottom', ticks=np.arange(-4., 4.1, 0.5), pad='20%', format='%.1f')
    plt.clabel(show_curve, inline=True, fontsize=6, inline_spacing=3)
    cbar.ax.tick_params(labelsize=8)
    # plt.xlabel('Sea Sursace Temperature Anomaly of 2015/12 (Unit:K)', labelpad=60)
    plt.imshow(ssta[251])

    # plt.contour(X, Y, data * 10000)
    plt.savefig(r'/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Img/ssha/201112.png', bbox_inches='tight',
                dpi=300)
    plt.show()


if __name__ == '__main__':
    postfix = '.nc'
    input_path = r'/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Data/Jason2/cycle128/'
    file_list = os.listdir(input_path)
    lon_all, lat_all, ssha_all = cycle_data_read(file_list)
    print(file_list)

    file = '/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Data/X222.195.148.75.342.1.52.22.nc'
    outputfile = '/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Img/Region/'
    dataset = nc.Dataset(file)
    print(dataset)
    lon = dataset.variables['lon'][:]
    lat = dataset.variables['lat'][:]
    sst = dataset.variables['sst'][:]
    # print(lon.shape, lat.shape, len(sst), sep='\n')
    ssta = anomaly_value(sst)
    # print(ssta, ssta.shape, sep='\n')
    draw_fig(lon_all, lat_all, ssha_all)
