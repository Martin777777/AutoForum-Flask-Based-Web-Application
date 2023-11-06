import traceback
import pymysql


def new_transaction_cloud(time, car_name, car_describe, link, transaction_mode, is_sold, contact, seller_id):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "INSERT INTO transaction(time, car_name, car_describe" \
          ", link, transaction_mode, is_sold, contact, seller_id)" \
          " VALUES('%s', '%s', '%s', '%s', '%s', '%d', '%s', '%d')" \
          % (time, car_name, car_describe, link, transaction_mode, is_sold, contact, seller_id)
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


def sold_item_cloud(id):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "UPDATE transaction SET is_sold = '%d' WHERE id = '%d'" % (1, id)
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


def collect_cloud(cid, tid, time):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "INSERT INTO collect(collecter_id, collected_transaction_id, time) " \
          "VALUES('%d', '%d', '%s')" % (cid, tid, time)
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


def not_collect_cloud(uid):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "DELETE FROM collect WHERE collecter_id = '%d'" % (uid)
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


def delete_transaction_cloud(id):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "DELETE FROM transaction WHERE id = '%d'" % (id)
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
