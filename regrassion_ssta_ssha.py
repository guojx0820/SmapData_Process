import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from matplotlib import font_manager


# 相关系数矩阵 r(相关系数) = x和y的协方差/(x的标准差*y的标准差) == cov（x,y）/σx*σy
# 相关系数0~0.3弱相关0.3~0.6中等程度相关0.6~1强相关

def regfun(data):
    X_train, X_test, Y_train, Y_test = train_test_split(data[:, 0:1], data[:, 1:2], train_size=.80)
    # print(X_train, Y_train)
    print("原始数据特征:", data[:, 0:1].shape,
          ",训练数据特征:", X_train.shape,
          ",测试数据特征:", X_test.shape)

    print("原始数据标签:", data[:, 1:2].shape,
          ",训练数据标签:", Y_train.shape,
          ",测试数据标签:", Y_test.shape)

    model = LinearRegression()
    model.fit(X_train, Y_train)

    a = model.intercept_  # 截距
    b = model.coef_  # 回归系数
    print("最佳拟合线:截距", a, ",回归系数：", b)
    return a, b


def plot_fig(data_frame):
    R34 = data_frame[0:12].corr()
    R12 = data_frame[12:24].corr()
    R3 = data_frame[24:36].corr()
    R4 = data_frame[36:48].corr()
    print('R-Region-Nino3.4：', R34)
    print('R-Region-Nino1+2：', R12)
    print('R-Region-Nino3：', R3)
    print('R-Region-Nino4：', R4)
    # R = data_frame.corr()
    # print('相关系数：', R)
    data_frame.head()
    sns.pairplot(data_frame, vars=['SSTA', 'SSHA'], hue='Region Nino Index',
                 kind='scatter', diag_kind='kde',
                 palette='husl',  # 设置调色板
                 markers='o',  # 设置不同系列的点样式（这里根据参考分类个数）
                 )

    plt.suptitle("Scatter of SSTA and SSHA - Dec.", y=1.02)
    # plt.text(0, 1, 'Y = ' + str(a1) + '* X +' + str(b1), color='red')
    # plt.text(112.8, 12, a)
    # plt.text(114.5, 12, "+")
    # plt.text(114.8, 12, b)
    # plt.text(115.8, 12, "X", color='red')
    # plt.text(0, 0, "R = " + str(R.SSHA.SSTA), color='red', transform=plt.transAxes)
    # # plt.text(113,10,R)
    plt.savefig("/Users/leo/Desktop/MarineTechTest9_EINino_LaNina/Img/Regrassion/pairplot_lo.png", dpi=300,
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
    # print(x, y, sep='\n')
    data1 = np.array([x, y]).T
    data2 = np.array([x, y]).T
    a1, b1 = regfun(data1)
    a2, b2 = regfun(data2)
    print(a1, b1, a2, b2, sep='\n')
    plot_fig(data_frame)
