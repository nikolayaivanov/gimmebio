
from os.path import basename


def get_sample_name_and_end(filename, sample_name_delims=None):
    """Return a tuple of sample name and read end."""
    base = basename(filename)
    for pattern, end in [('_R1.', 1), ('.R1.', 1), ('_1.', 1), ('_R2.', 2), ('.R2.', 2), ('_2.', 2)]:
        if pattern in base:
            sample_name = base.split(pattern)[0]
            if sample_name_delims:
                for delim in sample_name_delims:
                    sample_name = sample_name.split(delim)[0]
            return sample_name, end
    for pattern in ['.fq', '.fastq', '.fna', '.faa', '.fasta']:
        if pattern in base:
            if sample_name_delims:
                for delim in sample_name_delims:
                    sample_name = sample_name.split(delim)[0]
            return sample_name, 0
    assert False  # pattern unknown
