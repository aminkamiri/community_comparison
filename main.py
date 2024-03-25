from community_comparison_amin import CommunityComparison

# path="./"
# path_data_folder=path+"test_data"
# path_report_folder=path+"test_report"
# extension='csv'

path="./"
path_data_folder=path+"data"
path_report_folder=path+"report"
extension='parquet'


cc=CommunityComparison(path_data_folder,path_report_folder,extension=extension)
cc.create_all_reports()
