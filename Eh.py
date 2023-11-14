import sqlite3

Errorlist = []

def Check_Format(check_string):
    if r"'" in check_string:
        checked_string = check_string.replace(r"'", r"\'")
        return checked_string
    elif '\"' in check_string:
        checked_string = check_string.replace('\"', r'\"')
        return checked_string
    else:
        return check_string


target_db_connect = sqlite3.connect('./.db')    #目标数据库
target_db = target_db_connect.cursor()

source_db_connect = sqlite3.connect('./.db')    #源数据库
source_db = source_db_connect.cursor()

source_db_copy_connect = sqlite3.connect('./.db')   #备份一份源数据库
source_copy_db = source_db_copy_connect.cursor()

source_db_data = source_db.execute("select * from galleries;")

for source_data in source_db_data:
    source_gid = source_data[0]
    source_token = source_data[1]
    source_title = source_data[2]
    source_title_jp = source_data[3]
    source_thumb = source_data[4]
    source_category = source_data[5]
    source_posted = source_data[6]
    source_uploader = source_data[7]
    source_rating = source_data[8]
    source_language = source_data[9]
    print(source_gid, source_token)

    if source_language == "None":
        source_language = "NULL"

    target_db_check_sql = "select * from downloads where gid = " + str(source_gid) + ";"
    target_db_data = target_db.execute(target_db_check_sql)

    target_check = len(list(target_db_data))
    if target_check != 0:
        continue

    source_db_downloads_sql = "select * from downloads where gid =  " + str(source_gid) + ";"
    source_db_downloads_data = source_copy_db.execute(source_db_downloads_sql)
    source_check = len(list(source_db_downloads_data))

    if source_check == 0:
        source_state = 3
        source_legacy = 0
        source_time = 0
        source_position = None
    else:
        copy_db_sql = "select * from downloads where gid =  " + str(source_gid) + ";"
        copy_db_data = source_copy_db.execute(copy_db_sql)
        for copy_data in copy_db_data:
            source_state = copy_data[1]
            source_legacy = copy_data[2]
            source_time = copy_data[3]
            source_position = copy_data[5]
            print(source_state)

    target_insert_sql = "insert into downloads(gid, token, title, title_jpn, thumb, category, posted, uploader, " \
                        "rating, simple_language, state, legacy, time, label) Values('%d', '%s', '%s', '%s', '%s', '%d', " \
                        "'%s', '%s', '%f', '%s', '%d', '%d', '%d', '%s')" \
                        % (source_gid, str(source_token), str(source_title), str(source_title_jp), str(source_thumb),
                           source_category,
                           source_posted, str(source_uploader), source_rating, source_language, source_state,
                           source_legacy, source_time, "NULL")

    print(target_insert_sql)

    try:
        target_db.execute(target_insert_sql)
    except:
        try:
            target_insert_sql = "insert into downloads(gid, token, title, title_jpn, thumb, category, posted, uploader, " \
                                "rating, simple_language, state, legacy, time, label) Values('%d', '%s', '%s', '%s', '%s', '%d', " \
                                "'%s', '%s', '%f', '%s', '%d', '%d', '%d', '%s')" \
                                % (source_gid, str(source_token), "NULL", "NULL",
                                   str(source_thumb),
                                   source_category,
                                   source_posted, str(source_uploader), source_rating, source_language, source_state,
                                   source_legacy, source_time, "NULL")
            target_db.execute(target_insert_sql)
        except:
            Errorlist.append(source_gid)

'''

for row in target_db_data:
    print(row)
'''
target_db_connect.commit()
target_db_connect.close()
source_db_connect.close()
source_db_copy_connect.close()

with open("./test.txt", "w") as f:
    for eachline in Errorlist:
        f.write(str(eachline) + "\n")