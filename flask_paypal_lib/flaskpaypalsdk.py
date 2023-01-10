import json,requests,os
from flask import current_app

class FlaskPaypalSdk:
    """
    A class used to make the Transaction
    
    ...

    Attributes
    
    ----------
    currency_code:str
        the currency codes supported by paypal. Follow the link below to check:
        https://developer.paypal.com/docs/reports/reference/paypal-supported-currencies/.

    item_unit_value:int
        the cost of an item.
    item_name:str
        name of item or product
    item_quantity:int
        number of items to be bought.
    item_description
        note of the item.
    shipping_value:int
        cost of shipment
    handling_value:int
        cost of handling
    tax_value:int
        cost of taxes
    insurance_value:int
        cost of insurance
    shipping_discount:int
        cost of shipping discount
    discount_value:int
        discount in the item.
    intent:str
        capture or authorize the transaction
    return_url:str
        the route it would be redirected to complete the transaction after approval.
    cancel_url:str
        the route that it would be redirected to after a failed transaction.


    Methods
    -------
    init_app()
        initializes the library for the flask instance.
    config()
        configures the instance.
    create_order_route(app_instance,url,payment_route)
        registers the payment endpoint and creates the transaction
    complete_process()
        completes the process of capturing or approval
    get_order_id()
        gets the id of the transaction.
    
    """



    
    
    order_id=''
    approve_link=''
    authorize_link=''
    capture_link=''

    def __init__(self,
    currency_code:str,
    item_unit_value:int
    ,item_name:str
    ,item_quantity:int,
    item_description:str,
    shipping_value:int,
    handling_value:int,
    tax_value:int,
    insurance_value:int,
    shipping_discount:int,
    discount_value:int,
    intent:str,

    return_url:str,
    return_url_endpoint:str,
    cancel_url:str,
    app=None
    ):
        self.app=''
        self.currency_code=currency_code
        self.item_unit_value=str(item_unit_value)
        self.item_name=item_name
        self.item_quantity=str(item_quantity)
        self.item_description=item_description
        self.tax_value=str(tax_value)
        self.shipping_value=str(shipping_value)
        self.handling_value=str(handling_value)
        self.insurance_value=str(insurance_value)
        self.shipping_discount=str(shipping_discount)
        self.discount_value=str(discount_value)
        self.item_total=str(int(self.item_unit_value)*int(self.item_quantity)),
        self.total_amount=str(int(self.item_total[0])+int(self.tax_value)+int(self.shipping_value)+int(self.handling_value)+int(self.insurance_value)-int(self.shipping_discount)-int(self.discount_value))
        self.intent=intent
        self.return_url_endpoint=return_url_endpoint
        self.return_url=return_url 
       
        self.token=''
        self.headers={'Authorization':f"Bearer {self.token}",'Content-Type':'application/json', 'Prefer': 'return=representation'}
        self.base_url="https://api-m.paypal.com"
        self.payload=json.dumps({
                "intent":intent,
                "purchase_units":[
                        {
                                "items":[
                {
                    "name": self.item_name,
                    "unit_amount": {
                        "currency_code": self.currency_code,
                        "value": self.item_unit_value
                    },
                    "quantity": self.item_quantity,
                    "description":self.item_description
                }
            ],
            "amount":{

            "currency_code": self.currency_code,
            "value": self.total_amount,
            
            "breakdown": {
                "item_total": {
                        "currency_code": self.currency_code,
                        "value": self.item_total[0]
                },
                "tax_total": {
                        "currency_code": self.currency_code,
                        "value": self.tax_value
                },
                "shipping": {
                        "currency_code": self.currency_code,
                        "value": self.shipping_value
                },
                "handling": {
                        "currency_code": self.currency_code,
                        "value": self.handling_value
                 },
                "insurance": {
                        "currency_code": self.currency_code,
                        "value": self.insurance_value
                },
                "shipping_discount": {
                        "currency_code": self.currency_code,
                        "value": self.shipping_discount
                },
                "discount": {
                        "currency_code": self.currency_code,
                        "value": self.discount_value
                }



            }
        }



                        }
                ],
                "application_context":{
                    "return_url":return_url,
                    "cancel_url": cancel_url
                }
        }
        )
        if app:
            self.init_app(app)

    
    def init_app(self,app):
        """
        initializes the library.
        calls the generate token function.

        Parameters
        ----------
        app:Flask
        
        
        """
        if app:
            
            self.app=app

        else:
            print('flask instanced not passed')
        return
    
    def generate_access_token(self,client_id:str,client_secret_key:str):

        """
        This generates the access token.
        
        Parameters
        -----------
        client_id : client id from your Paypal dashboard.
        client_secret_key : client secret key from your Paypal dashboard.

        """
        auth=(client_id,client_secret_key)
        token_url=f"{self.base_url}/v1/oauth2/token"
        data={'grant_type':'client_credentials','ignoreCache':False,'return_client_metadata':True,'redirect_uri':''}
        response=requests.post(url=token_url,data=data,auth=auth).json()
        self.token=response['access_token']
        self.headers['Authorization']="Bearer "+self.token
        return self.token




    def _create_order(self):
        """
        creates the order and redirects the clients for authentication

        """
        order_url=f"{self.base_url}/v2/checkout/orders"
        response=requests.post(url=order_url,headers=self.headers,data=self.payload).json()
        self.order_id=response['id']
        self.approve_link=response['links'][1].get('href')

        
        return self.approve_link


    def get_order_id(self):
        """
        gets the id of the item or order.
        
        """
        return self.order_id
    

    def get_approval_link(self):
        return self.approve_link

    
    def _capture(self):
        """
        captures the payment made after approval.

      
        
        """
        capture_url=f"{self.base_url}/v2/checkout/orders/{self.get_order_id()}/capture"
        response=requests.post(url=capture_url,data='',headers=self.headers).json()
        return response
    
    def _authorize(self):
        """
        authorizes the payment made after approval.
        
        """
        authorize_url=f"{self.base_url}/v2/checkout/orders/{self.get_order_id()}/authorize"
        print(authorize_url)
        response=requests.post(url=authorize_url,data='',headers=self.headers)
        print(response.text)
        return response.json()

    
    def create_order_route(self,name_of_payment_route:str):
        """
        creates the route in which the client request would go through

        calls the __create_order method

        Parameters
        ----------
        app:Flask
            the flask object, this is to setup the route.
        
        
        
        """
        with self.app.app_context():
            @current_app.route(f'/{name_of_payment_route}')
            def create_order_route():
                print(self._create_order())
                return self.app.redirect(self._create_order())
    
    def complete_process(self):
        """
        this completes the transaction by either capturing or authorizing the payment
        registers an endpoint that would be redirected after approval.
        Parameters
        ----------
        """
        with self.app.app_context():
            @current_app.route(f'/{self.return_url_endpoint}')
            def complete_process():
                res=''
                if self.intent=="CAPTURE":
                    res=self._capture()
                elif self.intent=="AUTHORIZE":
                    res=self._authorize()
                else:
                    res='not successful'
                return res
