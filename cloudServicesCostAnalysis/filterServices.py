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
    #query based on number of indicated CPUs
    if(comp_selection == "a"):
        compSubquery = f'''
                    SELECT * FROM ec2_Instance
                    WHERE vCPUs >= 16
                    ORDER BY {OStype};
                    '''
    elif(comp_selection=="b"):
        compSubquery = f'''
                    SELECT * FROM ec2_Instance
                    WHERE vCPUs >= 4 AND vCPUs<=8
                    ORDER BY {OStype};
                    '''
    elif(comp_selection=="c"):
        compSubquery = f'''
                    SELECT * FROM ec2_Instance
                    WHERE vCPUs >= 1 AND vCPUs <=2
                    ORDER BY {OStype};
                    '''
    else:
        try:
            compSubquery = f'''
                    SELECT * FROM ec2_Instance
                    WHERE vCPUs =={comp_selection}
                    ORDER BY {OStype};
                    '''
        except:
            print("Invalid input")
            return None, []
    cur.execute(compSubquery);
    return cur.fetchall()

def memory_filtration(choice_memory_reqs, OStype):
    #filter memory requirements based on subquery for computational requirements (if it exists, else it queries from table normally)
    memSubquery = f'''SELECT * FROM {compSubquery}
                        WHERE Instance_Memory == {choice_memory_reqs}
                        ORDER BY {OStype};
                    '''
    
    cur.execute(memSubquery)
    return cur.fetchall()
        
def storage_filtration(ebs, storage_reqs, OStype):
    #filter storage requirements here, filter based on whether ebs is selected, use former memory query as a stackable subquery here (if applicable)
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
    print('\n')
    for row in res:
            print(f"Instance Name: {row[0]}, Instance API:{row[1]}, Cost(hourly): {row[os_col]}")
            print('\n')

def query_to_string(res, os_col):
    stringified = []
    for row in res:
            stringified.append((f"Instance Name: {row[0]}, Instance API: {row[1]}, Cost(hourly): {row[os_col]}"))
    return stringified
            

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
    a. High computational requirements\n
    b. Medium computational requirements\n
    c. Low computational requirements\n
    OR Enter a numeric value of CPUs
    >>Enter n to exclude<<
    Enter your choice: ''' 

    choice_compute = input(comp_options)
    if(choice_compute != "n"):
        res = comp_filtration(choice_compute, OStype)[:5]
        if(len(res) == 0):
            print("No matching results.")
            return
        print_instances(res,os_col)
        
    
    choice_memory_reqs = input('''
    Enter your choice memory requirements as a discrete value (GiB) (e.g. 1.0)
    >>Enter n to exclude<<
    
    Memory requirement: ''')
    if(choice_memory_reqs != "n"):
        res = memory_filtration(choice_memory_reqs, OStype)[:5]
        if(len(res) == 0):
            print("No matching results.")
            return
        print_instances(res,os_col)
    ebs_storage = input('''
    Elastic Block Storage allows you to manage storage by
    attaching "volumes" to ec2 instances that act similarly to a local hard drive
    and using snapshots to back up data on EBS volumes.
    
    Would you like only EBS Storage? Y/n:  ''')
    
    choice_storage_reqs = input('''
    Enter your choice storage requirements as a discrete value (GB) (e.g. 59)
    >>Enter n to exclude<<

    Enter your storage requirement: ''')
    
    if(choice_storage_reqs != "n"):
        ebs = False
        if(ebs_storage.lower()== "y"):
            ebs = True
        elif(ebs_storage.lower()!= "n"):
            print("Enter appropriate instructions")
            return
        res = storage_filtration(ebs, choice_storage_reqs, OStype)[:5]
        if(len(res) == 0):
            print("No matching results.")
            return
        print_instances(res,os_col)
    return
    

def filter(OS, choice_compute, choice_memory_reqs, ebs_storage, choice_storage_reqs):
    query_res = []
    #focus on linux reserved cost for this 
    if(OS.lower() == "linux"):
        OStype = "Linux_Reserved_cost"
        os_col = 7
    elif (OS.lower() == "windows"):
        OStype = "Windows_Reserved_cost"
        os_col = 10
    
    if(choice_compute != "n"):
        res = comp_filtration(choice_compute, OStype)[:5]
        if(len(res) == 0):
            print("No matching results.")
            return
        query_res = query_to_string(res, os_col)

    if(choice_memory_reqs != "n"):
        res = memory_filtration(choice_memory_reqs, OStype)[:5]
        if(len(res) == 0):
            print("No matching results.")
            return
        query_res = query_to_string(res, os_col)
    if(choice_storage_reqs != "n"):
        ebs = False
        if(ebs_storage.lower()== "y"):
            ebs = True
        elif(ebs_storage.lower()!= "n"):
            print("Enter appropriate instructions")
            return
        res = storage_filtration(ebs, choice_storage_reqs, OStype)[:5]
        if(len(res) == 0):
            print("No matching results.")
            return
        query_res = query_to_string(res, os_col)

    return query_res

if __name__ =="__main__":
    main()