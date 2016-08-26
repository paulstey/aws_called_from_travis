import pandas as pd
import sys
import urllib
import os


from tabulate import tabulate
from StringIO import StringIO


def get_number(filename):
    '''
    This is a simple function used to extract a single
    digit which appears in the file `filename`.
    '''
    f = open(filename, 'r')
    line = f.readline()
    res = line.rstrip()
    return res


def aws_download(linenum, df):
    '''
    Given a line number and dataframe, this downloads the "nt"
    and "aa" files from AWS. The line number specifies the row in the
    dataframe that has our genome of interest. Thus, `df` is just a
    lookup table for URLs.
    '''
    # get URLs and filenames
    nt_url = df.iloc[linenum, 2]
    aa_url = df.iloc[linenum, 3]
    nt_filename = nt_url[nt_url.rfind("/")+1::1]
    aa_filename = aa_url[aa_url.rfind("/")+1::1]

    # downloaded files to current dir
    nt_file = urllib.URLopener()
    nt_file.retrieve(nt_url, nt_filename)
    aa_file = urllib.URLopener()
    aa_file.retrieve(aa_url, aa_filename)

    return (nt_filename, aa_filename)


def run_assessments(nt_filename, aa_filename):
    os.system("python compare_nt2aa_bySeqID.py {0} {1} --to_stop 1 > /dev/null".format(nt_filename, aa_filename))


def write_results(nt_filename, aa_filename, df_results):
    '''
    This function writes the assessment results to (1) the .csv storing all
    previous runs, and (2) to STDOUT which allows us to pipe the results to
    the README.md file in this scripts caller.
    '''
    filename = os.path.basename(nt_filename).split("_")
    sp_name = "_".join(filename[0:2])
    mismatch_filename = sp_name + "_mismatch_ids.txt"

    # append row to results .csv file
    n = df_results.shape[0]
    num_missmatches = sum(1 for line in open(mismatch_filename))
    df_results.loc[n, :] = [sp_name, nt_filename, aa_filename, num_missmatches]
    df_results.to_csv("results_table.csv", index = False)

    print(tabulate(df_results, headers=["sp", "nt_filename", "aa_filename", "nt2aa_missmatches"], tablefmt='pipe'))


if __name__ == "__main__":
    input_file = sys.argv[1]
    num = get_number(input_file)

    df_urls = pd.read_csv("genome_urls.csv")
    df_results = pd.read_csv("results_table.csv")

    nt_filename, aa_filename = aws_download(int(num), df_urls)

    run_assessments(nt_filename, aa_filename)
    write_results(nt_filename, aa_filename, df_results)
