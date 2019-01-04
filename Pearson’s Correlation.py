from numpy.random import randn
from numpy.random import seed
from scipy.stats import pearsonr

data1 = [item[0] for item in DataSet]
data8 = [item[7] for item in DataSet]
# calculate Pearson's correlation


corr, _ = pearsonr(data1, data8)
print('Pearsons correlation: %.3f' % corr)



# N = []
# for l in l1:
#     y = [float(x) for x in l[0].split(';')]
#     N.append(y[3])
#
# n_high = max(N)
# n_low = min(N)
#
# for i in range(len(N)):
#     N[i] = (2 * (N[i] - n_low) / (n_high - n_low)) - 1
