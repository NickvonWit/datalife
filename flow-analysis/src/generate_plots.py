from datalife import DataLife
from datalife import data_branches_and_task_joins
from datalife import producer_consumer_ranking_table
from sankeydata import SankeyData
import os
import argparse
from pprint import pprint
from tabulate import tabulate

class Evaluate:  # Changed class name to follow convention
    dlife = None
    directory = None
    table = 'producer-consumer-ranking-table.csv'
    ctree = 'ctree.pdf'
    dfl = 'dflg-ctree.pdf'

    def __init__(self, dl, dir):
        self.dlife = dl
        self.directory = dir
        run_all(self, self.directory)


    def run_all(self, output):
        self.create_pc_ranking(output)
        self.create_ctree(output)
        self.create_dfl(output)


    def create_pc_ranking(self, output):
        df = producer_consumer_ranking_table(self.dlife.g)
        df.to_csv(output + self.table, header=None, index=None, sep=' ')
        print(tabulate(df, headers = 'keys', tablefmt = 'psql'))


    def create_ctree(self, output):

        caterpillar = self.dlife.caterpillar_tree(weight='value')

        sd = SankeyData()
        sd.import_graph(caterpillar)
        self.verbose_msg("Generating 1kgenomes-ctree.pdf", indent=4)
        sd.plot(options={'no_label':True, 'save_image':output + self.ctree})


    def create_dfl(self, output):

        new_g = data_branches_and_task_joins(self.dlife.g)

        sd = SankeyData()
        sd.import_graph(new_g)
        sd.highlight_edge_colors(cpath='purple', branch_join='lightgreen')
        sd.plot(options={'save_image':output + self.dfl})
