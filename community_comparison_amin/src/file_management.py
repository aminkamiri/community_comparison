#Developed by chatGPT, modified by Amin
import os

def check_folder_exists(folder_name = "report"):
    """
    Check if a folder with the specified name exists in the current working directory.

    Parameters:
    - folder_name (str): The name of the folder to check for existence. Defaults to "report".

    Returns:
    - bool: True if the folder exists, False otherwise.

    Example:
    >>> check_folder_exists("data")
    True
    >>> check_folder_exists("logs")
    False
    """
    # Get the current working directory
    current_directory = os.getcwd()

    # Construct the full path to the folder
    folder_path = os.path.join(current_directory, folder_name)

    # Check if the folder exists
    if os.path.exists(folder_path):
        return True
    else:
        return False

def create_folder(folder_name = "report"):
    """
    Create a folder with the specified name if it doesn't already exist.

    Parameters:
    ----------
    folder_name : str, optional
        The name of the folder to be created. Defaults to "report".

    Returns:
    -------
    None

    Notes:
    ------
    This function checks if the specified folder already exists. If it doesn't exist,
    it creates the folder using `os.makedirs` and prints a success message. If the folder
    already exists, it prints a message indicating that the folder is already present.

    Examples:
    --------
    >>> create_folder("my_folder")
    Folder 'my_folder' created successfully.

    >>> create_folder("existing_folder")
    Folder 'existing_folder' already exists.
    """
    
    # Check if the folder exists
    if not check_folder_exists(folder_name):
        # If it doesn't exist, create it
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created successfully.")
    else:
        print(f"Folder '{folder_name}' already exists.")

from pathlib import Path
def retrieve_all_filenames(path=".",where="**",extension="xlsx"):
    """
    Retrieve a list of filenames in the specified directory matching the given extension.

    Parameters:
    - path (str, optional): The path to the directory where the files should be searched.
      Default is the current directory.
    - where (str, optional): A subdirectory pattern to search within the specified path.
      Default is '**', which matches all subdirectories recursively.
    - extension (str, optional): The file extension to filter the files. Only files with
      this extension will be included in the result. Default is 'xlsx'.

    Returns:
    - list of str: A list of filenames (without the extension) that match the specified
      criteria within the given directory and its subdirectories.

    Example:
    >>> retrieve_all_filenames("/path/to/directory", "subdir", "csv")
    ['file1', 'file2', 'file3']
    """
    i=0
    lst=[]
    for f in Path(path).glob(f"{where}/*.{extension}"):
        filename=f.stem
        # print(filename)
        i+=1
        # print(i,str(f))
        lst.append(filename)
    return lst

if __name__=="__main__":
    # Check if the 'report' folder exists
    folder_name='report'
    if check_folder_exists(folder_name):
        print(f"The {folder_name} folder already exists.")
    else:
        print(f"The {folder_name} folder does not exist. Creating...")
        create_folder()
