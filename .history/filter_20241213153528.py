'''

'''
import sqlite3

def initialize_db():
    conn = sqlite3.connect('amazon.db')

    return conn, conn.cursor()

conn, cur = initialize_db()

compSubquery = "ec2_Instance"
memSubquery ="ec2_Instance"
storSubquery ="ec2_Instance"
OStype = ""
def comp_filtration(comp_selection, OStype):

    if(comp_selection == "1"):
        compSubquery = f'''
                    SELECT * FROM ec2_Instance
                    WHERE vCPUs >= 16
                    ORDER BY {OStype};
                    '''
    elif(comp_selection=="2"):
        compSubquery = f'''
                    SELECT * FROM ec2_Instance
                    WHERE vCPUs >= 4 AND vCPUs<=8
                    ORDER BY {OStype};
                    '''
    elif(comp_selection=="3"):
        compSubquery = f'''
                    SELECT * FROM ec2_Instance
                    WHERE vCPUs >= 1 AND vCPUs <=2
                    ORDER BY {OStype};
                    '''
    else:
        print("Invalid input")
        return None, []
    cur.execute(compSubquery);
    return cur.fetchall()

def memory_filtration(choice_memory_reqs, OStype):
    memSubquery = f'''SELECT * FROM {compSubquery}
                        WHERE Instance_Memory == {choice_memory_reqs}
                        ORDER BY {OStype};
                    '''
    
    cur.execute(memSubquery)
    return cur.fetchall()
        
def storage_filtration(ebs, storage_reqs, OStype):
    if(ebs):
        storSubquery = f'''SELECT * FROM {memSubquery}
                            WHERE Instance_Storage ==-1.0
                            ORDER BY {OStype};
                            '''
    else:
        storSubquery =f'''SELECT * FROM ({memSubquery})
                            WHERE Instance_Storage ==({storage_reqs})
                            ORDER BY {OStype};
                            '''
                            
    cur.execute(storSubquery)
    return cur.fetchall()

def print_instances(res, os_col):
    print('''
          
          ''')
    for row in res:
            print(f"Instance Name: {row[0]}, Instance API:{row[1]}, Cost(hourly): {row[os_col]}")
            print('\n')
    print('''
          
          ''')
def main():
    OS = input('''
    Choose desired OS system, Linux or Windows: ''')
    
    if(OS.lower() == "linux"):
        OStype = "Linux_Reserved_cost"
        os_col = 7
    elif (OS.lower() == "windows"):
        OStype = "Windows_Reserved_cost"
        os_col = 10
    else:
        print("Invalid input")
        return 
    comp_options ='''
    Desired computational power:\n
    1. High computational requirements\n
    2. Medium computational requirements\n
    3. Low computational requirements\n
    >>Enter n to exclude<<
    Enter your choice: ''' 

    choice_compute = input(comp_options)
    if(choice_compute != "n"):
        res = comp_filtration(choice_compute, OStype)[:5]
        print_instances(res,os_col)
        
    
    choice_memory_reqs = input('''Enter your choice memory requirements as a discrete value (GiB): ''')
    if(choice_memory_reqs != "n"):
        res = memory_filtration(choice_memory_reqs, OStype)[:5]
        print_instances(res,os_col)
    ebs_storage = input("Would you like only EBS Storage? Y/n [ENTER EBS STORAGE INFORMATION HERE]:  ")
    
    choice_storage_reqs = input("Enter your choice storage requirements as a discrete value (GB): ")
    
    if(choice_storage_reqs != "n"):
        ebs = False
        if(ebs_storage.lower()== "y"):
            ebs = True
        elif(ebs_storage.lower()!= "n"):
            print("Enter appropriate instructions")
            return
        res = storage_filtration(ebs, choice_storage_reqs, OStype)[:5]
        print_instances(res,os_col)
    return
    

    

if __name__ =="__main__":
    main()