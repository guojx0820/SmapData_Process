import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns


def reg_plot(data_frame):
    sns.set(color_codes=True)
    np.random.seed(sum(map(ord, "regression")))
    print(data_frame[0:12])
    R34 = data_frame[0:12].corr()
    R12 = data_frame[12:24].corr()
    R3 = data_frame[24:36].corr()
    R4 = data_frame[36:48].corr()
    print('R-Region-Nino3.4：', R34)
    print('R-Region-Nino1+2：', R12)
    print('R-Region-Nino3：', R3)
    print('R-Region-Nino4：', R4)
    sns.lmplot(x="SSTA", y="SSHA", hue="Region Nino Index", palette='husl', data=data_frame, aspect=1.5,
               markers=['o', 'x', 's', 'D'], legend=True)
    plt.text(-2.5, 0.28, 'R-3.4 = ' + str(round(R34.SSHA.SSTA, 3)), color='r')
    plt.text(-2.5, 0.26, 'R-1+2 = ' + str(round(R12.SSHA.SSTA, 3)), color='r')
    plt.text(-2.5, 0.24, 'R-3 = ' + str(round(R3.SSHA.SSTA, 3)), color='r')
    plt.text(-2.5, 0.22, 'R-4 = ' + str(round(R4.SSHA.SSTA, 3)), color='r')
    plt.title('Regrassion of SSTA & SSHA for Different Nino Index Region - Dec.', fontsize=14, y=1.02)
    plt.xlabel('SSTA(K)')
    plt.ylabel('SSHA(m)')
    # plot.map_lower(corrfunc)
    plt.savefig("/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Img/Regrassion/Regrass12.png", dpi=300,
                bbox_inches='tight')
    plt.show()


if __name__ == '__main__':
    ssha_nino_index = [-4.0, 16.0, -7.0, -4.0, 5.0, 4.0, 10.0, 18.0, 7.0, 4.0, 13.0, 11.0, -5.0, 8.0, -4.0, -4.0, -2.0,
                       3.0, 7.0, 17.0, 4.0, 2.0, 8.0, 4.0, -6.0, 13.0, -8.0, -5.0, 1.0, 4.0, 9.0, 20.0, 5.0, -1.0,
                       12.0, 8.0, 2.0, 11.0, -1.0, 2.0, 9.0, 6.0, 10.0, 9.0, 8.0, 9.0, 8.0, 13.0]
    ssta_nino_index = [-134.0, 121.0, -214.0, -156.0, -62.0, -56.0, 26.0, 230.0, -92.0, -129.0, 45.0, -2.0, -75.0, 2.0,
                       -166.0, -133.0, -100.0, -62.0, -25.0, 190.0, 19.0, -166.0, 41.0, 2.0, -134.0, 73.0, -244.0,
                       -173.0, -102.0, -84.0, 1.0, 205.0, -116.0, -188.0, 18.0, -46.0, -97.0, 102.0, -180.0, -130.0,
                       3.0, -4.0, 72.0, 146.0, -35.0, -46.0, 85.0, 84.0]
    region_list = ['Region-Nino3.4', 'Region-Nino3.4', 'Region-Nino3.4', 'Region-Nino3.4', 'Region-Nino3.4',
                   'Region-Nino3.4', 'Region-Nino3.4', 'Region-Nino3.4', 'Region-Nino3.4', 'Region-Nino3.4',
                   'Region-Nino3.4', 'Region-Nino3.4',
                   'Region-Nino1+2', 'Region-Nino1+2', 'Region-Nino1+2', 'Region-Nino1+2', 'Region-Nino1+2',
                   'Region-Nino1+2', 'Region-Nino1+2', 'Region-Nino1+2', 'Region-Nino1+2', 'Region-Nino1+2',
                   'Region-Nino1+2', 'Region-Nino1+2',
                   'Region-Nino3', 'Region-Nino3', 'Region-Nino3', 'Region-Nino3', 'Region-Nino3', 'Region-Nino3',
                   'Region-Nino3', 'Region-Nino3', 'Region-Nino3', 'Region-Nino3', 'Region-Nino3', 'Region-Nino3',
                   'Region-Nino4', 'Region-Nino4', 'Region-Nino4', 'Region-Nino4', 'Region-Nino4', 'Region-Nino4',
                   'Region-Nino4', 'Region-Nino4', 'Region-Nino4', 'Region-Nino4', 'Region-Nino4', 'Region-Nino4']
    x = np.array(ssta_nino_index) / 100.
    y = np.array(ssha_nino_index) / 100.
    data_frame = pd.DataFrame({'SSTA': x,
                               'SSHA': y,
                               'Region Nino Index': region_list})
    print(data_frame)
    reg_plot(data_frame)
