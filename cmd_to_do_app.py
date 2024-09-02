import sqlite3
import datetime

def db_connect():
    db=sqlite3.connect('cmd_based_todo.db')
    db.execute('CREATE TABLE IF NOT EXISTS Tasks (task_id INTEGER PRIMARY KEY, task_name TEXT, task_description TEXT, task_status TEXT, task_creation_date TEXT, task_priority TEXT)')
    db.close()
# task_id primary key, task_name, task_description, task_status, task_due_date, task_priority,

class To_Do:
    def __init__(self) -> None:
        pass
    def add_task(self,task):
        try:
            with sqlite3.connect('cmd_based_todo.db') as db:
                cursor=db.cursor()
                cursor.execute('INSERT INTO Tasks (task_name,task_description,task_status,task_creation_date,task_priority) VALUES (?,?,?,?,?)',(task.task_name,task.task_description,task.task_status,task.task_creation_date,task.task_priority))
                db.commit()
                print(f'Task {task.task_name} has been created')

        except Exception as e:
            return print('Error: '+str(e))

    def show_task_by_id(self):
        try:
            records=''
            with sqlite3.connect('cmd_based_todo.db') as db:
                db.row_factory=sqlite3.Row
                cursor=db.cursor()
                cursor.execute('SELECT * FROM Tasks WHERE task_status="Incomplete"')
                records=cursor.fetchall()


        except Exception as e:
            db.rollback()
            return print('Error: '+str(e))
        finally:
            db.close()
            for item in records:
                print(dict(item))
                

    def show_completed_tasks(self):
        records=''
        try:
            with sqlite3.connect('cmd_based_todo.db') as db:
                db.row_factory=sqlite3.Row
                cursor=db.cursor()
                cursor.execute('SELECT * FROM Tasks WHERE task_status="COMPLETE" ')
                records=cursor.fetchall()
        

        except Exception as e:
            db.rollback()
            return print('Error: '+str(e))

        finally:
            for i in records:
                print(dict(i))


    def show_task_by_priority(self):
        pass

    def task_completed(self,task_id):
        
        
        try:
            task_status='COMPLETE'
            with sqlite3.connect('cmd_based_todo.db') as db:
                cursor=db.cursor()
                cursor.execute('''UPDATE Tasks SET task_status=? WHERE task_id=? ''',(task_status,task_id))
                db.commit()

                if cursor.rowcount == 0:
                    return print('No id found in the database')
                else:
                    return print('Task has been completed!')
        except Exception as e:
            db.rollback()
            return('Error: '+str(e))
        

    def delete_task(self,task_id):
        
        try:
            with sqlite3.connect('cmd_based_todo.db') as db:
                cursor=db.cursor()
                cursor.execute('DELETE FROM Tasks WHERE task_id=? ',(task_id,))
                db.commit()

                if cursor.rowcount==0:
                    return print('No task found with this id')
                else:
                    return print('Task has been successfuly removed!')
        except Exception as e:
            db.rollback()
            return print("Error: "+str(e))

class Task:
    def __init__(self,task_name,task_description,task_status,task_creation_date,task_priority):
        self.task_name=task_name
        self.task_description=task_description
        self.task_status=task_status
        self.task_creation_date=task_creation_date
        self.task_priority=task_priority


    
if __name__=='__main__':
    print('Welcome to the To-Do app!')
    db_connect()
    while True:
        
        to_do_instance=To_Do()
        

        

        command_input=input(f'\nPlease insert your command: \n1. View all tasks in id order\n2. View all tasks in priority order\n3.Add new task\n4. Mark task as completed(provide task id)\n5. Delete task from To-Do((provide task id)\n6. Show completed tasks\n7. Exit app)\n: ')
        
        while command_input not in [str(i) for i in range(1,8)]:
            command_input=input(f'\nPlease insert your command: \n1. View all tasks in id order\n2. View all tasks in priority order\n3.Add new task\n4. Mark task as completed(provide task id)\n5. Delete task from To-Do((provide task id)\n6. Show completed tasks\n7. Exit app)\n: ')
        
        if command_input=='1':
            to_do_instance.show_task_by_id()
                
        elif command_input=='3':
            task_name=input('Task name: ')
            while task_name==" " or task_name=="":
                task_name=input('Task name cant be blank: ')
            task_description=input('Task description: ')
            task_status='Incomplete'
            task_creation_date=str(datetime.datetime.now())
            task_priority=input('Task priority LOW/MID/HIGH: ')
            while task_priority!='LOW' and task_priority!='MID' and task_priority!='HIGH':
                    task_priority=input('Task priority LOW/MID/HIGH: ')

            
            task_instance=Task(task_name,task_description,task_status,task_creation_date,task_priority)
            to_do_instance.add_task(task_instance)



        elif command_input=='4':
            task_id=''
            while task_id.isdigit()==False:
                task_id=input('Please input task id (must be integer): ')
            to_do_instance.task_completed(int(task_id))

        elif command_input=='5':
            task_id=''

            while task_id.isdigit()==False:
                task_id=input('Please provide a valid task id: ')
            to_do_instance.delete_task(task_id)

        elif command_input=='6':
            to_do_instance.show_completed_tasks()
        
        
        elif command_input=='7':
            break
        
