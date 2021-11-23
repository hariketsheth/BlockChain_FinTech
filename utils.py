from database import Database
import hashlib
import pygal
import time

db = Database()


def make_sme(name, address, ce):
    db.write_data('sme', {
        'name': name,
        'ce': ce,
        'address': address
    })


def update_sme(name, ce):
    hash_object = hashlib.sha1(name.encode())
    hex_dig = hash_object.hexdigest()
    old_data = db.get_data('sme/{}'.format(hex_dig[-15:]))
    db.write_data('sme', {
        'name': name,
        'ce': ce,
        'address': old_data['address']
    })


def make_ce(name, address, sme):
    db.write_data('enterprises', {
        'name': name,
        'sme': sme,
        'address': address
    })


def update_ce(name, sme):
    hash_object = hashlib.sha1(name.encode())
    hex_dig = hash_object.hexdigest()
    old_data = db.get_data('enterprises/{}'.format(hex_dig[-15:]))
    db.write_data('enterprises', {
        'name': name,
        'sme': sme,
        'address': old_data['address']
    })


def make_order(quote, amount, pd, dd, sme, ce='test', ce_name='test'):
    hash = hashlib.sha1(str(time.time()).encode())
    hex_dig = hash.hexdigest()
    uid = hex_dig[-15:]
    db.write_data('orders', {
        'quote': quote,
        'amount': amount,
        'payment_date': pd,
        'delivery_date': dd,
        'sme': sme,
        'ce': ce,
        'cename': ce_name,
        'approved': 'no',
        'sme_approved': 'no'
    }, flag=uid)
    return uid


def update_order(uid, approval):
    old_data = db.get_data('orders/{}'.format(uid))
    if approval:
        old_data['approved'] = 'yes'
        old_data['insurance'] = approval
        db.write_data('orders', old_data, flag=uid)
    else:
        db.write_data('orders', {}, flag=uid)


def update_order_sme(uid, wc, wcd):
    old_data = db.get_data('orders/{}'.format(uid))
    old_data['wc'] = wc
    old_data['wcd'] = wcd
    old_data['sme_approved'] = 'yes'
    db.write_data('orders', old_data, flag=uid)


def update_order_ce(uid, insurance):
    old_data = db.get_data('orders/{}'.format(uid))
    old_data['insurance'] = insurance
    old_data['approved'] = 'yes'
    db.write_data('orders', old_data, flag=uid)


def submit_request(sme, ceid):
    hash = hashlib.sha1(str(sme+ceid).encode())
    hex_dig = hash.hexdigest()
    uid = hex_dig[-15:]
    db.write_data('requests', {
        'ceid': ceid,
        'sme': sme,
        'accepted': 'no'
    }, flag=uid)
    return True


def add_sme(ceid, sme):
    old_data = db.get_data('enterprises/{}'.format(ceid))
    tmp = old_data.get('smes', None)
    if tmp is None:
        old_data['smes'] = [sme]
    else:
        tmp = [i for i in old_data['smes']]
        tmp += [sme]
        old_data['smes'] = tmp
    db.write_data('enterprises', old_data, ceid)
    return True


def make_line_graph1():
    graph = pygal.Line()
    graph.title = 'Past performance of the SME'
    graph.x_labels = ['Aug 2019', 'Sept 2019',
                      'Oct 2019', 'Nov 2019', 'Dec 2019', 'Jan 2020']
    graph.add('Amount',  [45000, 70000, 100000, 50000, 120000, 55000])
    graph_data = graph.render_data_uri()
    return graph_data


def make_line_graph2():
    graph = pygal.Line()
    graph.title = 'Past performance of the SME'
    graph.x_labels = ['Aug 2019', 'Sept 2019',
                      'Oct 2019', 'Nov 2019', 'Dec 2019', 'Jan 2020']
    graph.add('Working Capital', [10000, 18000, 25000, 20000, 40000, 21000])
    graph_data = graph.render_data_uri()
    return graph_data


if __name__ == '__main__':
    update_sme('Devyanshu Shukla', ['test'])


'''
ce: 
name:
address:bc
sme-approved: []

'''
'''
sme:
address: bc,
ce: [],
name: 
'''

''' 
name
'''


'''

wkc required
amount order

'''
