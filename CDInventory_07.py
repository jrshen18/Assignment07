'''
Title: CDInventory_07.py
Desc: Working with classes, functions structured error handling, and pickle module
DBiesinger, 2020-Jan-01, Created File.
Jeffrey Shen, 2020-Feb-25, Edited file for assignment06 and comments.
Douglas Klos, 2020-Mar-01, Grading, revised functions, added parameters.
Jeffrey Shen, 2020-Mar-07, Modified file from Doug's feedback and then added preliminary structure.
Jeffrey Shen, 2020-Mar-08, Included structured error handling and store via binary data (pickle module).
'''

'''DATA'''
# import modules
import pickle
# initialize variables
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

'''PROCESSING'''
class DataProcessor:
    '''Processing user action'''
    @staticmethod
    def user_add(cd_id, title, artist, table):
        """Adds CD title and artist from user input

        Args:
            cd_id (string): string representing the ID of the album
            title (string): string representing the Title of the album
            artist (string): string representing the Artist
            table (list of dicts): 2d structure, list of dictionaries containing cd information

        Returns:
            table (list of dicts): 2d structure, list of dictionaries containing cd information
        """
        dicRow = {'ID': cd_id, 'Title': title, 'Artist': artist}
        table.append(dicRow)
        return table

    @staticmethod    
    def user_del(id_to_delete, table):
        """Deletes ID from user input

        Args:
            id_to_delete (string): id representing the cd to remove from inventory
            table (list of dicts): 2d structure, list of dictionaries containing cd information

        Returns:
            table (list of dicts): 2d structure, list of dictionaries containing cd information
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == id_to_delete:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')
        return table

class FileProcessor:
    '''Processing file operations'''
    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name using pickle module (binary)

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        """
        # try to read file name from binary
        # if there is an error, FileNotFoundError is returned
        try:
            with open(file_name, 'rb') as objFile:
                table = pickle.load(objFile)
        except FileNotFoundError:
            print('File not found')
        return table

    @staticmethod
    def write_file(file_name, table):
        """Writes file data using pickle module

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        # write the file in binary
        with open(file_name, 'wb') as objFile:
            pickle.dump(table, objFile)

'''PRESENTATION'''
class IO:
    '''Processing I/O operations'''
    @staticmethod
    def del_input():
        """ Gets ID that user wants to delete.

        Args:
            None.

        Return:
            strIDDel.
        """
        # continue to loop if user input is returning an error
        while True:
            try:
                strIDDel = int(input('Which ID would you like to delete? ').strip())
                return strIDDel
            except ValueError as e:
                print('Not an integer')
                print('Build in error info:')
                print(type(e), e, e.__doc__, sep='\n')
                print() # extra space for layout
                IO.show_inventory(lstTbl)

    @staticmethod
    def get_user_input():
        """ Gets ID, Artist, and Album information from the user

        Args:
            None.

        Return:
            cd_id (int): integer representing the ID of the album
            title (string): string representing the Title of the album
            artist (string): string representing the Artist
        """
        # continue to loop if user input is returning an error
        while True:
            try:
                cd_id = int(input('Enter ID: '))
                title = input('What is the CD\'s title? ').strip()
                artist = input('What is the Artist\'s name? ').strip()
                return cd_id, title, artist
            except ValueError as e:
                print('Not an integer')
                print('Build in error info:')
                print(type(e), e, e.__doc__, sep='\n')
                print() # extra space for layout
                IO.show_inventory(lstTbl)

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """
        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x
        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.
        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

# 1. When program starts, read in the currently saved Inventory
lstTbl = FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()
    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    elif strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        # 3.3.2 Add item to the table
        cd_id, title, artist = IO.get_user_input()
        lstTbl = DataProcessor.user_add(cd_id, title, artist, lstTbl)
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get User input for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        strIDDel = IO.del_input()
        # 3.5.2 search thru table and delete CD
        lstTbl = DataProcessor.user_del(strIDDel, lstTbl)
        # show updated table
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
        # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')