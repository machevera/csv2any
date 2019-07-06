

import sys 
import utilex as u
import datetime 
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mpl_dates


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

    csv_filename =p_parameters[0]
    lim_inf = int(p_parameters[1])
    lim_sup = int(p_parameters[2])
    #src_date     =p_parameters[1]      
    #dest_type    =p_parameters[2]
    #dest_filename=p_parameters[3]
   
    plt.style.use('seaborn')

    data = pd.read_csv(csv_filename,sep=";")

    #print(data)
    data['FECHA'] = pd.to_datetime(data['FECHA'])
    data.sort_values('FECHA', inplace=True)

    duration_date = data['FECHA']
    duration = data['DURACION']

    #plt.plot_date(duration_date, duration, linestyle='solid')
    plt.plot(duration_date, duration, linestyle='solid')

    axis_font = {'fontname':'Calibri', 'size':'8'}

    plt.ylim(lim_inf,lim_sup)
    plt.rc('font',size=6)
    plt.gcf().autofmt_xdate()
    date_format = mpl_dates.DateFormatter('%b.%d')
    plt.gca().xaxis.set_major_formatter(date_format)


    plt.title(csv_filename)
    plt.xlabel('Fechas')
    plt.ylabel('Duracion')

    #plt.tight_layout()

    #plt.show()
    plt.savefig(csv_filename + ".png")

if __name__ == '__main__':

    db_filename = 'out/stats.db'
    csv_filename= 'out/stats.csv'
    #sql_filename= 'out/stats.sql'

    main(sys.argv[1:])
