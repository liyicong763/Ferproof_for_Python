import matplotlib.pyplot as plt
from pylab import * #支持中文
def paint(y1, y2,y3):
    plt.figure(figsize=(7.5,8))
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 18}
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 17}
    x = []
    for i in range(len(y1)):
        x.append(i)
    #plt.plot(x, y, 'ro-')
    #plt.plot(x, y1, 'bo-')
    #pl.xlim(-1, 11)  # 限定横轴的范围
    #list = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
    plt.ylim(0,700)  # 限定纵轴的范围
    plt.yticks(size=18)

    plt.plot(x, y1, color="red", label=u'prove time')
    plt.plot(x, y2, color="blue", label=u'verify time')
    # plt.plot(x, y3, color="green", label=u'numSquares time')
    # plt.plot(x, y3, color="green", label=u'numSquares time')
    plt.legend(prop=font1)  # 让图例生效
    plt.xticks(x, x, rotation=0, size=18)
    plt.margins(0)
    #plt.subplots_adjust(bottom=0.15)
    plt.xlabel(u"Number of samples (Increasing problem size)", fontdict=font2, fontsize=23)  # X轴标签
    plt.ylabel(u"time(ms)", fontdict=font2, fontsize=23)  # Y轴标签
    plt.title("Ferproof", fontdict=font2, fontsize=28)  # 标题
    ax = plt.gca()
    x_major_locator = MultipleLocator(40)
    # 把x轴的刻度间隔设置为1，并存在变量里
    y_major_locator = MultipleLocator(50)
    # 把y轴的刻度间隔设置为10，并存在变量里
    ax.xaxis.set_major_locator(x_major_locator)
    # 把x轴的主刻度设置为1的倍数
    ax.yaxis.set_major_locator(y_major_locator)
    # 把y轴的主刻度设置为10的倍数
    plt.xlim(0, 400)
    # 把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
    plt.ylim(0, 550)
    # 把y轴的刻度范围设置为-5到110，同理，-5不会标出来，但是能看到一点空白
    ax.grid(linestyle='--', linewidth=.5, color='.25', zorder=0)
    novel_resut = str(time.time())
    plt.rcParams['savefig.dpi'] = 2048  # 图片像素
    plt.rcParams['figure.dpi'] = 2048  # 分辨率
    plt.savefig('result/img/' + novel_resut + '.jpg')
    plt.show()

def bullet_paint(y1, y2,y3):
    plt.figure(figsize=(7.5,8))
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 18}
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 17}
    x = []
    for i in range(len(y1)):
        x.append(i)
    #plt.plot(x, y, 'ro-')
    #plt.plot(x, y1, 'bo-')
    #pl.xlim(-1, 11)  # 限定横轴的范围
    #list = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
    #plt.ylim(0,700)  # 限定纵轴的范围
    plt.yticks(size=18)

    plt.plot(x, y1, color="red", label=u'prove time')
    plt.plot(x, y2, color="blue", label=u'verify time')
    # plt.plot(x, y3, color="green", label=u'numSquares time')
    # plt.plot(x, y3, color="green", label=u'numSquares time')
    plt.legend(prop=font1)  # 让图例生效
    plt.xticks(x, x, rotation=0, size=18)
    plt.margins(0)
    #plt.subplots_adjust(bottom=0.15)
    plt.xlabel(u"Number of samples (Increasing problem size)", fontdict=font2, fontsize=23) #X轴标签
    plt.ylabel(u"time(ms)", fontdict=font2, fontsize=23) #Y轴标签
    plt.title("Bulletproofs", fontdict=font2, fontsize=28) #标题
    ax = plt.gca()
    x_major_locator = MultipleLocator(40)
    # 把x轴的刻度间隔设置为1，并存在变量里
    y_major_locator = MultipleLocator(400)
    # 把y轴的刻度间隔设置为10，并存在变量里
    ax.xaxis.set_major_locator(x_major_locator)
    # 把x轴的主刻度设置为1的倍数
    ax.yaxis.set_major_locator(y_major_locator)
    # 把y轴的主刻度设置为10的倍数
    plt.xlim(0, 400)
    # 把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
    plt.ylim(0, 5000)
    # 把y轴的刻度范围设置为-5到110，同理，-5不会标出来，但是能看到一点空白
    ax.grid(linestyle='--', linewidth=.5, color='.25', zorder=0)
    novel_resut = str(time.time())
    plt.rcParams['savefig.dpi'] = 2048  # 图片像素
    plt.rcParams['figure.dpi'] = 2048  # 分辨率
    plt.savefig('result/img/' + novel_resut + '.jpg')
    plt.show()

#paint([1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6], [1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6],[1,2,3,4,5,6])
def time_paint(y1, y2):
    plt.figure(figsize=(7, 7.5))
    mpl.rcParams['font.sans-serif'] = ['SimHei']
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 17}
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 17}
    x = []
    for i in range(len(y1)):
        x.append(i)
    #plt.plot(x, y, 'ro-')
    #plt.plot(x, y1, 'bo-')
    #pl.xlim(-1, 11)  # 限定横轴的范围
    #list = [0, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600]
    #plt.ylim(0,700)  # 限定纵轴的范围
    plt.yticks(size=15)

    plt.plot(x, y1, color="red", label=u'1 time')
    plt.plot(x, y2, color="blue", label=u'2 time')
    #plt.scatter(x, y1, color="red", marker='.')
    #plt.scatter(x, y2, color="blue", marker='.')
    # plt.plot(x, y3, color="green", label=u'numSquares time')
    # plt.plot(x, y3, color="green", label=u'numSquares time')
    plt.legend(prop=font1)  # 让图例生效
    plt.xticks(x, x, rotation=0, size=15)
    plt.margins(0)
    #plt.subplots_adjust(bottom=0.15)
    plt.xlabel(u"Number of samples", fontdict=font2) #X轴标签
    plt.ylabel(u"time(ms)", fontdict=font2) #Y轴标签
    plt.title("Bulletproofs", fontdict=font2) #标题
    ax = plt.gca()
    # x_major_locator = MultipleLocator(40)
    # 把x轴的刻度间隔设置为1，并存在变量里
    # y_major_locator = MultipleLocator(400)
    # 把y轴的刻度间隔设置为10，并存在变量里
    # ax.xaxis.set_major_locator(x_major_locator)
    # 把x轴的主刻度设置为1的倍数
    # ax.yaxis.set_major_locator(y_major_locator)
    # 把y轴的主刻度设置为10的倍数
    #plt.xlim(0, 400)
    # 把x轴的刻度范围设置为-0.5到11，因为0.5不满一个刻度间隔，所以数字不会显示出来，但是能看到一点空白
    plt.ylim(-100)
    # 把y轴的刻度范围设置为-5到110，同理，-5不会标出来，但是能看到一点空白
    # ax.grid(linestyle='--', linewidth=.5, color='.25', zorder=0)
    novel_resut = str(time.time())
    # plt.rcParams['savefig.dpi'] = 2048  # 图片像素
    # plt.rcParams['figure.dpi'] = 2048  # 分辨率
    # plt.savefig('result/img/' + novel_resut + '.jpg')
    plt.show()