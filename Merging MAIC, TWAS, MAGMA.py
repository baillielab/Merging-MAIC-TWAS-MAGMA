# -*- coding: utf-8 -*-
"""
Created on Thu Aug 27 17:20:10 2020

@author: migue
"""
import pandas as pd
#Set the paths to the files and the final name of the exported file
Path_to_MAIC = 'C:/Users/migue/Desktop/Baillie/maic_raw.txt'
Path_to_MAGMA = 'C:/Users/migue/Desktop/Baillie/broad.rand_2020_07_16.genes.out.sorted.TXT'
Path_to_TWAS_lungs = 'C:/Users/migue/Desktop/Baillie/Ix05/twasresults/TWAS.A.matched_gtex.lung.dat' #gtex
Path_to_TWAS_wholeblood = 'C:/Users/migue/Desktop/Baillie/Ix05/twasresults/TWAS.A.matched_gtex.wholeblood.dat' #gtex
Path_to_export = 'C:/Users/migue/Desktop/Baillie/' #without name
Name_of_exported_file= '.txt' 
#Import MAIC results
MAIC=pd.read_csv(Path_to_MAIC,sep='\t')
#Delete all columns except for the gene column, the MAIC score, and the contribuitors colunmn for simplicity, can chose not to
MAIC = MAIC.loc[:, MAIC.columns.intersection(['gene','maic_score','contributors'])]
MAIC=MAIC.rename(columns={"gene": "symbol"}) #Renaming the ene column to symbol, so that it can be merged with the MAGMA file
#Next, import the MAGMA file
MAGMA=pd.read_csv(Path_to_MAGMA, sep='\t')
#Merge MAGMA and MAIC on symbol
MAGMA_MAIC = pd.merge(MAGMA, MAIC, on =['symbol'] ,how = 'inner').dropna()
#Import the TWAS lung and wholeblood gtex files
TWAS_lung=pd.read_csv(Path_to_TWAS_lungs ,sep=' ')
TWAS_wholeblood=pd.read_csv(Path_to_TWAS_wholeblood, sep=' ')
#Next is merge each TWAS with the MAGMA_MAIC file
TWAS_lung=TWAS_lung.rename(columns={"ID": "symbol"})
TWAS_wholeblood=TWAS_wholeblood.rename(columns={"ID": "symbol"})
MAGMA_MAIC_TWAS_wholeblood=pd.merge(MAGMA_MAIC, TWAS_wholeblood, on =['symbol'], how='inner').dropna()
MAGMA_MAIC_TWAS_lung=pd.merge(MAGMA_MAIC, TWAS_lung, on =['symbol'], how='inner').dropna()
#Now, concatenate both df, clean table and export
MAGMA_MAIC_TWAS_wholebloodAndLung = pd.concat([MAGMA_MAIC_TWAS_wholeblood, MAGMA_MAIC_TWAS_lung])
MAGMA_MAIC_TWAS_wholebloodAndLung=MAGMA_MAIC_TWAS_wholebloodAndLung.drop(columns=['Unnamed: 0', 'CHR_y'])
MAGMA_MAIC_TWAS_wholebloodAndLung = MAGMA_MAIC_TWAS_wholebloodAndLung[['GENE', 'symbol','CHR_x','maic_score','contributors','START','STOP','NSNPS','NPARAM','N','ZSTAT','P','PANEL','FILE','P0','P1','HSQ','BEST.GWAS.ID','BEST.GWAS.Z','EQTL.ID','EQTL.R2','EQTL.Z','EQTL.GWAS.Z','NSNP','NWGT','MODEL','MODELCV.R2','MODELCV.PV','TWAS.Z','TWAS.P']]
MAGMA_MAIC_TWAS_wholebloodAndLung.to_csv(Path_to_export+Name_of_exported_file, sep='\t')
