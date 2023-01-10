# cake.py
"""
Cake functions
"""

from flask import request, session
from database import check_user_is_verified as check_is_verified, check_cake, red_cake, ad_cake

def append_cake(cakeId: int) -> None:
	"""Add cakes"""
	try:
		if session['cakeList']:
			# nothing to be done
			pass
	except:
		session['cakeList'] = []

	if check_is_verified(session['accessToken']) and check_cake(cakeId):
		cakes = list(session['cakeList'])
		cakes.append(cakeId)
		session['cakeList'] = cakes
		red_cake(cakeId)

def rm_cake(cakeId: int) -> None:
	"""Remove cakes"""
	if check_is_verified(session['accessToken']) and check_cake(cakeId):
		cakes = list(session['cakeList'])
		ind = cakes.index(cakeId)
		if ind >= 0:
			cakes.pop(ind)
			session['cakeList'] = cakes
			ad_cake(cakeId)
