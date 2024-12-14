'''

'''
import sqlite3

def initialize_db():
    conn = sqlite3.connect('amazon.db')

    return conn, conn.cursor()

conn, cur = initialize_db()



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

def memory_filtration(choice_memory_reqs, compute_subquery):
    cur.execute('''SELECT * FROM ?
    WHERE Instance_Memory ==?;''', (compute_subquery, choice_memory_reqs))
        
def storage_filtration(ebs, storage_reqs, choice_memory_subequery):
    if(ebs):
        cur.execute('''SELECT * FROM ?
    WHERE Instance_Storage ==-1.0;''', (choice_memory_subequery))
    else:
        cur.execute('''SELECT * FROM ?
        WHERE Instance_Storage ==?;''', (choice_memory_subequery, storage_reqs))
def main():
    comp_options ='''
    Desired computational power:\n
    1. High computational requirements\n
    2. Medium computational requirements\n
    3. Low computational requirements\n
    >>Enter n to exclude<<
    Enter your choice: ''' 
    choice_compute = input(comp_options)
    comp_filtration(choice_compute)
    
    choice_memory_reqs = input('''Enter your choice memory requirements as a discrete value (GiB): ''')
    memory_filtration(choice_memory_reqs)
    ebs_storage = input("Would you like only EBS Storage? Y/n [ENTER EBS STORAGE INFORMATION HERE]:  ")
    
    choice_storage_reqs = input("Enter your choice storage requirements as a discrete value (GB): ")
    ebs = False
    if(ebs_storage.lower()== "y"):
        ebs = True
    elif(ebs_storage.lower()!= "n"):
        print("Enter appropriate instructions")
        return
    storage_filtration(ebs, choice_storage_reqs)

    

if __name__ =="__main__":
    main()