import re
import os
import os.path as op
import shutil

import pandas as pd


def fix_runs(layout):
    """Remove zero-padding from run numbers in a dataset.

    A common mistake in dataset preparation is to include leading zeros in run
    numbers (e.g., *_run-01_* instead of _run-1_*).

    Parameters
    ----------
    layout : bids.BIDSLayout
    """
    RUN_REGEX = r'(_run-)[0]+(\d+_)'
    RUN_OUT_REGEX = r'\1\2'

    # Rename contents of text files
    text_files = layout.get(extension=['json', 'tsv'])
    for f in text_files:
        with open(f, 'r') as fo:
            d = fo.read()
        d = re.sub(RUN_REGEX, RUN_OUT_REGEX, d)
        with open(f, 'w') as fo:
            fo.write(d)

    # Rename files
    files = layout.get()
    for f in files:
        out_fname = re.sub(RUN_REGEX, RUN_OUT_REGEX, f.path)
        os.rename(f.path, out_fname)


def merge_datasets(source_dset, target_dset, project_name, sub, ses=None):
    """Merge one BIDS dataset into another.

    Parameters
    ----------
    source_dset : str
        Path to existing BIDS directory. The contents of source_dset are merged
        into target_dset.
    target_dset : str
        Path to existing BIDS directory. The contents of source_dset are merged
        into target_dset.
    project_name : str
        Name of the project. This is used to update a "master scans file" in
        the project's code directory, which includes the new files and columns
        for annotating the scan quality and inclusion.
    sub : str
        Subject identifier.
    ses : str or None, optional
        Session identifier. Default is None.
    """
    dset_files = ['CHANGES', 'README', 'dataset_description.json',
                  'participants.tsv']
    for dset_file in dset_files:
        if not op.isfile(op.join(target_dset, dset_file)):
            shutil.copyfile(op.join(source_dset, dset_file),
                            op.join(target_dset, dset_file))

    new_participants_df = pd.read_csv(
        op.join(source_dset, 'participants.tsv'),
        sep='\t').T.drop_duplicates().T
    orig_participants_df = pd.read_csv(
        op.join(target_dset, 'participants.tsv'),
        sep='\t').T.drop_duplicates().T

    # Check if row already in participants file
    matches = new_participants_df[
        (new_participants_df == orig_participants_df.loc[0]).all(axis=1)
    ]
    match = matches.index.values.size
    if not match:
        new_participants_df = pd.concat(
            [new_participants_df, orig_participants_df])
        new_participants_df.to_csv(
            op.join(target_dset, 'participants.tsv'),
            sep='\t', line_terminator='\n', na_rep='n/a', index=False)
    else:
        print('Subject/session already found in participants.tsv')

    source_sub_dir = op.join(source_dset, 'sub-{0}'.format(sub))
    target_sub_dir = op.join(target_dset, 'sub-{0}'.format(sub))
    if not op.isdir(target_sub_dir):
        shutil.copytree(source_sub_dir, target_sub_dir)
    elif ses is not None:
        scratch_ses_dir = op.join(source_sub_dir, 'ses-{0}'.format(ses))
        out_ses_dir = op.join(target_sub_dir, 'ses-{0}'.format(ses))
        if not op.isdir(out_ses_dir):
            shutil.copytree(scratch_ses_dir, out_ses_dir)
        else:
            print('Warning: Subject/session directory '
                  'already exists in dataset. Skipping.')
    else:
        print('Warning: Subject directory already exists in dataset. '
              'Skipping.')

    scans_file = 'sub-{sub}_scans.tsv'.format(sub=sub)
    if ses:
        scans_file = 'ses-{ses}/sub-{sub}_ses-{ses}_scans.tsv'.format(
            sub=sub, ses=ses)
    sub_scans_df = pd.read_csv(
        op.join(target_sub_dir, scans_file),
        sep='\t')

    # append scans.tsv file with remove and annot fields
    sub_scans_df['remove'] = 0
    sub_scans_df['annotation'] = ''

    # import master scans file
    master_scans_file = op.join(
        op.dirname(target_dset),
        'code/{}_scans.tsv'.format(project_name))
    if op.isfile(master_scans_file):
        master_scans_df = pd.read_csv(master_scans_file, sep='\t')
        master_df_headers = list(master_scans_df)
        master_scans_df = master_scans_df.append(sub_scans_df)
        master_scans_df.to_csv(master_scans_file, sep='\t',
                               line_terminator='\n', index=False,
                               na_rep='n/a',
                               columns=master_df_headers)
    else:
        tmp_df_headers = list(sub_scans_df)
        sub_scans_df.to_csv(
            master_scans_file, sep='\t', line_terminator='\n',
            na_rep='n/a', index=False, columns=tmp_df_headers)
