# 📬 Email Service
This is the backend email service that manage all the [reciclatusanimales.com](https://reciclatusanimales.com) apps email requests.

<div align="center"><img src="https://resources.reciclatusanimales.com/image/email-service.png" width=600></div>

It is built with [Django](https://www.djangoproject.com/) and [Django Background Tasks](https://django-background-tasks.readthedocs.io/) to handle the incoming emails as a queue, that runs an email dispatcher function to send emails and their respective automatic responses, if these are configured.
<br />

<div align="center"><img src="https://resources.reciclatusanimales.com/gif/email-service.gif" width=300></div>

<br />

## Features 📋
* Email queue handler.
* Configurable autoresponse emails.

<br/>
## Setup 🚀

To clone and run this application, you'll need [Git](https://git-scm.com), [pip](https://pip.pypa.io/) and [virtualenv](https://virtualenv.pypa.io/) installed on your computer. 

From your command line:

```bash
# Clone this repository
$ git clone https://github.com/reciclatusanimales/email-service.git

# Go into the project folder
$ cd email-service

# Create an environment
$ virtualenv .

# Install project dependencies
$ pip install -r requirements.txt

# Run migrations
$ manage.py migrate

# Run the project
$ manage.py runserver
```

You'll need to run the [Django Background Tasks](https://django-background-tasks.readthedocs.io/) ```manage.py process_tasks``` command to process the email queue. You can do it directly at the terminal or creating a Linux service like this:

```bash
[Unit]
Description=Email_sender

[Service]
Type=simple
WorkingDirectory=/your_working_directory/
ExecStart=/your_virtualenv_directory/bin/python /your_working_directory/manage.py process_tasks

[Install]
WantedBy=multi-user.target
```
<br />
Also, this app uses an API_KEY to authenticate every requester app and get access to the email enqueuer.

(This app does not have a demo, since its operation is entirely at the backend level, so it does not have a graphical interface.)

<br />

## Built with 🛠️
* [Django](https://www.djangoproject.com/) - v2.2.19
* [Django Background Tasks](https://django-background-tasks.readthedocs.io/) - v1.2.5




<br />
<br />

⌨️ por [Daniel Reyes Veas](https://github.com/danielreyesveas)
<br />
💾 [reciclatusanimales.com](https://reciclatusanimales.com)

<br />