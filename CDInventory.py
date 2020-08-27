#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with try / except statements and binary files.
# Change Log: (Who, When, What)
# SRomo, 2020-Aug-25, Created File
# SRomo, 2020-Aug-25, Added try / except statements
# SRomo, 2020-Aug-26, Added binary file code
# SRomo, 2020-Aug-26, Added higher level try / except statement
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    """Processing the in-memory data"""
    
    @staticmethod
    def add_cd_to_table(cdId, cdTitle, cdArtist, table):
        """Function to add the user input into the table

        Args:
            cdID: CD ID
            cdTitle: title of CD
            cdArtist: artist

        Returns:
            table
        """
        
        dicRow = {'ID': cdId, 'Title': cdTitle, 'Artist': cdArtist}
        table.append(dicRow)
        
        return table
        
    
    @staticmethod
    def remove_cd(table, userInput):
        """Function to remove a CD from the in-memory table
        
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            userInput: user inputted ID to delete

        Returns:
            None.

        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == userInput:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')


class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        
        try:
            with open(file_name, 'rb') as objFile:
                data = pickle.load(objFile)
                
                for row in data:
                    table.append(row)
            
                return table
                
        except FileNotFoundError:
            print('The file doesn\'t exist. No data could be loaded.\n')
        except:
            print('Something else went wrong.\n')
        


    @staticmethod
    def write_file(file_name, table):
        """Function to write data from the table to a file
        
        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns: 
            None
        """
        
        try:
            with open(file_name, 'wb') as objFile:
                pickle.dump(table, objFile)
            print('Data added to the .txt file!\n')
        except FileNotFoundError:
            print('The file doesn\'t exist. No data could be loaded.\n')
        except:
            print('Something else went wrong.\n')



# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] Load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] Delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x

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
        print('======================================\n')

    @staticmethod
    def add_cd():
        """Allows user to add a CD
        
        Args:
            strID: user input for CD ID
            strTitle: CD title
            strArtist: artist name
            
        Returns:
            intID, strTitle, strArtist
        
        """    
    
        try:
            intID = int(input('Enter ID: ').strip())
        except ValueError:
            print('Please enter an integer.')
            intID = int(input('Enter ID: ').strip())
    
        strTitle = input('What is the CD\'s title? ').strip()
        strArtist = input('What is the Artist\'s name? ').strip()
        
        return intID, strTitle, strArtist
        
        

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
   
while True:
    try:
        # 2.1 Display Menu to user and get choice
        IO.print_menu()
        strChoice = IO.menu_choice()
    
        # 3. Process menu selection
        # 3.1 process exit first
        if strChoice == 'x':
            break
        # 3.2 process load inventory from file
        if strChoice == 'l':
            print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
            strYesNo = input('Do you want to continue? [y/n] ')
            if strYesNo.lower() == 'y':
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
            intID, strTitle, strArtist = IO.add_cd()
            
            # 3.3.2 Add item to the table
            DataProcessor.add_cd_to_table(intID, strTitle, strArtist, lstTbl)
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.
        # 3.4 process display current inventory
        elif strChoice == 'i':
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.
        # 3.5 process delete a CD
        elif strChoice == 'd':
            # 3.5.1 get Userinput for which CD to delete
            # 3.5.1.1 display Inventory to user
            IO.show_inventory(lstTbl)
            # 3.5.1.2 ask user which ID to remove
            intIDDel = int(input('Which ID would you like to delete? ').strip())
            # 3.5.2 search thru table and delete CD
            DataProcessor.remove_cd(lstTbl, intIDDel)
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

    except KeyboardInterrupt:
        strYesNo = input('Are you sure you want to quit? [y/n] ').strip().lower()
        if strYesNo == 'y':
            break
        else:
            IO.print_menu()

