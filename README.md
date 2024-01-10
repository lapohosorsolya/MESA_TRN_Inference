# Pipeline for TRN inference from bulk RNA-seq data

*Repository of custom scripts for the MESA collaboration*

Author: Orsolya Lapohos (orsolya.lapohos@mail.mcgill.ca)

## Contents

+ [Objective](#objective)
+ [Download](#download)
+ [Environment](#environment)
+ [Required Inputs](#required-inputs)
+ [Pipeline](#pipeline)
  + [1. TF Selection](#1-tf-selection)
  + [2. TRN Inference](#2-trn-inference)
  + [3. TRN Analysis](#3-trn-analysis)


## Objective

To infer relationships between TFs and target genes that may explain mechanisms
driving differences between two groups or phenotypes.

Detailed description of the method can be found [here](/docs/method_description.pdf).

## Download

First, enter the specific directory where you want to store this repository:

    cd <path to repo storage dir>

Then, clone this repository to your server or local machine using the following command:

    git clone https://github.com/lapohosorsolya/MESA_TRN_Inference

## Environment

To set up an environment compatible with the downstream scripts, run the following:

    bash setup.sh -e <new virtual environment directory>

This will create a new environment on the specified path, and then install the required packages.


## Required Inputs

You will need the following files/directories before running the scripts:

| File | Location | Format | Requirements |
| --- | --- | ------ | ------ |
| Metadata File | NA | Tabular (.csv) | Each row refers to one sample and each column refers to a sample variable. The first column must contain sample IDs. One column should be titled "group" and contain only 2 unique values that will be used to separate the samples.  |
| Expression File | NA | Tabular (.csv) | Gene length-normalized RNA-seq data. Each row refers to one sample and each column (except first) refers to an Ensembl gene ID. First column must contain sample IDs that match the metadata file. |
| DEG File | Project Directory * | List (.txt separated by newline) | Must be named `degs.txt`. Ensembl gene IDs of the differentially expressed genes between the two sample groups (as determined by prior analysis). Suggested FDR cutoff: 0.05. |

\* A **Project Directory** should be made prior to running the scripts:

    mkdir <path to new project directory>

Then, please place a copy of the DEG list file into this directory:

    cp <path to deg file> <path to new project directory>


## Pipeline

Before running the following scripts, make sure you are in the right directory.

    cd <path to repo storage dir>/MESA_TRN_Inference

### 1. TF Selection

This script is used to select a set of candidate TFs from the expression data.

#### Usage

    <path to virtual environment>/.venv/bin/python3 select_tfs.py -e <path to expression file> -w <path to project directory>

#### Output

| File | Location | Format | Properties |
| --- | --- | ------ | ------ |
| TF File | Project Directory | List (.txt separated by newline) | Ensembl gene IDs of the selected TFs. This will be used in the next script. |
| Ranked TF Variance Plot | Project Directory | PDF | Plot of variance vs. ranked TFs, with an indicator line showing the automatically chosen cutoff. *This plot should be examined before moving on to the next script.* |

----

### 2. TRN Inference

This script is used to infer TRNs for two phenotypes using the selected TFs and the provided DEGs.

#### Usage

    <path to virtual environment>/.venv/bin/python3 construct_trn.py -m <path to metadata file> -e <path to expression file> -w <path to project directory>

#### Output

| File | Location | Format | Properties |
| --- | --- | ------ | ------ |
| TRN 1 | Project Directory | Array (.npy) | Adjacency matrix of the TRN for group/phenotype #1. |
| TRN 2 | Project Directory | Array (.npy) | Adjacency matrix of the TRN for group/phenotype #2. |
| Ordered TF List | Project Directory | List (.txt separated by newline) | Ensembl gene IDs of the TFs in the order that matches adjacency matrix rows. |
| Ordered Target List | Project Directory | List (.txt separated by newline) | Ensembl gene IDs of the target genes in the order that matches adjacency matrix columns. |

----

### 3. TRN Analysis

Since the outputs of step 2 do not contain any patient-specific information, they can be shared via Box. TRNs will be plotted and analyzed as written in the Method Description.

