import sys, getopt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import kneed


def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

    
def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'e:w:')
    except getopt.GetoptError:
        print('Incorrect usage.')
        sys.exit(2) 
    for opt, arg in opts:
        if opt == '-e':
            global exp_file
            exp_file = arg
        elif opt == '-w':
            global proj_dir
            proj_dir = arg


if __name__ == "__main__":

    main(sys.argv[1:])

    # read expression file
    exp_df = pd.read_csv(exp_file, index_col = 0)

    # read TF set
    all_tfs = np.loadtxt('./data/all_human_tfs.txt', dtype = str)

    # get list of TFs in expression data
    tfs_in_data = [ gene for gene in exp_df.columns if gene in all_tfs ]
        
    # subset expression data
    subset = exp_df[tfs_in_data].values
        
    # calculate variance for each tf
    variance = np.var(subset, axis = 0)

    # make a dataframe and sort the tfs by decreasing variance
    var_df = pd.DataFrame(columns = ['tf', 'variance'])
    var_df.tf = tfs_in_data
    var_df.variance = variance
    var_df.sort_values(by = 'variance', ascending = False, inplace = True)
    var_df.reset_index(inplace = True, drop = True)
    
    # use the automatic knee point method to select TFs if there are many
    if len(tfs_in_data) > 40:

        # max method
        kl = kneed.KneeLocator(var_df.index, var_df.variance, curve = 'convex', direction = 'decreasing')
        max_y = max(kl.y_difference)
        max_i = np.where(kl.y_difference == max_y)[0][0]
        max_x = kl.x_difference[max_i]

        # scale back to original
        x_cutoff = round((len(var_df)-1) * max_x)
        y_cutoff = var_df.variance.values[x_cutoff]

        # save TF list
        selected_tfs = var_df.tf.to_list()[:x_cutoff+1]
        np.savetxt(proj_dir + '/selected_tfs.txt', selected_tfs, fmt = '%s')

        # save plots
        x_max_lim = x_cutoff + 1
        if 2 * x_cutoff < len(kl.x):
            x_max_lim = 2 * x_cutoff

        fig, ax = plt.subplots(figsize = (6, 4))
        ax.plot(kl.x[:x_max_lim], kl.y[:x_max_lim], color = 'k')
        ax.vlines(x_cutoff, 0, var_df.variance.max(), linestyles = "--", colors = 'r')
        ax.hlines(y_cutoff, 0, x_max_lim, linestyles = "--", colors = 'r')
        ax.set_ylabel('variance')
        ax.set_xlabel('TF by rank')
        fig.savefig(proj_dir + '/ranked_tf_variance_with_cutoff.pdf', bbox_inches = 'tight')

        fig, ax = plt.subplots(figsize = (6, 4))
        ax.plot(kl.x[:x_max_lim], np.log1p(kl.y[:x_max_lim]), color = 'k')
        ax.vlines(x_cutoff, 0, np.log1p(var_df.variance.max()), linestyles = "--", colors = 'r')
        ax.hlines(y_cutoff, 0, x_max_lim, linestyles = "--", colors = 'r')
        ax.set_ylabel('log1p(variance)')
        ax.set_xlabel('TF by rank')
        fig.savefig(proj_dir + '/ranked_tf_variance_with_cutoff_log.pdf', bbox_inches = 'tight')

    else:

        # save TF list
        np.savetxt(proj_dir + '/selected_tfs.txt', var_df.tf.to_list(), fmt = '%s')

        # save plot
        fig, ax = plt.subplots(figsize = (6, 4))
        ax.plot(var_df.index, var_df.variance, color = 'k')
        ax.set_ylabel('variance')
        ax.set_xlabel('TF by rank')
        fig.savefig(proj_dir + '/ranked_tf_variance.pdf', bbox_inches = 'tight')
        
    print('TF selection complete.')