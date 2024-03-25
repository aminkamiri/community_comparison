from .. import CommunityComparison
import numpy as np
import warnings
path="./"
path_data_folder=path+"test_data"
path_report_folder=path+"test_report"

# cc.create_all_reports()

def test_get_all_methods_info():
  cc=CommunityComparison(path_data_folder,path_report_folder,extension='csv')
  df=cc.get_all_methods_info()
  assert(len(df)==3)
  assert(df.loc[df.method_name=='method3','no_of_community'].values[0]==3)
  assert(df.loc[df.method_name=='method3','min_node_size'].values[0]==2)
  assert(df.loc[df.method_name=='method3','max_node_size'].values[0]==3)
  assert(np.array_equal(df.loc[df.method_name=='method3','distribution_node_size'].values[0],np.array([3, 3, 2])))

def test_calculate_shape_similarities():
  cc=CommunityComparison(path_data_folder,path_report_folder,extension='csv')
  df=cc.calculate_shape_similarities()
  assert(len(df)==3)
  assert(df.iloc[0,0]=='method1' and df.iloc[0,1]=='method2')

def test_calculate_similarities_shared_nodes_based():
  cc=CommunityComparison(path_data_folder,path_report_folder,extension='csv')
  df=cc.calculate_similarities_shared_nodes_based()
  assert(len(df)==3)
  assert(df.iloc[0,0]=='method1' and df.iloc[0,1]=='method2')

def test_data_quality():
  path="./"
  # path_data_folder=path+"test_data"
  # path_report_folder=path+"test_report"
  # cc=CommunityComparison(path_data_folder,path_report_folder,extension='csv')
  
  path_data_folder=path+"data"
  path_report_folder=path+"report"
  cc=CommunityComparison(path_data_folder,path_report_folder,extension='parquet')
  set_al_nodes=set()
  for method,df in cc.dfs.items():
    set_al_nodes = set_al_nodes | set(df.node.values)
  
  for method,df in cc.dfs.items():
    ghost_nodes=set_al_nodes - set(df.node.values)
    if len(ghost_nodes)>0:
      warnings.warn(f"Method {method} misses {len(ghost_nodes)} nodes, i.e., %{100*len(ghost_nodes)/len(set_al_nodes):.2f} of all nodes.")

  # assert(1=1)
  #warnings for some nodes not being in some