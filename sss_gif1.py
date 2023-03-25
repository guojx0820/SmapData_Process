import imageio, os
import moviepy.editor as mp

def create_gif(image_list, gif_name, duration):
    frames = []
    for image_name in image_list:
        frames.append(imageio.imread(image_name))
    imageio.mimsave(gif_name, frames, 'GIF', duration=duration)
    return


def main():
    postfix = '.jpg'
    postfix1 = 'Global_SSS_All2.gif'
    prefix = ['2020_01170',  '2020_02170',
                             '2020_02160',  '2020_03160',
                                            '2020_03150',  '2020_04150',
                                                           '2020_04140',  '2020_05140',
                                                                          '2020_05130',  '2020_06130',
                                                                                         '2020_06120',  '2020_07120',
                                                                                                        '2020_07110',  '2020_08110',
                                                                                                                       '2020_08100',  '2020_09100',
                                                                                                                                      '2020_0990',   '2020_1090',
                                                                                                                                                     '2020_1080',   '2020_1180',
                                                                                                                                                                    '2020_1170',   '2020_1270',
                                                                                                                                                                                   '2020_1260',   '2021_0160',
                                                                                                                                                                                                  '2021_0150',   '2021_0250',
                                                                                                                                                                                                                 '2021_0240',   '2021_0340',
                                                                                                                                                                                                                                '2021_0330',   '2021_0430',
                                                                                                                                                                                                                                               '2021_0420',   '2021_0520',
                                                                                                                                                                                                                                                              '2021_0510.',  '2021_0610.',
                                                                                                                                                                                                                                                                             '2021_060',    '2021_070',
                                                                                                                                                                                                                                                                                            '2021_07-10.', '2021_08-10.',
                                                                                                                                                                                                                                                                                                           '2021_08-20',  '2021_09-20',

              '2020_01-30',  '2020_02-30',
                             '2020_02-40',  '2020_03-40',
                                            '2020_03-50',  '2020_04-50',
                                                           '2020_04-60',  '2020_05-60',
                                                                          '2020_05-70',  '2020_06-70',
                                                                                         '2020_06-80',  '2020_07-80',
                                                                                                        '2020_07-90',  '2020_08-90',
                                                                                                                       '2020_08-100', '2020_09-100',
                                                                                                                                      '2020_09-110', '2020_10-110',
                                                                                                                                                     '2020_10-120', '2020_11-120',
                                                                                                                                                                    '2020_11-130', '2020_12-130',
                                                                                                                                                                                   '2020_12-140', '2021_01-140',
                                                                                                                                                                                                  '2021_01-150', '2021_02-150',
                                                                                                                                                                                                                 '2021_02-160', '2021_03-160',
                                                                                                                                                                                                                                '2021_03-170', '2021_04-170',
                                                                                                                                                                                                                                               '2021_04-180', '2021_05-180', '2021_06-180', '2021_07-180', '2021_08-180', '2021_09-180']
    input_directory = '/Users/leo/Desktop/MarineTechTest8/Results/Img2/'
    output_directory = '/Users/leo/Desktop/'
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    file_list = os.listdir(input_directory)
    path_list = []
    sum = 0
    for k in prefix:
        for i in file_list:
            if i.endswith(postfix) and i[0:].startswith(k):
                sum += 1
                print(sum, k, i)
                file_path = input_directory + i
                # print(file_path)
                path_list.append(file_path)

    print(path_list)

    gif_path = output_directory + postfix1
    duration = 0.5
    create_gif(path_list, gif_path, duration)


if __name__ == '__main__':
    main()
    vfc = mp.VideoFileClip("/Users/leo/Desktop/Global_SSS_All2.gif")
    vfc.write_videofile("/Users/leo/Desktop/Global_SSS_All2.mp4")
