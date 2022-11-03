import requests as req
import webbrowser as wb

API_key = "ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6VXhNaUo5LmV5SnVZVzFsSWpvaU1UWTFORFV4TWpVM01TNHpNalE0TnpFaUxDSmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2TnpNNE1EVjkub0tSRlBaRHhBTUJ6RkRTTjdjS3BmeC1DNUR6TzhLUjVtNkdfRTdvUGZaaVRqSFBqV1VuQ1RCQl9tRjhIVktfckNRZVpZUmJkSjRqTlk2dTRCVEgtc0E="
Integration ={"moto": "2068846",
                      "auth":"2142780", 
                      "cards": "192190", 
                      "wallet":	"194572",
                      "CAGG": "192493"}

iFrames ={ "cards": "180743",
                  "installment": "180742", 
                  "valU": "181460",     
}

def input_choose(): 
    while True:
        print("""Enter the desired method:
            1 for card
            2 for wallet
            3 for kiosk
            4 cash
            5 Invoice link creation
            6 product link creation """)
        
        try:
            value = input("please enter a value between 0 and 6:")
            value = int(value)
        except ValueError:
            print ('Valid number, please')
            continue
        if 0 <= value <= 6:
           match value:
                    case 1:
                        integration_id = Integration["cards"]
                        iframe = iFrames["cards"]
                        payment_token = auth_order_pay(amount=4000, integration_id= integration_id )
                        wb.open(f"https://accept.paymobsolutions.com/api/acceptance/iframes/{iframe}?payment_token={payment_token}")
                    case 2:
                        integrat = "auth"
                    case 3: 
                        integrat = "cards"
                    case 4: 
                        integrat = "wallet"
                    case 5: 
                        integrat = "CAGG"
                
                        break    
        else:
            print ("please enter a valid number")

def auth(API_key):
    payload = {"api_key":API_key}
    r = req.post("https://accept.paymob.com/api/auth/tokens",json=payload)
    
    print(r.json())
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