# checks for inconsistencies

import _import
from common import *
from datetime import datetime, date
from Mailman.MailList import MailList

from kn.leden.models import KnUser, KnGroup, Seat, Alias

DAYS_IN_YEAR = 365.242199

def check_geinteresseerden():
	print "GEINTERESSEERDEN"
	es = frozenset(map(lambda m: m.email.lower(),
		KnGroup.objects.get(name=MEMBER_GROUP).user_set.all()))
	ml = MailList('geinteresseerden', False)
	for m in ml.members:
		if m.lower() in es:
			print "%s in geinteresseerden" % m

def check_namespace():
	print "NAMESPACE"
	cn = set(map(lambda c: c.name, 
		filter(lambda c: not c.isVirtual, KnGroup.objects.all())))
	un = set(map(lambda m: m.username, KnUser.objects.all()))
	sn = set(map(lambda s: s.name if s.isGlobal else s.group.name \
					+ '-' + s.name, Seat.objects.all()))
	an = set(map(lambda a: a.source, Alias.objects.all()))
	
	n = set()
	for o in (cn, un, sn, an):
		inter = n.intersection(o)
		if len(inter) != 0:
			for el in inter:
				print '%s: namespace conflict' % el
		n = n.union(o)
	
	for a in Alias.objects.all():
		if not a.target in n:
			print '%s -> %s, target doesn\'t exist' % \
					(a.source, a.target)


def check_commissions():
	print "COMMISSIONS"
	for c in KnGroup.objects.all():
		if len(c.description) < 15:
			print "%s: description too short (<15)" % c.name
		if c.isVirtual:
			if c.user_set.count() != 0:
				print "%s: virtual commission got members" % \
						c.name
def check_members():
	print "MEMBERS"

	ledeng = dict()
	c = 0
	while True:
		c += 1
		ms = date(2004 + c, 8, 1)
		if datetime.now().date() < ms:
			break
		ledeng[c] = KnGroup.objects.get(name='leden%s' % c)

	for m in KnUser.objects.all():
		if m.dateJoined is None:
			print "%s: dateJoined is None" % m.username
		else:
			if m.dateJoined < date(2004, 4, 1):
				print "%s: joined before constitution" % \
						m.username
			c = 0
			while True:
				c += 1
				ms = date(2004 + c, 8, 1)
				if datetime.now().date() < ms:
					break
				if m.dateJoined > ms:
					continue
				if len(ledeng[c].user_set.filter(
						username=m.username)) == 0:
					print "%s: should be in leden%s" \
							% (m.username, c)
				
		if m.dateOfBirth is None:
			print "%s: dateOfBirth is None" % m.username
		else:
			age = (datetime.now().date() - m.dateOfBirth).days \
					/ DAYS_IN_YEAR
			if age < 15:
				print "%s: age < 15" % m.username
			elif age > 40:
				print "%s: age > 40" % m.username 
		if m.password == '$$' or \
		   m.password == '':
			print "%s: no empty password" % m.username
		if m.addr_street == '':
			print "%s: no empty addr_street" % m.username
		if m.addr_zipCode == '':
			print "%s: no empty addr_zipcode" % m.username
		if m.addr_number == '':
			print "%s: no empty addr_number" % m.username
		if m.addr_city == '':
			print "%s: no empty addr_city" % m.username
		if not m.gender in ('m', 'v'):
			print "%s: gender not in {m, v}" % m.username
		if m.telephone is None:
			print "%s: telephone is None" % m.username
		elif m.telephone == '':
			print "%s: empty telephone" % m.username
		elif not m.telephone[0:1] == '+':
			print "%s: un-normalised telephone" % m.username
		if m.studentNumber is None:
			print "%s: studentNumber is None" % m.username
		elif len(m.studentNumber) != 7:
			print "%s: student number of incorrect length" \
					% m.username
		if (not m.is_active and
				len(m.groups.filter(name=MEMBER_GROUP)) > 0):
			print "%s: not active" % m.username

if __name__ == '__main__':
	check_commissions()
	check_members()
	check_namespace()
	check_geinteresseerden()