try {

	$mail = new PHPMailer(true);
	// Configuración cabeceras del mensaje	
	$mail->IsHTML(true);
	$mail->From = "noresponder@medlog.uy";

	$mail->FromName = "Medlog";
	$mail->AddAddress('UY863-administrationmtc@medlog.com');
	$mail->AddAttachment($_FILES['archivo1']['tmp_name'], 'Curriculum.' . $ext);
	$mail->AddEmbeddedImage('../images/logo.png', 'logo');
	$mail->Subject = "Contacto desde WEB MEDLOG Uruguay / Trabajar";
	$mail->CharSet = "UTF-8";
} catch (Exception $e) {
        echo "Mailer Error: ".$mail->ErrorInfo;
}