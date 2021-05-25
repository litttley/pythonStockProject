
import smtplib
from email.header import Header
from email.mime.text import MIMEText


class MailUtils(object):
    def __init__(self):
        # 导入配置文件，内部有邮箱配置信息
        self.from_addr = "xxxxx@163.com"
        self.to_addr = "xxxxx@qq.com"
        self.smtp_server = "smtp.163.com"
        self.password = "xxxxx"

    # 发送邮件的程序，需要指定主题和邮件的内容
    def send_email(self, subject, text):
        try:
            msg = MIMEText(text, 'plain', 'utf-8')
            msg['From'] = self.from_addr
            msg['To'] = self.to_addr
            msg['Subject'] = Header(subject, 'utf-8').encode()
            server = smtplib.SMTP_SSL(self.smtp_server, 465)
            server.login(self.from_addr, self.password)
            server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
            server.quit()
            return True
        except Exception as e:
            print('发送失败%s' % e)
            return False


if __name__ == '__main__':
    MailUtils().send_email('测试', '测试2')
