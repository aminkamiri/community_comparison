# Developed by Amin
# docstrings are created by chtGPT and modified by Amin
import pandas as pd
from itertools import combinations
# pip install gudhi
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from .file_management import create_folder,retrieve_all_filenames
from .list_similarity import calculate_list_similarity_measures

class CommunityComparison:
  """
  A class for comparing communities identified by a method (stored in data files) and generating reports.

  Args:
      path_data (str): The path to the directory containing data files.
      path_report (str): The path to the directory where reports will be generated.
      extension (str, optional): The file extension of the data files (default is 'parquet').

  Attributes:
      path_data (str): The path to the data directory.
      path_report (str): The path where reports are saved.
      methods (list): A list of data file names found in the data directory.
      dfs (dict): A dictionary of dataframes created from the data files.

  Methods:
      datafile_to_dataframes(extension):
          Reads data files with the specified extension and returns a dictionary of dataframes.

  Example:
      cc = CommunityComparison("./data", "./reports",extension='parquet')
      # Initializes the class with data and report paths.

      cc.create_all_reports()
      # Create reports that show the most similar methods at the top
      ## general_info.csv (general description of the communities created by each methods)
      ## similarity_shape_based.csv (shaped based similarities of the communities created by methods)
      ## similarity_shared_nodes_based.csv (shared-nodes-based similarities of the communities created by methods)
  """
  def __init__(self,path_data,path_report,extension='parquet') -> None: 
    self.path_data=path_data+'/'
    self.path_report=path_report+'/'
    self.methods, self.dfs= self.datafile_to_dataframes(extension)
    print(f"The following data files have been found in the folder {path_data}:\n{', '.join(self.methods)}\n")

    create_folder(path_report) #creates the folder if does not exist
    print(f"Reports are created in the folder {path_report}")

    print("Initialization completed!")

  def datafile_to_dataframes(self, extension):
    """
    Reads data files with the specified extension and returns a dictionary of dataframes.

    Args:
        extension (str): The file extension of the data files.

    Returns:
        tuple: A tuple containing a list of data file names and a dictionary of dataframes.

    Raises:
        Exception: If an unknown file extension is provided.
    """
    filenames =retrieve_all_filenames(self.path_data,extension=extension)
    d_func={'parquet' : pd.read_parquet
            , 'csv' : pd.read_csv
            }
    if extension in d_func:
      read_func=d_func[extension]
    else:
      raise Exception(f"Unknown file extension. We only accept {d_func.keys()}")
    dfs = {filename: read_func(f'{self.path_data}{filename}.{extension}') for filename in filenames}
    return filenames,dfs

  def create_all_reports(self):
    funcs=[ \
          {'func':self.get_all_methods_info
            ,'report_name':'general_info'
            , 'report_description': 'general description of the communities created by each methods'
          },
          {'func':self.calculate_shape_similarities
            ,'report_name':'similarity_shape_based'
            , 'report_description': 'shaped based similarities of the communities created by methods'
          },
          {'func':self.calculate_similarities_shared_nodes_based
            ,'report_name':'similarity_shared_nodes_based'
            , 'report_description': 'shared-nodes-based similarities of the communities created by methods'
          }          
          ]
    for d in funcs:
      self.create_report_for_function(d['func'],
                                      d['report_name'],
                                      d['report_description'])
    

  def create_report_for_function(self,func,report_name,report_description):
    print(f"Creating {report_name}.csv ({report_description})... ")
    df_all_info=func()
    df_all_info.to_csv(f'{self.path_report}/{report_name}.csv')
    print(f"{report_name}.csv is created!")
    
  def get_method_info(self,method_name,df):
    d={}
    d['method_name']=method_name
    d['no_of_community']=df['community'].nunique()
    df_temp=df.groupby('community').count().sort_values('node',ascending=False)
    d['min_node_size']=df_temp['node'].min()
    d['max_node_size']=df_temp['node'].max()
    d['distribution_node_size']=df_temp['node'].values
    return d

  def get_all_methods_info(self):
    lst=[]
    for k,v in self.dfs.items():
      lst.append(self.get_method_info(k,v))
    df_all_info=pd.DataFrame(lst)
    return df_all_info

  def calculate_shape_similarities(self):
    lst=[]
    df_all_info=self.get_all_methods_info()
    for method1, method2 in combinations(self.methods, 2):
      list1=list(df_all_info.loc[df_all_info.method_name==method1,['distribution_node_size']].values[0][0])
      list2=list(df_all_info.loc[df_all_info.method_name==method2,['distribution_node_size']].values[0][0])
      d={'method1':method1, 'method2':method2}
      d.update(calculate_list_similarity_measures(list1,list2))
      lst.append(d)
    df_shape_similarity=pd.DataFrame(lst)
    return df_shape_similarity.sort_values('cosine_similarity',ascending=False)


  def calculate_two_methods_similarity_shared_nodes_based(self,method1,method2):
    """
    Calculates the similarity between two community detection methods based on shared nodes.

    This method compares two community detection methods by measuring the proportion of shared nodes
    between the communities they identify. For each two communities that share at least one node, the
    number od shared nodes is multiplied by two and divided by the sum of nodes of the two communities.
    That is (2 * shared_nodes_number)/ (community_x_nodes+community_y_nodes) which is a number between
    0 and 1. The similarity score is finally calculated as the average of all percentages.

    Args:
        method1 (str): The name of the first community detection method.
        method2 (str): The name of the second community detection method.

    Returns:
        float: The similarity score between the two methods based on shared nodes.

    Example:
        similarity_score = community_comparison.calculate_two_methods_similarity_shared_nodes_based("method1", "method2")
        # Calculates the similarity score between "method1" and "method2" based on shared nodes.
    """
    dfs=self.dfs
    

    df_temp=dfs[method1].merge(dfs[method2],on='node',suffixes=(f'_{method1}', f'_{method2}')).groupby([f'community_{method1}',f'community_{method2}']).count().sort_values('node',ascending=False).reset_index().rename(columns={'node': 'node_count_shared'})
    df_method1=dfs[method1].groupby('community').count().sort_values('node',ascending=False).reset_index().rename(columns={'node': f'node_count_{method1}', 'community':f'community_{method1}'})
    df_method2=dfs[method2].groupby('community').count().sort_values('node',ascending=False).reset_index().rename(columns={'node': f'node_count_{method2}', 'community':f'community_{method2}'})
    df_shared_nodes=df_temp.merge(df_method1,right_on=f'community_{method1}',left_on=f'community_{method1}').merge(df_method2,right_on=f'community_{method2}',left_on=f'community_{method2}')
    # .rename(
    #   columns={'node_count_x': 'shared_node_count','node_count_y': 'node_count_community_x','node_count': 'node_count_community_y'})
    df_shared_nodes['prcntg1']=2*df_shared_nodes['node_count_shared']/(df_shared_nodes[f'node_count_{method1}'] + df_shared_nodes[f'node_count_{method2}'])
    df_shared_nodes['prcntg2']=df_shared_nodes['node_count_shared']/(df_shared_nodes[f'node_count_{method1}'] + df_shared_nodes[f'node_count_{method2}']-df_shared_nodes['node_count_shared'])

    
    # df_temp2=dfs[method1].merge(dfs[method2],on='node').groupby(['community_x','community_y']).count().sort_values('node',ascending=False).reset_index().rename(columns={'node': 'node_count'})
    # df_method1=dfs[method1].groupby('community').count().sort_values('node',ascending=False).reset_index().rename(columns={'node': 'node_count'})
    # df_method2=dfs[method2].groupby('community').count().sort_values('node',ascending=False).reset_index().rename(columns={'node': 'node_count'})
    # df_shared_nodes2=df_temp2.merge(df_method1,right_on='community',left_on='community_x').merge(df_method2,right_on='community',left_on='community_y').rename(
    #   columns={'node_count_x': 'shared_node_count','node_count_y': 'node_count_community_x','node_count': 'node_count_community_y'})
    # df_shared_nodes2['prcntg1']=2*df_shared_nodes2.shared_node_count/(df_shared_nodes2.node_count_community_x + df_shared_nodes2.node_count_community_y)
    # df_shared_nodes2['prcntg2']=df_shared_nodes2.shared_node_count/(df_shared_nodes2.node_count_community_x + df_shared_nodes2.node_count_community_y-df_shared_nodes2.shared_node_count)
    
    return df_shared_nodes.sort_values('prcntg2',ascending=False),df_shared_nodes['prcntg1'].mean(),df_shared_nodes['prcntg2'].mean()


  def calculate_similarities_shared_nodes_based(self):
    lst=[]
    for method1, method2 in combinations(self.methods, 2):
      df_shared_nodes,m1,m2=self.calculate_two_methods_similarity_shared_nodes_based(method1,method2)
      d={'method1':method1, 'method2':method2,'similarity_score1':m1,'similarity_score2':m2}
      lst.append(d)
      df_shared_nodes.to_csv(f"{self.path_report}/{method1}-{method2}.csv")
    df_similarity=pd.DataFrame(lst)
    return df_similarity.sort_values('similarity_score2',ascending=False)


if __name__=="__main__":
  path="./"
  path_data_folder=path+"data"
  path_report_folder=path+"report"
  cc=CommunityComparison(path_data_folder,path_report_folder,extension='parquet')
  cc.create_all_reports()