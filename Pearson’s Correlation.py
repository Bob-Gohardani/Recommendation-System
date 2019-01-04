from numpy.random import randn
from numpy.random import seed
from scipy.stats import pearsonr

data1 = [item[0] for item in DataSet]
data8 = [item[7] for item in DataSet]
# calculate Pearson's correlation


corr, _ = pearsonr(data1, data8)
print('Pearsons correlation: %.3f' % corr)

