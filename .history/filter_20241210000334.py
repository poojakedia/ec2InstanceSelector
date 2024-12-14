'''

'''
import sqlite3
def __init__():
    conn = sqlite3.connect('amazon.db')

    cur = conn.cursor()
def readInput():
    comp_options ='''
    Desired computational power:\n
    1. High computational requirements\n
    2. Medium computational requirements\n
    3. Low computational requirements\n
    >>Enter n to exclude<<
    Enter your choice: ''' 
    choice_compute = input(comp_options)
    
    choice_memory_reqs = input('''Enter your choice memory requirements as a discrete value (GiB): ''')
    
    ebs_storage = input("Would you like only EBS Storage? [ENTER EBS STORAGE INFORMATION HERE]:  ")
    choice_storage_reqs = input("Enter your choice storage requirements as a discrete value (GB): ")


def comp_filtration(comp_selection):
    if(comp_selection == 1):
        pass
        
