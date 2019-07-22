import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_excel('/home/manan/Desktop/final_results.xlsx')


# Plot settings

plt.figure();
ax = plt.axes()
ax.xaxis.set_major_locator(plt.MaxNLocator(10))
ax.xaxis.set_minor_locator(plt.MaxNLocator(50))
ax.yaxis.set_major_locator(plt.MaxNLocator(10))
ax.yaxis.set_minor_locator(plt.MaxNLocator(50))
ax.xaxis.grid(True, which='minor')
ax.grid(which = 'major', linestyle='-', linewidth = 0.9, alpha=1.0)
ax.grid(which = 'minor', linestyle=':', linewidth = 0.6, alpha=0.8)

num = int(input('What do you want to keep constant \n1. Diameter \n2. Height\n'))
rows =[]
if num == 1:
    plt.xlabel('Height (mm)')
    dw = float(input('Enter the diameter in mm \n'))
    diameter = data.loc[:,'Diameter (mm)'].values
    for ind in range(len(diameter)):
        if diameter[ind] == dw:
            rows.append(ind)
    x = [data.loc[rows[i]][0] for i in range(len(rows))]
    th = [data.loc[rows[i]][2] for i in range(len(rows))]
    exp1c = [data.loc[rows[i]][4] for i in range(len(rows))]
    exp1co = [data.loc[rows[i]][5] for i in range(len(rows))]
    exp2c = [data.loc[rows[i]][6] for i in range(len(rows))]
    exp2co = [data.loc[rows[i]][7] for i in range(len(rows))]
    exp = [data.loc[rows[i]][11] for i in range(len(rows))]

    plt.scatter(x,th,label='theoretical')
    plt.scatter(x,exp,label='experimental average')
    plt.scatter(x,exp1c,label='experimental 1 center')
    plt.scatter(x,exp1co,label='experimental 1 corner')
    plt.scatter(x,exp2c,label='experimental 2 center')
    plt.scatter(x,exp2co,label='experimental 2 corner')
    plt.title('dT/dt with Height at constant Diameter of ' + str(dw) +' mm')
    plt.legend(loc = 'upper right')
    plt.ylabel('dT/dt')
    plt.show()

elif num == 2:
    plt.xlabel('Diameter (mm)')
    lw = float(input('Enter the height in mm \n'))
    height = data.loc[:,'Height (mm)'].values
    for ind in range(len(height)):
        if height[ind] == lw:
            rows.append(ind)
    x = [data.loc[rows[i]][1] for i in range(len(rows))]
    th = [data.loc[rows[i]][2] for i in range(len(rows))]
    exp1c = [data.loc[rows[i]][4] for i in range(len(rows))]
    exp1co = [data.loc[rows[i]][5] for i in range(len(rows))]
    exp2c = [data.loc[rows[i]][6] for i in range(len(rows))]
    exp2co = [data.loc[rows[i]][7] for i in range(len(rows))]
    exp = [data.loc[rows[i]][11] for i in range(len(rows))]

    plt.plot(x,th,label='theoretical')
    plt.scatter(x,exp,label='experimental average')
    plt.scatter(x,exp1c,label='experimental 1 center')
    plt.scatter(x,exp1co,label='experimental 1 corner')
    plt.scatter(x,exp2c,label='experimental 2 center')
    plt.scatter(x,exp2co,label='experimental 2 corner')
    plt.title('dT/dt with Diameter at constant Height of ' + str(lw) +' mm')
    plt.legend(loc = 'upper right')
    plt.ylabel('dT/dt')
    plt.show()
