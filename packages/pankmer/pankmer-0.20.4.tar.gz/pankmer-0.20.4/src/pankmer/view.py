#The visualization of :zsh:`pankmer view` is an adaptation of the visualization of `Panagram <https://github.com/kjenike/Panagram>`_ , another k-mer based pangenome tool by Katie Jenike, Sam Kovaka, Shujun Ou, Stephen Hwang, Srividya Ramakrishnan, Ben Langmead, Zach Lippman, and Michael Schatz.

#Adapted from:
#https://github.com/kjenike/Panagram

# Imports ======================================================================

import seaborn as sns
import os
import os.path
import numpy as np
import pandas as pd
import pysam
from functools import reduce
from itertools import product
import math
from Bio import bgzf
from argparse import ArgumentParser
import json
from pyfaidx import Fasta

import pysam
import os.path
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
from Bio import Phylo
from scipy import signal
from dash import Dash, dcc, html, Input, Output, ctx, State, no_update
from scipy.cluster import hierarchy
from io import StringIO
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist, squareform
import dash_bootstrap_components as dbc

# Constants ====================================================================
ANCHOR_DIR = 'anchors'
TABIX_COLS = ['chr', 'start', 'end', 'name', 'type', 'strand']
TABIX_TYPES = {'start': int, 'end': int}
GENE_TABIX_COLS = TABIX_COLS + ['unique', 'universal']
GENE_TABIX_TYPES = {'start': int, 'end': int, 'unique': int, 'universal': int}
COLORSCALE_CREST = [f'rgb({int(r*255)}, {int(g*255)}, {int(b*255)})' for r, g, b in sns.color_palette('crest', as_cmap=True).colors]
COLORSCALE_MAKO = [f'rgb({int(r*255)}, {int(g*255)}, {int(b*255)})' for r, g, b in sns.color_palette('mako', as_cmap=True).colors]

# Classes ======================================================================

class ScoreMap:
    """read in a score map file from disk and represent it as a
    NumPy array
    
    Parameters
    ----------
    directory : str or Path-like
        display index directory
    anchor : str
        name of anchor genome
    """

    def __init__(self, directory, anchor):
        with open(os.path.join(directory, 'config.json'), 'r') as f:
            config = json.load(f)
        self.prefix = os.path.join(directory, ANCHOR_DIR, anchor) # prefix for data and metadata files
        self.sizes = pd.DataFrame(config['sizes'][anchor], columns=('name', 'size')).set_index('name')['size'] # Chromosome sizes
        self.genomes = config['genomes']
        self.number_of_genomes = len(self.genomes)
        self.score_bitsize = int(math.ceil(self.number_of_genomes/8)) # good, score_bitsize logic matches pankmer
        self.bitmaps = None
        self.steps = [1, config['lowres_step']] # number of steps for maps
        step_sizes = pd.DataFrame(
            {step: np.ceil(self.sizes/step) for step in self.steps}, dtype=int)
        self.offsets = step_sizes.cumsum().shift(fill_value=0) # offset value for start position
        self._read() # Read in the data

    def _read(self):
        self.blocks = {
            s : self.load_bgz_blocks(f'{self.prefix}.{s}.gzi')
            for s in self.steps}
        self.bitmaps = {
            s : bgzf.BgzfReader(f'{self.prefix}.{s}.bgz', 'rb')
            for s in self.steps}

    def load_bgz_blocks(self, file_name):
        with open(file_name, "rb") as idx_in:
            n_blocks = np.fromfile(idx_in, "uint64", 1)[0]
            dtype = [("rstart", "uint64"), ("dstart", "uint64")]
            blocks = np.zeros(int(n_blocks)+1, dtype=dtype)
            blocks[1:] = np.fromfile(idx_in, dtype, n_blocks)
        return blocks.astype([("rstart", int), ("dstart", int)])

    def query(self, contig, start: int = 0, end=None, step: int = 1):
        bstep = reduce(max, (s for s in self.steps if step % s == 0), 1)
        scores = self._query(contig, start,
            end if (end is not None) else self.sizes.loc[contig], step, bstep)
        return np.unpackbits(scores, bitorder="big", axis=1)[:,-self.number_of_genomes:]

    def _query(self, contig, start, end, step, bstep):
        byte_start = self.score_bitsize * (self.offsets.loc[contig,bstep] + (start//bstep))
        length = int((end - start) // bstep)
        step //= bstep
        blk = np.searchsorted(self.blocks[bstep]["dstart"], byte_start, side="right")-1
        blk_offs = byte_start - self.blocks[bstep]["dstart"][blk]
        blk_start = self.blocks[bstep]["rstart"][blk]
        self.bitmaps[bstep].seek(bgzf.make_virtual_offset(blk_start, blk_offs))
        buf = self.bitmaps[bstep].read(length * self.score_bitsize)

        scores = np.frombuffer(buf, "uint8").reshape(
            (len(buf)//self.score_bitsize, self.score_bitsize))

        return scores[::step] if step > 1 else scores

    def close(self):
        if self.bitmaps is not None:
            for f in self.bitmaps.values():
                f.close()

class AnchorMap:
    """Read an anchormap
    
    Parameters
    ---------
    directory
        path to display anchormap directory
    """

    def __init__(self, directory):
        self.prefix = directory
        with open(os.path.join(self.prefix, 'config.json'), 'r') as f:
            config = json.load(f)
        self.distance_file = os.path.join(self.prefix, "distance.tsv")
        self.genomes = config['genomes']
        self.k = config['kmer_size']
        self.lowres_step = 100 
        self.chr_bin_kbp = 200
        self.gff_anno_types = 'gene'
        self.number_of_genomes = len(config['genomes'])
        self.anchor_genomes = config['anchors']
        self.n_anchor_genomes = len(config['anchors'])
        self.anchor_dir = os.path.join(self.prefix, ANCHOR_DIR)
        self.anno_dir = os.path.join(self.prefix, 'anno')
        self.mash = os.path.join(self.prefix, 'mash')
        self.bitmaps = dict()
        self.gene_tabix = dict()
        self.anno_tabix = dict()
        for g in self.anchor_genomes:
            self.bitmaps[g] = ScoreMap(self.prefix, g)
            self.gene_tabix[g] = self._load_tabix(g, "gene")
            self.anno_tabix[g] = self._load_tabix(g, "anno")
        self._load_chr_bins()

    def _load_tabix(self, genome, typ):
        fname = os.path.join(self.anno_dir, f"{genome}.{typ}.bed.bgz")
        if not os.path.exists(fname):
            return None
        if not (os.path.exists(f"{fname}.csi") or os.path.exists(f'{fname}.tbi')):
            raise FileNotFoundError("Index file not found: '{fname}.csi' or '{fname}.tbi' must be preset")
        return pysam.TabixFile(fname, parser=pysam.asTuple(),
            index=(f'{fname}.csi' if os.path.exists(f'{fname}.csi') else f'{fname}.tbi'))

    def chr_bin_coords(self, genome, chrom):
        binlen = self.chr_bin_kbp*1000
        size = self.bitmaps[genome].sizes[chrom]
        starts = np.arange(0,size,binlen)
        ends = np.clip(starts+binlen, 0, size)
        return pd.DataFrame({"genome": genome, "chr": chrom, "start": starts,
                            "end": ends})

    def count_occs(self, occs):
        ret = np.zeros(self.number_of_genomes, "uint32")
        occs, counts = np.unique(occs, return_counts=True)
        ret[occs-1] = counts
        return ret

    def _load_chr_bins(self):
        _occ_idx = pd.RangeIndex(1, self.number_of_genomes+1)
        _total_occ_idx = tuple(f'{x}_occ_{y}' for x, y in product(["total"], _occ_idx))
        _gene_occ_idx = tuple(f'{x}_occ_{y}' for x, y in product(["gene"], _occ_idx))
        with open(os.path.join(self.prefix, 'config.json'), 'r') as f:
            config = json.load(f)
        arr = np.zeros(0, "uint32")
        chrs_rows = []
        for gid, (genome, sizes) in enumerate(config['sizes'].items()):
            for chrom, size in sizes:
                occs = self.query_bitmap(genome, chrom, 0, size, self.lowres_step).sum(axis=1)
                chrs_rows.append((genome, chrom, gid, size, *self.count_occs(occs)))
                coords = self.chr_bin_coords(genome,chrom)
                for _ ,c in coords.iterrows():
                    st = c["start"] // self.lowres_step
                    en = c["end"] // self.lowres_step
                    bin_counts = self.count_occs(occs[st:en])
                    arr = np.append(arr, bin_counts)
        self.chrs = pd.DataFrame(chrs_rows,
            columns=('genome','chr','id','size')+_total_occ_idx)
        self.chrs = self.chrs.set_index(['genome', 'chr'])
        g = self.chrs["size"].groupby("genome")
        self.genome_sizes = pd.DataFrame({
            "length" : g.sum(),
            "chr_count" : g.count()
        })
        for x in _gene_occ_idx:
            self.chrs[x] = 0
        for genome in config['anchors']:
            for chrom, start, end, *_ in self.gene_tabix[genome].fetch():
                counts = self.query_occ_counts(genome, chrom, int(start), int(end))
                self.chrs.loc[(genome,chrom), _gene_occ_idx] += counts
        
        names = self.chrs.columns.str

        total_cols = names.startswith("total_occ_")
        gene_cols = names.startswith("gene_occ_")
        self.chr_occ = self.chrs.loc[:,total_cols | gene_cols].copy()
        cols = self.chr_occ.columns.str.split("_occ_", expand=True)
        self.chr_occ.columns = cols.set_levels(cols.levels[1].astype(int), level=1)

        self.genome_occ = self.chr_occ.groupby(level="genome", sort=False).sum()
        normalize = lambda df: df.divide(df.sum(axis=1), axis=0)
        
        self.genome_occ_freq = pd.concat({
            "total" : normalize(self.genome_occ["total"]),
            "gene" : normalize(self.genome_occ["gene"]),
        }, axis=1)
        
        self.chr_occ_freq = pd.concat({
            "total" : normalize(self.chr_occ["total"]),
            "gene" : normalize(self.chr_occ["gene"]),
        }, axis=1)
        self.genome_occ_avg = (self.genome_occ_freq["total"]*_occ_idx).sum(axis=1).sort_values()
        self.chr_occ_avg = (self.chr_occ_freq["total"]*_occ_idx).sum(axis=1).sort_values()

        arr = arr.reshape((len(arr)//self.number_of_genomes,
                           self.number_of_genomes))
        idx = pd.MultiIndex.from_frame(pd.concat([self.chr_bin_coords(genome, chrom).drop(columns=["end"])
            for genome, sizes in config['sizes'].items()
            for chrom, _ in sizes]))
        self.chr_bins = pd.DataFrame(arr, columns=_total_occ_idx, index=idx).sort_index()

    def close(self):
        for b in self.bitmaps.values():
            b.close()
    
    def query_bitmap(self, genome, chrom, start=None, end=None, step=1):
        return self.bitmaps[genome].query(chrom, start, end, step)

    def query_occ_counts(self, genome, chrom, start, end, step=1):
        occs = self.query_bitmap(genome, chrom, start, end, step).sum(axis=1)
        return self.count_occs(occs)

    def query_genes(self, genome, chrom, start, end):
        rows = self.gene_tabix[genome].fetch(chrom, start, end)
        gene_rows = []
        for chrom, start, end, *rest in rows:
            counts = self.query_occ_counts(genome, chrom, int(start), int(end))
            unique = counts[0]
            universal = counts[-1]
            gene_rows.append((chrom, start, end, *rest, unique, universal))
        return pd.DataFrame(gene_rows, columns=GENE_TABIX_COLS).astype(GENE_TABIX_TYPES)

    def query_anno(self, genome, chrom, start, end):
        rows = self.anno_tabix[genome].fetch(chrom, start, end)
        return pd.DataFrame(((chrom, start, end, name, 'gene', strand) for chrom, start, end, name, _, strand in rows), columns=TABIX_COLS).astype(TABIX_TYPES)


# Functions ====================================================================

def view(params):

    with open(os.path.join(params.anchormap, 'config.json'), 'r') as f:
        config = json.load(f)
    for name in config["genomes"] + config["anchors"]:
        if len(name) >37:
            raise RuntimeError(f"genome name {name} is too long for pankmer view")

    SG_window =53
    poly_order = 3
    SG_polynomial_order = 3
    SG_check = [1]

    buff = 1000

    index = AnchorMap(params.anchormap) #Directory that contains the anchor direcotry

    anchor_name, chrs = index.chrs.index[0]
    if params.genome is not None:
        anchor_name = params.genome
    if params.chrom is not None:
        chrs = params.chrom

    x_start_init = 0 if params.start is None else params.start
    xe = 1000000 #index.chrs.loc[(anchor_name,chrs),"size"]
    x_stop_init  = xe if params.end is None else params.end
    bins = 200#params.max_chr_bins
    opt_bed_file = params.bookmarks
    window_size = index.chr_bin_kbp*1000
    n_skips_start = index.lowres_step

    num_samples = len(index.genomes)
    kmer_len = index.k
    rep_list = index.gff_anno_types
    labels = list(index.anchor_genomes)

    colors = sns.color_palette('crest', n_colors=num_samples).as_hex()


    def get_newick(node, parent_dist, leaf_names, newick='') -> str:
        """
        Convert sciply.cluster.hierarchy.to_tree()-output to Newick format.
        :param node: output of sciply.cluster.hierarchy.to_tree()
        :param parent_dist: output of sciply.cluster.hierarchy.to_tree().dist
        :param leaf_names: list of leaf names
        :param newick: leave empty, this variable is used in recursion.
        :returns: tree in Newick format
        """
        if node.is_leaf():
            return "%s:%.2f%s" % (leaf_names[node.id], parent_dist - node.dist, newick)
        else:
            if len(newick) > 0:
                newick = "):%.2f%s" % (parent_dist - node.dist, newick)
            else:
                newick = ");"
            newick = get_newick(node.get_left(), node.dist, leaf_names, newick=newick)
            newick = get_newick(node.get_right(), node.dist, leaf_names, newick=",%s" % (newick))
            newick = "(%s" % (newick)
            return newick

    def get_x_coordinates(tree):
        #Adapted from:
        #https://github.com/plotly/dash-phylogeny
        """Associates to  each clade an x-coord.
           returns dict {clade: x-coord}
        """
        xcoords = tree.depths()
        if not max(xcoords.values()):
            xcoords = tree.depths(unit_branch_lengths=True)
        return xcoords

    def get_y_coordinates(tree, dist=1.3):
        #Adapted from:
        #https://github.com/plotly/dash-phylogeny
        """
           returns  dict {clade: y-coord}
           The y-coordinates are  (float) multiple of integers (i*dist below)
           dist depends on the number of tree leafs
        """
        maxheight = tree.count_terminals()  # Counts the number of tree leafs.
        # Rows are defined by the tips/leafs
        ycoords = dict((leaf, maxheight - i * dist) for i, leaf in enumerate(reversed(tree.get_terminals())))
        def calc_row(clade):
            for subclade in clade:
                if subclade not in ycoords:
                    calc_row(subclade)
            ycoords[clade] = (ycoords[clade.clades[0]] +
                              ycoords[clade.clades[-1]]) / 2
        if tree.root.clades:
            calc_row(tree.root)
        return ycoords

    def get_clade_lines(orientation='horizontal', y_curr=0, start_coord=0, x_curr=0, y_bot=0, y_top=0,
                        line_color='rgb(25,25,25)', line_width=0.5):
        #Adapted from:
        #https://github.com/plotly/dash-phylogeny
        """define a shape of type 'line', for branch
        """
        branch_line = dict(type='line',
                           layer='below',
                           line=dict(color=line_color,
                                     width=line_width)
                           )
        if orientation == 'horizontal':
            branch_line.update(x0=start_coord,
                               y0=y_curr,
                               x1=x_curr,
                               y1=y_curr)
        elif orientation == 'vertical':
            branch_line.update(x0=x_curr,
                               y0=y_bot,
                               x1=x_curr,
                               y1=y_top)
        else:
            raise ValueError("Line type can be 'horizontal' or 'vertical'")
        return branch_line

    def biggest_num_in_clade(clade, kmer_num):
        if clade.clades:
            m = 0
            for c in clade.clades:
                tmp_m = biggest_num_in_clade(c, kmer_num)
                if tmp_m > m:
                    m = tmp_m
            return m
        else:
            tmp_name = str(clade)
            clade_num = kmer_num[tmp_name]
            return clade_num

    def draw_clade(color_code, total_kmers, kmer_num, palette, clade, start_coord, line_shapes, line_color="grey", line_width=5, x_coords=0, y_coords=0):
        #Adapted from:
        #https://github.com/plotly/dash-phylogeny
        """Recursively draw the tree branches, down from the given clade"""
        x_curr = x_coords[clade]
        y_curr = y_coords[clade]
        if str(clade) != "Clade" and str(clade) != "AT":
            tmp_name = str(clade)
            line_color = color_code[tmp_name]#palette[int(((kmer_num[tmp_name])/total_kmers)*100)-1]
        elif clade.clades:
            
            line_color = palette[int(biggest_num_in_clade(clade, kmer_num))+10]
            #line_color = "grey"
            #Now we have to find the all of the children, and which one has the highest value   
        # Draw a horizontal line from start to here
        branch_line = get_clade_lines(orientation='horizontal', y_curr=y_curr, start_coord=start_coord, x_curr=x_curr,
                                      line_color=line_color, line_width=line_width)
        line_shapes.append(branch_line)
        if clade.clades:
            # Draw a vertical line connecting all children
            y_top = y_coords[clade.clades[0]]
            y_bot = y_coords[clade.clades[-1]]
            #Now we have to get the right color though. It should be the max value of any children 
            line_shapes.append(get_clade_lines(orientation='vertical', x_curr=x_curr, y_bot=y_bot, y_top=y_top,
                                               line_color=line_color, line_width=line_width))
            # Draw descendants
            for child in clade:
                draw_clade(color_code, total_kmers, kmer_num, palette, child, x_curr, line_shapes, x_coords=x_coords, y_coords=y_coords)


    def create_tree(x_start_init, x_stop_init, raw_counts, n_skips):
        #Adapted from:
        #https://github.com/plotly/dash-phylogeny

        tree_tmp1 = raw_counts 
        #We need to sum up the number of times that kmers occur in each column (aka, each sample)
        kmer_num_tmp = tree_tmp1.sum(axis=0)
        
        matrix = linkage(
            tree_tmp1.transpose(),
            method='ward',
            metric='euclidean'
        )
        tree_tmp2 = hierarchy.to_tree(matrix, False)
        treedata = get_newick(tree_tmp2, tree_tmp2.dist, index.genomes)
        
        palette = sns.color_palette("RdPu", 130).as_hex()
        total_kmers = max(kmer_num_tmp) #[-1] #kmer_num_tmp["Solqui2"]
        kmer_num = {}
        color_code = {}
        kmer_num_raw = {}
        #cntr = 0
        for k in range(0, len(kmer_num_tmp)):#kmer_num_tmp.keys():
            kmer_num[index.genomes[k]] = float(((kmer_num_tmp[k])/total_kmers)*100)
            kmer_num_raw[index.genomes[k]] = kmer_num_tmp[k]
            color_code[index.genomes[k]] = palette[int(((kmer_num_tmp[k])/total_kmers)*100)+10]
        #treedata = "(A, (B, C), (D, E))"
        handle = StringIO(treedata)
        tree = Phylo.read(handle, "newick")
        #tree = Phylo.read(tree_file, "newick")
        x_coords = get_x_coordinates(tree)
        y_coords = get_y_coordinates(tree)
        line_shapes = []
        draw_clade(color_code, total_kmers, kmer_num, palette, tree.root, 0, line_shapes, line_color= "blue",#'rgb(25,25,25)',
                    line_width=12, x_coords=x_coords,
                    y_coords=y_coords)
        my_tree_clades = x_coords.keys()
        X = []
        Y = []
        text = []
        color = []
        sizes = []
        color_hist = {}
        for cl in my_tree_clades:
            X.append(x_coords[cl])
            Y.append(y_coords[cl])
            text.append(cl.name)
            tmp_name = str(cl.name)
            #if tmp_name.count("_") > 0:
            #    tmp_name = tmp_name.split("_")[1]
            if str(cl.name) == "None":
                this_color = "grey"
                color.append(this_color)
                sizes.append(5)
            else:
                #this_color = "grey"
                this_color = color_code[tmp_name]
                color.append(this_color)
                sizes.append(10)
        #graph_title = "Pansol Phylgenetic Tree"#create_title(virus_name, nb_genome)
        intermediate_node_color = 'rgb(100,100,100)'
        axis = dict(showline=False,
                    zeroline=False,
                    showgrid=False,
                    showticklabels=False,
                    title=''  # y title
                    )
        label_legend = []
        an_x = []
        an_y = []
        for t in range(0,len(text)):
            if text[t] != None:
                label_legend.append(text[t])
                an_x.append(X[t])
                an_y.append(Y[t])
        nodes = []
        node = dict(type='scatter',
                        x=X,
                        y=Y,
                        mode='markers',
                        marker=dict(color=color,
                                    size=sizes),
                        text=text,  # vignet information of each node
                        #hoverinfo='',
                        showlegend=False
                        )
        nodes.append(node)

        def make_anns(x,y, text, kmer_num, i):
            tmp_txt = text#""
            tmp_txt += " - " + str(kmer_num[tmp_txt])[:4] + "% " #(" + str(kmer_num_raw[tmp_txt]) + ")" 
            return dict(xref='x', yref='y', x=x, y=y, text="\t" + tmp_txt,
                showarrow=False,
                xanchor='left',
                yanchor='middle',)

        annotations = []
        for i in range(0, len(label_legend)):
            annotations.append(make_anns(an_x[i], an_y[i], label_legend[i], kmer_num, i))
        max_x = max(an_x)
        layout = dict(#title=graph_title,
                      paper_bgcolor='rgba(0,0,0,0)',
                      #dragmode="select",
                      #font=dict(family='Balto', size=22),
                      # width=1000,
                      #height=1500,
                      autosize=True,
                      showlegend=True,
                      xaxis=dict(showline=True,
                                 zeroline=False,
                                 showgrid=True,  # To visualize the vertical lines
                                 ticklen=4,
                                 showticklabels=True,
                                 title='Branch Length',
                                 autorange=False,
                                 #range=[0, 0.1]
                                 ),
                      yaxis=axis,
                      hovermode='closest',
                      shapes=line_shapes,
                      plot_bgcolor='rgb(250,250,250)',
                      legend={'x': 0, 'y': 1},
                      annotations=annotations,
                      xaxis_range=[0,int(max_x*1.2)]
                      )
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{"type": "scatter", 'colspan':1}]], #, None, {"type": "bar"} ]], #, {"type": "pie"} , {"type": "pie"} ]],
            horizontal_spacing=0.01,
            #subplot_titles=("This region","CDS","Exons","Genes", "Whole chromosome")
        )
        fig.add_trace(node, row=1, col=1)
        fig.update_layout(layout)
        #Sort the hist bars 
        hist_y = []#list(kmer_num_tmp.values()).sort()
        hist_x = []

        fig.update_yaxes(visible=False, showticklabels=False)
        fig.update_layout(margin=dict(
                t=20,
                b=10,
                l=10,
                r=10))
        return fig

    def get_local_info(x_all, bar_sum_regional, bar_sum_global_tmp, anchor_name, chrs):
        fig = make_subplots(
            rows=2, cols=2,
            specs=[[{"type": "bar", "colspan": 2}, None],
               [{"type": "bar"}, {"type": "bar"}]],
            subplot_titles=("Whole chromosome",  "This region", 
                "Genes", ), 
            vertical_spacing=0.1,
        )
        x = []
        for i in range(1,num_samples+1):
            x.append(i)
        #This region
        y=[(i/sum(bar_sum_regional[1:])*100) for i in bar_sum_regional[1:]]
        y_whole=[(i/sum(bar_sum_global_tmp)*100) for i in bar_sum_global_tmp]
        #.sum(axis=1)
        
        fig.append_trace(go.Bar(x=x, y=y, marker_color=colors, showlegend=False), row=2, col=1)
        fig.append_trace(go.Bar(x=x, y=y_whole, marker_color=colors, showlegend=False), row=1, col=1)

        totals = 0
        gene_comp_tmp = []
        gene_comp = []
        for i in range(1, num_samples+1):
            totals += index.chr_occ.loc[(anchor_name, chrs), ("gene",i)]
            gene_comp_tmp.append(index.chr_occ.loc[(anchor_name, chrs), ("gene",i)])
        
        for t in gene_comp_tmp:
            gene_comp.append(t/totals*100)
        
        fig.append_trace(go.Bar(x=x, y=[a_i - b_i for a_i, b_i in zip(gene_comp, y_whole)], marker_color=colors, showlegend=False), row=2, col=2)
        #fig.update_layout(xaxis_title_text="K-mers shared in X samples", yaxis_title_text='Frequency (log)')
        fig.update_xaxes(title_text="# of genomes", row=2, col=1)
        fig.update_yaxes(title_text="Difference from whole chromosome", row=2, col=1)
        fig.update_yaxes(title_text="Percent of k-mers", row=1, col=1)
        fig.update_yaxes(type="log", row=1, col=1)
        fig.update_yaxes(type="log", row=2, col=1)
        fig.update_yaxes(type="log", row=2, col=2)
        fig.update_layout(height=1000)
        
        return fig

    def plot_interactive(n_skips, layout, bins, bitmap_counts, name, zs_tmp, plot_rep, plot_gene, start_coord, end_coord, gene_locals, gene_names, anchor_name, chrs):
        window_filter = SG_window
        poly_order = SG_polynomial_order
        shared_kmers = [1]
        tmp_lst = []
        rep_colors = sns.color_palette('mako', n_colors=len(rep_list )).as_hex()
        fig = make_subplots(        
            rows=13, cols=1,
            shared_xaxes=True,
            specs=[
                [{"type": "scatter"}], 
                [{"type": "scatter", 'rowspan':2}], [None ], 
                [{"type": "scatter", 'rowspan':2}], [None ],
                [{"type": "bar", 'rowspan':8}] ] + [[None]]*7,
            subplot_titles=("Ref. Sequence Position","Gene Annotation", "Annotation",  "Conserved K-mers" )
        )

        t_start = time.time()

        #We are adjusting the start and stop positions to account for the skipping. 
        #The adjusted value should be the index, whereas the start_coord and end_coord are the real coordinates 
        adjusted_x_start = int(start_coord/n_skips)
        adjusted_x_stop = int(end_coord/n_skips)

        #Get the bins
        bin_size = ((end_coord-start_coord)/bins)
        adjusted_bin_size = (bin_size/n_skips)
        cntr = 0
        
        cats_tmp = [([0] * (bins+1)) for _ in range(num_samples+1)]
        cntr = 0
        x_tracker = 0
        #Here we are filling in the bins for the main figure.    
        bin_size_int = int(bin_size) + 1

        adjusted_bin_size_init = int(adjusted_bin_size) + 1

        cntr = start_coord
        x = []
        while cntr < end_coord:
            x.append(cntr)
            cntr += bin_size_int
        t2 = time.perf_counter()
        print(f"\tMains set up {t2 - t_start:0.4f} seconds")
        cntr = 0
        cats_tmp = np.zeros((bins+1,num_samples+1), int)
        start = 0
        for i in range(bins):
            end = min(start + adjusted_bin_size_init, len(bitmap_counts))
            vals,counts = np.unique(bitmap_counts[start:end], return_counts=True)
            cats_tmp[i+1][vals] = counts
            start = end

        cats_tmp = cats_tmp.T
        t3 = time.perf_counter()
        print(f"\tBuilding the bins {t3 - t2:0.4f} seconds")
        plot_rep = True
        #Add a line plot that will cover the different repetative elements. 
        if plot_rep == True:
            cntr = 0
            anno_locals_all = []
            all_y_reps = []
            all_rep_colors = []
            df = index.query_anno(anchor_name, chrs, start_coord, end_coord)
            
            for i in rep_list:
                if i == "exon":
                    exon_y   = []
                    exon_tmp = []
                    bounds = df[df["type"]==i].loc[:, ["start", "end"]]
                    bounds["break"] = None #pd.NA
                    exon_tmp = bounds.to_numpy().flatten()
                    e = 0
                    while e < len(exon_tmp):
                        exon_y.append(0.5) #[cntr]*len(rep_types_tmp)
                        exon_y.append(0.5)
                        exon_y.append(None)
                        e += 3
                    fig.add_trace(go.Scattergl(x=exon_tmp, y=exon_y, 
                        line=dict(color="#a0da39", width=5), name=i), row=2, col=1)
                else:
                    bounds = df[df["type"]==i].loc[:, ["start", "end"]]
                    bounds["break"] = None #pd.NA
                    anno_locals_tmp = bounds.to_numpy().flatten()
                    if len(anno_locals_tmp) > 0:
                        rep_y = [cntr,cntr,None]*(int(len(anno_locals_tmp)/3))

                        fig.append_trace(go.Scattergl(x=anno_locals_tmp, y=rep_y, #mode='markers+lines',
                            line=dict(color=rep_colors[cntr]), name=i, legendgroup="group2", 
                            legendgrouptitle_text="Annotations", hoverinfo='name'
                            #hovertemplate=i
                            ), #layout_yaxis_range=[0,(len(rep_list))],
                            row=4, col=1)
                    cntr += 1
            fig.update_yaxes(visible=False, row=4, col=1)
            fig.update_xaxes(showticklabels=False, row=4, col=1)
        t4 = time.perf_counter()
        print(f"\tRepeats {t4 - t3:0.4f} seconds")
        if plot_gene == True:
            gene_locals_tmp = []
            gene_names_tmp = []
            intron_locals_tmp = []
            i = 0
            while i < len(gene_names):
                gene_names_tmp.extend([gene_names[i], gene_names[i], None])
                i += 1
            gene_y = [2]*len(gene_names_tmp)

            fig.append_trace(go.Scattergl(x=gene_locals, y=gene_y, 
                line=dict(color="#3b528b", width=10), 
                text=gene_names_tmp, hovertemplate='<br>x:%{x}<br>m:%{text}', legendgroup="group2", 
                name="Gene"), row=2, col=1)
            fig.update_layout(clickmode='event+select')
            #Now add the exons: 
            i = 0

            fig.update_yaxes(visible=False, range=[-1,4], row=2, col=1)
            fig.update_xaxes(showticklabels=False, row=2, col=1)
        
        t5 = time.perf_counter()
        print(f"\tGene plotting {t5 - t4:0.4f} seconds")
        #This is the conserved kmer plotting section
        bar_sum_regional = []
        bar_sum_names = []
        bar_sum_regional.append(sum(cats_tmp[0]))
        bar_sum_names.append(str(0))
        fig.append_trace(go.Bar(x=x, y=cats_tmp[0], name=str(0),
                legendgroup="group1", 
                legendgrouptitle_text="Conserved K-mers",
                marker=dict(color='grey'), 
                marker_line=dict(color='grey')
                ), 
                row=6, col=1 )
        t6 = time.perf_counter()
        print(f"\tConserved k-mers (grey) {t6 - t5:0.4f} seconds")
        for i in range(1, len(cats_tmp)):
            bar_sum_regional.append(sum(cats_tmp[i]))
            #bar_sum_global.append(names_simp.count(i))
            bar_sum_names.append(str(i))
            fig.append_trace(go.Bar(x=x, y=cats_tmp[i], name=str(i),
                legendgroup="group1", 
                legendgrouptitle_text="Conserved K-mers",
                marker=dict(color=colors[i-1]), 
                marker_line=dict(color=colors[i-1])
                ), 
                row=6, col=1 )

        fig.update_layout(barmode='stack', bargap=0.0)
        fig.update_xaxes(showticklabels=False, row=6, col=1)

        t7 = time.perf_counter()
        print(f"\tConserved kmers, non-grey {t7 - t6:0.4f} seconds")
        #Now we will add the smoothing line. There are three parameters that we adjust
        # for sk in shared_kmers:
        #     y_tmp = cats_tmp[int(sk)][:-1]
        #     for i in range(0, int(sk)):
        #         y_tmp = [a + b for a, b in zip(y_tmp, cats_tmp[int(i)][:-1])] #cats_tmp[int(sk)][:-1]
        #     fig.append_trace(go.Scatter(x=x, y=signal.savgol_filter(y_tmp,window_filter,poly_order), 
        #         name="Savitzky-Golay - "+str(sk), marker=dict(color="grey"), mode='lines'), row=6, col=1)

        t8 = time.perf_counter()
        print(f"\tSmoothing line {t8 - t7:0.4f} seconds")
        #Now we add the reference sequence:
        y_ref = [1, 1]
        x_ref = [start_coord, end_coord]
        tickvals = []
        ticktxt = []
        cntr = start_coord
        #yvals = []
        interval = int((end_coord-start_coord)/10)
        while cntr <= end_coord:
            tickvals.append(cntr)
            ticktxt.append(str(cntr))
            #yvals.append(1)
            cntr += interval
        yvals = [1]*len(tickvals)
        fig.append_trace(go.Scattergl(x=tickvals, y=yvals, text=ticktxt, 
            textposition='top center', showlegend=False, 
            mode='lines+markers+text', line=dict(color="grey"), 
            marker = dict(size=5, symbol='line-ns')), row=1, col=1)
        t9 = time.perf_counter()
        print(f"\tFinishing touches {t9 - t8:0.4f} seconds")
        fig.update_yaxes(visible=False, range=[0.9,4], row=1, col=1)
        fig.update_xaxes(visible=False, title_text="Sequence position", row=1, col=1)
        fig.update_layout(template="simple_white" ) #,
        t10 = time.perf_counter()
        print(f"\tTruly finishing touches {t10 - t9:0.4f} seconds")
        fig.update_xaxes(title_text="Sequence position", row=6, col=1)
        fig.update_yaxes(title_text="# of k-mers", range=[0,adjusted_bin_size_init]  , row=6, col=1)
        fig.update_layout(height=1000, xaxis_range=[start_coord,end_coord], font=dict(size=16))
        return fig, bar_sum_names, bar_sum_regional, colors, gene_names_tmp

    def make_gene_whole_chr(x, locs):
        z_genes = [0]*(len(x)+2)
        g = 0
        while g < len(locs):
            x_bin = int(int(locs[g])/window_size)
            if x_bin < len(z_genes):
                z_genes[x_bin] += 1
            g += 1
        return z_genes

    def plot_chr_whole( start_coord, end_coord, anchor_name, this_chr, genes): 
        z_1 = index.chr_bins.loc[anchor_name, "total_occ_1"][this_chr]
        z_9 = index.chr_bins.loc[anchor_name, f"total_occ_{num_samples}"][this_chr]
        y, x = [], []
        cntr = 0
        for xtmp in z_1:
            x.append(cntr)
            y.append(1)
            cntr += window_size

        z_genes = [0]*len(x)
        if index.gene_tabix[anchor_name] is not None:
            #genes = index.query_genes(anchor_name, this_chr, 0, index.chrs.loc[anchor_name, this_chr]["size"])
            if len(genes) > 0:
                bounds = genes["start"].to_numpy() #genes.loc[:, ["start"]].to_numpy()
                z_genes = make_gene_whole_chr(x, bounds) 
                
        chr_fig = make_subplots(rows=3, cols=1, 
            specs=[[{"type": "heatmap",}], [{"type": "heatmap",}], [{"type": "heatmap",}]],
            shared_xaxes=True,
            subplot_titles=("K-mer and gene density accross whole chromosome", "",
                ""),
            vertical_spacing = 0.0
            )

        chr_fig.append_trace(go.Heatmap(x=x, z=z_9, y=y, type = 'heatmap', colorscale=COLORSCALE_MAKO[::-1], showlegend=False, showscale=False), row=1, col=1)
        chr_fig.append_trace(go.Scatter(x=[start_coord, start_coord, None, end_coord, end_coord, None, start_coord, end_coord, ], showlegend=False,
                       y=[0.5, 1.5, None, 0.5, 1.5, None, 1.45, 1.45 ],
                       mode='lines',
                       line_color='#1dd3b0', line_width=8), row=1, col=1)

        chr_fig.append_trace(go.Heatmap(x=x, z=z_1, y=y, type = 'heatmap', colorscale=COLORSCALE_MAKO[::-1], showscale=False), row=2, col=1)
        chr_fig.append_trace(go.Scatter(x=[start_coord, start_coord, None, end_coord, end_coord], showlegend=False,
                       y=[0.5, 1.5, None, 0.5, 1.5],
                       mode='lines',
                       line_color='#1dd3b0', line_width=8), row=2, col=1)

        chr_fig.append_trace(go.Heatmap(x=x, z=z_genes, y=y, type = 'heatmap', colorscale=COLORSCALE_MAKO[::-1], showscale=False ), row=3, col=1)
        chr_fig.append_trace(go.Scatter(x=[start_coord, start_coord, None, end_coord, end_coord, None, start_coord, end_coord,], showlegend=False, 
                       y=[0.5, 1.5, None, 0.5, 1.5, None, 0.55, 0.55],
                       mode='lines',
                       line_color='#1dd3b0', line_width=8), row=3, col=1)
        
        chr_fig.update_yaxes( range=[0.5,1.5], showticklabels=False, row=1, col=1)
        chr_fig.update_yaxes( range=[0.5,1.5], showticklabels=False, row=2, col=1)
        chr_fig.update_yaxes( range=[0.5,1.5], showticklabels=False, row=3, col=1)
        chr_fig.update_xaxes(fixedrange=True, range=[0,index.chrs.loc[anchor_name, this_chr]["size"]], row=1, col=1)
        chr_fig.update_xaxes(fixedrange=True, range=[0,index.chrs.loc[anchor_name, this_chr]["size"]], row=2, col=1)
        chr_fig.update_xaxes(fixedrange=True, row=3, col=1)
        chr_fig.update_xaxes(title_text="Sequence position", range=[0,index.chrs.loc[anchor_name, this_chr]["size"]], row=3, col=1)
        chr_fig.update_yaxes(title_text="Univ.", row=1, col=1)
        chr_fig.update_yaxes(title_text="Uniq.", row=2, col=1)
        chr_fig.update_yaxes(title_text="Genes", row=3, col=1)
        chr_fig.update_layout(clickmode='event+select', dragmode="select", selectdirection='h')
        chr_fig.update_layout(height=350)
        chr_fig.update_layout(margin=dict(b=10, l=10, r=10), font=dict(size=15))
        
        return chr_fig

    def plot_whole_genome(anchor_name):
        spec = []
        sub_titles = []
        h = num_chrs[anchor_name]*250
        for chrom in index.chrs.loc[anchor_name].index: #i in range(0, num_chrs[anchor_name]):
            spec.append([{"type": "heatmap",}])
            spec.append([{"type": "heatmap",}])
            spec.append([{"type": "heatmap",}])
            sub_titles.append(chrom)
            sub_titles.append("")
            sub_titles.append("")
        
        wg_fig = make_subplots(rows=(3*num_chrs[anchor_name]), cols=1, 
            specs=spec, #[[{"type": "heatmap",}], [{"type": "heatmap",}], [{"type": "heatmap"}]],
            shared_xaxes=True,
            subplot_titles=sub_titles, #("K-mer and gene density accross whole chromosome", "", ""),
            vertical_spacing = 0.0
            )
        cntr = 1
        for chrom in index.chrs.loc[anchor_name].index:
            x = list(index.chr_bins.loc[(anchor_name, chrom)].index)
            if len(x)!=1:
                wg_fig.append_trace(go.Heatmap(x=x, z=index.chr_bins.loc[anchor_name, f"total_occ_{num_samples}"][chrom], 
                    y=[1]*(len(x)), type = 'heatmap', colorscale=COLORSCALE_MAKO[::-1], showlegend=False,showscale=False), row=((cntr*3)-2), col=1)
                wg_fig.append_trace(go.Heatmap(x=x, z=index.chr_bins.loc[anchor_name, "total_occ_1"][chrom], 
                    y=[1]*(len(x)), type = 'heatmap', colorscale=COLORSCALE_MAKO[::-1], showscale=False), row=((cntr*3)-1), col=1)
            
            if cntr == 1:
                wg_fig.update_layout(xaxis={'side': 'top'}) 
            cntr += 1
        
        wg_fig.update_layout(clickmode='event', plot_bgcolor='rgba(0,0,0,0)')
        wg_fig.update_layout(height=h)
        return wg_fig

    def plot_gene_content(gene_names,universals,uniques,sizes, sort_by, colors, uniq_avg, univ_avg, start_coord, end_coord, anchor_name, chrs):
        colors = ['#ffd60a', '#440154']
        d = {
            "Names":gene_names,
            "Universal": universals/sizes,
            "Unique":uniques/sizes
        }
        uniq_avg = uniq_avg/100
        univ_avg = univ_avg/100
        df = pd.DataFrame(d)
        x = []
        cntr = 0
        for i in range(0, len(df['Universal'])):
            x.append(cntr)
            cntr +=1
        cntr = 0
        df_sorted = df.sort_values(sort_by[-1])
        df_sorted['X'] = x
        fig = go.Figure(data=[go.Scattergl(x=x, y=df_sorted[sort_by[cntr]], text=df_sorted['Names'], marker=dict(color=colors[cntr]),
                name="% "+sort_by[cntr], mode="markers")])
        cntr += 1
        while cntr < len(sort_by): #s in sort_by:  
            fig.add_trace(go.Scattergl(x=x, y=df_sorted[sort_by[cntr]], text=df_sorted['Names'],  marker=dict(color=colors[cntr]),
                name="% " + sort_by[cntr], mode="markers"))
            cntr += 1
        fig.update_layout(clickmode='event+select')    
        fig.update_layout(hovermode='x unified')
        local_genes = index.query_genes(anchor_name, chrs, start_coord, end_coord)
        local_gene_list = local_genes['name']
        df2 = df_sorted.loc[df_sorted['Names'].isin(local_gene_list)]

        fig.add_trace(go.Scattergl(x=df2['X'], y=df2['Universal'], marker=dict(color='#FF2192', size=10), 
            mode="markers", hoverinfo='skip', showlegend=False))
        fig.add_trace(go.Scattergl(x=df2['X'], y=df2['Unique'], marker=dict(color='#FF2192', size=10), 
            mode="markers", hoverinfo='skip', showlegend=False))

        fig.add_hline(y=uniq_avg, line_dash='dash', line_color='goldenrod')
        fig.add_hline(y=univ_avg, line_dash='dash', line_color='#440154')
        #fig.update_layout(height=500)
        fig.update_layout(
            title={"text":"k-mer content in individual genes",
                "xanchor": "center",
                "x":0.5,
                "y":0.9,
                "yanchor": "top"
                },
            xaxis_title=sort_by[0] + " k-mer content rank",
            yaxis_title="% of k-mers",
            margin=dict(
                t=20,
                b=10,
                l=10,
                r=10),
            font=dict(
                size=16,
            ),
        )
        return fig

    #Tab 1 bar chart of each genome 
    def read_pangenome_comp():
        fig = make_subplots(rows=1, cols=1)
        for i, g in enumerate(index.genomes):
            fig.append_trace(go.Bar(y=index.anchor_genomes, x=index.genome_occ_freq["total", i+1], name=i+1, #orientation='h',
                legendgrouptitle_text="n. samples",
                marker=dict(color=colors[i]), 
                marker_line=dict(color=colors[i]), orientation='h',
                ), row=1, col=1)
        fig.update_layout(barmode='stack' )#,orientation='h')
        fig.update_layout(font=dict( #height=1500, 
            size=26,
            ), plot_bgcolor='rgba(0,0,0,0)')
        fig.update_layout(
            updatemenus = [
            dict(type="buttons",direction="left", #showactive=True, x=0, y=0, 
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,#0.11,
                xanchor="left",
                y=1.05,
                yanchor="top",
                buttons=list([
                dict(args=[{'xaxis.type': 'linear'}],label="Linear", method="relayout"
                    ),
                dict(args=[{'xaxis.type': 'log'}],label="Log",method="relayout"
                    )
                ])
            ),])
        return fig#, genome_comp_totals

    def read_genome_comp(anchor_name):
        totals = index.chr_occ_freq.loc[anchor_name,"total"]

        fig = make_subplots(rows=len(totals), cols=1)

        for i,(c,freqs) in enumerate(totals.iterrows()):
            perc = freqs*100
            fig.add_trace(go.Bar(x=perc.index, y=perc, marker_color=colors, showlegend=False,), row=i+1,col=1)
        fig.update_yaxes(type="log")
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)')
        return fig

    #Tab 1 dendrogram 
    def make_all_genome_dend():
        df = pd.read_table(index.distance_file, index_col=0)
        fig = ff.create_dendrogram(df, colorscale=['black']*8,
                                   labels=df.columns, orientation='right' )
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(size=10,))
        for i in range(len(fig['data'])):
            fig['data'][i]['xaxis'] = 'x2'
        dendro_leaves = list(fig['layout']['yaxis']['ticktext'])
        heat_data = df.loc[dendro_leaves,dendro_leaves].to_numpy()
        heatmap = [go.Heatmap(x=dendro_leaves, y=dendro_leaves, z=1-heat_data,
            colorscale=COLORSCALE_MAKO[::-1])]
        heatmap[0]['x'] = heatmap[0]['y'] = fig['layout']['yaxis']['tickvals']
        heatmap[0].colorbar.lenmode = 'fraction'
        heatmap[0].colorbar.len = 0.8
        for data in heatmap:
            fig.add_trace(data)
        fig.update_layout({'showlegend': False, 'hovermode': 'closest',
            'paper_bgcolor':'rgba(0,0,0,0)', 'plot_bgcolor':'rgba(0,0,0,0)'
            })
        fig.update_yaxes(scaleanchor="x", scaleratio=1) 
        # Edit xaxis
        fig.update_layout(xaxis={'domain': [.3, 1], 'showgrid': False,
            'showline': False, 'zeroline': False, 'showticklabels': False,
            'gridcolor':'rgba(0,0,0,0)', 'ticks':""})
        # Edit xaxis2
        fig.update_layout(xaxis2={'domain': [0, .1], 'showgrid': False,
            'showline': False, 'zeroline': False, 'showticklabels': False,
            'gridcolor':'rgba(0,0,0,0)', 'ticks':""})
        # Edit yaxis
        fig.update_layout(yaxis={'domain': [0, 1], 'showgrid': False,
            'showline': False, 'zeroline': False, 'gridcolor':'rgba(0,0,0,0)',
            'ticks': ""})
        return fig

    def read_genome_size_files():
        seqs = []
        sizes = []
        for l in labels:
            seqs.append([l, len(index.chrs.loc[l].index)])
            sizes.append([l, index.chrs.loc[l]["size"].sum()])

        sizes_df = pd.DataFrame(sizes, columns=['Sample','Size'])
        seqs_df = pd.DataFrame(seqs, columns=['Sample','Seq'])
        
        sizes_df = sizes_df.sort_values(by=['Size'])
        seqs_df = seqs_df.sort_values(by=['Seq'])
        return sizes_df, seqs_df

    def make_genome_count_plot(anchor_name):
        counts = index.genome_sizes["chr_count"].sort_values()
        fig = go.Figure(data=[go.Scattergl(x=counts.index,y=counts,
                                           line_color='black')])
        fig.update_yaxes(title_text="n. scaffolds",)
        fig.add_vline(x=anchor_name, line_dash="dash", line_color="darkgray")
        fig.update_layout(font=dict(size=20,), plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)')
        return fig

    def make_genome_size_plot(anchor_name):
        sizes = index.genome_sizes["length"].sort_values()
        fig = go.Figure(data=[go.Scattergl(x=sizes.index,y=sizes,
                                           line_color='black')])
        fig.update_yaxes(title_text="genome size",)
        fig.add_vline(x=anchor_name, line_dash="dash", line_color="darkgray")
        fig.update_layout(font=dict(size=20,), plot_bgcolor='rgba(0,0,0,0)',
                          paper_bgcolor='rgba(0,0,0,0)')
        return fig

    # def plot_avgs(anchor_name):
    #     fig = go.Figure(data=[ go.Scattergl(x=index.genome_occ_avg.index,
    #                     y=index.genome_occ_avg, line_color='black')])
    #     fig.add_vline(x=anchor_name, line_dash="dash", line_color="darkgray")
    #     fig.update_yaxes(title_text="Average k-mer",)
    #     fig.update_layout(font=dict(size=20,), plot_bgcolor='rgba(0,0,0,0)',
    #                       paper_bgcolor='rgba(0,0,0,0)')
    #     return fig

    def make_avg_kmer_fig(this_anchor):
        fig = make_subplots(rows=1, cols=1)

        avgs = index.chr_occ_avg[this_anchor]

        fig = go.Figure(data=[go.Scattergl(x=avgs.index, y=avgs)])
        fig.update_yaxes(title_text="Average k-mer",)
        fig.update_xaxes(title_text="Chromosome",)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',  font=dict(size=20))

        fig.update_layout(
            updatemenus = [
            dict(type="buttons",direction="left", #showactive=True, x=0, y=0, 
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,#0.11,
                xanchor="left",
                y=1.2,
                yanchor="top",
                buttons=list([
                dict(args=[{'yaxis.type': 'linear'}],label="Linear", method="relayout"
                    ),
                dict(args=[{'yaxis.type': 'log'}],label="Log",method="relayout"
                    )
                ])
            ),])

        return fig

    def make_genes_per_chr_fig(anchor_name):
        x = []
        y = []
        for c in range(0, len(chrs_list[anchor_name])):
            this_chrom = chrs_list[anchor_name][c]
            x.append(this_chrom)
            try:
                y.append(len(index.query_genes(anchor_name, this_chrom, 0, index.chrs.loc[anchor_name, this_chrom]["size"]))/index.chrs.loc[anchor_name, this_chrom]["size"])
            except:
                print(anchor_name + "\t" + this_chrom)
        fig = go.Figure(data=[(go.Scattergl(x=x, y=y))])
        fig.add_trace(go.Scattergl(x=x, y=y))
        fig.update_yaxes(title_text="Gene density",)
        fig.update_xaxes(title_text="Chromosome",)
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)',  font=dict(size=20))
        fig.update_layout(
            updatemenus = [
            dict(type="buttons",direction="left", #showactive=True, x=0, y=0, 
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,#0.11,
                xanchor="left",
                y=1.2,
                yanchor="top",
                buttons=list([
                dict(args=[{'yaxis.type': 'linear'}],label="Linear", method="relayout"
                    ),
                dict(args=[{'yaxis.type': 'log'}],label="Log",method="relayout"
                    )
                ])
            ),])
        return fig

    def make_gene_per_genome_fig(anchor_name):
        
        fig = make_subplots(rows=1, cols=1)
        colors = ['#ffd60a', '#440154']
        gene_names = []
        universals = []
        uniques = []
        sizes = []
        genes = list()
        for chrom in index.chrs.loc[anchor_name].index:
            try:
                g = index.query_genes(anchor_name, chrom, 0, index.chrs.loc[anchor_name, chrom]["size"])
            except: 
                continue
            genes.append(g)
        genes = pd.concat(genes)
        genes["size"] = genes["end"] - genes["start"]
        
        x = [i for i in range(0, len(genes['universal']))]
        genes['universal'] = genes['universal']/genes["size"]
        genes['unique'] = genes['unique']/genes["size"]
        df_sorted = genes.sort_values('universal')
        df_sorted['X'] = x
        fig.add_trace(go.Scattergl(x=x, y=df_sorted['unique'], text=df_sorted["chr"] + ":" + df_sorted['name'], marker=dict(color=colors[0]),
                name="Proportion "+"Unique", mode="markers"))
        fig.add_trace(go.Scattergl(x=x, y=df_sorted['universal'], text=df_sorted["chr"] + ":" +df_sorted['name'], marker=dict(color=colors[1]),
                name="Proportion "+"Universal", mode="markers"))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', font=dict(size=20) )
        fig.update_xaxes(title_text="Genes",)
        fig.update_yaxes(title_text="Proportion of gene",)
        fig.update_layout(hovermode='x unified')

        return fig
    
    def plot_anno_conserve(anchor_name):
        file_name="gene_var.txt"
        all_avgs = []
        all_stds = []
        all_names = []
        all_lens = []

        d_anno = {"Standard_dev":all_stds, #np.log10(all_stds),#all_stds,
            "Average":all_avgs,
            "Name":all_names,
            "Length":all_lens,
            #"Sweep":is_sweep
        }
        df_anno = pd.DataFrame(d_anno)
        fig = px.scatter(df_anno,x="Average", y="Standard_dev", marginal_y='histogram', 
            marginal_x='histogram',
            hover_name="Name", 
            #color="Sweep",
            opacity=0.5,
            color=np.log10(df_anno["Length"])
        )
        return fig

    ##### READ DATA
    chrs_list = {}
    chr_lens = {}
    num_chrs = {}
    cntr = 0
    pre_bed_info = {}
    #chr_nums = 12
    for l in labels:
        num_chrs[l] = len(index.chrs.loc[l])
        chrs_list[l] = index.chrs.loc[l].index
        #chr_lens[l] = index.chrs.loc[l]["size"]
        pre_bed_info[l] = []
    t = time.time()
    cnts_tmp = []
    x = []
    all_chrs = {} #This is where we keep the raw, str, counts 
    
    if opt_bed_file != None: 
        #The optional bed file was provided 
        with open(opt_bed_file, "r") as f:
            line = f.readline()
            while line:
                tmp = line.strip().split("\t")
                pre_bed_info[tmp[0]].append(tmp[1] + ":" + tmp[2] + "-" + tmp[3])
                line = f.readline()


    for i in range(1, num_chrs[anchor_name]+1):
        chrs=index.chrs.loc[anchor_name].index[i-1] #"chr" + str(i)
        chr_start = 0

        chr_end = index.chrs.loc[anchor_name, chrs]["size"]#chr_lens[anchor_name][i-1] #308452471
        all_chrs[chrs] = index.query_bitmap(anchor_name, chrs, chr_start, chr_end, n_skips_start)
    chrs = index.chrs.loc[anchor_name].index[0] #"chr1"

    #Parsing the counts will return the number of genomes present at each kmer position, based on the counts
    # names_simp = all_chrs[chrs].sum(axis=1)#tmp.sum(axis=1)
    bar_sum_global = {}

    for l in labels:
        bar_sum_global[l] = {}
        cntr = 0
        if l in index.anchor_genomes:
            for c in index.chrs.loc[l].index:
                counts = index.chr_bins.loc[(l,c)].sum(axis=0)
                bar_sum_global[l][c] = counts.to_numpy()#bar_sum_global_tmp
                cntr +=1

    tmp = 0
    
    #Read in the repeats file (this has the annotated repeats from Shujun)     
    zs_tmp = []
    gene_names = {}
    gene_locals = {}
    exon_locals = {}
    exon_names = {}
    all_rep_types = {}
    gene_content = {}

    #This will have the figure componants that we need 
    layout = go.Layout(
        margin=go.layout.Margin(
            l=10,  # left margin
            r=10,  # right margin
            b=10,  # bottom margin
            t=10  # top margin
        )
    )
    ##Set the smoothing variables. These will be changable later on. 
    window_filter = 53
    SG_window =53
    poly_order = 3
    SG_polynomial_order = 3
    SG_check = [1]

    shared_kmers = [1]
    x_start_init_adjust = int(x_start_init/n_skips_start)
    x_stop_init_adjust = int(x_stop_init/n_skips_start)
    #### NEED TO ADJUST THE START INIT AND STOP INIT SO THAT WE TAKE THE SKIPS INTO ACCOUNT
    #Here is where we make the main plot 
    #if len(index.chr_bins.loc[(anchor_name,chrs)]) > 1:
    genes = index.query_genes(anchor_name, chrs, 0, index.chrs.loc[anchor_name, chrs]["size"])
    bounds = genes.loc[:, ["start", "end"]]
    bounds["break"] = None #pd.NA
    #gene_locals[l][chrom] = bounds.to_numpy().flatten()
    gene_names = genes['name']

    # main_fig, bar_sum_names, bar_sum_regional, colors, gene_names_tmp = plot_interactive(n_skips_start,
    #     layout, bins, names_simp[x_start_init_adjust:x_stop_init_adjust], chrs, zs_tmp, True, True, 
    #     x_start_init, x_stop_init, bounds.to_numpy().flatten(), gene_names, anchor_name, chrs
    # )

    local_genes = len(index.query_genes(anchor_name, chrs, x_start_init, x_stop_init))

    sort_by = ["Unique","Universal"]
    tmp = [(i/sum(bar_sum_global[anchor_name][chrs])*100) for i in bar_sum_global[anchor_name][chrs]]
    uniq_avg = tmp[1]
    univ_avg = tmp[-1]

    universals = genes["universal"]
    uniques = genes["unique"]

    sizes = genes["end"]-genes["start"] #genes["size"]

    x, z_1, z_9, y = {}, {}, {}, {}

    #Now we need to make the pangenome plot
    #This is going to be a bar chart 
    whole_genome_hists_fig      = read_genome_comp(anchor_name)
    all_genomes_dend_fig        = make_all_genome_dend()
    pangenome_comp_fig          = read_pangenome_comp()

    chrs = index.chrs.loc[anchor_name].index[0] #"chr1"

    config = {"toImageButtonOptions" : {"format" : "svg", "width" : None, "height" : None} , "scrollZoom": False}
    tab_style = {"background-color": "lightgrey", "font-size": 36}

    PANGENOME_TAB = [
            html.Div(id="PanInfo1", children=[
                html.I("PanKmer index of " + str(num_samples) + " genomes"),
                html.Br(),
                html.Label('Select a genome: '),
                dcc.Dropdown(labels, anchor_name, style=dict(width='40%', height='110%', verticalAlign="middle"), id="genome_select_dropdown"),
                html.Br(),
            ], style={'padding':'1%', 'font-size':'24px', 'textAlign': 'left', "border":"2px grey solid"}),
            html.Div([dbc.Row([
                dbc.Col(dcc.Graph(id="all_genome_sizes", className="six columns",
                    config=config, style={"font-size": 30, "height" : 500, 'display': 'inline-block'}#,figure = pg_size_fig, 
                )),
                dbc.Col(dcc.Graph(id="pangenome_num_seqs", className="six columns",
                    config=config, style={"font-size": 30, "height" : 500, 'display': 'inline-block'}#,figure = pg_count_fig
                ))])
            ]),
            html.Div(className="w3-half", children=[
                dcc.Graph(id="all_genomes",style={"font-size": 20, "height" : '90vh'}, config=config),
            ]),
            html.Div(className="w3-half", children=[
                dcc.Graph(id="all_genomes_kmer_comp",
                    config=config, style={"font-size": 30, "height" : 150*index.n_anchor_genomes}#, figure = pangenome_comp_fig
                )
            ]),
            # html.Div(className="w3-third", children=[
            #     dcc.Graph(id="average_kmer_content",
            #         config=config, style={"font-size": 30, "height" : 500}#figure = pangenome_avg_fig,
            #     )
            # ]),
            ]

    #def render_anchor_tab():
    #    return 
    ANCHOR_TAB = [
            html.Div(children=[
                    html.I("Anchor genome " + anchor_name, id="anchor_labels"),
                    html.Br(),
                    html.Label('Select a chromosome: '),
                    dcc.Dropdown(chrs_list[anchor_name], chrs, style=dict(width='40%', height='110%', verticalAlign="middle", ), id="chr_select_dropdown"),
                    html.Br(),
                ], style={'padding-top' : '1%', 'padding-left' : '1%', 'padding-bottom' : '1%', 'padding-right' : '1%', 'font-size':'24px', 'textAlign': 'left', "border":"2px grey solid", }),
            html.Div(className="w3-third",children=[
                dcc.Graph(id="gene_content", config=config), #gene_content_fig)
            ],), 
            html.Div(className="w3-third",children=[
                dcc.Graph(id="genes_per_chr",
                config=config)
            ],),
            html.Div(className="w3-third",children=[
                dcc.Graph(id="avg_kmer_chr", config=config) #, figure = avg_kmer_per_chr_fig
            ],),
            html.Div(className="w3-threequarter",children=[
                dcc.Graph(id="all_chromosomes", config=config, style={"height" : num_chrs[anchor_name]*250})
            ]),
            html.Div(className="w3-quarter",children=[
                dcc.Graph(id="all_chromosomes_hists", style={"height" : num_chrs[anchor_name]*250},
                    figure = whole_genome_hists_fig, 
                    config=config
                )
            ]),
        ]

    #def render_chromosome_tab():
    #    return [
    CHROMOSOME_TAB = [
            html.Div(children=[ # info panel
                html.Div(children=[ #left side
                    html.I(anchor_name + "." + chrs + ":", id="chr_name"),
                    dcc.Input(id="Chrs_Info", placeholder=str(x_start_init) + "-" + str(x_stop_init), debounce=True),
                    html.Br(),
                    html.I("Genes in this region: " + str(local_genes), id='regional_genes'),
                    html.Br(),
                    html.Label('Pre-selected regions: '),
                    dcc.Dropdown(pre_bed_info[anchor_name], chrs + ":" + str(x_start_init) + "-" + str(x_stop_init) , style=dict(width='100%', height='110%', verticalAlign="middle", ), id="pre_regions_dropdown"),
                ],style={"display": "inline-block"}),
                
                html.Div(children=[#right side
                    html.I("K-mer length: " + str(kmer_len),style={"display": "inline-block",}),
                    html.Br(),
                    html.I("Number of bins: " + str(bins), style={'display': 'inline-block'}),
                    html.Br(),
                    html.I("Step size: " + str(n_skips_start), style={"display": "inline-block",}, id='step_size_out'),
                    html.Br(),
                ], style={"display": "inline-block", 'padding-left' : '10%'}),

            ], style = {'padding-top' : '1%', 'padding-left' : '1%', 'padding-bottom' : '1%', 'padding-right' : '1%', 'font-size':'24px', "border":"2px grey solid"}),

            html.Div(children=[ #summary 
                html.Div(className="w3-container", children=[
                        #left figure
                        dcc.Graph(id="chromosome",
                            config=config, style={"font-size": 20, "height" : 350}) #figure = chr_fig, 
                ])
            ]),

            html.Div(children=[ 
                html.Div(className="w3-container", children=[
                    html.Div(className="w3-threequarter", children=[
                        #left figure - calling this the "Main" figure
                        dcc.Graph(id="primary", config=config,  #,figure = main_fig
                            style={"height": 1000,  "font-size": 20})
                    ]), #style={'padding-top' : '1%', 'padding-left' : '1%', 'padding-bottom' : '1%', 'padding-right' : '1%', 
                    html.Div(className="w3-quarter", children=[
                        dcc.Graph(id="Secondary", 
                            #Now we have the phylogenetic tree
                            #figure = get_local_info(names_simp[x_start_init:x_stop_init], #exon_comp[chrs], 
                            #gene_comp[anchor_name][chrs], 
                            #bar_sum_regional, bar_sum_global[anchor_name][chrs], anchor_name, chrs), 
                            config=config,
                            style={"height": 1000, "font-size": 20}),
                    ])
                ])
            ]),
            html.Div(children=[
                html.Div(className="w3-container", children=[
                    html.Div(className="w3-third", children=[
                        dcc.Graph(id="Genes", 
                            #figure=gene_content_plot, 
                            config=config,
                            style={"font-size": 20, "height":750}),
                    ]),
                    html.Div(className="w3-twothird", children=[
                        dcc.Graph(id="Third", 
                            #This is the histogram section
                            config=config,
                            style={"font-size": 20, "height":750}),
                    ]),
                ])
            ])
        ]

    ANNOTATION_TAB = html.Div(children=[
            dcc.Graph(id="annotation_conservation",
                figure=plot_anno_conserve(anchor_name),
                config=config,
                style={"height": 1000, "font-size": 20}
            )
        ])

    app = Dash(__name__,
        external_stylesheets=[dbc.themes.FLATLY], # dbc_css
        url_base_pathname=params.url_base,
        suppress_callback_exceptions=True
    )
    app.layout = html.Div([
        #html.Div(id = 'parent', children = [
        html.H1(id = 'H1', children = 'PanKmer View', style = {'textAlign':'center', "font-size": 64}), 
        dcc.Tabs(id="tabs", value="pangenome", style={"font-size": 36}, children=[
            dcc.Tab(value="pangenome", label='Pangenome', style=  tab_style, children=PANGENOME_TAB),
            dcc.Tab(value="anchor", label='Anchor genome', style= tab_style, children=ANCHOR_TAB),
            dcc.Tab(value="chromosome", label='Chromosome', style=tab_style, children=CHROMOSOME_TAB), 
            dcc.Tab(value="annotation", label='Annotation', style=tab_style, children=ANNOTATION_TAB), 
        ]),

        html.Div(id="tab-content"),

        html.Div(chrs, style={"display" : "none"}, id="selected-chrom-state"),
        html.Div(anchor_name, style={"display" : "none"}, id="selected-anchor-state"),
        html.Div(x_start_init,id='start-coord-state',style={"display" : "none"} ),
        html.Div(x_stop_init,id='end-coord-state',style={"display" : "none"} ),
        html.Div(x_stop_init,id='chr-genes-state',style={"display" : "none"} ),
    ])

    def get_buffer(tmp_start, tmp_stop, n_skips):
        min_dist = n_skips*bins*8
        act_dist = tmp_stop-tmp_start
        if act_dist >= min_dist:
            return 0 #The distance between start and stop are good enough 
        else: #
            return 1 #int((min_dist - act_dist)/2)+1 
    last_reset_click = 0

    def set_coords(anchor, chrom=None, start=0, end=None):
        anchor_chrs = index.chrs.loc[anchor].index
        if chrom not in anchor_chrs:
            chrom = anchor_chrs[0]
        if end is None:
            end = index.chrs.loc[(anchor, chrom), "size"]

        genes = index.query_genes(anchor, chrom, start, end)

        return anchor, chrom, start, end

    @app.callback(
        Output('selected-anchor-state', 'children'), #pangenome
        Output('selected-chrom-state', 'children'),  #anchor
        Output('start-coord-state','children'),   #start_coord div (constant?)
        Output('end-coord-state','children'),   #x_end div (constant?)
        #Output('chr-genes-state','children'),   #x_end div (constant?)
        Output('chromosome', 'relayoutData'),        #chromosome
        Output('Chrs_Info', 'value'),                #chromosome
        Output('chr_name', 'children'),              #chromosome
        Input('genome_select_dropdown', 'value'),     #pangenome, anchor, chromosome
        Input('chr_select_dropdown', 'value'),   #anchor, chromosome
        Input('all_chromosomes','relayoutData'), #anchor -> chromosome
        Input('primary', 'clickData'),           #chromosome
        Input('primary', 'relayoutData'),        #chromosome
        Input('chromosome', 'selectedData'),     #chromosome
        Input('Genes', 'clickData'),             #chromosome
        Input('Chrs_Info', 'value'),             #chromosome
        Input('pre_regions_dropdown', 'value'),  #chromosome
        #Input('all_chromosomes','relayoutData'), #anchor -> chromosome
        State('selected-anchor-state', 'children'),
        State('selected-chrom-state', 'children'),
        State('start-coord-state', 'children'),
        State('end-coord-state', 'children'),
        State('chr-genes-state', 'children'),
    )
    def nav_callback(anchor_dropdown, chr_dropdown, anctab_chrs_relayout, chrtab_primary_click, chrtab_primary_relayout, chrtab_chr_select, chrtab_gene_click, user_chr_coords, pre_selected_region, anchor, chrom, start_coord, end_coord, chr_genes):
        triggered_id = ctx.triggered_id

        n_skips = 100
        click_me_genes = True
        click_me_rep = True
        print("Triggered_id: "+ str(triggered_id))

        if triggered_id == "genome_select_dropdown":
            anchor, chrom, start_coord, end_coord = set_coords(anchor_dropdown)

        elif triggered_id == "chr_select_dropdown":
            anchor, chrom, start_coord, end_coord = set_coords(anchor, chr_dropdown)

        elif triggered_id == "pre_regions_dropdown":
            if pre_selected_region != None:
                chrom = pre_selected_region.split(":")[0]

                start_coord = int(pre_selected_region.split(":")[1].split("-")[0])
                end_coord = int(pre_selected_region.split(":")[1].split("-")[1])
                n_skips = 1

        #Select start/end coordinates, triggers CHROMOSOME
        elif triggered_id == 'Chrs_Info':
            start_coord = int(user_chr_coords.strip().split('-')[0]) 
            end_coord  = int(user_chr_coords.strip().split('-')[1])

        #Select chromosome (region) in anchors tab, triggers CHROMOSOME
        elif triggered_id == 'all_chromosomes':
            #Get the chromosome number 
            if anctab_chrs_relayout != None and len(anctab_chrs_relayout)>1:
                chr_num_tmp = list(anctab_chrs_relayout.keys())[0].split('.')[0].split('axis')[1] #if anctab_chrs_relayout != None and len(anctab_chrs_relayout)>1:
                if len(chr_num_tmp) == 0:
                    chr_num = 1
                else:
                    chr_num = int(int(chr_num_tmp)/3)+1
                
                chrom = index.chrs.index[chr_num-1]
                anchor, chrom, start_coord, end_coord = set_coords(anchor, chrom)

        #Chromosome gene plot, triggers CHROMOSOME
        elif triggered_id == 'Genes':
            if chrtab_gene_click != None:
                this_gene_name = chrtab_gene_click['points'][0]['text']

                genes = index.query_genes(anchor, chrom, 0, index.chrs.loc[(anchor, chrom), "size"]).set_index("name")

                this_gene = genes.loc[this_gene_name]

                start_coord = int(this_gene['start'])
                end_coord = int(this_gene['end'])

        #Chromosome top plot, triggers CHROMOSOME
        elif triggered_id == 'chromosome':
            if not "range" in chrtab_chr_select:
                return (no_update,)*7
            if "x2" in chrtab_chr_select['range'].keys():
                start_coord = int(chrtab_chr_select['range']['x2'][0])
                end_coord = int(chrtab_chr_select['range']['x2'][1])
            elif "x" in chrtab_chr_select['range'].keys():
                start_coord = int(chrtab_chr_select['range']['x'][0])
                end_coord = int(chrtab_chr_select['range']['x'][1])
            else:
                start_coord = int(chrtab_chr_select['range']['x3'][0])
                end_coord = int(chrtab_chr_select['range']['x3'][1])
        

        #Chromosome main plot, triggers CHROMOSOME
        elif triggered_id == 'primary':
            if chrtab_primary_relayout != None and 'xaxis4.range[0]' in chrtab_primary_relayout.keys():
                start_coord = int(chrtab_primary_relayout['xaxis4.range[0]'])
                end_coord = int(chrtab_primary_relayout['xaxis4.range[1]'])
            #elif chrtab_primary_click != None:

        if (end_coord - start_coord) <= bins:
            start_coord = start_coord - 175
            end_coord = end_coord + 175

        return (
            anchor, chrom, start_coord, end_coord, #chr_genes,
            chrtab_chr_select,
            update_output_div(chrom, start_coord, end_coord, anchor), 
            update_out_chr(chrom, anchor), 
        )


    @app.callback(
        Output('all_genome_sizes', 'figure'),        #pangenome
        Output('pangenome_num_seqs', 'figure'),      #pangenome
        Output('all_genomes', 'figure'),
        Output('all_genomes_kmer_comp', 'figure'),
        # Output('average_kmer_content', 'figure'),    #pangenome
        Input('tabs', 'value'),
        Input('selected-anchor-state', 'children')
    )
    def pangenome_callback(tab, anchor_name):
        # if tab != "pangenome":
        #     return ({},)*5 #+ (no_update,)
        print("pangenome_callback")
        triggered_id = ctx.triggered_id            
        if triggered_id != "selected-anchor-state":
            return (no_update,)*4
        # return all_genomes_dend_fig, pangenome_comp_fig, make_genome_count_plot(anchor_name), plot_avgs(anchor_name), make_genome_size_plot(anchor_name)#, anchor_name
        return make_genome_size_plot(anchor_name), make_genome_count_plot(anchor_name), all_genomes_dend_fig, pangenome_comp_fig#, anchor_name

    @app.callback(
        Output('all_chromosomes', 'figure'),         #anchor
        Output('gene_content', 'figure'),            #anchor
        Output('genes_per_chr', 'figure'),           #anchor
        Output('avg_kmer_chr', 'figure'),            #anchor
        Output('chr_select_dropdown', 'options'),    #anchor
        Output('anchor_labels', 'children'),         #anchor
        #Output('selected-chrom-state', 'children'),  #anchor
        Input('tabs', 'value'),
        Input('selected-anchor-state', 'children')
    )
    def anchor_callback(tab, anchor_name):
        # if tab != "anchor":
        #     return ({},)*4 + (no_update,)*2
        print("anchor_callback")
        triggered_id = ctx.triggered_id
        if triggered_id != "selected-anchor-state":
            return (no_update,)*6

        return (
            plot_whole_genome(anchor_name),
            make_gene_per_genome_fig(anchor_name),
            make_genes_per_chr_fig(anchor_name),
            make_avg_kmer_fig(anchor_name),
            update_chromosome_list(anchor_name), 
            anchor_name, 
        )
        
    @app.callback(
        Output('chromosome','figure'),               #chromosome
        Output('primary','figure'),                  #chromosome
        Output('Secondary', 'figure'),               #chromosome
        Output('Third', 'figure'),                   #chromosome
        Output('Genes', 'figure'),                   #chromosome
        Output('regional_genes', 'children'),        #chromosome
        Input('tabs', 'value'),                  #all
        Input('start-coord-state','children'),   #start_coord div (constant?)
        Input('end-coord-state','children'),   #x_end div (constant?)
        State('selected-chrom-state', 'children'),
        State('selected-anchor-state', 'children'),
    )
    def chromosome_callback(tab, start_coord, end_coord, chrs, anchor_name):
        print("chromosome_callback\t" + str(tab))
        tic = time.perf_counter()
        if tab != "chromosome":
            return ({},)*5 + (no_update,)#+ (no_update,)*4

        triggered_id = ctx.triggered_id

        n_skips = 100
        click_me_genes = True
        click_me_rep = True
        chr_num = chrs_list[anchor_name].get_loc(chrs)+1

        #Bookmarks, select from chromosome, triggers CHROMOSOME
        toc = time.perf_counter()
        print(f"pre update all in {toc - tic:0.4f} seconds")
        return update_all_figs(chr_num, click_me_rep, click_me_genes, chrs, anchor_name, 0, start_coord, end_coord,n_skips) 

    def update_all_figs(chr_num, click_me_rep, click_me_genes, chrom, anchor_name, redo_wg, start_coord, end_coord, n_skips):
        print("update_all_figs")
        tic = time.perf_counter()
        all_genes = index.query_genes(anchor_name, chrom, 0, index.chrs.loc[anchor_name, chrom]["size"])
        bounds = all_genes.loc[:, ["start", "end"]]
        bounds["break"] = None
        gene_names = all_genes["name"]
        toc_tmp = time.perf_counter()
        print(f"All_genes in {toc_tmp - tic:0.4f} seconds")
        if get_buffer(start_coord, end_coord, n_skips_start) == 1:
            n_skips = 1

        bitmap = index.query_bitmap(anchor_name, chrom, start_coord, end_coord, n_skips) #.sum(axis=1)
        bitmap_counts = bitmap.sum(axis=1)
        toc_tmp_1 = time.perf_counter()
        print(f"query bitmap {toc_tmp_1 - toc_tmp:0.4f} seconds")
        fig1, bar_sum_names, bar_sum_regional, colors, gene_names_tmp = plot_interactive(
            n_skips, layout, bins, bitmap_counts, 
            chrom, zs_tmp, click_me_rep, click_me_genes,  
            int(start_coord), int(end_coord), 
            bounds.to_numpy().flatten(), 
            gene_names, anchor_name, chrom
        )
        toc_tmp_2 = time.perf_counter()
        print(f"main fig in {toc_tmp_2 - toc_tmp:0.4f} seconds")
        local_gene_list = index.query_genes(anchor_name, chrom, int(start_coord), int(end_coord))

        sort_by = ["Unique","Universal"]
        tmp = [(i/sum(bar_sum_global[anchor_name][chrom])*100) for i in bar_sum_global[anchor_name][chrom]]
        uniq_avg = tmp[1]
        univ_avg = tmp[-1]

        universals = all_genes["universal"]
        uniques = all_genes["unique"]
        sizes = all_genes["end"]-all_genes["start"]
        toc_tmp_3 = time.perf_counter()
        print(f"querying in {toc_tmp_2 - toc_tmp_3:0.4f} seconds")
        fig4 = plot_gene_content(gene_names,universals,uniques,sizes,sort_by, colors, uniq_avg, univ_avg, int(start_coord), int(end_coord), anchor_name, chrom)
        toc_tmp_31 = time.perf_counter()
        print(f"fig 4 plot in {toc_tmp_31 - toc_tmp_3:0.4f} seconds")
        chr_fig = plot_chr_whole(start_coord, end_coord, anchor_name, chrom, all_genes)
        toc_tmp_32 = time.perf_counter()
        print(f"chr fig in {toc_tmp_32 - toc_tmp_31:0.4f} seconds")
        fig2 = get_local_info(bitmap_counts, bar_sum_regional, bar_sum_global[anchor_name][chrom], anchor_name, chrom)
        toc_tmp_33 = time.perf_counter()
        print(f"fig 4 plot in {toc_tmp_33 - toc_tmp_32:0.4f} seconds")
        fig3 = create_tree(start_coord, end_coord, bitmap, n_skips)
        toc_tmp_4 = time.perf_counter()
        print(f"tree plot in {toc_tmp_4 - toc_tmp_33:0.4f} seconds")
        #if redo_wg == 1:
        big_plot = no_update#plot_whole_genome(anchor_name)
        toc_tmp_5 = time.perf_counter()
        print(f"plots big in {toc_tmp_5 - toc_tmp_4:0.4f} seconds")
        pg_sizes_fig = make_genome_size_plot(anchor_name)
        toc_tmp_6 = time.perf_counter()
        print(f"plots sizes in {toc_tmp_6 - toc_tmp_5:0.4f} seconds")
        pg_scaffolds_fig = make_genome_count_plot(anchor_name)
        toc_tmp_7 = time.perf_counter()
        print(f"plots scfs in {toc_tmp_7 - toc_tmp_6:0.4f} seconds")
        # pg_avgs = plot_avgs(anchor_name)
        # toc_tmp_8 = time.perf_counter()
        # print(f"plots avgs in {toc_tmp_8 - toc_tmp_7:0.4f} seconds")

        tab2_gene_density_fig = no_update #make_genes_per_chr_fig(anchor_name)
        toc_tmp_9 = time.perf_counter()
        # print(f"plots density in {toc_tmp_9 - toc_tmp_8:0.4f} seconds")

        tab2_avg_fig = no_update#make_avg_kmer_fig(anchor_name)
        toc_tmp_10 = time.perf_counter()
        print(f"plots avg tab2 in {toc_tmp_10 - toc_tmp_9:0.4f} seconds")

        tab2_sorted_genes = no_update#make_gene_per_genome_fig(anchor_name)
        toc_tmp_11 = time.perf_counter()
        print(f"plots sorted in {toc_tmp_11 - toc_tmp_10:0.4f} seconds")
        #else:
        #    big_plot = no_update
        #    pg_sizes_fig = no_update
        #    pg_avgs = no_update
        #    pg_scaffolds_fig = no_update
        #    tab2_gene_density_fig = no_update
        #    tab2_avg_fig = no_update
        #    tab2_sorted_genes = no_update
        toc = time.perf_counter()
        print(f"Update all in {toc - tic:0.4f} seconds")
        return (
            chr_fig, fig1, fig2, fig3, fig4,  
            update_gene_locals(local_gene_list, chrom, start_coord, end_coord, anchor_name)
        )

    def update_output_div(chrs, start, stop, anchor_name):
        return f'{start}-{stop}'

    def update_out_chr(chrs, anchor_name):
        return f'{anchor_name}.{chrs}:'

    def update_gene_locals(local_gene_list, chrs, start_coord, end_coord, anchor_name):
        printme = ""
        if len(local_gene_list)==1:
            printme += "Genes: "
            printme += local_gene_list['name'][0] + ": "
            printme += local_gene_list['name'][0]
            # printme += local_gene_list['attr'][0] 
        elif len(local_gene_list)<=25:
            printme += "Genes: "
            for i in local_gene_list['name']:
                printme += i + ", "
        else:
            printme = "Genes in this region: " + str(len(local_gene_list))
        return f'{printme}'

    def update_anchor_name(anchor_name):
        return f'{anchor_name}'

    def update_chromosome_list(anchor_name):
        return_me = [{'label': i, 'value': i} for i in index.chrs.loc[anchor_name].index]
        return return_me 

    app.run_server(host=params.host, port=params.port, debug=not params.ndebug)


def parse_arguments():
    parser = ArgumentParser(description="Interactive veiw of anchormap")
    parser.add_argument(
        "anchormap",
        metavar="<anchormap/>",
        help="directory containing anchormap"
    )
    parser.add_argument('--genome')
    parser.add_argument('--chrom')
    parser.add_argument('--start')
    parser.add_argument('--end')
    parser.add_argument('--bookmarks')
    parser.add_argument('--ndebug', action='store_true')
    parser.add_argument('--url_base', default='/')
    parser.add_argument('--port', default='8050')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--max-chr-bins', default=350)
    return parser.parse_args()

def main():
    args = parse_arguments()
    view(args)




# Execute ======================================================================

if __name__ == '__main__':
    main()
