// emailapp/send_email.js
const nodemailer = require('nodemailer');

async function sendEmail(config, toEmail, subjectEmail, htmlEmail, textEmail) {
    let transporter = nodemailer.createTransport({
        host: config.smtphost,
        port: config.smtpport,
        secure: true,
        auth: {
            user: config.email,
            pass: config.smtp_password,
        },
    });

    let mailOptions = {
        from: config.email,
        to: toEmail,
        cc: config.cc_mail,
        bcc: config.bcc_mail,
        subject: subjectEmail,
        text: textEmail,
        html: htmlEmail,
    };

    return transporter.sendMail(mailOptions);
}

module.exports = sendEmail;
