from flask import Flask, render_template, request, abort
from werkzeug.routing import BaseConverter, Rule
from flask_mail import Mail, Message



app = Flask(
	__name__,
	template_folder='templates',
	static_folder='static'
)

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super().__init__(url_map)
        self.regex = items[0]
        
app.config['MAIL_SERVER'] = 'smtp.mailgun.org'
app.config['MAIL_PORT'] = 587 
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'postmaster@codeleap.org'
app.config['MAIL_PASSWORD'] = '5b295ac3be138aa5d5acb177d5bf3bd5-73f745ed-9301e2f7'
app.config['MAIL_DEFAULT_SENDER'] = 'no_reply@codeleap.org'

mail = Mail(app)

app.url_map.converters['regex'] = RegexConverter

def send_zoom_url_email(name, email):
    zoom_url = "https://us04web.zoom.us/j/79343753140?pwd=KatEtBLdFr1MKpSHxH9gAy4xXn3SqV.1"

    subject = "Zoom Meeting URL for Introduction to Python"
    body = f"Dear {name},\n\nThank you for registering for Introduction to Python. Here is the Zoom meeting URL:\n\n{zoom_url}\n\nWe are looking forward to seeing you there!\n\nBest regards,\nYour Python Team"

    message = Message(subject=subject, recipients=[email], body=body)

    try:
        mail.send(message)
    except Exception as e:
        # Handle email sending errors here, e.g., logging the error
        print(f"Error sending email: {e}")


@app.route('/')
def home_page():
	return render_template(
		'home.html'
  	)

@app.route('/about')
def about_page():
	return render_template(
		'home.html'
  	) #Change Later

@app.route('/register')
def register_page():
	return render_template(
		'register.html'
  	)

@app.route('/register_email', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Send email with Zoom meeting URL
        send_zoom_url_email(name, email)

        return render_template(
	    	'register.html',
            registered=True
  	    )

@app.route('/faq')
def faq_page():
	return render_template(
		'faq.html'
  	)

@app.errorhandler(404)
def not_found_error(error):
	return render_template(
		'error404.html'
  	)

@app.errorhandler(500)
def internal_error(error):
	return render_template(
		'error500.html'
  	)

@app.before_request
def check_routes():
    rule = request.url_rule
    if rule and not any(url.rule == rule.rule for url in app.url_map.iter_rules() if isinstance(url, Rule)):
        abort(404)

if __name__ == "__main__":
	app.run(
		host='0.0.0.0',
		port=8080
	)
