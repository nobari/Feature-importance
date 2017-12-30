print(__doc__)

# Preliminaries
# Load pandas
import pandas as pd

# Input files
path_sur="Surroundings.json"
path_pos="sales_granular.csv"

# Loading the surroundings to a dataframe and fixing the index
pd_sur=pd.read_json(path_sur)
pd_sur.set_index('store_code',inplace=True)

# Counts the number of each feature
def atr2count(j):
    c={}
    for k in j.iterkeys():
        c[k]=len(j[k])
    return c

# For each POS quantitavely defines each of its features
pd_sur.surroundings=pd_sur.surroundings.map(atr2count)

# Expand each feature to a single column
pd_sur_sum=pd_sur.surroundings.apply(pd.Series)

# Make sure to have unique set of POSs while summing up its features for duplicates
pd_sur_uni_sum=pd_sur_sum.groupby('store_code').sum()

# Loading the pos transactions to a dataframe and fixing the index
pd_pos=pd.read_csv(path_pos,index_col='store_code')

# Aggregating all the transactions of each POS while fixing the type to Int64 just in case
pd_pos_sum = pd_pos.sum(axis=1)
pd_pos_sum = pd_pos_sum.astype(long)

# Make sure to have unique set of POSs while summing up its transactions for duplicates
# Renaming the column's name
pd_pos_uni_sum=pd.DataFrame(pd_pos_sum.groupby(['store_code']).sum())
pd_pos_uni_sum.rename(columns={0: 'purchase_count'}, inplace=True)
# DEBUG: pd_pos_uni_sum.purchase_count.sort_values(ascending=False)

# Joining the POS transactions & surroundings' features, this method lets the Nan to remain
pd_sum_missing=pd.concat([pd_sur_uni_sum,pd_pos_uni_sum],axis=1)
# Saving to a file for later use
pd_sum_missing.to_csv("sur_pos_all.csv")

# Joining the POS transactions & surroundings' features, this method only lets POS with Surroundings' feature to survive
pd_sum=pd_sur_uni_sum.join(pd_pos_uni_sum,how='inner')
pd_sum.purchase_count = pd_sum.purchase_count.astype(long)
# Saving to a file for later use
pd_sum.to_csv("sur_pos.csv")
