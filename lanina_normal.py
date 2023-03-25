import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


def anomaly_value(sst):
    # print(sst, sst.shape, sep='\n')
    sst_month_mean = np.mean(sst, 0)
    # print(sst_month_mean)
    ssta = sst - sst_month_mean
    # print(ssta, ssta.shape, sep='\n')
    return ssta


def min_mean_max(data):
    data_min = np.round(np.min(data[i]))
    data_mean = np.round(np.mean(data[i]))
    data_max = np.round(np.max(data[i]))
    return data_min, data_mean, data_max


def draw_fig(lon, lat, ssta):
    fig, axes = plt.subplots(2, 1)

    axes[0].set_title('SSTA of 2000/' + str(i % 12 + 1) + ' La Nina')
    map = Basemap(projection='cyl', resolution='l', llcrnrlat=-30., urcrnrlat=30., llcrnrlon=60., urcrnrlon=301.,
                  ax=axes[0],
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
    show_ssta = map.contourf(x, y, ssta[i], 10, alpha=1.0, cmap=plt.cm.jet, levels=cmap_lev)
    show_curve = map.contour(x, y, ssta[i], 10, colors='darkgray', linewidths=0.75)
    # cbar = map.colorbar(show_ssta, 'bottom', ticks=np.arange(-4., 4.1, 0.5), pad='30%', format='%.1f')
    plt.clabel(show_curve, inline=True, fontsize=6, inline_spacing=3)
    plt.imshow(ssta[i])

    axes[1].set_title('SSTA of 2013/' + str(j % 12 + 1) + ' Normal Year')
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
    show_ssta = map.contourf(x, y, ssta[j], 10, alpha=1.0, cmap=plt.cm.jet, levels=cmap_lev)
    show_curve = map.contour(x, y, ssta[j], 10, colors='darkgray', linewidths=0.75)
    cbar = map.colorbar(show_ssta, 'bottom', ticks=np.arange(-4., 4.1, 0.5), pad='30%', format='%.1f')
    plt.clabel(show_curve, inline=True, fontsize=6, inline_spacing=3)
    plt.xlabel('Sea Sursace Temperature Anomaly(Unit:K)', labelpad=60)
    plt.imshow(ssta[j])
    plt.savefig(outputfile + '2000_2013_' + str(i % 12 + 1) + '.jpg', bbox_inches='tight', dpi=300)
    plt.show()


if __name__ == '__main__':
    file = '/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Data/X222.195.148.75.342.1.52.22.nc'
    outputfile = '/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Img/Region/'
    dataset = nc.Dataset(file)
    print(dataset)
    lon = dataset.variables['lon'][:]
    lat = dataset.variables['lat'][:]
    sst = dataset.variables['sst'][:]
    print(lon.shape, lat.shape, len(sst), sep='\n')
    ssta = anomaly_value(sst)
    for i, j in zip(range(108, 120, 11), range(264, 276, 11)):
        draw_fig(lon, lat, ssta)
        # break
