import json
import sqlite3
import threading
import os
import pickle
import time
import requests

lock = threading.Lock()


def get_courses():
    a = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    usd = a.json()['Valute']['USD']['Value']
    eur = a.json()['Valute']['EUR']['Value']
    returns = [usd, eur]
    return returns

class DB:
    def __init__(self, database):
        self.connection = sqlite3.connect(database, check_same_thread=False)
        self.cursor = self.connection.cursor()

        self.connection.isolation_level = None


    def add_user(self, user_id, username, ref_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT user_id FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result == None:
                    self.cursor.execute('INSERT INTO users (user_id, username, status, balance, ref_balance, ref_id, pay_count, new_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id, username, 'reg', '0', '0', ref_id, 0, 'Новый покупатель'))
                    return
                else:
                    return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    
    def check_userstat(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT status FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result == None:
                    return None
                else:
                    if result[0] == 'rules':
                        return 'rules'
                    elif result[0] == 'ok':
                        return 'ok'
                    elif result[0] == 'ban':
                        return 'ban'
                    elif result[0] == 'reg':
                        return 'reg'
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_status(self, user_id, status):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET status=? WHERE user_id=?', (status, user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_all_faq(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT lan FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result[0] == 'en':
                    self.cursor.execute('SELECT id, eng_name FROM faq')
                    result = self.cursor.fetchall()
                    return result
                else:
                    self.cursor.execute('SELECT id, name FROM faq')
                    result = self.cursor.fetchall()
                    return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_all_faq_adm(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name FROM faq')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_faq(self, name, eng_name, text, eng_text, photo):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO faq (name, eng_name, text, eng_text, photo) VALUES (?, ?, ?, ?, ?)', (name, eng_name, text, eng_text, photo))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_faq(self, faqid, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT lan FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result[0] == 'en':
                    self.cursor.execute('SELECT eng_name, eng_text, photo FROM faq WHERE id=?', (faqid,))
                    result = self.cursor.fetchone()
                    return result
                else:
                    self.cursor.execute('SELECT name, text, photo FROM faq WHERE id=?', (faqid,))
                    result = self.cursor.fetchone()
                    return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_faq_adm(self, faqid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name, text, photo FROM faq WHERE id=?', (faqid,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changefaq_name(self, faqid, name, eng_name):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE faq SET name=?, eng_name=? WHERE id=?', (name, eng_name, faqid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changefaq_text(self, faqid, text, eng_text):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE faq SET text=?, eng_text WHERE id=?', (text, eng_text, faqid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_faq(self, faqid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM faq WHERE id=?', (faqid,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_all_cat(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT lan FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result[0] == 'en':
                    self.cursor.execute('SELECT en FROM lanset')
                    lantp = self.cursor.fetchone()
                    if lantp[0] == 1:
                        self.cursor.execute('SELECT id, eng_name FROM categories')
                        result = self.cursor.fetchall()
                    else:
                        self.cursor.execute('SELECT id, name FROM categories')
                        result = self.cursor.fetchall()
                    return result
                else:
                    self.cursor.execute('SELECT ru FROM lanset')
                    lantp = self.cursor.fetchone()
                    if lantp[0] == 1:
                        self.cursor.execute('SELECT id, name FROM categories')
                        result = self.cursor.fetchall()
                    else:
                        self.cursor.execute('SELECT id, eng_name FROM categories')
                        result = self.cursor.fetchall()
                    return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_all_cat_adm(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name FROM categories')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_cat(self, name, eng_name):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO categories (name, eng_name) VALUES (?, ?)', (name, eng_name))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_subcat(self, catid, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT lan FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result[0] == 'en':
                    self.cursor.execute('SELECT en FROM lanset')
                    lantp = self.cursor.fetchone()
                    if lantp[0] == 1:
                        self.cursor.execute('SELECT id, eng_name FROM subcategories WHERE categoryid=?', (catid,))
                        result = self.cursor.fetchall()
                    else:
                        self.cursor.execute('SELECT id, eng_name FROM subcategories WHERE categoryid=?', (catid,))
                        result = self.cursor.fetchall()
                    return result
                else:
                    self.cursor.execute('SELECT ru FROM lanset')
                    lantp = self.cursor.fetchone()
                    if lantp[0] == 1:
                        self.cursor.execute('SELECT id, name FROM subcategories WHERE categoryid=?', (catid,))
                        result = self.cursor.fetchall()
                    else:
                        self.cursor.execute('SELECT id, eng_name FROM subcategories WHERE categoryid=?', (catid,))
                        result = self.cursor.fetchall()
                    return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_subcat_adm(self, catid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name FROM subcategories WHERE categoryid=?', (catid,))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_subcat(self, catid, name, eng_name):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO subcategories (categoryid, name, eng_name) VALUES (?, ?, ?)', (catid, name, eng_name))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_goods(self, subcatid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name FROM goods WHERE subcategoryid=?', (subcatid,))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_cat_name(self, catid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name FROM categories WHERE id=?', (catid,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_subcat_name(self, subcatid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name FROM subcategories WHERE id=?', (subcatid,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changename_cat(self, catid, name, eng_name):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE categories SET name=?, eng_name=? WHERE id=?', (name, eng_name, catid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changename_subcat(self, subcatid, name, eng_name):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE subcategories SET name=?, eng_name=? WHERE id=?', (name, eng_name, subcatid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_good(self, subcatid, name, eng_name, description, eng_desc, photo, price, currency):
        with self.connection:
            try:
                lock.acquire(True)
                courses = get_courses()
                if currency == "rub":
                    price_eur = str(float(price)/float(courses[1]))
                    price_usd = str(float(price)/float(courses[0]))
                elif currency == "usd":
                    price_usd = str(price)
                    price = str(float(price)*float(courses[0]))
                    price_eur = str(float(price)/float(courses[1]))
                elif currency == "eur":
                    price_eur = str(price)
                    price = str(float(price)*float(courses[1]))
                    price_usd = str(float(price)/float(courses[0]))
                self.cursor.execute('INSERT INTO goods (subcategoryid, name, eng_name, description, eng_desc, price, photo, price_usd, price_eur) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (subcatid, name, eng_name, description, eng_desc, price, photo, price_usd, price_eur))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_goodinfo(self, goodid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name, description, price, photo FROM goods WHERE id=?', (goodid,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_namegood(self, goodid, name, eng_name):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE goods SET name=?, eng_name=? WHERE id=?', (name, eng_name, goodid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_descgood(self, goodid, desc, eng_desc):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE goods SET description=?, eng_desc=? WHERE id=?', (desc, eng_desc, goodid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_pricegood(self, goodid, price, currency):
        with self.connection:
            try:
                lock.acquire(True)
                courses = get_courses()
                if currency == "rub":
                    price_eur = str(float(price)/float(courses[1]))
                    price_usd = str(float(price)/float(courses[0]))
                elif currency == "usd":
                    price_usd = str(price)
                    price = str(float(price)*float(courses[0]))
                    price_eur = str(float(price)/float(courses[1]))
                elif currency == "eur":
                    price_eur = str(price)
                    price = str(float(price)*float(courses[1]))
                    price_usd = str(float(price)/float(courses[0]))
                self.cursor.execute('UPDATE goods SET price=? WHERE id=?', (price, goodid))
                self.cursor.execute('UPDATE goods SET price_usd=? WHERE id=?', (price_usd, goodid))
                self.cursor.execute('UPDATE goods SET price_eur=? WHERE id=?', (price_eur, goodid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_good(self, goodid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT photo FROM goods WHERE id=?', (goodid,))
                result = self.cursor.fetchone()
                if result[0] == 'None':
                    self.cursor.execute('DELETE FROM goods WHERE id=?', (goodid,))
                else:
                    try:
                        os.remove(f'images/{result[0]}')
                    except:
                        pass
                    self.cursor.execute('DELETE FROM goods WHERE id=?', (goodid,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()
    def get_namecat(self, catid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name FROM categories WHERE id=?', (catid,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_cat(self, catid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id FROM subcategories WHERE categoryid=?', (catid,))
                result = self.cursor.fetchall()
                for i in result:
                    self.cursor.execute('DELETE FROM goods WHERE subcategoryid=?', (i[0],))
                self.cursor.execute('DELETE FROM subcategories WHERE categoryid=?', (catid,))
                self.cursor.execute('DELETE FROM categories WHERE id=?', (catid,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_namesubcat(self, subcatid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name FROM subcategories WHERE id=?', (subcatid,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_subcat(self, subcatid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM goods WHERE subcategoryid=?', (subcatid,))
                self.cursor.execute('DELETE FROM subcategories WHERE id=?', (subcatid,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def check_goods(self, subcatid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name FROM goods WHERE subcategoryid=?', (subcatid,))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_goods_user(self, subcatid, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT lan FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                self.cursor.execute('SELECT currency FROM curryncyset WHERE status=?', (1,))
                curr = self.cursor.fetchone()[0]
                if result[0] == 'en':
                    self.cursor.execute('SELECT en FROM lanset')
                    lantp = self.cursor.fetchone()
                    if lantp[0] == 1:
                        if curr == 'rub':
                            self.cursor.execute('SELECT id, eng_name, eng_desc, price, photo FROM goods WHERE subcategoryid=?', (subcatid,))
                        else:
                            self.cursor.execute(f'SELECT id, eng_name, eng_desc, price_{curr}, photo FROM goods WHERE subcategoryid=?', (subcatid,))
                        result = self.cursor.fetchall()
                    else:
                        if curr == 'rub':
                            self.cursor.execute('SELECT id, name, description, price, photo FROM goods WHERE subcategoryid=?', (subcatid,))
                        else:
                            self.cursor.execute(f'SELECT id, name, description, price_{curr}, photo FROM goods WHERE subcategoryid=?', (subcatid,))
                        result = self.cursor.fetchall()
                    return result
                else:
                    self.cursor.execute('SELECT ru FROM lanset')
                    lantp = self.cursor.fetchone()
                    if lantp[0] == 1:
                        if curr == 'rub':
                            self.cursor.execute('SELECT id, name, description, price, photo FROM goods WHERE subcategoryid=?', (subcatid,))
                        else:
                            self.cursor.execute(f'SELECT id, name, description, price_{curr}, photo FROM goods WHERE subcategoryid=?', (subcatid,))
                        result = self.cursor.fetchall()
                    else:
                        if curr == 'rub':
                            self.cursor.execute('SELECT SELECT id, eng_name, eng_desc, price, photo FROM goods WHERE subcategoryid=?', (subcatid,))
                        else:
                            self.cursor.execute(f'SELECT SELECT id, eng_name, eng_desc, price_{curr}, photo FROM goods WHERE subcategoryid=?', (subcatid,))
                        result = self.cursor.fetchall()
                    return result
            except:
                self.connection.rollback()
            finally:
                lock.release()
    def add_box(self, user_id, goodid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO box (user_id, goodid) VALUES (?, ?)', (user_id, goodid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_box(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT goodid FROM box WHERE user_id=?', (user_id,))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_good_info(self, goodid, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT lan FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                self.cursor.execute('SELECT currency FROM curryncyset WHERE status=?', (1,))
                curr = self.cursor.fetchone()[0]
                if result[0] == 'en':
                    if curr == 'rub':
                        self.cursor.execute('SELECT eng_name, price FROM goods WHERE id=?', (goodid,))
                    else:
                        self.cursor.execute(f'SELECT eng_name, price_{curr} FROM goods WHERE id=?', (goodid,))
                    result = self.cursor.fetchone()
                    return result
                else:
                    if curr == 'rub':
                        self.cursor.execute('SELECT name, price FROM goods WHERE id=?', (goodid,))
                    else:
                        self.cursor.execute(f'SELECT name, price_{curr} FROM goods WHERE id=?', (goodid,))
                    result = self.cursor.fetchone()
                    return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_box_good(self, goodid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM box WHERE goodid=?', (goodid,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def boxlclear(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM box WHERE user_id=?', (user_id,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_supports(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT supports FROM supports WHERE id=1')
                result = self.cursor.fetchone()
                result = json.loads(result[0])
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def update_supports(self, whatToDo, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                if whatToDo == "delete":
                    self.cursor.execute('SELECT supports FROM supports WHERE id=1')
                    result = self.cursor.fetchone()
                    resultList = json.loads(result[0])
                    resultList.remove(user_id)
                    newList = json.dumps(resultList)
                    self.cursor.execute('UPDATE supports SET supports=? WHERE id=1', (newList, ))
                    return
                elif whatToDo == "add":
                    self.cursor.execute('SELECT supports FROM supports WHERE id=1')
                    result = self.cursor.fetchone()
                    resultList = json.loads(result[0])
                    resultList.append(user_id)
                    newList = json.dumps(resultList)
                    self.cursor.execute('UPDATE supports SET supports=? WHERE id=1', (newList, ))
                    return
            except:
                self.connection.rollback()
                return Exception
            finally:
                lock.release()

    def get_balance(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result[0] == None:
                    return 0
                else:
                    return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_user_refbalance(self, user_id, currency):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT ref_balance FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                courses = get_courses()

                if result[0] == None:
                    return 0
                else:
                    if currency == "rub":
                        return result[0]
                    elif currency == "usd":
                        return (float(result[0])/float(courses[0]))
                    elif currency == "eur":
                        return (float(result[0])/float(courses[1]))
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def obnyl_refbal(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET ref_balance=? WHERE user_id=?', ('0', user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_refproc(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT ref FROM admin')
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_refproc_for_user(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)

                self.cursor.execute('SELECT ref FROM admin')
                globalRef = self.cursor.fetchone()
                globalRef = globalRef[0]

                self.cursor.execute('SELECT ref_procent FROM users WHERE user_id=?', (user_id,))
                personalRefResult = self.cursor.fetchone()
                personalRefResult = personalRefResult[0]

                if personalRefResult == None:
                    personalRef =  0
                else:
                    personalRef = int(personalRefResult)
                
                if int(personalRef) != int(globalRef) and personalRefResult != None:
                    return personalRef
                else:
                    return globalRef
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_ref(self, ref):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE admin SET ref=?', (ref,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_waitorders(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                tovars = []
                self.cursor.execute('SELECT tovars, types FROM orders WHERE user_id=? AND status=? ORDER BY id DESC LIMIT 1', (user_id, 'wait'))
                result = self.cursor.fetchall()
                for i in result:
                    a = pickle.loads(i[0])
                    tovars.append(a)
                return [tovars, result[0][1]]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_reply_id(self, type):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT msg_id FROM orders WHERE types=? LIMIT 1', (type, ))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()                

    def get_actorders(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                tovars = []
                self.cursor.execute('SELECT tovars FROM orders WHERE user_id=? AND status=? LIMIT 2', (user_id, 'active'))
                result = self.cursor.fetchall()
                for i in result:
                    a = pickle.loads(i[0])
                    tovars.append(a)            
                return tovars
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_endorders(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                tovars = []
                self.cursor.execute('SELECT tovars FROM orders WHERE user_id=? AND status=? ORDER BY id DESC LIMIT 2', (user_id, 'end'))
                result = self.cursor.fetchall()
                for i in result:
                    a = pickle.loads(i[0])
                    tovars.append(a)            
                return tovars
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_order(self, user_id, tovars, adress, comment, promocode):
        with self.connection:
            try:
                lock.acquire(True)
                tovars = pickle.dumps(tovars)
                self.cursor.execute('INSERT INTO orders (user_id, status, tovars, adress, comment, time_of_creating, promo) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, 'wait', tovars, adress, comment, time.time(), promocode))
                self.cursor.execute('SELECT id FROM orders WHERE user_id=? ORDER BY id DESC LIMIT 1', (user_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def remove_old_orders(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM orders WHERE time_of_creating<? AND status=?', ((int(time.time()) - 18000), "wait"))
                print("canceled")
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()


    def upd_ordertype(self, order_id, types):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE orders SET types=? WHERE id=?', (types, order_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def upd_msg_id(self, order_id, msg_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE orders SET msg_id=? WHERE id=?', (msg_id, order_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()


    def pay_order(self, order_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE orders SET status=? WHERE id=?', ('active', order_id))
                self.cursor.execute('SELECT user_id FROM orders WHERE id=?', (order_id,))
                usr = self.cursor.fetchone()
                self.cursor.execute('UPDATE users SET pays=?, pay_count=pay_count+1 WHERE user_id=?', ('yes', usr[0]))
                self.cursor.execute('SELECT pay_count FROM users WHERE user_id=?', (usr[0],))
                result = self.cursor.fetchone()[0]
                if result == None or result <5:
                    return
                elif result >4 and result <10:
                    self.cursor.execute('UPDATE users SET procent=? WHERE user_id=?', ('5', usr[0]))
                elif result >9 and result < 15:
                    self.cursor.execute('UPDATE users SET procent=? WHERE user_id=?', ('10', usr[0]))
                elif result >14:
                    self.cursor.execute('UPDATE users SET procent=? WHERE user_id=?', ('15', usr[0]))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_order_status(self, order_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT status FROM orders WHERE id=?', (order_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def pay_balance(self, user_id, amount):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                bal = float(result[0]) - float(amount)
                self.cursor.execute('UPDATE users SET balance=? WHERE user_id=?', (bal, user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_referal(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT ref_id FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_balance(self, user_id, amount):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT balance FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                bal = float(result[0]) + float(amount)
                self.cursor.execute('UPDATE users SET balance=? WHERE user_id=?', (bal, user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_refbalance(self, user_id, amount):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT ref_balance FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                bal = float(result[0]) + float(amount)
                self.cursor.execute('UPDATE users SET ref_balance=? WHERE user_id=?', (bal, user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_all_activeorders(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id FROM orders WHERE status=?', ('active',))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_order_info(self, order_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT tovars, adress, comment, photo FROM orders WHERE id=?', (order_id,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_order_userid(self, order_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT user_id FROM orders WHERE id=?', (order_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def order_end(self, order_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE orders SET status=? WHERE id=?', ('end', order_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def order_cancel(self, order_id, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE orders SET status=? WHERE id=?', ('cancel', order_id))
                result = self.cursor.fetchone()
                self.cursor.execute('UPDATE users SET pay_count=pay_count-1 WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_users_pay(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT user_id FROM users WHERE pays=?', ('yes',))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_all_users(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT user_id FROM users')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_all_users(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, user_id FROM users ORDER BY id ASC')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_user_info(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT username, balance, pay_count FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def ban_user(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET status=? WHERE user_id=?', ('ban', user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def unban_user(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET status=? WHERE user_id=?', ('ok', user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def check_ban(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT status FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result[0] == 'ban':
                    return False
                else:
                    return True
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_all_refs(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT user_id FROM users WHERE ref_id=?', (user_id,))
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_order_price(self, order_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT tovars FROM orders WHERE id=?', (order_id,))
                result = self.cursor.fetchone()
                a = pickle.loads(result[0])
                return a
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_adm_delivery(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, name, status FROM delivery')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_delivery_adm(self, name, engname, cost, currency):
        with self.connection:
            try:
                lock.acquire(True)
                course = get_courses()

                if currency == "rub":
                    usd = float(cost)/float(course[0])
                    eur = float(cost)/float(course[1])
                elif currency == "usd":
                    usd = float(cost)
                    cost = float(cost)*float(course[0])
                    eur = float(cost)/float(course[1])
                elif currency == "eur":
                    eur = float(cost)
                    cost = float(cost)*float(course[1])
                    usd = float(cost)/float(course[0])

                usd = str(float('{:.2f}'.format(usd)))
                eur = str(float('{:.2f}'.format(eur)))
                cost = str(float('{:.2f}'.format(cost)))
                self.cursor.execute('INSERT INTO delivery (name, eng_name, cost, status, cost_usd, cost_eur) VALUES (?, ?, ?, ?, ?, ?)', (name, engname, cost, 'off', usd, eur))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_delivery_info(self, delid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name, cost, status FROM delivery WHERE id=?', (delid,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()
    def get_delivery_infouser(self, delid, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT lan FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                self.cursor.execute('SELECT currency FROM curryncyset WHERE status=?', (1,))
                curr = self.cursor.fetchone()[0]
                if result[0] == 'en':
                    if curr == 'rub':
                        self.cursor.execute('SELECT eng_name, cost, status FROM delivery WHERE id=?', (delid,))
                    else:
                        self.cursor.execute(f'SELECT eng_name, cost_{curr}, status FROM delivery WHERE id=?', (delid,))
                    result = self.cursor.fetchone()
                    return result
                else:
                    if curr == 'rub':
                        self.cursor.execute('SELECT name, cost, status FROM delivery WHERE id=?', (delid,))
                    else:
                        self.cursor.execute(f'SELECT name, cost_{curr}, status FROM delivery WHERE id=?', (delid,))
                    result = self.cursor.fetchone()
                    return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def delivery_stat(self, delid, status):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE delivery SET status=? WHERE id=?', (status, delid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_delivery_name(self, delid, name, engname):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE delivery SET name=?, eng_name=? WHERE id=?', (name, engname, delid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_delivery_cost(self, delid, cost, currency):
        with self.connection:
            try:
                lock.acquire(True)
                courses = get_courses()
                price = cost

                if currency == "rub":
                    price_eur = float(price)/float(courses[1])
                    price_usd = float(price)/float(courses[0])
                elif currency == "usd":
                    price_usd = float(price)
                    price = float(price)*float(courses[0])
                    price_eur = float(price)/float(courses[1])
                elif currency == "eur":
                    price_eur = float(price)
                    price = float(price)*float(courses[1])
                    price_eur = float(price)/float(courses[0])

                price_usd = str(float('{:.2f}'.format(price_usd)))
                eur = str(float('{:.2f}'.format(eur)))
                price = str(float('{:.2f}'.format(price)))

                self.cursor.execute('UPDATE delivery SET cost=? WHERE id=?', (price, delid))
                self.cursor.execute('UPDATE delivery SET cost_usd=? WHERE id=?', (price_usd, delid))
                self.cursor.execute('UPDATE delivery SET cost_usd=? WHERE id=?', (price_eur, delid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_deliveryuser(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT lan FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                self.cursor.execute('SELECT currency FROM curryncyset WHERE status=?', (1,))
                curr = self.cursor.fetchone()[0]
                if result[0] == 'en':
                    if curr == 'rub':
                        self.cursor.execute('SELECT id, eng_name, cost FROM delivery WHERE status=?', ('on',))
                    else:
                        self.cursor.execute(f'SELECT id, eng_name, cost_{curr} FROM delivery WHERE status=?', ('on',))
                    result = self.cursor.fetchall()
                    return result
                else:
                    if curr == 'rub':
                        self.cursor.execute('SELECT id, name, cost FROM delivery WHERE status=?', ('on',))
                    else:
                        self.cursor.execute(f'SELECT id, name, cost_{curr} FROM delivery WHERE status=?', ('on',))
                    result = self.cursor.fetchall()
                    return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_qiwi_stat(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT status FROM payments WHERE name=?', ('QIWI',))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_crypto_stat(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT status FROM payments WHERE name=?', ('CRYPTO',))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_yoomoney_stat(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT status FROM payments WHERE name=?', ('YOOMONEY',))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_paym(self, paym):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT status FROM payments WHERE name=?', (paym,))
                result = self.cursor.fetchone()
                if result[0] == 'on':
                    self.cursor.execute('UPDATE payments SET status=? WHERE name=?', ('off', paym))
                else:
                    self.cursor.execute('UPDATE payments SET status=? WHERE name=?', ('on', paym))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def get_count_refs(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT COUNT(*) FROM users WHERE ref_id=?', (user_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def get_user_status(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT status FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_rules(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT text FROM rules')
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changetoken(self, paym, token):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE payments SET token=? WHERE name=?', (token, paym))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_token(self, paym):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT token FROM payments WHERE name=?', (paym,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_question(self, user_id, text):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO questions (user_id, question) VALUES (?, ?)', (user_id, text))
                self.cursor.execute('SELECT id FROM questions WHERE user_id=? ORDER BY id DESC LIMIT 1', (user_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_questions(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, user_id FROM questions')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_quest(self, questid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT user_id, question FROM questions WHERE id=?', (questid,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_quest(self, questid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM questions WHERE id=?', (questid,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_balance(self, user_id, balance):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET balance=? WHERE user_id=?', (balance, user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_promo(self, name, userid, procent):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO promo (name, user_id, procent) VALUES (?, ?, ?)', (name, userid, procent))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def check_promo(self, name, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT procent FROM promo WHERE name=? AND user_id=?', (name, user_id))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def del_promo(self, order_id, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT promo FROM orders WHERE id=? AND user_id=?', (order_id, user_id))
                result = self.cursor.fetchone()
                self.cursor.execute('DELETE FROM promo WHERE name=? AND user_id=?', (result[0], user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_paycount(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT pay_count FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result[0] == None or result[0] == 'None':
                    return 0
                else:
                    return int(result[0])
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def updateprocent(self, user_id, count):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET procent=? WHERE user_id=?', (count, user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def update_personal_procent(self, user_id, count):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET ref_procent=? WHERE user_id=?', (str(count), user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_procent(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT procent FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()[0]
                if result == None:
                    return 0
                else:
                    return int(result)
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def get_personal_procent(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT ref_procent FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()[0]
                if result == None:
                    return 0
                else:
                    return int(result)
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_withdraw(self, user_id, amount, req):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('INSERT INTO withdraws (user_id, amount, req) VALUES (?, ?, ?)', (user_id, amount, req))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_withdraws(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id FROM withdraws')
                result = self.cursor.fetchall()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_withdraw(self, withid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT user_id, amount, req FROM withdraws WHERE id=?', (withid,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def with_del(self, withid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM withdraws WHERE id=?', (withid,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_userstatus_new(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT new_status FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_promoadm(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT name, procent FROM promo WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result == None or result == "None":
                    self.cursor.execute('SELECT lan FROM users WHERE user_id=?', (user_id,))
                    result = self.cursor.fetchone()
                    lan = result[0]
                    if lan == "en":
                        return "Absent"
                    else:
                        return "Отсутствует"
                else:
                    return f'<b>{result[0]}</b> -- {result[1]}%'
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_count_buyspr(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT tovars FROM orders WHERE user_id=? AND status IN ("active", "end")', (user_id,))
                result = self.cursor.fetchall()
                total = 0
                for i in result:
                    a = pickle.loads(i[0])
                    total=total+a[-1]     
                return total
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_refbalance(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT ref_balance FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result[0] == None:
                    return 0
                else:
                    return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def update_language(self, user_id, lan):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET lan=? WHERE user_id=?', (lan, user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_langugage(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT lan FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()
    
    def change_language(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT lan FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result[0] == 'en':
                    self.cursor.execute('UPDATE users SET lan=? WHERE user_id=?', ('ru', user_id))
                else:
                    self.cursor.execute('UPDATE users SET lan=? WHERE user_id=?', ('en', user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def admchange_status(self, user_id, status):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET new_status=? WHERE user_id=?', (status, user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def del_delivery(self, delid):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('DELETE FROM delivery WHERE id=?', (delid,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changerules(self, rules):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE rules SET text=?', (rules,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_username(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT username FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result[0] == None:
                    return user_id
                else:
                    return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def subname_catname(self, goodname):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT subcategoryid FROM goods WHERE name=?', (goodname,))
                result = self.cursor.fetchone()[0]
                self.cursor.execute('SELECT categoryid, name FROM subcategories WHERE id=?', (result,))
                result1 = self.cursor.fetchone()
                subname = result1[1]
                catid = result1[0]
                self.cursor.execute('SELECT name FROM categories WHERE id=?', (catid,))
                catname = self.cursor.fetchone()[0]
                returns = [catname, subname]
                return returns
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_bottoken(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT token FROM token')
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_bottoken(self, token):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE token SET token=?', (token,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_reviewpay(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT pay FROM reviewpay')
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def change_reviewpay(self, pay):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE reviewpay SET pay=?', (pay,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_languagesadm(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT ru, en FROM lanset')
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def changestatlan_ru(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT ru FROM lanset')
                result = self.cursor.fetchone()
                if result[0] == 0:
                    self.cursor.execute('UPDATE lanset SET ru=?', (1,))
                else:
                    self.cursor.execute('UPDATE lanset SET ru=?', (0,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()


    def changestatlan_en(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT en FROM lanset')
                result = self.cursor.fetchone()
                if result[0] == 0:
                    self.cursor.execute('UPDATE lanset SET en=?', (1,))
                else:
                    self.cursor.execute('UPDATE lanset SET en=?', (0,))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()


    def check_lan_on(self, lan):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute(f'SELECT {lan} FROM lanset')
                result = self.cursor.fetchone()
                if result[0] == 1:
                    return 'ok'
                else:
                    return 'no'
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def update_usernamerev(self, username, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE users SET usernamerev=? WHERE user_id=?', (username, user_id))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_usernamerev(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT usernamerev FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()


    def check_countlan(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT ru, en FROM lanset')
                result = self.cursor.fetchone()
                if result[0] == 1 and result[1] == 1:
                    return 'ok'
                else:
                    return 'no'
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def check_questionsusr(self, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id FROM questions WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                if result == None:
                    return 'ok'
                else:
                    return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def add_toquest(self, questid, msg):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT question FROM questions WHERE id=?', (questid,))
                quest = self.cursor.fetchone()[0]
                quest=f'{quest}\n----------\n{msg}'
                self.cursor.execute('UPDATE questions SET question=? WHERE id=?', (quest, questid))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def check_lanadd(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT ru, en FROM lanset')
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_good_info_wcurr(self, goodid, user_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT lan FROM users WHERE user_id=?', (user_id,))
                result = self.cursor.fetchone()
                self.cursor.execute('SELECT currency FROM curryncyset WHERE status=?', (1,))
                curr = self.cursor.fetchone()[0]
                if result[0] == 'en':
                    if curr == 'rub':
                        self.cursor.execute('SELECT eng_name, price FROM goods WHERE id=?', (goodid,))
                    else:
                        self.cursor.execute(f'SELECT eng_name, price_{curr} FROM goods WHERE id=?', (goodid,))
                    result = self.cursor.fetchone()
                    return result
                else:
                    if curr == 'rub':
                        self.cursor.execute('SELECT name, price FROM goods WHERE id=?', (goodid,))
                    else:
                        self.cursor.execute(f'SELECT name, price_{curr} FROM goods WHERE id=?', (goodid,))
                    result = self.cursor.fetchone()
                    return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def get_currency_fromorder(self, order_id):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT currency FROM orders WHERE id=?', (order_id,))
                result = self.cursor.fetchone()
                return result[0]
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def update_pricesgood(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT id, price FROM goods')
                result = self.cursor.fetchall()
                course = get_courses()
                for good in result:
                    usd = float(good[1])/float(course[0])
                    usd = str(float('{:.2f}'.format(usd)))
                    eur = float(good[1])/float(course[1])
                    eur = str(float('{:.2f}'.format(eur)))
                    self.cursor.execute('UPDATE goods SET price_usd=?, price_eur=? WHERE id=?', (usd, eur, good[0]))
                
                self.cursor.execute('SELECT id, cost FROM delivery')
                result = self.cursor.fetchall()
                for deliv in result:
                    usd = float(deliv[1])/float(course[0])
                    usd = str(float('{:.2f}'.format(usd)))
                    eur = float(deliv[1])/float(course[1])
                    eur = str(float('{:.2f}'.format(eur)))
                    self.cursor.execute('UPDATE delivery SET cost_usd=?, cost_eur=? WHERE id=?', (usd, eur, deliv[0]))
                return
            except Exception as ex:
                print(ex)
                self.connection.rollback()
            finally:
                lock.release()

    def get_currencysetadm(self):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('SELECT currency FROM curryncyset WHERE status=?', (1,))
                result = self.cursor.fetchone()
                return result
            except:
                self.connection.rollback()
            finally:
                lock.release()

    def upd_currencyon(self, currency):
        with self.connection:
            try:
                lock.acquire(True)
                self.cursor.execute('UPDATE curryncyset SET status=?', (0,))
                self.cursor.execute('UPDATE curryncyset SET status=? WHERE currency=?', (1, currency))
                return
            except:
                self.connection.rollback()
            finally:
                lock.release()