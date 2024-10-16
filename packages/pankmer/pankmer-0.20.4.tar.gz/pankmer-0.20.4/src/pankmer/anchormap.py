from Bio.bgzf import BgzfWriter
import gff2bed
import json
import os.path
import os
import pybedtools
import pysam
import tarfile
import subprocess
import warnings
from math import floor
from itertools import accumulate, chain
import pandas as pd

from pankmer.tree import adj_to_ani
from pankmer.adjacency_matrix import get_adjacency_matrix
from pankmer.anchor import get_regional_scores, check_for_bgzip, get_chromosome_sizes_from_anchor
from pankmer.index import load_metadata
from pankmer.parse_genomes_input import remove_seq_ext

LOWRES_STEP = 100

def batch_anchor(size, n: int = 1, lowres_step: int = LOWRES_STEP):
    total_length = sum(size)
    cumulative_size = tuple(accumulate(size))
    def get_coord(x):
      for c, s, cs in zip(size.index, size, cumulative_size):
          if x <= cs:
              return c, x + s - cs
    index_points = [x - (x % lowres_step) for x in range(total_length)[::floor(total_length/n)]]
    if total_length - index_points[-1] < lowres_step:
        index_points.pop()
    index_intervals = zip(((x+1) for x in index_points), index_points[1:]+[total_length])
    batches = []
    for start, end in index_intervals:
        batch_start_chrom, batch_start_pos = get_coord(start)
        batch_end_chrom, batch_end_pos = get_coord(end)
        if batch_start_chrom == batch_end_chrom:
            batch={batch_start_chrom: [(batch_start_pos, batch_end_pos)]}
        else:
            batch = dict(chain(
                ((batch_start_chrom, [(batch_start_pos, size[batch_start_chrom])]),),
                ((c, [(1, size.loc[c])]) for c in size[batch_start_chrom:batch_end_chrom][1:-1].index),
                ((batch_end_chrom, [(1, batch_end_pos)]),),
            ))
        batches.append(batch)
    return batches

def anchormap(index, output_dir, anchors, anno, threads: int = 1, n_batches: int = 1):
    """Generate an anchormap for visualization

    Parameters
    ----------
    index : str
        path to a directory or tar file containing PanKmer index
    output_dir
        directory for output files
    anchors
        iterable of paths to anchor genomes
    anno
        iterable of paths to annotation files
    threads : int
        number of threads to use
    n_batches : int
        number of region batches to use
    """

    metadata = load_metadata(
        index,
        index if os.path.isfile(index) and tarfile.is_tarfile(index) else ""
    )
    for name in metadata.genomes.values():
        if len(name) > 37:
            warnings.warn(f"genome name {name} may be too long for use with pankmer view")
    for anchor in anchors:
        name = remove_seq_ext(os.path.basename(anchor))
        if len(name) > 37:
            warnings.warn(f"anchor genome name {os.path.basename(name)} may be too long for use with pankmer view")
        check_for_bgzip(anchor)
    os.mkdir(output_dir)
    os.mkdir(os.path.join(output_dir, "anchors"))
    os.mkdir(os.path.join(output_dir, "anno"))
    print("loading index")
    print("writing distance matrix")
    (1 - adj_to_ani(get_adjacency_matrix(index))).to_csv(
        os.path.join(output_dir, 'distance.tsv'), sep='\t')
    print('writing config')
    sizes = {remove_seq_ext(os.path.basename(a)): get_chromosome_sizes_from_anchor(a).set_index('name')['size']
             for a in anchors}
    with open(os.path.join(output_dir,'config.json'), 'w') as f:
        json.dump({
            'prefix': output_dir,
            'kmer_size': metadata.kmer_size,
            'genomes': list(metadata.genomes[i] for i in range(len(metadata.genomes))),
            'anchors': [remove_seq_ext(os.path.basename(a)) for a in anchors],
            'lowres_step': LOWRES_STEP,
            'sizes': {a: [[chrom, size] for chrom, size in zip(s.index, s)]
                      for a, s in sizes.items()}},
            f)
    for anchor, anno in zip(anchors, anno):
        a = remove_seq_ext(os.path.basename(anchor))
        print(f"collecting regional scores for {a}")
        with BgzfWriter(
            os.path.join(output_dir, "anchors", f"{a}.1.bgz"), "wb"
        ) as scores_out, BgzfWriter(
            os.path.join(output_dir, "anchors", f"{a}.{LOWRES_STEP}.bgz"), "wb"
        ) as scores_out_lowres:
            for n, batch in enumerate(batch_anchor(sizes[a], n_batches, LOWRES_STEP)):
                print(f"Scoring batch {n} of {a}: {batch}")
                regcov_dict = get_regional_scores(
                    index,
                    anchor,
                    batch,
                    # {c: [[1, sizes[a][c]]] for c in sizes[a].index},
                    threads=threads,
                    score_format="bytes"
                )
                print(f"converting batch {n} to bytes")
                scores = b"".join(
                    bytes(s)
                    for c, regions in batch.items()
                    for region in regions
                    for s in regcov_dict[c][region]
                )
                print(f"writing scoremap for batch {n}")
                scores_out.write(scores)
                scores_out_lowres.write(scores[::LOWRES_STEP])
        for step in 1, LOWRES_STEP:
            subprocess.run(
                (
                    "bgzip",
                    "-rI",
                    os.path.join(output_dir, "anchors", f"{a}.{step}.gzi"),
                    os.path.join(output_dir, "anchors", f"{a}.{step}.bgz"),
                )
            )
        print("formatting annotations")
        for type in "gene", "anno":
            bed = os.path.join(output_dir, "anno", f"{a}.{type}.bed")
            tbx = os.path.join(output_dir, "anno", f"{a}.{type}.bed.bgz")
            pybedtools.BedTool(gff2bed.convert(gff2bed.parse(anno))).saveas(bed).sort().saveas(bed)
            pysam.tabix_compress(bed, tbx, force=True)
            pysam.tabix_index(tbx, force=True, preset='bed', zerobased=True, csi=True)
