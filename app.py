import os
import stripe
from flask import Flask, jsonify, request, Response
from flask_cors import CORS



# bootstrap app -------------------------------------
app = Flask('Stripe')
#draw config values from .json file
#see format in example .json file
#NOTE:global_config.json is in gitignore

os_env = os.environ

if 'DEBUG' in os_env:
	DEBUG = os_env['DEBUG']

if 'STRIPE_PK' in os_env:
	stripe_pk=os_env['STRIPE_PK']
else:
	stripe_pk='xxx'

if 'STRIPE_SK' in os_env:
	stripe_sk=os_env['STRIPE_SK']
else:
	stripe_sk='xxx'	

STRIPE= {
		"sec":stripe_sk,
		"pub":stripe_pk
	}

app.config.from_object(__name__)
try:
	app.config.from_json('global_config.json')

except:
	print("No Config File")
	#continue without config file

#--------------------------------------------------
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/pubkey', methods=['GET'])
def pub_key():
    return {"pk":app.config['STRIPE'].get("pub")}

@app.route('/charge/card', methods=['POST'])
def charge_card():
	stripe.api_key = app.config['STRIPE'].get("sec")
	data=request.json
	print(data)
	amount = data.get('amount')
	currency = data.get('currency')
	description = data.get('description')
	destination = data.get('destination')
	token = data.get('token')
	capture = data.get('capture')
	charge = stripe.Charge.create(
		amount=amount, 
		currency=currency,
		description=description,
		source=token,
		capture=capture,
		transfer_group=destination
	)
	print(str(charge))
	return {"receipt":charge.get('receipt_url'),"id":charge.get('id'),"amnt":charge.get('amount'),"status":"still need to make status logic"}



if __name__ == '__main__':
    app.run()