import traceback
import pymysql


def register_company_cloud(confirmed, name, manager, phone, email):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "INSERT INTO companies(confirmed, name, manager, phone" \
          ", email) VALUES('%d', '%s', '%s', '%s', '%s')" % (
              confirmed, name, manager, phone, email)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        # Error rollback
        traceback.print_exc()
        db.rollback()
        return False
    # Close database connection
    db.close()
    return True


def register_successful_cloud(id):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "UPDATE companies SET confirmed = '%d' WHERE id = '%d'" % (1, id)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        # Error rollback
        traceback.print_exc()
        db.rollback()
        return False
    # Close database connection
    db.close()
    return True


def new_activity_cloud(name, time, place, describe, organizer, announcer_id):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "INSERT INTO activities(name, time, place, " \
          "`describe`, organizer, announcer_id) " \
          "VALUES('%s', '%s', '%s', '%s', '%s', '%d')" % \
          (name, time, place, describe, organizer, announcer_id)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        # Error rollback
        traceback.print_exc()
        db.rollback()
        return False
    # Close database connection
    db.close()
    return True


def new_want_cloud(uid, aid, time):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "INSERT INTO want(wanter_id, wanted_activity_id, time) " \
          "VALUES('%d', '%d', '%s')" % (uid, aid, time)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        # Error rollback
        traceback.print_exc()
        db.rollback()
        return False
    # Close database connection
    db.close()
    return True


def not_want_cloud(uid):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "DELETE FROM want WHERE wanter_id = '%d'" % (uid)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        # Error rollback
        traceback.print_exc()
        db.rollback()
        return False
    # Close database connection
    db.close()
    return True


def delete_activity_cloud(id):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "DELETE FROM activities WHERE id = '%d'" % (id)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        # Error rollback
        traceback.print_exc()
        db.rollback()
        return False
    # Close database connection
    db.close()
    return True
