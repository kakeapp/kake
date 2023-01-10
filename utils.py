# utils.py

import os
import dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_verification_mail(emailid: str, verify_url: str) -> None:
    """ Used to send verification mail """
    dotenv.load_dotenv(".env")
    email = os.environ.get("KAKE_EMAILID")
    message = Mail(
        from_email=email,
        to_emails=emailid,
        subject='Kake app verification',
        html_content=HTML.replace("#something", verify_url))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)

def send_checkout_token(emailid: str, token: str) -> None:
    """ Send checkout token to email id """
    dotenv.load_dotenv(".env")
    email = os.environ.get("KAKE_EMAILID")
    message = Mail(
        from_email=email,
        to_emails=emailid,
        subject='Kake app checkout token',
        html_content=CHECKOUT_HTML.replace("#token", token))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)
    print("sent token", token)


CHECKOUT_HTML = """
<html>
<style>
	* {
		padding: 10px;
		margin: 0;
		background-color: aqua;
	}

	.center {
		text-align: center;
	}

	.token {
		background-color: gray;
		color: gray;
		transition: 1s;
	}

	.token:hover {
		color: white;
	}

	div {
		padding: 20px;
	}

	div h3 {
		padding: 10px;
		background-color: chocolate;
	}

	button {
		padding: 10px;
		border: 0;
		color: white;
		margin: 5px;
		background-color: #555;
	}

	button:hover {
		background-color: #111;
	}

	div p {
		padding: 10px;
	}
</style>

<body>
	<div>
		<h3 class="center">Checkout token</h3>
		This is the token used for checking out of the cart. Please ensure that it is not shared with anyone.
		<div class="token center">#token</div>
	</div>
</body>

</html>
"""

HTML = """
<html>
  <style>
    * {
  padding: 0;
  margin: 0;
  background-color: aqua;
}

.center {
  text-align: center;
}

div {
  padding: 20px;
}

div h3{
  padding: 10px;
  background-color: chocolate;
}

button {
  padding: 10px;
  border: 0;
  color: white;
  margin: 5px;
  background-color: #555;
}

button:hover {
  background-color: #111;
}

div p {
  padding: 10px;
}
  </style>
  <body>
    <div class='center'>
      <h3>Verification Email</h3>
      <p>Your profile registration will be done as soon as you click on verify below.</p>
      <a href="#something"><button>Verify!</button></a>
      <p>If you did not make this registration, please change your email access and take necessary precautions.</p>
    </div>
  </body>
</html>
"""
