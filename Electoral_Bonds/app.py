from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import asc, func


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:VivekSQL5@localhost/electoral_bonds'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class BondsPurchased(db.Model):
    __tablename__ = 'bond_purchase'
    Sr_No = db.Column(db.Integer, primary_key=True)
    Reference_No_URN = db.Column(db.String(25))
    Journal_Date = db.Column(db.Date)
    Date_of_Purchase = db.Column(db.Date)
    Date_of_Expiry = db.Column(db.Date)
    Name_of_the_Purchaser = db.Column(db.String(100))
    Prefix = db.Column(db.String(2))
    Bond_Number = db.Column(db.Integer)
    Denominations = db.Column(db.String(100))
    Issue_Branch_Code = db.Column(db.String(50))
    Issue_Teller = db.Column(db.Integer)
    Status_ = db.Column(db.String(10))

    def __repr__(self):
        return "<BondsPurchased %r>" % self.Bond_Number


class BondsRedeemed(db.Model):
    __tablename__ = 'bond_redeemed'
    Sr_No = db.Column(db.Integer, primary_key=True)
    Date_of_Encashment = db.Column(db.Date)
    Name_of_the_political_party = db.Column(db.String(100))
    Account_No_of_the_Party = db.Column(db.String(100))
    Prefix = db.Column(db.String(2))
    Bond_Number = db.Column(db.Integer)
    Denominations = db.Column(db.String(100))
    Pay_Branch_Code = db.Column(db.String(50))
    Pay_Teller = db.Column(db.Integer)

    def __repr__(self):
        return "<BondsRedeemed %r>" % self.Bond_Number


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/purchasedata', methods=['POST', 'GET'])
def get_purchase_data():
    att_dict = {'company': 'Name_of_the_Purchaser', 'reference': 'Reference_No_URN', 'bondnumber': 'Bond_Number',
                'journaldate': 'Journal_Date', 'dateofpurchase': 'Date_of_Purchase', 'dateofexpiry': 'Date_of_Expiry'}

    if request.method == 'POST':
        submitted = []
        for key, val in request.form.items():
            if val:
                submitted.append((key, val))

        try:
            query = db.session.query(BondsPurchased)
            for key2, val2 in submitted:
                query = query.filter(getattr(BondsPurchased, att_dict.get(key2)) == val2)
            data = query.all()
            count = len(data)
            temp = db.session.query(BondsPurchased.Name_of_the_Purchaser).distinct().order_by(asc(BondsPurchased.Name_of_the_Purchaser)).all()
            return render_template('purchase.html', data=data, count=count, temp=temp)

        except Exception as e:
            return 'There was error fetching data.\n' + str(e)

    else:
        count = 0
        temp = db.session.query(BondsPurchased.Name_of_the_Purchaser).distinct().order_by(asc(BondsPurchased.Name_of_the_Purchaser)).all()
        return render_template('purchase.html', count=count, temp=temp)


@app.route('/redeemdata', methods=['POST', 'GET'])
def get_redeem_data():
    att_dict2 = {'dateofencash': 'Date_of_Encashment', 'party': 'Name_of_the_political_party', 'bondnumber2': 'Bond_Number'}
    if request.method == 'POST':
        submitted2 = []
        for key2, val2 in request.form.items():
            if val2:
                submitted2.append((key2, val2))


        try:
            query2 = db.session.query(BondsRedeemed)
            for key22, val22 in submitted2:
                query2 = query2.filter(getattr(BondsRedeemed, att_dict2.get(key22)) == val22)
            data2 = query2.all()
            count2 = len(data2)
            temp2 = db.session.query(BondsRedeemed.Name_of_the_political_party).distinct().order_by(asc(BondsRedeemed.Name_of_the_political_party)).all()
            return render_template('redeem.html', data2=data2, count2=count2, temp2=temp2)

        except Exception as e:
            return 'There was error fetching data.\n' + str(e)

    else:
        count2 = 0
        temp2 = db.session.query(BondsRedeemed.Name_of_the_political_party).distinct().order_by(asc(BondsRedeemed.Name_of_the_political_party)).all()
        return render_template('redeem.html', count2=count2, temp2=temp2)


@app.route('/analyse', methods=['POST', 'GET'])
def analyse():
    an_dict = {'party3': 'Name_of_the_political_party', 'bondnumber3': 'Bond_Number', 'company3': 'Name_of_the_Purchaser'}
    if request.method == 'POST':
        submitted3 = []
        for key3, val3 in request.form.items():
            if val3:
                submitted3.append((key3, val3))
        try:

            query = db.session.query(
                BondsPurchased.Bond_Number,
                BondsPurchased.Name_of_the_Purchaser,
                BondsRedeemed.Name_of_the_political_party,
                BondsPurchased.Denominations,
                BondsPurchased.Date_of_Purchase,
                BondsPurchased.Date_of_Expiry,
                BondsRedeemed.Date_of_Encashment,
                BondsPurchased.Status_,
            ).join(
                BondsRedeemed, BondsPurchased.Bond_Number == BondsRedeemed.Bond_Number, isouter=True
            )

            for key33, val33 in submitted3:
                if key33 == 'company3':
                    query = query.filter(getattr(BondsPurchased, an_dict.get(key33)) == val33)
                elif key33 == 'party3':
                    query = query.filter(getattr(BondsRedeemed, an_dict.get(key33)) == val33)
                else:
                    query = query.filter(getattr(BondsPurchased, an_dict.get(key33)) == val33)
            data_an = query.all()
            count = len(data_an)
            parties = db.session.query(BondsRedeemed.Name_of_the_political_party).distinct().order_by(
                asc(BondsRedeemed.Name_of_the_political_party)).all()
            companies = db.session.query(BondsPurchased.Name_of_the_Purchaser).distinct().order_by(
                asc(BondsPurchased.Name_of_the_Purchaser)).all()

            m = [int(''.join(row.Denominations.split(','))) for row in data_an]
            money = sum(m)
            return render_template('analyse.html', data_an=data_an, parties=parties, companies=companies, count=count, money=money)

        except Exception as e:
            return 'There was error fetching data.\n' + str(e)
    else:
        parties = db.session.query(BondsRedeemed.Name_of_the_political_party).distinct().order_by(asc(BondsRedeemed.Name_of_the_political_party)).all()
        companies = db.session.query(BondsPurchased.Name_of_the_Purchaser).distinct().order_by(asc(BondsPurchased.Name_of_the_Purchaser)).all()
        count = 0
        money = 0
        return render_template('analyse.html', parties=parties, companies=companies, count=count, money=money)


if __name__ == '__main__':
    app.run(debug=True)

