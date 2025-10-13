import smtplib

try:
    connection = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)  # Setting a 10-second timeout
    connection.ehlo()
    connection.starttls()
    connection.login("izaqyos@gmail.com", "itgr fweg mjak qarn")
    connection.sendmail("izaqyos@gmail.com", "izaqyos@me.com", "test message from my smtp python script")
    connection.quit()
    print("Email sent successfully!")
except smtplib.SMTPException as e:
    print(f"Error sending email: {e}")
except TimeoutError:
    print("Connection timed out. Check your network or SMTP settings.")
