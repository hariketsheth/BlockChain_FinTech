from flask import Flask, render_template, request, redirect, url_for, session
import utils
import mongo
import hashlib

app = Flask(__name__, static_url_path='/static')
app.debug = True
app.secret_key = "Nothing"

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def Login():
    if "name" in session:
        link_map = {'SME': '/sme', 'CE': '/ce', "Capitalist": '/capital'}
        return redirect(link_map[session['category']])
    return render_template('Login.html')


@app.route("/logout")
def exit():
    session.clear()
    return redirect("/")

@app.errorhandler(404)
def error404(error):
    return render_template('404.html'), 404

@app.route("/sme/invoice/<order>")
def sme_invoice(order):
    if "name" not in session:
        return redirect("/")
    if session['category'] != "SME":
        return redirect("/")
    name = session['name']
    data = utils.db.get_data('orders/'+order)
    sme_name = utils.db.get_data('sme/'+data['sme'])['name']
    return render_template('/sme/invoice.html', data=data, id=order, sme_name=sme_name, name=name)

@app.route("/sme")
def smeindex():
    if "name" not in session:
        return redirect("/login")
    if session['category'] != "SME":
        return redirect("/login")

    sme = session['hash']
    name = session['name']
    temp = utils.db.get_data('orders')
    orders = {}
    for i in temp:
        if temp[i]['sme'] == sme:
            orders[i] = temp[i]
    print(orders)
    return render_template('/sme/index.html', data=orders, name=name)

@app.route("/sme/request")
def sme_request_to_ce():
    if "name" not in session:
        return redirect("/")

    if session['category'] != "SME":
        return redirect("/")

    sme = session['hash']

    submitted = utils.db.get_data('requests')
    entp = utils.db.get_data('enterprises')
    cd = {}
    if submitted is not None:
        for i in submitted:
            if submitted[i]['sme'] == sme:
                class_name = "right label label-success" if submitted[i]['accepted'] == 'yes' else "right label label-danger"
                label = "Accepted" if submitted[i]['accepted'] == 'yes' else "Not Accepted"
                name = entp[submitted[i]['ceid']]['name']
                cd[i] = {
                    'class': class_name,
                    'name': name,
                    'label': label
                }
    return render_template('/sme/request.html', data=entp, submitted=cd, name=session['name'])


@app.route("/sme/request/submit", methods=['POST'])
def submit_sme_request():
    sme = session['hash']
    ceid = request.form['sme']
    utils.submit_request(sme, ceid)
    return ''

@app.route("/sme/decision")
def sme_decision():
    if "name" not in session:
        return redirect("/")
    if session['category'] != "SME":
        return redirect("/")

    temp = utils.db.get_data('orders')
    data = {}
    for i in temp:
        if temp[i]['sme_approved'] == 'no' and 'invested' not in temp[i]:
            data[i] = temp[i]
    # print(data)
    return render_template('/sme/order.html', data=data, name=session['name'])


@app.route('/sme/approve', methods=['POST'])
def sme_approve():
    hash_number = request.form['HashCode']
    workingcapital = request.form['WorkingCapital']
    captialdeadline = request.form['CapitalDeadline']
    utils.update_order_sme(hash_number, workingcapital, captialdeadline)
    return "Error"


@app.route('/sme/reject', methods=['POST'])
def sme_reject():
    hash_number = request.form['HashCode']
    utils.db.write_data('orders', {}, hash_number)
    return "Error"

@app.route("/ce")
def core():
    if "name" not in session:
        return redirect("/login")
    if session['category'] != "CE":
        return redirect("/login")
    temp = utils.db.get_data('orders')
    orders = {}
    for i in temp:
        if temp[i]['ce'] == session['hash']:
            orders[i] = temp[i]
    smes = utils.db.get_data('sme')
    sms = [orders[i]['sme'] for i in orders]
    sm = {}
    for i in sms:
        sm[i] = smes[i]['name']
    return render_template('/ce/index.html', data=orders, smemap=sm, name=session['name'])


@app.route("/ce/decision")
def ce_decision():
    if "name" not in session:
        return redirect("/")
    if session['category'] != "CE":
        return redirect("/")

    temp = utils.db.get_data('orders')
    data = {}
    for i in temp:
        if temp[i]['approved'] == 'no' and temp[i]['sme_approved'] == 'yes' and 'invested' not in temp[i]:
            data[i] = temp[i]
    if 'decision' in request.args:
        decision = request.args.get('decision')
        uid = request.args.get('hash')
        if decision == 'y':
            intd = request.args.get('intd')
            utils.update_order(uid, intd)

        else:
            utils.update_order(uid, False)
        return redirect('/ce/decision')
    else:
        return render_template('/ce/approve_order.html', data=data, name=session['name'])


@app.route('/ce/approve', methods=['POST'])
def ce_approve():

    hash_number = request.form['HashCode']
    insurance = request.form['Insurance']
    print(hash_number, insurance)
    utils.update_order_ce(hash_number,  insurance)
    return "Error"


@app.route('/ce/reject', methods=['POST'])
def ce_reject():
    hash_number = request.form['HashCode']
    utils.db.write_data('orders', {}, hash_number)
    return "Error"


@app.route("/capital")
def capital():
    if "name" not in session:
        return redirect("/login")
    if session['category'] != "Capitalist":
        return redirect("/login")

    return render_template('/cap/index.html', name=session['name'])


@app.route("/capital/market")
def capital_market():
    if "name" not in session:
        return redirect("/")
    if session['category'] != "Capitalist":
        return redirect("/")

    temp = utils.db.get_data('orders')
    smes = utils.db.get_data('sme')
    sm = {}
    data = {}
    for i in temp:
        if temp[i]['approved'] == 'yes' and 'invested' not in temp[i]:
            data[i] = temp[i]
    sms = [data[i]['sme'] for i in data]
    for i in sms:
        try:
            sm[i] = smes[i]['name']
        except:
            pass
    return render_template('/cap/marketplace.html', data=data, smemap=sm, name=session['name'])


@app.route("/capital/view/<order>")
def capital_view(order):
    if "name" not in session:
        return redirect("/")

    if session['category'] != "Capitalist":
        return redirect("/")

    data = temp = utils.db.get_data('orders/'+order)
    sme_name = utils.db.get_data('sme/'+data['sme'])['name']
    return render_template('/cap/vieworder.html', data=data, graph_data1=utils.make_line_graph1(), graph_data2=utils.make_line_graph2(), smename=sme_name, name=session['name'])


@app.route("/ce/create")
def CreateOrder():
    if "name" not in session:
        return redirect("/")
    if session['category'] != "CE":
        return redirect("/")

    ce = session['hash']
    joined = utils.db.get_data('enterprises/{}'.format(ce))
    smes = utils.db.get_data('sme')
    cp = {}
    if 'smes' in joined:
        lst = joined['smes']
        for i in lst:
            try:
                cp[i] = {
                    'name': smes[i]['name']
                }
            except:
                pass
    return render_template('/ce/createorder.html', smes=cp)


@app.route("/ce/accept")
def acceptsme():

    if "name" not in session:
        return redirect("/")
    if session['category'] != "CE":
        return redirect("/")

    ce = session['hash']
    submitted = utils.db.get_data('requests')
    smes = utils.db.get_data('sme')
    cd = {}
    for i in submitted:
        if submitted[i]['ceid'] == ce and submitted[i]['accepted'] == 'no':
            name = smes[submitted[i]['sme']]['name']
            cd[i] = {
                'name': name,
                'sme': submitted[i]['sme']
            }
    return render_template('/ce/accept.html', data=cd, name=session['name'])


@app.route("/ce/accept/submit", methods=['POST'])
def submit_sme_accept():
    ce = session['hash']
    hashc = request.form['HashCode']
    flag = request.form['flag']
    old_data = utils.db.get_data('requests/{}'.format(hashc))
    if flag == 'true':
        sme = request.form['sme']
        utils.add_sme(ce, sme)
        old_data['accepted'] = 'yes'
        utils.db.write_data('requests', old_data, hashc)
    return ''


@app.route('/login_action', methods=['POST'])
def login_action():

    email = request.form['email']
    password = request.form['password']
    print(email, password)
    data = mongo.Login(email, password)

    link_map = {'SME': '/sme', 'CE': '/ce', "Capitalist": '/capital'}

    if data['check']:
        data['link'] = link_map[data['category']]
        session['name'] = data['name']
        session['category'] = data['category']
        session['hash'] = data['hash']
        return data
    return data


@app.route('/create_order', methods=['POST'])
def create_order():
    ce = session['hash']
    ce_name = session['name']

    amount = request.form['Amount']
    quote = request.form['Quote']
    payment_date = request.form['Payment']
    delievery_date = request.form['Delievery']
    sme = request.form['SME']

    uid = utils.make_order(quote, amount, payment_date,
                           delievery_date, sme, ce=ce, ce_name=ce_name)

    return "Error"


@app.route('/sign_action', methods=['POST'])
def sign_action():

    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    category = request.form['category']
    hash_object = hashlib.sha1(email.encode())
    hashc = hash_object.hexdigest()[-15:]

    myc = {'Capitalist': 'investors', 'CE': 'enterprises', 'SME': 'sme'}
    link_map = {'SME': '/sme', 'CE': '/ce', "Capitalist": '/capital'}

    data = {}
    data['check'] = False

    print(name, email, password, category)
    if mongo.Register(email, name, password, category, hashc):
        utils.db.write_data(myc[category], {
            'name': name,
            'email': email
        }, hashc)

        data['check'] = True
        data['link'] = link_map[category]

        session['name'] = name
        session['category'] = category
        session['hash'] = hashc
        return data

    return data


if __name__ == "__main__":
    app.run(port=5001)
