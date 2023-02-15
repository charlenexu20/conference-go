import json
import pika
import django
import os
import sys
from django.core.mail import send_mail


sys.path.append("")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "presentation_mailer.settings")
django.setup()


# Create a function that will process the message when it arrives
def process_approval(ch, method, properties, body):
    content = json.loads(body)
    presenter_name = content["presenter_name"]
    presenter_email = content["presenter_email"]
    title = content["title"]

    send_mail(
        subject="Your presentation has been accepted",
        message=f"{presenter_name}, we're happy to tell you that your presentation {title} has been accepted",
        from_email="admin@conference.go",
        recipient_list=[f"{presenter_email}"],
        fail_silently=False,
    )


def process_rejection(ch, method, properties, body):
    content = json.loads(body)
    presenter_name = content["presenter_name"]
    presenter_email = content["presenter_email"]
    title = content["title"]

    send_mail(
        subject="Your presentation has been rejected",
        message=f"{presenter_name}, we're sorry to tell you that your presentation {title} has been rejected",
        from_email="admin@conference.go",
        recipient_list=[f"{presenter_email}"],
        fail_silently=False,
    )


# Create a main method to run
def main():
    parameters = pika.ConnectionParameters(host="rabbitmq")
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue="presentation_approvals")
    channel.basic_consume(
        queue="presentation_approvals",
        on_message_callback=process_approval,
        auto_ack=True,
    )
    channel.queue_declare(queue="presentation_rejections")
    channel.basic_consume(
        queue="presentation_rejections",
        on_message_callback=process_rejection,
        auto_ack=True,
    )
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
