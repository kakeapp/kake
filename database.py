# database.py

import mysql.connector as sql
from utils import send_verification_mail
from flask import url_for
import os
import secrets


def gen_token() -> str:
    """Creates a token"""
    return secrets.token_hex()


def create_connection() -> None:
    """function to create connection with mysql db """
    global CON, CUR
    CON = sql.connect(user=os.environ.get("MYSQLDB_USERNAME"), host=os.environ.get("MYSQLDB_DBHOST"), \
        passwd=os.environ.get("MYSQLDB_PASSWD"), database=os.environ.get("MYSQLDB_DBNAME"))
    CUR = CON.cursor(buffered=True)
    print("Created connection")


def get_cakes() -> list[str]:
    """Returns a list of cakes"""
    CUR.execute("SELECT * FROM CAKES")
    return CUR.fetchall()


def get_cart(cakes: list[int]) -> dict:
	"""Returns list of cakes from the cart"""
	cost = 0
	result = {}
	for i in range(len(cakes)):
		CUR.execute(f"SELECT * FROM CAKES WHERE ID={cakes[i]}")
		data = CUR.fetchone()
		cakes[i] = str(cakes[i])
		cost += int(data[3])
		if cakes[i] in result.keys():
			result[cakes[i]]['qty'] += 1
		else:
			result[cakes[i]] = {
				'qty': 1,
				'data': data
			}

	return cost,result


def red_cake(cakeId: int) -> None:
    """Reduce the number of cakes"""
    if not check_cake(cakeId):
        return

    CUR.execute(
        f"UPDATE CAKES SET QTYPRESENT=QTYPRESENT-1 WHERE ID={cakeId}"
    )
    CON.commit()

def ad_cake(cakeId: int) -> None:
    """Reduce the number of cakes"""
    if not check_cake(cakeId):
        return

    CUR.execute(
        f"UPDATE CAKES SET QTYPRESENT=QTYPRESENT+1 WHERE ID={cakeId}"
    )
    CON.commit()

def get_cake_qty(cakeId: int) -> int:
    """Get numbers of cakes"""
    if not check_cake(cakeId):
        return

    CUR.execute(
        f"SELECT QTYPRESENT FROM CAKES WHERE ID={cakeId}"
    )
    return CUR.fetchall()[0]

    
def create_user(username: str, emailid: str, passwd: str, verify_url: str,
                accessToken: str) -> None:
    """Creates a user profile"""
    # commenting for now
    send_verification_mail(emailid=emailid, verify_url=verify_url)
    id = gen_token()[:10]
    CUR.execute(
        f"INSERT INTO AUTH(ID, ACCESS_TOKEN, EMAIL_ID, PASSWD, USERNAME) VALUES('{id}', '{accessToken}', '{emailid}', '{passwd}', '{username}')"
    )
    print(
        f"INSERT INTO AUTH(ID, ACCESS_TOKEN, EMAIL_ID, PASSWD, USERNAME) VALUES('{id}', '{accessToken}', '{emailid}', '{passwd}', '{username}')"
    )
    CON.commit()


def check_if_access_token_exists(accessToken: str) -> bool:
	"""Check if there is a user with ACCESS_TOKEN accessToken"""
	CUR.execute(f"SELECT * FROM AUTH WHERE ACCESS_TOKEN='{accessToken}'")
	return CUR.rowcount != 0


def verify_user(accessToken: str) -> None | str:
	"""Verifies the user"""
	CUR.execute(
		f"UPDATE AUTH SET VERIFIED=TRUE WHERE ACCESS_TOKEN='{accessToken}'"
	)
	CON.commit()


def check_cake(cakeId: int) -> bool:
	"""Checks if cake exists"""
	CUR.execute(f"SELECT * FROM CAKES WHERE ID={cakeId}")
	return CUR.rowcount == 1

def check_user_is_verified(accessToken: str) -> bool:
	"""Checks if the user is verified"""
	CUR.execute(
		f"SELECT VERIFIED FROM AUTH WHERE ACCESS_TOKEN='{accessToken}'")
	return CUR.rowcount == 1

def check_usr(emailid: str, passwd: str) -> bool:
	"""Check if user with emailid and passwd exists"""
	CUR.execute(
		f"SELECT * FROM AUTH WHERE EMAIL_ID='{emailid}' AND PASSWD='{passwd}'")
	data = CUR.fetchall()
	return len(data) == 1


def get_access_token(emailid: str, passwd: str) -> str:
    """Gets user accessToken"""
    CUR.execute(
        f"SELECT ACCESS_TOKEN FROM AUTH WHERE EMAIL_ID='{emailid}' AND PASSWD='{passwd}'"
    )
    data = CUR.fetchall()
    return data[0]


def check_email(emailid: str) -> bool:
    """Check if email id already exists"""
    CUR.execute(f"SELECT * FROM AUTH WHERE EMAIL_ID='{emailid}'")
    data = CUR.fetchall()
    print(data)
    return len(data) == 0


def close_connection() -> None:
    """function to close connection with mysql db"""
    if CON:
        CON.close()
        print("Closed connection")


CUR = None  # Cursor Object
CON = None  # Connection Object
