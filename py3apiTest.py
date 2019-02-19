"""Standalone test of python api - shows non-functionality of value reutrns"""
# api version 1.0
# tested with python 2.7 and 3.6, 3.7
import sys
print(sys.version)

from pslf import pslf_core
from pslf import pslf_beans
from pslf import pslf_collections
from pslf import pslf_queries

pslfPath = r"C:\Program Files (x86)\GE PSLF"
savPath = r"C:\LTD\pslf_systems\GE_ex\g4_a1.sav"

print( pslf_core.start_pslf(pslfPath) )
print( pslf_core.load_case(savPath) )
pslf_core.solve_case_default_parameters() 

load = pslf_queries.find_load_by_index(0)
#print load.p which should be 1000
print(load.p)

gen = pslf_queries.find_generator_by_index(0)
#print gen0 pgen 
print(gen.pgen)
