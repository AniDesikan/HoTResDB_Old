<?php 
if($_SERVER["REQUEST_METHOD"] == "POST"){
    $to = "pushkar@bu.edu"; // this is your Email address
    $from = $_POST['email']; // this is the sender's Email address
    $first_name = $_POST['fname'];
    $last_name = $_POST['lname'];
    $subject = "Database Access Request";
    $subject2 = "Copy of your Registration";
    $message = $first_name . " " . $last_name . " is requesting database access. Go to http://10.231.6.30/VHFUserAccess.html to edit user access.";
    $message2 = "Here is a copy of your account details " . $first_name . "\n\n" . "Username: " . $_POST['uname']. "\n\n" . "Password: " . $_POST['pword'] . "\n\n" . "Name: " . $first_name . " " . $last_name . "\n\n" . "Email: " . $from;

    $headers = "From:" . $from;
    $headers2 = "From:" . $to;
    mail($to,$subject,$message,$headers);
    mail($from,$subject2,$message2,$headers2); // sends a copy of the message to the sender
    echo "Request Sent. Thank you " . $first_name . ", we will contact you shortly.";
}
?>