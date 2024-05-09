from flask import Flask, request, render_template, render_template_string, redirect, url_for
import os
import random

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")

@app.route('/register', methods=['GET', 'POST'])
def chall():
	if request.method == "POST":
		name = request.form['user']
		template = '''
<html>
<head><title>Sloth dev</title></head>
<body>
<<center>

<h1>Lazy Dev</h1>
<br><br>

<table>
<tr>
<td>
<div>
     <img src="{{ url_for('static', filename='mem.jpg') }}" alt="Image">
</div>
</td>
</tr>
<tr>
<td>
    <h3>website location : ./website.png</h3>
</td>
</tr>
</table>

</center>
<!-- Hello %s  -->
<!-- ======================================== -->
<!-- I asked the developer to keep the page as much as simple you can -->
<!-- ======================================== -->
<!-- But i didnt expect this, he made it very simple -->
<!-- ======================================== -->
</body>
</html>
		''' % name

		return render_template_string(template)


@app.route("/logout")
def logout():
	return redirect(url_for('home'))

if __name__ == "__main__":
	app.run(port=5000)
