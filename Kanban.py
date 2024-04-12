import csv
import os
import tabulate
b=[]
#os.chdir("Documents/Kanban")
ignore=['.git','.vscode']
working_board=None
path=os.getcwd()
def boards():
    b.clear()
    for dir in os.listdir(path):
#        print(dir)
        if os.path.isdir(dir):
            if dir in ignore:
                continue
            b.append(dir)
    b.sort()
def add_board():
       print("Add Board")
       print("_"*67,"\n")
       name=input("\nEnter board name \n>>").strip()
       if name in b:
           print("Board Already Exists !!!")
           return
       else:
           os.mkdir(name)
           b.append(name)
def ls_boards():
    for i,board in enumerate(b):
        print(f"{i+1}. {board}")
def use_board():
    global working_board , path
    print("Select Board")
    print("_"*67,"\n")
    ls_boards()
    choice=int(input("\n\nEnter Board Number \n>>"))
    print()
    if choice>len(b):
        print("\nEnter valid choice")
    working_board=b[choice-1]
    path=os.path.join(os.getcwd(),working_board)
    os.chdir(path)
    init()

def rm_board():
    for i,board in enumerate(b):
        print(f"{i+1}. {board}")
    choice=int(input("\nEnter Board Number \n>>"))
    print()
    if choice>len(b):
        print("\nEnter valid choice !!!")
        return
    for file in os.listdir(b[choice-1]):
        os.remove(os.path.join(b[choice-1],file))
    os.rmdir(b[choice-1])
def init():
    files=["todo.csv","done.csv","inprogress.csv","queued.csv","waiting.csv"]
    for file in files:
        if not os.path.exists(os.path.join(path,file)):
            with open(file,"w") as f:
                pass               
def name_parser():
    usr=input("\nEnter Names split by comma\n>>")
    names=[]
    for name in usr.split(","):
        names.append(name.strip())
    return names
def add():
    print("Add Task")
    print("_"*67,"\n")
    print("1. ToDo")
    print("2. In Progress")
    print("3. Queued")
    print("4. Waiting")
    print("5. Done")
    choice=int(input("\nEnter type of task\n>>"))-1
    print()
    files=["todo.csv","inprogress.csv","queued.csv","waiting.csv","done.csv"]
    if choice+1>len(files):
        print("\nEnter valid choice !!!")
        return
    file=os.path.join(path,files[choice])
    task=input("\nEnter Task Name\n>>")
    print("Assignees:")
    assign=name_parser()
    print("Reportees:")
    report=name_parser()
    print("Priority:")
    print("1. High")
    print("2. Medium")
    print("3. Low")
    priority=int(input("\nEnter Priority\n>>"))
    with open(file,"r")as f:
        task_id=f"F{choice}-"+str(len(list(csv.reader(f)))+1)
    with open(file,"a") as f:
        writer=csv.writer(f)
        writer.writerow([task_id,task,assign,report,priority])
def pr(i):
    if i == 1:
        return "High"
    elif i==2:
        return "Medium"
    elif i==3:
        return "Low"
def ft(i):
    nbr=int(i.pop())
    p=pr(nbr)
    i.append(p)
    return i
def ls():
    files=["todo.csv","done.csv","inprogress.csv","queued.csv","waiting.csv"]
    for file in files:
        print(f"\n\n{file.capitalize()}\n{'_'*35}\n")
        with open(file,"r") as f:
            reader=csv.reader(f)
            table=[]
            for i in reader:
                table.append(ft(i))
            print(tabulate.tabulate(table,headers=['Task Id','Task Name','Assignees','Reporters','Priority'],tablefmt="fancy_grid"))        
def rmv():
    print("Delete Task")
    print("_"*67,"\n")
    ls()
    id=input("\nEnter Task ID to delete\n>>")
    print()
    files=["todo.csv","inprogress.csv","queued.csv","waiting.csv","done.csv"]
    file=int(id[1])
    with open(files[file],"r") as f:
        reader=csv.reader(f)
        old=list(reader)
    new=[]
    i=1
    for j in old:
        if j[0]==id:
            continue
        j[0]=f"F{file}-{i}"
        new.append(j)
        i+=1
    with open(files[file],"w") as f:
        writer=csv.writer(f)
        writer.writerows(new)        
def mv():
    print("Change Status")
    print("_"*67,"\n")
    ls()
    id=input("\nEnter Task ID to change status\n>>")
    print()
    files=["todo.csv","inprogress.csv","queued.csv","waiting.csv","done.csv"]
    file=int(id[1])
    print("1. ToDo")
    print("2. In Progress")
    print("3. Queued")
    print("4. Waiting")
    print("5. Done")
    choice=int(input("\nEnter new status for the task\n>>"))-1
    with open(files[file],"r") as f:
        reader=csv.reader(f)
        old=list(reader)
#    print(old)
    new=[]
    i=1
    for j in old:
        if j[0]==id:
            popped=j
            continue
        j[0]=f"F{file}-{i}"
        new.append(j)
        i+=1
    with open(files[file],"w") as f:
        writer=csv.writer(f)
        writer.writerows(new)
    if choice+1>len(files):
        print("\nEnter valid choice !!!")
        return
    file_new=os.path.join(path,files[choice])
    with open(file_new,"r")as f:
        task_id=f"F{choice}-"+str(len(list(csv.reader(f)))+1)
    popped[0]=task_id
    with open(file_new,"a") as f:
        writer=csv.writer(f)
        writer.writerow(popped)
boards()
# # add_board()
# use_board()
# init()
# add()
# rmv()
# mv()
# ls()
# rm_board()
#print(path)

def tasks_driver():
    while True:
        print("Task Management System")
        print("_"*67,"\n")
        print("Current Working Board:", working_board,"\n")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Change Task Status")
        print("4. List Tasks")
        print("5. Exit")
        choice = int(input("\nEnter your choice\n>>"))    
        print()
        if choice == 1:
            add()
        elif choice == 2:
            rmv()
        elif choice == 3:
            mv()
        elif choice == 4:
            ls()
        elif choice == 5:
            os.chdir("..")
            path=os.getcwd()
            break
        else:
            print("Invalid choice. Please try again.")

def board_driver():
    while True:
        print("Kanban Board Management System")
        print("_"*67,"\n")
        print("1. Add Board")
        print("2. Use Board")
        print("3. Delete Board")
        print("4. List Boards") 
        print("5. Exit")
        choice = int(input("\nEnter your choice\n>>"))
        print()
        if choice == 1:
            add_board()
        elif choice == 2:
            use_board()
            tasks_driver()
        elif choice == 3:
            rm_board()
        elif choice == 4:
            ls_boards() 
        elif choice == 5:
            break
        else:
            print("Invalid choice. Please try again.")

def main():
    boards()
    board_driver()
    print("\t\tThanks for Trying this program \n\n\t\t  A Program by TBA5854\n")

if __name__ == "__main__":
    main()
