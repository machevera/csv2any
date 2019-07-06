

import sys 
import sqlite3
import utilex as u
import datetime 

#[folder_name,sub_application,memname,jobname,node,ini_str,dur_str]

def load_csv(p_filename, p_date):
    print('... load csv ...')
    print(f"Leyendo Archivo  : {p_filename}")
    print(f"Fecha            : {p_date}")

    #---

    temp = [line.strip().split('|') for line in open(p_filename)]

    temp = [u.striplist(temp) for temp in temp] 

    data=[]
    
    #data.append(["filedate","folder_name","sub_application","memname","jobname","node","start","finish"])

    for row in temp:
        #print(row)
        #fecha de fin
        v_finish_dt = datetime.datetime.strptime(row[5],"%Y%m%d%H%M%S")
        #duracion en centesimas de segundo
        duracion = int(row[6])
        #inicio de job
        v_start_dt = v_finish_dt - datetime.timedelta(seconds=duracion/100)
        #data
        new_row=[p_date,row[0],row[1],row[2],row[3],row[4],v_start_dt.strftime('%Y-%m-%d %H:%M:%S'),v_finish_dt.strftime('%Y-%m-%d %H:%M:%S')]
        #agrego a la lista
        data.append(new_row)

    return data


def register_db(p_data):
    print('... data ...')
    print(f"Registrando BD   : {db_filename}") 
    #---
    sql_command="INSERT INTO malla (file_date,folder_name,sub_application,memname,jobname,node,start_date,end_date) VALUES(?,?,?,?,?,?,?,?)"
    #crea la base de datos
    con = sqlite3.connect(db_filename) # si no esta la crea

    #insert registros
    cur=con.cursor()
    cur.executemany(sql_command, p_data)
    con.commit()

def register_csv(p_data):
    print('... data ...')
    print(f"Registrando CSV  : {csv_filename}") 

    f = open(csv_filename,'a')  
    
    for item in p_data:
        text=','.join(item)
        f.write(text+"\n")
    f.close



def register_sql(p_data,p_dest_filename):
    print('... register sql ...')
    print(f"Escribiendo SQL  : {p_dest_filename}") 
    #---
    sql_command="INSERT INTO malla (file_date,folder_name,sub_application,memname,jobname,node,start_date,end_date) VALUES "
    #crea la base de datos

    f = open(p_dest_filename,'a')  
    
    #configuracion de ejecución
    f.write("SET FEEDBACK OFF" + "\n\n")
    f.write("ALTER SESSION SET NLS_DATE_FORMAT='YYYY-MM-DD HH24:MI:SS' ;" + "\n\n")

    #mapea los comaandos
    sql_commands =[ sql_command + "('"+"','".join(item)+"');" for item in p_data]

    for sql in sql_commands:
        #print(sql)
        f.write(sql+"\n")

    f.close

def main(p_parameters):

   src_filename =p_parameters[0]
   src_date     =p_parameters[1]      
   dest_type    =p_parameters[2]
   dest_filename=p_parameters[3]
   
   if dest_type=='':
       dest_type='ORA'

   data = load_csv(src_filename,src_date)



   if dest_type == 'CSV':
        register_csv(data)    
   elif dest_type == 'DB':
        register_db(data)
   elif dest_type == 'ORA':     
        register_sql(data,dest_filename)
   elif dest_type == 'CON':     
        register_con(data)


if __name__ == '__main__':

    db_filename = 'out/stats.db'
    csv_filename= 'out/stats.csv'
    #sql_filename= 'out/stats.sql'

    main(sys.argv[1:])
