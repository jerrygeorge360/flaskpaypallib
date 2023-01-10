import unittest,os
from unittest.mock import patch ,MagicMock
from flask import Flask,current_app
import jwt
import requests
from flask_paypal_sdk import Sandbox
import uuid

class TestPayPalSDK(unittest.TestCase):

    
    def setUp(self):
        app = Flask(__name__)
        app.testing=True
        self.app=app.test_client()
        self.test_obj=Sandbox('USD',10, 'shirts', 6, 'nice shirt', 10, 20,2, 3, 7,2, 'CAPTURE', 'http://localhost:5000/okme','okme', 'http://localhost:2000')
        self.test_obj.init_app(app)
    
    
    def test_init(self):
        # self.assertIsInstance(test_obj.app, Flask)
        self.assertIsInstance(self.test_obj.currency_code, str)
        self.assertIsInstance(self.test_obj.item_unit_value, str)
        self.assertIsInstance(self.test_obj.item_name, str)
        self.assertIsInstance(self.test_obj.item_quantity, str)
        self.assertIsInstance(self.test_obj.item_description, str)
        self.assertIsInstance(self.test_obj.tax_value, str)
        self.assertIsInstance(self.test_obj.shipping_value, str)
        self.assertIsInstance(self.test_obj.discount_value, str)
        self.assertIsInstance(self.test_obj.item_total, tuple)
        self.assertIsInstance(self.test_obj.total_amount,str)
        self.assertIsInstance(self.test_obj.intent,str)
        self.assertIsInstance(self.test_obj.return_url, str)
        self.assertIsInstance(self.test_obj.token, str)
        self.assertIsInstance(self.test_obj.base_url, str)
        self.assertIsInstance(self.test_obj.headers, dict)
        self.assertIsInstance(self.test_obj.payload, str)

        

    @patch("flask_paypal_lib.sandbox.requests")
    def test_generate_access_token(self,mock_requests):
        token=jwt.encode({"some":"payload"}, key="secret_key",algorithm="HS256")
        mock_response=MagicMock()
        mock_response.status_code=200
        mock_response.json.return_value={"access_token":f"{token}"}
        mock_requests.post.return_value=mock_response
        self.assertEqual(self.test_obj.generate_access_token(os.environ.get('client_id'),os.environ.get('client_secret_key')),token)
        
    @patch("flask_paypal_lib.sandbox.requests")
    def test_create_order(self,mock_requests):
        mock_response=MagicMock()
        mock_response.status_code=200
        mock_response.json.return_value={'id':uuid.uuid4(),'links':['link0',{'href':'https://sample.com'}]}
        mock_requests.post.return_value=mock_response
        self.assertEqual(self.test_obj._create_order(), 'https://sample.com')
        
    
    def test_get_order_id(self):
        self.assertIsNotNone(self.test_obj.get_order_id())
        self.assertIsInstance(self.test_obj.get_order_id(), str)


    def test_get_approval_link(self):
        self.assertIsNotNone(self.test_obj.get_approval_link())
        self.assertIsInstance(self.test_obj.get_approval_link(), str)
    
    @patch("flask_paypal_lib.sandbox.requests")
    def test_capture(self,mock_requests):
        mock_response=MagicMock()
        mock_response.status_code=200
        mock_response.json.return_value={'status':'ok'}
        mock_requests.post.return_value=mock_response
        self.assertEqual(self.test_obj._capture(),{'status':'ok'})
        

    @patch("flask_paypal_lib.sandbox.requests")
    def test_authorize(self,mock_requests):
        mock_response=MagicMock()
        mock_response.status_code=200
        mock_response.json.return_url={'status':'ok'}
        mock_requests.get.return_value=mock_response
        
        
        # self.assertEqual(self.test_obj._authorize(),'ok')

    @patch("flask_paypal_lib.sandbox.requests")
    def test_create_order_route(self,mock_requests,name="name_of_route"):
        mock_response=MagicMock()
        mock_response.status_code=200
        mock_response.json.return_value={'id':uuid.uuid4(),'links':['link0',{'href':'https://sample.com'}]}
        mock_requests.post.return_value=mock_response
        self.assertEqual(self.test_obj._create_order(),"https://sample.com")
        self.test_obj.create_order_route(name)
        result=self.app.get(f"/{name}")
        self.assertEqual(result.status_code,302)


    @patch("flask_paypal_lib.sandbox.requests")
    def test_complete_process(self,mock_requests):

        mock_response=MagicMock()
        mock_response.status_code=200
        mock_response.json.return_url={}
        mock_requests.get.return_value=mock_response
        self.test_obj.complete_process()
        result=self.app.get('/okme')
        self.assertEqual(result.status_code, 200)


if __name__=="__main__":
    unittest.main()