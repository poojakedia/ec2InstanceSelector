'''

'''
import sqlite3

def initialize_db():
    conn = sqlite3.connect('amazon.db')

    return conn, conn.cursor()

conn, cur = initialize_db()
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
    if(comp_selection == "1"):
        cur.execute('''
                    SELECT * FROM ec2_Instance
                    WHERE vCPUs >= 16;''')
    elif(comp_selection=="2"):
        cur.execute('''
                    SELECT * FROM ec2_Instance
                    WHERE vCPUs >= 4 AND vCPUs<=8;''')
    elif(comp_selection=="3"):
        cur.execute('''
                    SELECT * FROM ec2_Instance
                    WHERE vCPUs >= 1 AND vCPUs <=2;''')

def memory_filtration(choice_memory_reqs):
    cur.execute('''SELECT * FROM ec2_Instance
    WHERE Instance_Memory ==?;''', (choice_memory_reqs))
        
def main():
    pass

if __name__ =="__main__":
    main()