import numpy as np
#import matplotlib.pyplot as plt
import xlsxwriter
import glob

file_path = sorted(glob.glob('C:/MY_MCNP/MCNPINPUT/VTR/single_assembly/Material_Analysis/*mcta?'))
workbook = xlsxwriter.Workbook('Na_Loop.xlsx')
name = str(file_path)
name = name[-35:]

energy_array = np.zeros((3, 13))
start_read_erg = False
start_read = False
k=0
for i, f in enumerate(file_path):
    with open(file_path[i], 'r') as data:
        for line in data:
            if start_read_erg:
                temp = [x for x in line.split('  ')]
                if temp[0] == 't':
                    start_read_erg = False
                else:
                    for j, element in enumerate(temp):
                        if j>0:
                            energy_array[0][l] = temp[j]
                            l+=1
            if start_read:
                temp = [x for x in line.split('  ')]
                if temp[0] == 'tfc':
                    start_read = False
                    break
                else:
                    for j, element in enumerate(temp):
                        if j > 0:
                            mean = element[:11]
                            var = temp[12:]
                            energy_array[1][l] = element[:11]
                            energy_array[2][l] = element[12:]
                            l+=1
                            #print(mean, var)
            if 'et' in line:
                start_read_erg = True
                l = 0
            if 'vals' in line:
                start_read = True
                l = 0
    worksheet = workbook.add_worksheet()

    for row, data in enumerate(energy_array):
        worksheet.write_row(row, 0, data)


workbook.close()

#    plt.plot(energy_array[0][:-2], energy_array[1][:-2])
#    #plt.yscale('log')
#    plt.xscale('log')
##    plt.show()
 #   print(energy_array)


