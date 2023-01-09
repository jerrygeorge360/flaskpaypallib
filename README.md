# Flask-Paypal-SDK

## Description
This easy to use library ensures seamless integration of the paypal sdk into the flask framework.
(Invoices and subscriptions yet to be added.)

## Installing the Flask-paypal-sdk.

    pip install flask-paypal-sdk

## Quick start

    From flask import Flask,render_template
    from flask_paypal_sdk import Sandbox
    app=Flask(__name__)

    # The home route that displays the item to be bought.

    @app.route("/")
    def home_page():
        return render_template("index.html")


    # This is the implementation of the groundnut payment. 

    ground_nut=Sandbox(configuration of what you are selling)

    # Initialize the app

    ground_nut.init_app(app)

    ground_nut.create_order()

    ground_nut.create_route('ground_nut')

    ground_nut.complete_process()

    # Implementation of beans payment.

    beans = Sandbox(configuration of what you are selling)
    
    # initialize the app

    beans.init_app(app)

    beans.create_order()

    beans.create_route('beans')

    beans.complete_process()

This is for the the front. As easy as just adding the link.

    home_page.html

    
    <a href="https://www.sample.com/groundnut">Buy Now </a>

    <a href="https://www.sample.com/beans"> Buy Now</a>


### Prerequisites
+ You should have your client id and client secret key

**You can do that by:**
---    
**Sandbox**



+ Get a Paypal account <a href="https://www.paypal.com/us/webapps/mpp/account-selection">Here</a>

+ Create an App and get the client id and secret key from <a href="https://developer.paypal.com/developer/applications">here</a>
 (<em> You are getting it from the business account</em>)

**Live**
+ Log into the <a href="https://developer.paypal.com/api/rest/production/"> Developer</a> Dashboard with your merchant account.

+ On the My Apps & Credentials page, change to Live.

+ Click Create App in the REST API apps section.

+ Type a name for your app and click Create App.
    
+ Make a note of your REST API client ID and secret.

## Steps needed to make a payment
1. **Import the module.**
2. **Create an instance of the class.**
3. **Initialize the instance.**
4. **Call the generate token method**
4. **Call the create route method**
5. **Call the create or approve method**
6. **Call the complete process method.**
7. **Hoera!! you are done.**
---
## Terms that you need to know.
+ **capture** : 
Payment capture is the process to complete a credit or debit card purchase by capturing or settling the funds for the transaction. After the payment has been authorized, the capture request can be submitted by the payment gateway to the issuing bank either immediately or at a time of the merchant's choosing.

+ **authorize** :
Card authorization is approval from a credit or debit card issuer (usually a bank or credit union) that states the cardholder has sufficient funds or the available credit needed to cover the cost of a transaction they're using a card to complete.


### To capture a payment.(sandbox)
    
    from sandbox import FlaskPaypalSdk

    Payer = Sandbox('USD',10, 'shirts', 6, 'nice shirts', 10, 20,2, 3, 7,2, 'CAPTURE', 'http://localhost:5000/okme','okme', 'http://localhost:5000')

    Payer.init_app(app)

    Payer.generate_access_token("client_id","client_secret_key")

    Payer.create_order()

    Payer.create_route('stockings')

    Payer.complete_process()


### To approve a payment.
    
    Payer = Sandbox('USD',10, 'shirts', 6, 'nice shirt', 10, 20,2, 3, 7,2, 'AUTHORIZE', 'http://localhost:5000', 'http://localhost:5000')
    
    Payer.init_app(app)
    
    Payer.generate_access_token("client_id","client_secret_key")
    
    Payer.create_order()
    
    Payer.create_route('stockings')
    
    Payer.complete_process()

---

## Parameters
+ currency code
+ item_unit_value
+ item_name
+ item_quantity
+ item_description
+ shipping_value
+ handling_value
+ tax_value
+ insurance_value
+ shipping_discount
+ discount_value
+ intent
+ return_url
+ return_url_endpoint
+ cancel_url
+ app (also supports app factory method.)

**N.B**: any parameters you would not use such as the shipping_discount e.t.c pass in a "0"(zero).

---