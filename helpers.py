import re
import psycopg2

def sql_feed(hostname, database, username, pwd, port_id, state):
    # hostname = 'localhost', database = 'brandon', username = 'brandon', pwd = 'Br@0nat9am', port_id = 5433
    conn = None
    cur = None
    try:
        print("started try block")
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id
        )

        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS drone_data')

        create_script = ''' CREATE TABLE IF NOT EXISTS drone_data (
                                id BIGSERIAL PRIMARY KEY NOT NULL,
                                pitch FLOAT NOT NULL,
                                roll FLOAT NOT NULL,
                                yaw FLOAT NOT NULL,
                                xvelocity FLOAT NOT NULL,
                                yvelocity FLOAT NOT NULL,
                                zvelocity FLOAT NOT NULL, 
                                lowtemp FLOAT NOT NULL,
                                hightemp FLOAT NOT NULL,
                                tof FLOAT NOT NULL,
                                height FLOAT NOT NULL,
                                battery FLOAT NOT NULL,
                                barometer FLOAT NOT NULL,
                                time FLOAT NOT NULL,
                                xacc FLOAT NOT NULL,
                                yacc FLOAT NOT NULL,
                                zacc FLOAT NOT NULL)'''
        cur.execute(create_script)


        insert_script = '''INSERT INTO drone_data (pitch, roll, yaw, xvelocity, yvelocity, zvelocity, lowtemp, hightemp, 
                            tof, height, battery, barometer, time, xacc, yacc, zacc) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        cur.execute(insert_script, state)

        # insert_values = [(243, 54.2, 43543, 243, 54.2, 43543, 243, 54.2, 43543, 243, 54.2, 43543, 243, 54.2, 43543, 54.777),  # example how to insert multiple states
        #                 (554, .99542, 4342423543, .3000243, 58444.2, 43, 2, 4.2, 3, 23, 5, 3, 2, 2, 3, 4.7)]
        # for record in insert_values:
        #     cur.execute(insert_script, record)

        conn.commit()  # to actually save the database changes
        print("committed to table")
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
            print('Successful insertion into table')

def state_formatter(state, complete):
    final_vals_lst = []
    val_lst = re.split("\;", state)
    desired_val_inds = list(range(0,16))
    if (not complete):
        desired_val_inds = [0,1,2,9]
    for i in desired_val_inds:
        final_vals_lst.append(float(val_lst[i].split(":")[1]))
    return tuple(final_vals_lst)

def main():
    print(state_formatter('pitch:0.03243;roll:0;yaw:121;vgx:0;vgy:0;vgz:0;templ:93;temph:96;tof:6553;h:0;bat:72;baro:-51.69;time:0;agx:-1.00;agy:2.00;agz:-1000.00;\r\n', True))
    sql_feed('localhost', 'brandon', 'brandon', 'Br@0nat9am', '5433', (0.03243, 0.0, 121.0, 0.0, 0.0, 0.0, 93.0, 96.0, 6553.0, 0.0, 72.0, -51.69, 0.0, -1.0, 2.0, -1000.0))
if __name__ == '__main__':
    main()