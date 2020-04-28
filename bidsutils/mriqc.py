import os.path as op
import shutil
from glob import glob

import pandas as pd


def merge_mriqc_derivatives(source_dir, target_dir):
    """Merge MRIQC results into final derivatives folder.

    Parameters
    ----------
    source_dir : str
        Path to existing MRIQC derivatives folder. Files from source_dir are
        merged into target_dir.
    target_dir : str
        Path to existing MRIQC derivatives folder. Files from source_dir are
        merged into target_dir.
    """
    reports = glob(op.join(source_dir, '*.html'))
    reports = [f for f in reports if 'group_' not in op.basename(f)]
    for report in reports:
        shutil.copy(report, op.join(target_dir, op.basename(report)))

    logs = glob(op.join(source_dir, 'logs/*'))
    for log in logs:
        shutil.copy(log, op.join(target_dir, 'logs', op.basename(log)))

    derivatives = glob(op.join(source_dir, 'sub-*'))
    derivatives = [x for x in derivatives if '.html' not in op.basename(x)]
    for derivative in derivatives:
        shutil.copytree(
            derivative,
            op.join(target_dir, op.basename(derivative))
        )

    csv_files = glob(op.join(source_dir, '*.csv'))
    for csv_file in csv_files:
        out_file = op.join(target_dir, op.basename(csv_file))
        if not op.isfile(out_file):
            shutil.copyfile(csv_file, out_file)
        else:
            new_df = pd.read_csv(csv_file)
            old_df = pd.read_csv(out_file)
            out_df = pd.concat((old_df, new_df))
            out_df.to_csv(out_file, line_terminator='\n', na_rep='n/a',
                          index=False)
