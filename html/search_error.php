<?php
if(isset($_POST['submit'])){
    //$to = "hydrinium.h2@gmail.com"; // this is your Email 
	$to = "pushkar@bu.edu";
    //$bcc = "jvlo@bu.edu"; //Bcc recipients
	//$bcc = "hydrinium.h2@gmail.com";
    $from = $_POST['email']; // this is the sender's Email address
    $first_name = $_POST['first_name'];
    $last_name = $_POST['last_name'];
	$data = $_POST['search_data'];
    $subject = "Error Report from HoTResDB user";
    $subject2 = "Copy of error report";
    $message = $first_name . " " . $last_name . " wants to report an error with the following search: " . "\n\n" . $data . "\n\n". "Additional comments:" . "\n\n" . $_POST['message'];
    $message2 = "Here is a copy of your message " . $first_name . "\n\n" . $_POST['message'];

    $headers = "From:" . $from;
    //$headers .="BCC: jvlo@bu.edu" //.PHP_EOL
    $headers2 = "From:" . $to;
    mail($to,$subject,$message,$headers);
    mail($from,$subject2,$message2,$headers2); // sends a copy of the message to the sender
	echo '<script language="javascript">';
    echo "alert('Error report sent. Thank you for your help! We will contact you shortly.');";
	echo '</script>';
	echo "<script>self.close();</script>";
    // You can also use header('Location: thank_you.php'); to redirect to another page.
    }
?>
<html>
	<title>Search Error!</title>
	<head>
		<!----Load CSS style sheets---->
		<link rel="stylesheet" type="text/css" href = "http://bioed.bu.edu/students_16/groupA/VHFstyle.css">
		<link rel="stylesheet" type="text/css" href = "http://bioed.bu.edu/students_16/groupA/VHFquerystyle.css">


		<!----Load Jquery ui API---->
		<!--Load jquery ui api-->
		<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
		<script src="//code.jquery.com/jquery-1.10.2.js"></script>
		<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
		<script type = "text/javascript">
			//Collect variables from search page and parse
			var data = window.opener.data;
			console.log(data);
			//Initialize string to be added into message with search parameters based on data
			var error_part = '';
			
			//find index of genes in search
			var symbol_start = data.search('genes');
			var symbol_end = symbol_start + data.substring(symbol_start).indexOf('&');
			//collect substring and parse (start at 6 after to get ride of 'genes=')
			var data_genes = data.substring(symbol_start + 6, symbol_end);
			var gene_symbol_list = data_genes.split('%0D%0A');
			
			//do the same with Ensemble search
			var ens_start = data.search('ensembl');
			var ens_end = ens_start + data.substring(ens_start).indexOf('&');
			var data_ens = data.substring(ens_start + 10, ens_end);
			var ens_list = data_ens.split('%0D%0A');
			
			//Same with username
			var u_start = data.search('username');
			var u_end = data.length - 1;
			var user = data.substring(u_start, u_end);
			
			//check if select-all was chosen
			var check_all = data.includes('select-all-fields=on');
			console.log(check_all);
			if (check_all == true){
				error_part = ' Viruses: All \n Strains: All \n Datatypes: All \n Genes: ';
				error_part = error_part.concat(gene_symbol_list);
				error_part = error_part.concat('\n Ensemble IDs: ');
				error_part = error_part.concat(ens_list);
				error_part = error_part.concat('\n Username: ');
				error_part = error_part.concat(user);
			}
			else{
				error_part = ' Viruses::: ';
				var check1 = data.includes('evirus=ebola');
				if (check1 == true){
					error_part = error_part.concat('Ebola ');
				}
				var check2 = data.includes('mvirus=marburg');
				if (check2 == true){
					error_part = error_part.concat('Marburg ');
				}
				var check3 = data.includes('lvirus=lassa');
				if (check3 == true){
					error_part = error_part.concat('Lassa ');
				}
				error_part = error_part.concat('\n Ebola strains::: ');
				var check4 = data.includes('estrain1=Mayinga');
				if (check4 == true){
					error_part = error_part.concat('Mayinga ');
				}
				var check5 = data.includes('estrain2=Kikwit');
				if (check5 == true){
					error_part = error_part.concat('Kikwit ');
				}
				error_part = error_part.concat('\n Marburg strains::: ');
				var check6 = data.includes('mstrain=Angola');
				if (check6 == true){
					error_part = error_part.concat('Angola ');
				}
				error_part = error_part.concat('\n Lassa strains::: ');
				var check7 = data.includes('lstrain=Josiah');
				if (check7 == true){
					error_part = error_part.concat('Josiah ');
				}
				error_part = error_part.concat('\n Datatypes::: ');
				var check8 = data.includes('type1=RNA');
				if (check8 == true){
					error_part = error_part.concat('RNAseq ');
				}
				var check9 = data.includes('type2=Micro');
				if (check9 == true){
					error_part = error_part.concat('Microarray ');
				}
				var check10 = data.includes('type3=Nanostring');
				if (check10 == true){
					error_part = error_part.concat('Nanostring ');
				}
				var check11 = data.includes('survivors=Yes');
				if (check11 == true){
					error_part = error_part.concat(' \n Survivors::: Yes');
				}
				else{
					error_part = error_part.concat(' \n Survivors::: No');
				}
				error_part = error_part.concat('\n Genes::: ');
				error_part = error_part.concat(gene_symbol_list);
				error_part = error_part.concat('\n Ensemble IDs::: ');
				error_part = error_part.concat(ens_list);
				error_part = error_part.concat('\n Username::: ');
				error_part = error_part.concat(user);
			}
			//set value of hidden variable
			$(document).ready(function() {
				$('#search_data').val(error_part);
			});
			
		
			function checkvalue(field){
            var fname=field[0].value;
            var lname=field[1].value;
            var email=field[2].value;
            var comment=field[3].value;
            console.log(field);
            console.log(fname);
            console.log(lname);
            console.log(email);
            console.log(comment);
            if (fname == "" || lname == "" || email== ""){
                window.alert("Please fill in required fields");
                return false;
            } else {
                return true;
            }
		};
		</script>
	</head>
	<body>
	<div class = "search_data_outer_div" >
		<p>We're sorry, something went wrong. The database is still in development and we apologize for the error. To help us prevent this from happening again, please fill out the form below.</p> <br>
		<div class="search_field_box">
            <form action="" method="post" onsubmit="return checkvalue(this);">
            <div>First Name: </div>
                <div class="search" id ="fname"><input type="text" name="first_name"></div>
            <div>Last Name: </div>
                <div class="search" id ="lname"><input type="text" name="last_name"></div>
            <div>E-mail:</div>
                <div class="search" id="email"><input type="text" name="email" value=""></div>
            <div>Comment: <i>*optional</i></div>
                <div class="input_textarea" id="comment"><textarea cols="60" rows="10" name="message" value=" "></textarea></div> 
			<br>
			<input id = "search_data" name = "search_data" type="hidden" value = "data"/>
			<i>Note:  Your search parameters will be automatically sent to us with the information you enter.</i>
			<br>
            <div class = "center">
				<br><br>
                <div class = "search_field_title"><input id ="button" type = "submit" name="submit" value ="Send" /></div>
                <div class = "search_field_title"><input type = "reset" value ="Reset"/></div>
	        </div>
            </form>
		</div>
		<br>
		<br>
		<p>To try again, please go back to the search page and modify the search parameters by removing some of the genes.</p>
		<br>
		<h2>OR</h2>
		<br>
		<p>If you would prefer to send us suggestions or a more detailed message, please visit our <a href = "http://hotresdb.bu.edu/VHFContact.php" target="_blank">contact page</a>.</p>
		<br>
		<br>
		Thank you! <br>
		The HoTResDB Team
		<br>
		<br>
	</div>
	</body>

</html>

