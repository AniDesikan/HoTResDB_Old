<?php
$message = "";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $fname = $_POST['first_name'];
    $lname = $_POST['last_name'];
    $email = $_POST['email'];
    $comment = $_POST['message'];

    // Validate inputs
    if (empty($fname) || empty($lname) || empty($email) || empty($comment)) {
        $message = "Please fill in all fields";
    } else {
        // Email address where you want to receive the messages
        $to = "pushkar@bu.edu";
        $subject = "HoTResDB Contact Form Submission";
        $message_body = "First Name: $fname\n";
        $message_body .= "Last Name: $lname\n";
        $message_body .= "Email: $email\n";
        $message_body .= "Message: $comment\n";

        // Additional headers
        $headers = "From: HoTResDB " . "\r\n" .
                   "X-Mailer: PHP/" . phpversion();



        // Send email
        if (mail($to, $subject, $message_body, $headers)) {
            $message = "Your message has been sent successfully!";
        } else {
            $message = "Failed to send your message. Please try again later.";
        }
    }
    
    echo $message; // Send the message back to JavaScript for display
}
?>
