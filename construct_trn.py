import sys, os, getopt
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNetCV
from tqdm import tqdm


def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn


def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'm:e:w:')
    except getopt.GetoptError:
        print('Incorrect usage.')
        sys.exit(2) 
    for opt, arg in opts:
        if opt == '-m':
            global meta_file
            meta_file = arg
        elif opt == '-e':
            global exp_file
            exp_file = arg
        elif opt == '-w':
            global proj_dir
            proj_dir = arg
        

def construct_TRN(X, y_mat):
    targets = np.shape(y_mat)[1]
    coef_mat = np.empty([np.shape(X)[1], targets])
    for i in tqdm(range(targets), total = targets):
        y = y_mat[:, [i]]
        EN_model = ElasticNetCV(l1_ratio = 0.5, cv = 5)
        EN_model.fit(X, y)
        coef_mat[:, i] = EN_model.coef_
    return coef_mat


if __name__ == "__main__":

    main(sys.argv[1:])

    # read files
    metadata = pd.read_csv(meta_file, index_col = 0)
    exp_df = pd.read_csv(exp_file, index_col = 0)
    degs = np.loadtxt(proj_dir + '/degs.txt', dtype = str)
    tfs = np.loadtxt(proj_dir + '/selected_tfs.txt', dtype = str)

    # log transform and scale
    exp = np.log2(exp_df + 1).to_numpy()
    norm_exp = StandardScaler().fit(exp).transform(exp)

    # find indices of tf columns
    mask_tfs = [ (gene in tfs) for gene in exp_df.columns ]
    ind_tfs = np.where(mask_tfs)[0]

    # remove any tfs from degs (no self-edges)
    targets = [ gene for gene in degs if gene not in tfs ]

    # find indices of target columns
    mask_targets = [ (gene in targets) for gene in exp_df.columns ]
    ind_targets = np.where(mask_targets)[0]

    # save lists of TFs and targets to accompany output TRNs
    ordered_tfs = exp_df.columns[ind_tfs].to_list()
    ordered_targets = exp_df.columns[ind_targets].to_list()
    np.savetxt(proj_dir + '/trn_ordered_tfs.txt', ordered_tfs, fmt = '%s')
    np.savetxt(proj_dir + '/trn_ordered_target.txt', ordered_targets, fmt = '%s')

    # subset normalized expression matrix
    X = norm_exp[:, ind_tfs]
    y = norm_exp[:, ind_targets]

    # split expression into two groups
    groups = sorted(list(set(metadata.group.to_list())))
    if len(groups) != 2:
        print('Metadata file does not contain exactly 2 unique values in the "group" column!')
        if smode != 3:
            sys.exit(2)

    # get indices of samples
    ind_0 = np.where(metadata.group == groups[0])[0]
    ind_1 = np.where(metadata.group == groups[1])[0]

    # split X and y using indices
    X_0 = X[ind_0, :]
    y_0 = y[ind_0, :]
    X_1 = X[ind_1, :]
    y_1 = y[ind_1, :]

    # construct Elastic Net TRN
    trn_0 = construct_TRN(X_0, y_0)
    trn_1 = construct_TRN(X_1, y_1)

    # save TRNs
    np.save(proj_dir + '/trn_{}.npy'.format(groups[0]), trn_0)
    np.save(proj_dir + '/trn_{}.npy'.format(groups[1]), trn_1)

    print('TRN inference complete.')