import requests as req
import webbrowser as wb

API_key = "ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6VXhNaUo5LmV5SnVZVzFsSWpvaU1UWTFORFV4TWpVM01TNHpNalE0TnpFaUxDSmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2TnpNNE1EVjkub0tSRlBaRHhBTUJ6RkRTTjdjS3BmeC1DNUR6TzhLUjVtNkdfRTdvUGZaaVRqSFBqV1VuQ1RCQl9tRjhIVktfckNRZVpZUmJkSjRqTlk2dTRCVEgtc0E="
Integration = {"moto": "2068846",
                      "auth": "2142780",
                      "cards": "192190",
                      "wallet":	"194572",
                      "CAGG": "192493"}

iFrames = {"cards": "180743",
                  "installment": "180742",
                  "valU": "181460",
}

amount = 4000

def input_choose():
    while True:
        print("""Enter the desired method:
            1 for card
            2 for wallet
            3 for kiosk
            4 Invoice link creation
            5 product link creation
            6 refund
            7 void""")
        
        value = input("please enter a value between 0 and 6:")
        try:
            value = int(value)
        except ValueError:
            print('Valid number, please')
            continue
        if 0 <= value <= 7:
           match value:
                    case 1:
                        integration_id = Integration["cards"]
                        iframe = iFrames["cards"]
                        payment_token = auth_order_pay(
                            amount=4000, integration_id=integration_id)
                        wb.open(
                            f"https://accept.paymobsolutions.com/api/acceptance/iframes/{iframe}?payment_token={payment_token}")
                    case 2:
                        integration_id = Integration["wallet"]
                        payment_token = auth_order_pay(
                            amount=4000, integration_id=integration_id)
                        wallet_payload = {
                                    "source": {
                                        "identifier": "01010101010",
                                        "subtype": "WALLET"
                                    },
                                    "payment_token": payment_token}
                        
                        
                        wallet_resp = req.post(url="https://accept.paymob.com/api/acceptance/payments/pay", json=wallet_payload)
                        red_url = wallet_resp.json()['redirect_url']
                        wb.open(red_url)
                    case 3: 
                        integration_id=Integration["CAGG"]
                        payment_token = auth_order_pay(
                            amount=4000, integration_id=integration_id)
                        kiosk_payload={
                            "source" : {
                                "identifier" : "AGGREGATOR",
                                "subtype" : "AGGREGATOR"
                            }, 
                            "payment_token": payment_token
                        }
                        kiosk_resp= req.post(url="https://accept.paymob.com/api/acceptance/payments/pay", json=kiosk_payload)
                        kiosk_id=kiosk_resp.json()['id']
                        kiosk_pending_status=kiosk_resp.json()['pending']
                        kiosk_success_status=kiosk_resp.json()['success']
                        print(kiosk_resp)
                        print("order_id:", kiosk_id)
                        print("Kiosk pending status:", kiosk_pending_status)
                        print("Kiosk success status:", kiosk_success_status)
                    case 4: 
                        invoice_link_payload={
                            "auth_token":auth(API_key),
                            "api_source":"INVOICE",
                             "amount_cents":40000,
                             "currency":"EGP",
                             "shipping_data":{
                                 "first_name":"YASSER",
                                 "last_name":"MOHD",
                                 "phone_number":"01010101010",
                                 "email":"lkasdfk@gmail.com",
                                 "street":"",
                                 "city":"",
                                 "country":"",
                                 "postal_code":""
                                 },
                             "integrations":["2872216","194572","2068846"],
                             "items":[{"name":"Etida",
                                       "amount_cents":40000,
                                       "quantity":"1",
                                       "description":"down payment"}],
                             "delivery_needed":"false"
                             }
                        invoice_link_resp=req.post("https://accept.paymobsolutions.com/api/ecommerce/orders",json=invoice_link_payload)
                        if invoice_link_resp.status_code == 201:
                            red_url=invoice_link_resp.json()["order_url"]
                            id=invoice_link_resp.json()["id"]
                            print(id)
                            wb.open(red_url)
                        else:
                          print(invoice_link_resp.text)
                    case 5: 
                        product_link_payload ={
                            "auth_token":auth(API_key),
                            "product_name":input("Please enter the product name: "),
                             "amount_cents":input("Please enter the product amount in cents: "),
                             "currency":"EGP",
                             "inventory":"300",
                             "delivery_needed":"false",
                             "integrations":["192493","194572","2068846"],
                             "allow_quantity_edit":"false",
                             "product_description":"Tshirt from Adidas"}
                        product_link_resp = req.post("https://accept.paymob.com/api/ecommerce/products",json=product_link_payload)
                        if product_link_resp.status_code == 201:
                                    red_url=product_link_resp.json()["product_url"]
                                    id=product_link_resp.json()["id"]
                                    print(id)
                                    wb.open(red_url)
                        else: 
                            print(product_link_resp.text)
                        break    
                    case 6: 
                        refund_payload ={
                            "auth_token": auth(API_key),
                            "transaction_id": input("Please enter the transaction ID you'd like to refund: "),
                            "amount_cents": input("please enter the amount you'd like to refund: ")
                        }
                        refund = req.post("https://accept.paymob.com/api/acceptance/void_refund/refund", json=refund_payload)
                        print(refund.status_code)
                        print("transaction refund ID:", refund.json()["id"])
                    case 7: 
                        void_payload= {
                            "transaction_id":{input("please enter the transaction ID to be voided: ")}
                            }
                        authToken = auth(API_key)
                        voided = req.post("https://accept.paymob.com/api/acceptance/void_refund/void?token={authToken}", json=void_payload)
                        print(voided.json())
        else:           
            print ("please enter a valid number")

def auth(API_key):
    payload = {"api_key":API_key}
    r = req.post("https://accept.paymob.com/api/auth/tokens",json=payload)
    
    # print(r.json())
    print("Authenticated")
    print(r.status_code)
    print("\n=======================================\n")
    return r.json()["token"]

def order(auth, amount):
    payload = { "auth_token": auth,
    "currency":"EGP",
    "amount_cents": amount
    }
    r=req.post("https://accept.paymob.com/api/ecommerce/orders",json=payload)
    print("order created")
    print(r.status_code)

    print("\n=======================================\n")

    return r.json()["id"]

def pay_token(auth, amount, order_id, integration):
    payload = { "auth_token":auth,
    "amount_cents": amount,
    "order_id" : order_id,
    "expiration": 3600, 
    "billing_data": {
        "apartment": "803", 
        "email": "claudette09@exa.com", 
        "floor": "42", 
        "first_name": "Clifford", 
        "street": "Ethan Land", 
        "building": "8028", 
        "phone_number": "+86(8)9135210487", 
        "shipping_method": "PKG", 
        "postal_code": "01898", 
        "city": "Jaskolskiburgh", 
        "country": "CR", 
        "last_name": "Nicolas", 
        "state": "Utah"
    },
    "currency" : "EGP",
    "integration_id" : integration}
    r=req.post("https://accept.paymob.com/api/acceptance/payment_keys",json=payload)
    # print(r.text)
    print("pay token generated")
    print(r.status_code)
    print("\n=======================================\n")

    return r.json()["token"]

def auth_order_pay(amount, integration_id): 
    auth_token = auth(API_key)
    order_id = order(auth_token, amount)
    payment_token =  pay_token(auth_token, amount, order_id, integration_id)
    return payment_token
    

# # auth(API_key)
# x=input("""Enter the desired method:
#         1 for card
#         2 for wallet
#         3 for kiosk
#         4 cash
#         5 Invoice link creation
#         6 product link creation """)

# switch(x): 
#     case(x == 1):
#         integration_id = Integration["cards"]
#         iframe = iFrames["cards"]
#         payment_token = auth_order_pay(amount=4000, integration_id= integration_id )
#         wb.open(f"https://accept.paymobsolutions.com/api/acceptance/iframes/{iframe}?payment_token={payment_token}")

input_choose()