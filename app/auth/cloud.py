import traceback
import pymysql


def register_cloud(confirmed, email, username, password_hash, about_me, avater_img):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "INSERT INTO users(confirmed, email, username, password_hash" \
          ", about_me, avatar_img) VALUES('%d', '%s', '%s', '%s', '%s', '%s')" % (
              confirmed, email, username, password_hash, about_me, avater_img)
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


def confirm_cloud(email):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "UPDATE users SET confirmed = '%d' WHERE email = '%s'" % (1, email)
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


def reset_password_cloud(password, email):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "UPDATE users SET password_hash = '%d' WHERE email = '%s'" % (password, email)
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


def change_password_cloud(password, email):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "UPDATE users SET password_hash = '%d' WHERE email = '%s'" % (password, email)
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


def change_email_cloud(newemail, email):
    db = pymysql.connect(host="bj-cdb-gz290k7a.sql.tencentcdb.com", port=60405, user="root", password="i4gotitABC",
                         db="Car")
    cursor = db.cursor()
    sql = "UPDATE users SET email = '%d' WHERE email = '%s'" % (newemail, email)
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
