function getCookie(username) {
        var name = username + "=";
        var ca = document.cookie.split(';');
    //    console.log(ca);
        for(var i = 0; i < ca.length; i++) {
            var c = ca[i];
    //        console.log(c);
            while (c.charAt(0) == ' ') {
                c = c.substring(1);
            }
            if (c.indexOf(name) == 0) {
                return c.substring(name.length, c.length);
            }
        }
        return "";
    }
    
    
    //Checks cookie
    function checkCookie() {
        var username=getCookie("username");
        return username;
    }
    
    //Checks User Cookie
    function CheckUser() {
    //    console.log("Script works")
        var username=getCookie("username");
    //    console.log(username);
        if (username) {
    //        $(".topcorner").html("Welcome" + username);
            document.getElementsByClassName("topcorner")[0].innerHTML = "Welcome " + username;
            document.getElementById("login_button").innerHTML = "Log Out";
            document.getElementById("login_button").removeAttribute("formaction");
            document.getElementById("login_button").setAttribute("onclick", "resetCookie()");
    //        console.log(document.getElementsByClassName("topcorner")[0]);
    //        console.log("User")
        }
        else {
            document.getElementById("login_button").innerHTML = "Log In";
            document.getElementById("login_button").setAttribute("formaction", "VHFLogin.html");
            document.getElementsByClassName("topcorner")[0].innerHTML =  "Welcome Guest";
    //        console.log(document.getElementsByClassName("topcorner")[0]);
    //        console.log("Test2");
        }
        return username;
    }
    
    //Logout function
    function logout(){
        $( "form" ).on( "submit", function (event) {
            //Don't refresh page after submitting
            event.preventDefault();
        });
        var username=getCookie("username");
    //    console.log(username, "adfasfsa");
    }
    
    //Reset Cookie
    function resetCookie(){
    //    console.log("Cookie Reset")
        d ="Thu, 01 Jan 1970 00:00:00 UTC";
        var expires = "expires:"+d; // changes expire time to UTC and sets as variable expires
        document.cookie = "username=" + "; " + expires; // Set Username to null
        //document.cookie = "session="; // Set session Id to null
        //document.cookie = expires;// Add very old expires time
    }
    
    //Function to set Cookie
    function setCookie(){
        var cname = document.getElementById("uname").value; // Set username in login as cookie username
    //    console.log(cname);
        var d = new Date();
        d.setTime(d.getTime() + 20*(1000*60)); //Set expire time as 20 minutes past current time
        var expires = "expires="+d.toUTCString(); // changes expire time to UTC and sets as variable expires
        ////console.log(expires);-->
        var cvalue = Math.floor((Math.random()*Math.pow(10,13))+1); //Set cookie id as random number
    //    var domain = ";domain=hotresdb-development.bu.edu"// Add domain to cookie
        document.cookie = "username=" + cname + "; " + expires; // Add username to cookie
        //document.cookie = "session=" + cvalue; expires;// Add session id to cookie
        //document.cookie = expires;// Add expiration time to cookie
    }
    
    //Idle logout function
    var idleInterval = null;
    var idleTime = 0;
    $(document).ready(function () {
        user_status = checkCookie();
        if (user_status){ // If the user is logged in, start idle timer
            timer_reset();
        }
    });
    function timer_reset(){
        //Increment the idle time counter every minute.
        idleInterval = setInterval(timerIncrement, 60*1000); // 1 minute
    
        //Zero the idle timer on mouse movement.
        $(this).mousemove(function (e) {
            idleTime = 0;
    //        console.log("Timer Reset");
        });
        $(this).keypress(function (e) {
            idleTime = 0;
    //        console.log("Timer Reset");
        });
    }
    function timerIncrement() {
        idleTime = idleTime + 1;
        console.log(idleTime);
        if (idleTime > 19) { // 20 minutes
            resetCookie();
            clearInterval(idleInterval);
            CheckUser();
            alert("Idle session detected. User logged out.");
        }
    }
    $(document).ready(function () {
        CheckUser();
    //    $('#loading_image').show();
    //    console.log("Test");
    });
    
    {/* // type = "text/javascript"> */}
    //Javascript to check if current server is development and assign google ID based on server type
    var ID = "";
    if(window.location.href.indexOf("development") > -1) {
            ID = "";
    }
    else{
            ID = "UA-80347666-2";
    }
    
    window.ga=window.ga||function(){(ga.q=ga.q||[]).push(arguments)};ga.l=+new Date;
    ga('create', ID, 'auto');
    // //console.log(ID);-->
    ga('send', 'pageview');
    //>
    // async src='https://www.google-analytics.com/analytics.js'>//>
    // //- End Google Analytics -->
    
    // //--Java/AJAX Functions---->
    // // type = "text/javascript">
            $(document).ready(function(){
                    // Toggles the Search boxes
                    $('#ebov, #marv, #lasv').change(function(){
                            var name_id = "#search_field_" + (this).getAttribute("id");
                            var bool = (this).checked;
                            var virus_checked = $(".virus").is(":checked");
                            $(name_id).toggle();
                            if (bool == true){
                                    $('.strainname').show();
                            }
                            if (bool == false && virus_checked == false){
                                    $('.strainname').hide();
                            }
                            //$('#Microbox').show();-->
                            //$('#strain_label').show();-->
                            //console.log($('#strain_label'));-->
                            //var num_checked = $(".strain_width").children(":visible").length; //Checks if there are any other strains selected, if not removes select all option as well-->
                            //console.log(num_checked);-->
                            //if (num_checked == 0){-->
                                    //$('#strain_label').hide();-->
                            //}-->
                    });
    
    
                            //Strain Checkbox logic
                    var may_bool, kik_bool, mak_bool, ang_bool, jos_bool, all_bool, strain_bool;
                    var RNA_vote = Micro_vote = Nano_vote = Surv_vote =0;
    function count_checks(){ //Counts number of checked checkboxes
            may_bool = $('#maybox').prop("checked");
            kik_bool = $('#kikbox').prop("checked");
            mak_bool = $('#makbox').prop("checked");
            ang_bool = $('#angbox').prop("checked");
            jos_bool = $('#josbox').prop("checked");
            num_checked = may_bool + kik_bool + mak_bool + ang_bool + jos_bool;
            //console.log(num_checked);-->
            return num_checked;
    }
    function datatype_vote(RNAseq ,Microarray, Nanostring, Survival){//Counts number of strains which require each datatype to be visible
            RNA_vote += RNAseq;
            Micro_vote += Microarray;
            Nano_vote += Nanostring;
            Surv_vote += Survival;
            //console.log(RNA_vote, Micro_vote, Nano_vote,Surv_vote);-->
            return [RNA_vote, Micro_vote, Nano_vote, Surv_vote];
            }
    //Resets all votes when a select-all button is clicked
    $("#select-all-strain").change(function(){
                            strain_bool = $('#select-all-strain').prop("checked");
            if (strain_bool == true){
                    datatype_vote(-RNA_vote+4,-Micro_vote+1,-Nano_vote+1,-Surv_vote+2); //Set votes to state where all are checked [4,1,1,2]
            }
            if (strain_bool == false){
                    datatype_vote(-RNA_vote,-Micro_vote,-Nano_vote,-Surv_vote); //Set all votes to 0
            }
    });
                    $("#select-all-fields").change(function(){
                            all_bool = $('#select-all-fields').prop("checked");
            if (all_bool == true){
                    datatype_vote(-RNA_vote+4,-Micro_vote+1,-Nano_vote+1,-Surv_vote+2); //Set votes to state where all are checked [4,1,1,2]
            }
            if (all_bool == false){
                    datatype_vote(-RNA_vote,-Micro_vote,-Nano_vote,-Surv_vote); //Set all votes to 0
            }
    });
                    $('#maybox').change(function(){
                            var num_checked = count_checks();
                            //var visible_checkbox = $(".strainname").find(":checkbox:visible");-->
                            if (may_bool == true){
                            datatype_vote(1,1,0,0);
            $('#RNAbox').show();
            $('#Microbox').show();
            $('.Datatype, .datatype').show();
            $('#datatype_label').show();
            //console.log(may_bool);-->
                            }
                            if (may_bool == false && num_checked == 0){ //If mayinga is unchecked an other strains are un checked Then hide all checkboxes
            datatype_vote(-1,-1,0,0);
            $('#RNAbox').hide();
            $('#Microbox').hide();
            $('.Datatype, .datatype').hide();
            $('#datatype_label').hide();
            //console.log("may State 1");-->
                            }
            else if (may_bool == false && num_checked > 0){ //If mayinga is unchecked but other strains are checked Then hide only checkboxes that need to be hidden, mostly microarray
            var votes = datatype_vote(-1,-1,0,0);
            if (votes[0] == 0){
                    $('#RNAbox').hide();
                    }
            if (votes[1] == 0){
                    $('#Microbox').hide();
                    }
            if (votes[0] + votes[1] + votes[2] == 0){
                    $('.Datatype').hide();
                    $('#datatype_label').hide();
                    }
            //console.log("may State 2");-->
                            }
                    });
    
                    $('#kikbox').change(function(){
            var num_checked = count_checks()
            if (kik_bool == true){
            datatype_vote(1,0,0,1);
            $('#RNAbox').show();
            $('.Datatype, .datatype').show();
            $('#datatype_label').show();
                            }
            if (kik_bool == false && num_checked == 0){
            datatype_vote(-1,0,0,-1);
            $('#RNAbox').hide();
                                    $('.Datatype, .datatype').hide();
            $('#datatype_label').hide();
            //console.log("kik state 1");-->
                            }
                            if (kik_bool == false && num_checked > 0){
                                    var votes = datatype_vote(-1,0,0,-1);
                                    if (votes[0] == 0){
                                    $('#RNAbox').hide();
                                    }
                                    //console.log("kik state 2");-->
                            }
                    });
    
                    $('#makbox').change(function(){
                            var num_checked = count_checks()
                            if (mak_bool == true){
            datatype_vote(1,0,1,1);
            $('#Nanobox, #RNAbox, #Nanostring_div').show();
            $('.Datatype, .datatype').show();
            $('#datatype_label').show();
                            }
            if (mak_bool == false && num_checked == 0){
            datatype_vote(-1,0,-1,-1);
            $('#Nanobox, #RNAbox, #Nanostring_div').hide();
                                    $('.Datatype,.datatype').hide();
            $('#datatype_label').hide();
            //console.log("mak state 1");-->
                            }
                            if (mak_bool == false && num_checked > 0){
                                    var votes = datatype_vote(-1,0,-1,-1);
                                    if (votes[2] == 0){
                                    $('#Nanobox, #Nanostring_div').hide();
                                    }
                                    if (votes[3] == 0){
                                    }
                                    //console.log("mak state 2");-->
                            }
                    });
    
                    $('#angbox').change(function(){
                            var num_checked = count_checks()
                            if (ang_bool == true){
            datatype_vote(1,0,0,0);
            $('#RNAbox').show();
            $('.Datatype, .datatype').show();
            $('#datatype_label').show();
                            }
            if (ang_bool == false && num_checked == 0){
            datatype_vote(-1,0,0,0);
            $('#RNAbox').hide();
                                    $('.Datatype, .datatype').hide();
            $('#datatype_label').hide();
            //console.log("ang state 1");-->
                            }
                            if (ang_bool == false && num_checked > 0){
                                    var votes = datatype_vote(-1,0,0,0);
                                    if (votes[0] == 0){
                                    $('#RNAbox').hide();
                                    }
                                    //console.log("ang state 2");-->
                            }
                    });
    
                    $('#josbox').change(function(){
                            var num_checked = count_checks()
                            if (jos_bool == true){
            datatype_vote(1,0,0,0);
            $('#RNAbox').show();
            $('.Datatype, .datatype').show();
            $('#datatype_label').show();
                            }
            if (jos_bool == false && num_checked == 0){
            datatype_vote(-1,0,0,0);
            $('#RNAbox').hide();
                                    $('.Datatype, .datatype').hide();
            $('#datatype_label').hide();
            //console.log("jos state 1");-->
                            }
                            if (jos_bool == false && num_checked > 0){
                                    var votes = datatype_vote(-1,0,0,0);
                                    if (votes[0] == 0){
                                    $('#RNAbox').hide();
                                    }
                                    //console.log("jos state 2");-->
                            }
                    });
                    $('#ebov').change(function(){
                            if (may_bool == true){
                                    //console.log(may_bool);-->
                                    datatype_vote(-1,-1,0,0);
                            }
                            if (kik_bool == true){
                                            datatype_vote(-1,0,0,0);
                            }
                            if (mak_bool == true){
                                            datatype_vote(-1,0,-1,-1);
                            }
                            $('#search_field_ebov').find("input:checkbox").attr('checked', false);
                            var num_checked = count_checks()
                            var ebov_bool = $('#ebov').prop('checked');
                            //console.log(num_checked);-->
            if (ebov_bool == false && num_checked == 0){
            //datatype_vote(-1,-1,-1,-1);-->
            $('#Nanobox, #RNAbox, #Nanostring_div').hide();
            $('#Microbox').hide();
                                    $('.Datatype,.datatype').hide();
            $('#datatype_label').hide();
            $('#Microbox, #RNAbox, #Nanobox').find("input:checkbox").attr('checked', false);
                            }
                            if (ebov_bool == false && num_checked > 0){
                                    var votes = datatype_vote(0,0,0,0);
                                    if (votes[0] == 0){
                                    $('#RNAbox').hide();
                                    $('#RNAbox').find("input:checkbox").attr('checked', false);
                                    }
                                    if (votes[1] == 0){
                    $('#Microbox').hide();
                    $('#Microbox').hide().find("input:checkbox").attr('checked', false);
                    }
                                    if (votes[2] == 0){
                                    $('#Nanobox, #Nanostring_div').hide();
                                    $('#Nanobox, #Nanostring_div').find("input:checkbox").attr('checked', false);
                                    }
                            }
                    //console.log(votes);-->
    
                    });
                    $('#marv').change(function(){
                            if (ang_bool == true){
                                            //console.log(may_bool);-->
                                            datatype_vote(-1,0,0,0);
                                    }
                            $('#search_field_marv').find("input:checkbox").attr('checked', false);
                            var num_checked = count_checks()
                            var marv_bool = $('#marv').prop('checked');
            if (marv_bool == false && num_checked == 0){
            //datatype_vote(-1,0,0,0);-->
            $('#RNAbox').hide();
            $('#RNAbox').find("input:checkbox").attr('checked', false);
                                    $('.Datatype, .datatype').hide();
            $('#datatype_label').hide();
                            }
                            if (marv_bool == false && num_checked > 0){
                                    var votes = datatype_vote(0,0,0,0);
                                    if (votes[0] == 0){
                                    $('#RNAbox').hide();
                                    $('#RNAbox').find("input:checkbox").attr('checked', false);
                                    }
                            }
                    });
                    $('#lasv').change(function(){
                            if (jos_bool == true){
                                            datatype_vote(-1,0,0,0);
                                    }
                            $('#search_field_lasv').find("input:checkbox").attr('checked', false);
                            var num_checked = count_checks()
                            var lasv_bool = $('#marv').prop('checked');
            if (lasv_bool == false && num_checked == 0){
            //datatype_vote(-1,0,0,0);-->
            $('#RNAbox').hide();
            $('#RNAbox').find("input:checkbox").attr('checked', false);
                                    $('.Datatype, .datatype').hide();
            $('#datatype_label').hide();
                            }
                            if (lasv_bool == false && num_checked > 0){
                                    var votes = datatype_vote(0,0,0,0);
                                    if (votes[0] == 0){
                                    $('#RNAbox').hide();
                                    $('#RNAbox').find("input:checkbox").attr('checked', false);
                                    }
                            }
                    });
    
                    //Toggles all fields visibility
                    $('#select-all-fields').change(function(){
                            var rna, nano, micro, ebov, marv, lasv, select;
                            select = $('#select-all-fields').prop("checked");
                            //rna = $('#RNAbox').is(":visible");-->
                            //nano = $('#Nanobox').is(":visible");-->
                            //micro = $('#Microbox').is(":visible");-->
                            //ebov = $('#search_field_ebov').is(":visible");-->
                            //marv = $('#search_field_marv').is(":visible");-->
                            //lasv = $('#search_field_lasv').is(":visible");-->
                            $('.Datatype').show();
                            //var test = $('#select-all-fields').is(":visible");-->
                            //console.log(test);-->
                            if (select == true){
                                    $('#RNAbox').show();
                                    $('#Nanobox').show();
                                    $('#Microbox').show();
                                    $('#search_field_ebov').show();
                                    $('#search_field_marv').show();
                                    $('#search_field_lasv').show();
                                    $('#strain_label').show();
                                    $('#datatype_label').show();
                                    $('.strainname').show();
                                    $('.survivor').show();
                                    $('.datatype').show();
                                    //$('#Nanostring_div').show();-->
                            }
                            if (select == false){
                                    $('#RNAbox').hide();
                                    $('#Nanobox').hide();
                                    $('#Microbox').hide();
                                    $('#search_field_ebov').hide();
                                    $('#search_field_marv').hide();
                                    $('#search_field_lasv').hide();
                                    $('#strain_label').hide();
                                    $('#datatype_label').hide();
                                    $('.Datatype').hide();
                                    $('.strainname').hide();
                                    $('.survivor').hide();
                                    $('.datatype').hide();
                                    $('#Nanostring_div').hide();
                            }
    
                    });
                    //Toggles all viruses
                    $('#select-all-virus').change(function(){
                            var ebov, marv, lasv, select;
                            select = $('#select-all-virus').prop("checked");
                            //ebov = $('#search_field_ebov').is(":visible");-->
                            //marv = $('#search_field_marv').is(":visible");-->
                            //lasv = $('#search_field_lasv').is(":visible");-->
                            if (select == true){
                                    $('#search_field_ebov').show();
                                    $('#search_field_marv').show();
                                    $('#search_field_lasv').show();
                                    $('#strain_label').show();
                                    $('.strainname').show();
                            }
                            if (select == false){
                                    $('#search_field_ebov').hide();
                                    $('#search_field_marv').hide();
                                    $('#search_field_lasv').hide();
                                    $('#RNAbox').hide();
                                    $('#Nanobox').hide();
                                    $('#Microbox').hide();
                                    $('.Datatype, .datatype').hide();
                                    $('#strain_label').hide();
                                    $('#datatype_label').hide();
                                    $('.strainname').hide();
                            }
                    });
    
                    //Toggles all Data Types
                    $('#select-all-strain').change(function(){
                            var rna, nano, micro, select;
                            select = $('#select-all-strain').prop("checked");
                            if (select == true){
                                    $('#RNAbox').show();
                                    $('#Microbox').show();
                                    $('.Datatype').show();
                                    $('#datatype_label').show();
                                    $('.datatype').show();
                                    if ($('#makbox').is(":visible")){
                                            $('#Nanobox, #Nanostring_div').show();
                                    }
                            }
                            if (select == false){
                                    $('#RNAbox').hide();
                                    $('#Microbox').hide();
                                    $('#Nanobox, #Nanostring_div').hide();
                                    $('.Datatype').hide();
                                    $('#datatype_label').hide();
                                    $('.datatype').hide();
                            }
                    });
    
                    ///CHECK COOKIE HERE///
                    var username = CheckUser();
                    $( "form[id='searchGene']" ).on( "submit", function (event) {
                    //Don't refresh page after submitting
                    event.preventDefault();
    
                    //Check if at least one virus box is checked
    
    
                    //Check if at least one virus box is checked
    
    
                    //Check for special characters
    
                    if(VHFform.genes.value.match(/[`~!@#\$%\^&\*\;\(\)\=_+\\\[\]{\}\?,\.\<\>]/)) {
                            alert('Cannot use special characters.');
                            return false;
                    }
                    if(VHFform.samples.value.match(/[`~!@#\$%\^&\*\;\(\)\=+\\\[\]{\}\?,\.\<\>]/)) {
                            alert('Cannot use special characters.');
                            return false;
                    }
                    if ( !document.getElementById("gene_inner").value) {
                            //alert and exit function if empty
                            alert("Please enter a gene ID.");
                            return false;
                    }
                    if (!document.getElementById("sample_inner").value) {
                            //alert and exit function if empty
                            alert("Please enter a dataset.");
                            return false;
                    }
                    //reload
                    //location.reload();
    
                    //go to counts graph tab
    
                    $('.appended').remove();
                    $('.append').remove();
                    //$('.search_result_header2').remove();
    
    
                    //Convert the form data into one string of key/value pairs for our python script to read
                    //Eg, "search_text='ABL1'&num_paths=4"
                    data = $( this ).serialize();
                    data += "&username=" + encodeURIComponent(username);
                    console.log(data)
                    //When the user submits the form, this function will be called
                    AjaxPlotChart(data);
                    $("#tabs").tabs("refresh");
                    $("#tabs").tabs( "option", "active", 3);
                    });
            });
    
    
            //Declare variables to be used later
            var DPI_array;
            var Count_array;
            var FC_array;
            var RNAseq_FC;
            var microarray_FC;
            var study_per_gene;
            var gene_per_study;
    
            function groupByArray(xs, key) {
                    return xs.reduce(function (rv, x) {
                            var v = key instanceof Function ? key(x) : x[key];
                            var el = rv.find((r) => r && r.key === v);
                            if (el) {
                                    el.values.push(x);
                            } else {
                                    rv.push({ key: v, values: [x] });
                            }
    
                    return rv;
            }, []); }
    
    
            function AjaxPlotChart(data) {
            $('#loading_image').show(); //when request is sent, show loading image
            //jquery to make ajax request to server
                    console.log(data);
                    $.ajax(
                    {
                            type: "POST",
                            url: "/cgi-bin/VHFQueries_new.py", //CGI script for charts
                            data: data,
                            dataType: "json",
                            success: function(response) //run function once we get response
                            {
                                    sessionStorage.clear(); //Clears any previous data
                                    $('#loading_image').hide();
                                    //Notify Google Analytics of search
                                    ga('send', 'event', 'search', 'click');
                                    console.log(response); //for debugging
                                    /*-------JSON OBJECT NOTES-------
                                            0 - gene summary table data
                                            1 - count line data
                                            2 - FC line data
                                            3 - DPI array data
                                            4 - count table data
                                            5 - FC table data
                                            6 - Heat Map X axis
                                            7 - Gene per study data
                                            8 - study per gene data
                                            9 - empty results
                                            10 - DPI heat map
                                            11 - DS heat map
                                            12 - microarray DPI_array
                                            13 - unclustered fold change data
                                            14 - microarray count data
                                            15 - nanostring count data
                                    */
    
                                            //////GENE SUMMARY FUNCTIONS/////
                                            drawGeneSummTable(response[0]);
                                            sessionStorage.setItem("Response0", JSON.stringify(response[0]));
    
                                            /////COUNT LINE RNAseq FUNCTIONS//////
                                            sessionStorage.setItem("CountLine", JSON.stringify(response[1])); //Stores data for later use
                                            sessionStorage.setItem("CountLine_all", JSON.stringify(response[1])); //To have microarray data appended
    
                                            /////FC LINE FUNCTIONS//////
                                            RNAseq_FC = response[2];
                                            study_per_gene = response[8];
                                            gene_per_study = response[7];
                                            sessionStorage.setItem("FCLine",JSON.stringify(response[2]));
    
                                            ////DAYS POST INFECTION////
                                            DPI_array = response[3];
                                            sessionStorage.setItem("DPI_array",JSON.stringify(response[3]));
                                            appendExpHeader(response[3]);
    
                                            /////TABLES//////
                                            Count_array = response[4];
                                            drawCountTable(response[4], response[3]);
                                            sessionStorage.setItem("Count_array",JSON.stringify(response[4]));
                                            FC_array = response[5];
                                            drawFCTable(response[5], response[3]);
                                            sessionStorage.setItem("FC_array",JSON.stringify(response[5]));
    
                                            /////PARSE DATA/////
                                            sessionStorage.setItem("Response7",JSON.stringify(response[7]));
                                            sessionStorage.setItem("Response8",JSON.stringify(response[8]));
                                            parseCountsStudyPerGene(response[1], response[8]);
                                            parseCountsGenePerStudy(response[1], response[7]);
                                            parseFCGenePerStudy(response[2], response[7]);
                                            parseFCStudyPerGene(response[2], response[8]);
    
    
                                            /////HEAT MAP//////
                                            //localStorage.setItem("Response1", JSON.stringify(response[1]));  //Stores data for heatmap for debugging-->
                                            //localStorage.setItem("Response6", JSON.stringify(response[6]));  //Stores data for heatmap for debugging-->
                                            //localStorage.setItem("Response10",JSON.stringify(response[10])); //Stores data for heatmap for debugging-->
                                            //localStorage.setItem("Response11",JSON.stringify(response[11])); //Stores data for heatmap for debugging-->
                                            sessionStorage.setItem("Response6", JSON.stringify(response[6]));
                                            sessionStorage.setItem("Response10",JSON.stringify(response[10]));
                                            sessionStorage.setItem("Response11",JSON.stringify(response[11]));
                                            //console.log(response[11]);
                                            sessionStorage.setItem("Response12",JSON.stringify(response[12]));
                                            sessionStorage.setItem("Response13",JSON.stringify(response[13]));
    
                                            /////Store microarray and nanostring data/////
                                            sessionStorage.setItem("Response14",JSON.stringify(response[14]));
                                            sessionStorage.setItem("Response15",JSON.stringify(response[15]));
                                            //sessionStorage.setItem("Response23",JSON.stringify(response[23]));
                                            //sessionStorage.setItem("Response24",JSON.stringify(response[24]));
                                            draw_nano_count_line(response[15]);
                                            //delayed activation of table scroll bars to adjust for size of table after search
                                            activate_scrollbars();
                                            for (var i = 0; i < response[0].length; i++) {
                                                    //Google Analytics loop, send each gene name in search results from response[0]
                                                    ga('send', 'event', 'search', 'submit', 'gene', response[0][i][1]);
                                            }
                                            if (response[9].length > 0){
                                                    console.log(response[8]);
                                                    //emptyGenesAlert(response[6]);
                                                    printEmpty(response[9],response[6]);
                                            }
                                            if(!$.isArray(response[1]) &&  !response[1].length && !$.isArray(response[13]) &&  !response[13].length) {
                                                    ga('send', 'event', 'search', 'No_result');
                                                    alert('The gene you searched for is either not in the database or you did not include the gene name in a form the database recognizes. Please use the Browse function to find the gene name. To see unpublished data you must log in.');
                                                    return;
                                            }
                                            $("#microarray_alert").hide();
                            },
                            error: function(data, status)
                            {
                                    console.log(status);
                                    console.log(data);
    
                                    ///LIVE PAGE PRINT OUT/////
                                    //$('#loading_image').hide();-->
                                    $("#microarray_alert").hide();
                                    console.log("Something went wrong in function 1 (RNAseq pipeline)");
                                    var search_error_window = window.open("/search_error.php", '_blank','width=500,height=500');
    
    
    
                                    //////////DEBUGGING MESSAGE///////////
                                    $("#error").html(data['responseText']);
                                    response(data);
    
                                    alert("We're sorry, it looks like something went wrong. Please contact us with your search parameters in the contact page so that we can investigate the issue.");
                            }
                    });
            }
    
            function drawGeneSummTable(array) {
                    var tr;
                    for (var i = 0; i < array.length; i++) {
                    tr = $('<tr/>');
                    tr.append("<td class = 'appended'>" + array[i][1] + "</td>");
                    tr.append("<td class = 'appended'>" + array[i][2] + "</td>");
                    tr.append("<td class = 'appended'>" + array[i][3] + "</td>");
                    tr.append("<td class = 'appended'>" + array[i][4] + "</td>");
                    tr.append("<td class = 'appended'><a target='_blank' href='http://www.genecards.org/cgi-bin/carddisp.pl?gene=" + array[i][2] + "'>Click for more information</a></td>");
    
                    $('.search_result_tab').append(tr);
            }
            }
    
            var DPI_checker = 0;
    
            function appendExpHeader(array) {
                    //Add DPI array to table
                    var tr;
                    if (DPI_checker == 0){
                            for (var i = 0; i < array.length; i++) {
                                    tr = $('<td/>');
                                    tr.append('<div class = "append">');
                                    tr.append(array[i]);
                                    tr.append(' DPI</div>');
                                    $('.search_result_table_header').append(tr);
                                    DPI_checker = 1;
                            }
                    }
            }
    
            function drawCountTable(array, DPI_array) {
                    var tr;
                    //Get max length of DPI array and add 5 to fit table format because there are 5 columns already filled before adding data
                    var max = DPI_array.length;
                    max = max + 5;
                    for (var i = 0; i < array.length; i++) {
                            tr = $('<tr/>');
                            //reset count to 0 to compare against dpi array index
                            var count = 0;
                            for (var j = 0; j < array[i].length; j++) {
                                    if (isNaN(array[i][j]) == true){
                                            tr.append("<td class = 'appended' style = 'min-width:90px;'><div style = 'overflow:auto;'>" + array[i][j] + "</div></td>");
                                    }
                                    else{
                                    var num = array [i][j];
                                    if (num != null){
                                            var rounded = Math.round(num*100)/100;
                                    }
                                    else{
                                            var rounded = num;
                                    }
                                    tr.append("<td class = 'appended' style = 'min-width:90px;'>" + rounded + "</div></td>");
                                    }
                                    count++;
                            }
                            //while loop to fill the rest of the table with blank spaces until end of array (compare count against max)
                            while (count < max){
                                    tr.append("<td class = 'appended' style = 'min-width:90px;'></div></td>");
                                    count++;
                            }
                            $('.search_result_tab2').append(tr);
            }
            }
    
            function drawFCTable(array, DPI_array) {
                    var tr;
                    //Get max length of DPI array and add 5 to fit table format
                    var max = DPI_array.length;
                    max = max + 5;
                    for (var i = 0; i < array.length; i++) {
                            tr = $('<tr/>');
                            //reset count to 0 to compare against dpi array index
                            var count = 0;
                            for (var j = 0; j < array[i].length; j++) {
                                    if (isNaN(array[i][j]) == true){
                                            tr.append("<td class = 'appended' style = 'min-width:90px;'><div style = 'overflow:auto;'>" + array[i][j] + "</div></td>");
                                    }
                                    else{
                                    var num = array [i][j];
                                    if (num != null){
                                            var rounded = Math.round(num*100)/100;
                                    }
                                    else{
                                            var rounded = num;
                                    }
                                    tr.append("<td class = 'appended' style = 'min-width:90px;'>" + rounded + "</div></td>");
                                    }
                                    count++;
                            }
                            //while loop to fill the rest of the table with blank spaces until end of array (compare count against max)
                            while (count < max){
                                    tr.append("<td class = 'appended' style = 'min-width:90px;'></div></td>");
                                    count++;
                            }
                            $('.search_result_tab3').append(tr);
            }
            }
    
            function emptyGenesAlert(array) {
                    alert("No results for the following gene-study-strain combinations: \n \n" + array.join("\n"));
            }
    
            ///PRINT ALL EMPTY RESULTS///////
            function printEmpty(array1, array2) {
                    var h2node = document.createElement("u");
                    var linebreak = document.createElement("br");
                    var h2text = document.createTextNode("Results could not be found for the following entries (in one or more datasets):");
                    h2node.appendChild(h2text);
    
                    var tabl = document.createElement("table");
                    tabl.setAttribute("id", "emptyrestbl");
    
                    document.getElementById("emptyresultstable").appendChild(linebreak);
                    document.getElementById("emptyresultstable").appendChild(h2node);
                    document.getElementById("emptyresultstable").appendChild(tabl);
                    printEmptyTable(array1);
    
                    //var theDiv = document.getElementById("#emptyresultstable");
                    //var content = document.createTextNode("<br><br><br><br><h2>Results could not be //found for the following entries:</h2><br><table id='emptyrestbl'></table>");
                    //theDiv.appendChild(str);
            }
    
            function printEmptyTable(array1){
                    var tr;
                    for (var i =0; i<array1.length; i++){
                            tr = $('<tr/>');
                            tr.append ("<td class = 'appended'>" + array1[i] + "</td>");
                            $('#emptyrestbl').append(tr);
                    }
            }
    //>
    // type = "text/javascript">
    //Checks css changes and automatically reloads page
    function reloadcss(){
            $("link").each(function() {
                    if ($(this).attr("type").indexOf("css") > -1) {
                            $(this).attr("href", $(this).attr("href") + "?id=" + new Date().getMilliseconds());
                    }
            });
    }
    //>
    // type = "text/javascript">
    ///Select all checkboxes///
    function checkAll(bx) {
            var cbs = document.getElementsByTagName('input');
            //console.log(cbs);-->
            var user_status = CheckUser();
            for(var i=0; i < cbs.length; i++) {
                    if(cbs[i].type == 'checkbox' && user_status =="") {
                            if (cbs[i].id !="makbox" && cbs[i].id !="nanostring"){
                                    cbs[i].checked = bx.checked;
                            }
                    }
                    else{
                            cbs[i].checked = bx.checked;
                    }
            }
    }
    
    ///Deselect all checkboxes on page reload///
    function uncheckAll() {
            var cbs = document.getElementsByTagName('input');
            //console.log(cbs);-->
            for(var i=0; i < cbs.length; i++) {
                    if(cbs[i].type == 'checkbox') {
                            cbs[i].checked = false;
                    }
            }
    }
    
    ///Select checkboxes in current div///
    function checkdiv(bx) {
            var cbs = $(bx).closest(".search_field_row").find("input:visible");  // Pretty slow, but simpler than javascript.
            for(var i=0; i < cbs.length; i++) {
                    cbs[i].checked = bx.checked;
            }
    }
    
    //>
    // type = "text/javascript">
    ///////COOKIE FUNCTIONS////////////////////-->
    //-->
    //-->
    ////Get Cookie-->
    //function getCookie(username) {-->
            //var name = username + "=";-->
            //var ca = document.cookie.split(';');-->
            ////console.log(ca);-->
            //for (var i = 0; i < ca.length; i++){-->
                    //var c = ca[i];-->
                    //while (c.charAt(0) == ' ') {-->
                            //c=c.substring(1);-->
                    //}-->
                    //if (c.indexOf(name) == 0) {-->
                            //return c.substring(name.length, c.length);-->
                    //}-->
            //}-->
            //return "";          -->
    //}-->
    
    ////Check cookie-->
    //function checkCookie() {-->
            //var username = getCookie("username");-->
            //if (username != ""){-->
                    //$(".topcorner").html("Welcome " + username);-->
                    //console.log(username);-->
            //}-->
    //return username;-->
    //}-->
    //>
    // type = "text/javascript">
    
    //Tabs function
    $(function() {
            $( "#tabs" ).tabs();
    });
    
    //Fill the parameters with a simple example search. Adds each of the following values to checkboxes or textboxes
    function fillExample(){
            resetsamplecart()
            addtosamplecart('EBOV_PBMC_Aerosol_RNASeq');
            checksamplecart();
            carttosamples();
            addtocart('isg15');
            addtocart('irf3');
            checkcart();
            carttosearch();
    }
    //>
    // type = "text/javascript">
            //script to open Counts tab
            function opentab5(){
                    var index = "1";
                    $('#tabs').tabs("option", "active", index);
            }
    //>
    // type = "text/javascript">
    //Second row of Tabs
    $(document).ready(function() {
            $('.Content_Area').children('div').addClass('tabPane');
            $('.Content_Area .tabPane:not(":first")').hide();     //Hide content of all tabs but first
            $('#sub_tabs li:first-child a').addClass('active'); //default active (highlighted) tab is first one
            $('#sub_tabs ul a').click(function(e) {
            e.preventDefault();
            $(this).parent('li').siblings().children('a').removeClass('active'); //Set all other tabs not active (highlighted) on click
            $(this).addClass('active'); //set current tab as active (highlighted) on click
            var target = $(this).attr('href');
            $(target).show().siblings().hide(); //Show current tab, hide others
            //console.log($(target).siblings());-->
            //if ($($target).has('div#tabs').length == true) {-->
                    //$($target).addClass('subTabs');-->
                    //$('.subTabs').find('.tabPane:first').show();-->
                    //$('.subTabs').children('#sub_tabs').find('li a').removeClass('active');-->
                    //$('.subTabs').children('#sub_tabs').find('li:first-child a').addClass('active');-->
            //}-->
            });
    });
    
    //Third row of Tabs
    $(document).ready(function() {
            $('.Content_Area_b').children('div').addClass('tabPane');
            $('.Content_Area_b .tabPane:not(":first")').hide();   //Hide content of all tabs but first
            $('#sub_tabs_b li:first-child a').addClass('active'); //default active (highlighted) tab is first one
            $('#sub_tabs_b ul a').click(function(e) {
            e.preventDefault();
            $(this).parent('li').siblings().children('a').removeClass('active'); //Set all other tabs not active (highlighted) on click
            $(this).addClass('active'); //set current tab as active (highlighted) on click
            var target = $(this).attr('href');
            $(target).show().siblings().hide(); //Show current tab, hide others
            //console.log($(target).siblings());-->
            //if ($($target).has('div#tabs').length == true) {-->
                    //$($target).addClass('subTabs');-->
                    //$('.subTabs').find('.tabPane:first').show();-->
                    //$('.subTabs').children('#sub_tabs').find('li a').removeClass('active');-->
                    //$('.subTabs').children('#sub_tabs').find('li:first-child a').addClass('active');-->
            //}-->
            });
    });
    
    //Fourth row of Tabs
    $(document).ready(function() {
            $('.Content_Area_c').children('div').addClass('tabPane');
            $('.Content_Area_c .tabPane:not(":first")').hide();   //Hide content of all tabs but first
            $('#sub_tabs_c li:first-child a').addClass('active'); //default active (highlighted) tab is first one
            $('#sub_tabs_c ul a').click(function(e) {
            e.preventDefault();
            $(this).parent('li').siblings().children('a').removeClass('active'); //Set all other tabs not active (highlighted) on click
            $(this).addClass('active'); //set current tab as active (highlighted) on click
            var target = $(this).attr('href');
            $(target).show().siblings().hide(); //Show current tab, hide others and Resizes the chart to fit div after it is un-hidden as hidden objects can't be resized?
            //console.log($(target).siblings());-->
            //if ($($target).has('div#tabs').length == true) {-->
                    //$($target).addClass('subTabs');-->
                    //$('.subTabs').find('.tabPane:first').show();-->
                    //$('.subTabs').children('#sub_tabs').find('li a').removeClass('active');-->
                    //$('.subTabs').children('#sub_tabs').find('li:first-child a').addClass('active');-->
            //}-->
            //console.log("Tab Clicked");-->
            load_highchart();
            });
    });
    
    //Fifth row of Tabs
    $(document).ready(function() {
            $('.Content_Area_d').children('div').addClass('tabPane');
            $('.Content_Area_d .tabPane:not(":first")').hide();   //Hide content of all tabs but first
            $('#sub_tabs_d li:first-child a').addClass('active'); //default active (highlighted) tab is first one
            $('#sub_tabs_d ul a').click(function(e) {
            e.preventDefault();
            $(this).parent('li').siblings().children('a').removeClass('active'); //Set all other tabs not active (highlighted) on click
            $(this).addClass('active'); //set current tab as active (highlighted) on click
            var target = $(this).attr('href');
            $(target).show().siblings().hide(); //Show current tab, hide others and Resizes the chart to fit div after it is un-hidden as hidden objects can't be resized?
            //console.log($(target).siblings());-->
            //if ($($target).has('div#tabs').length == true) {-->
                    //$($target).addClass('subTabs');-->
                    //$('.subTabs').find('.tabPane:first').show();-->
                    //$('.subTabs').children('#sub_tabs').find('li a').removeClass('active');-->
                    //$('.subTabs').children('#sub_tabs').find('li:first-child a').addClass('active');-->
            //}-->
            //console.log("Tab Clicked");-->
            load_highchart();
            });
    });
    //>
    // type = "text/javascript">
    function appendToStorage(name, data){
            var string1 = sessionStorage.getItem(name);
            var string2 = sessionStorage.getItem(data);
            var array1 = JSON.parse(string1);
            var array2 = JSON.parse(string2);
    
            //check if both arrays are filled in (all possible combinations)
            if (array2.length > 0 && array1.length > 0){
                    var combined = array1.concat(array2);
            }
            else if (array2 === null && array1.length > 0){
                    var combined = array1
            }
            else if (array1 === null && array2.length > 0){
                    var combined = array2
            }
            //console.log(combined);
            sessionStorage.setItem(name,JSON.stringify(combined));
    }
    
    ///New search function///
    function reloadPg() {
            location.reload();
    }
    //>
    // type = "text/javascript">
    $(function() {
            $('#gen_counts').click(function() {
                    header = ['Gene', 'Virus', 'Data_Type', 'Strain', 'Study_Name'];
                    tableheader = header.concat(DPI_array);
                    tablehead = [tableheader];
                    for (var i = 0; i < Count_array.length; i++) {
                            for (var j = 0; j < Count_array[i].length; j++){
                            //console.log(Count_array[i][j]);
                            if (typeof Count_array[i][j] == "string") {
                                    Count_array[i][j] = Count_array[i][j].replace(/(\r\n|\n|\r)/gm,"");
                            }
                            }
                    }
                    data = tablehead.concat(Count_array);
                    //console.log(Count_array)
                    console.log('data loaded');
                    //console.log(data);
                    var csvContent = "data:text/csv;charset=utf-8,";
                    data.forEach(function(infoArray, index){
    
                            dataString = infoArray.join(",");
                            csvContent += index < data.length ? dataString+ "\n" : dataString;
    
                    });
                    //console.log(data)
                    var encodedUri = encodeURI(csvContent);
                    var link = document.createElement("a");
                    link.setAttribute("href", encodedUri);
                    link.setAttribute("download", "count_results.csv");
    
                    link.click();
            });
    });
    //////////////////DOWNLOAD FUNCTIONS////////////////////
    $(function() {
            $('#gen_FC').click(function() {
                    //CSV Header
                    header = ['Gene', 'Virus', 'Data_Type', 'Strain', 'Study_Name'];
                    //Add DPI list to header
                    tableheader = header.concat(DPI_array);
                    tablehead = [tableheader];
                    for (var i = 0; i < FC_array.length; i++) {
                            for (var j = 0; j < FC_array[i].length; j++){
                            //console.log(Count_array[i][j]);
                            if (typeof FC_array[i][j] == "string") {
                                    FC_array[i][j] = FC_array[i][j].replace(/(\r\n|\n|\r)/gm,"");
                            }
                            }
                    }
                    data = tablehead.concat(FC_array);
                    console.log('data loaded');
                    //console.log(ftable);
                    var csvContent = "data:text/csv;charset=utf-8,";
                    data.forEach(function(infoArray, index){
    
                            dataString = infoArray.join(",");
                            csvContent += index < data.length ? dataString+ "\n" : dataString;
    
                    });
                    var encodedUri = encodeURI(csvContent);
                    var link = document.createElement("a");
                    link.setAttribute("href", encodedUri);
                    link.setAttribute("download", "FC_results.csv");
    
                    link.click();
            });
    });
    
    //>
    
    // type = "text/javascript">
    //Combined General Gene Search
    $(document).ready(function(){
            $( ".combined_search" ).on( "click", function (event) {
                    var terms = document.getElementsByClassName('browse_searchbar');
                    for (var i = 0; i < terms.length; i++) {
                            //check for special characters
                            if (terms.item(i).value.match(/[`~!@#\$%\^&\*\;\(\)\=_+\\\[\]{\}\?,\.\<\>]/)) {
                                    alert('Cannot use special characters.');
                                    return false;
                            }
                            //alert and exit function if empty
                            if (!terms.item(i).value || terms.item(i).value.match(/^\s*$/)) {
                                    alert("Please fill in all search terms or remove empty terms");
                                    return false;
                            }
                            //set input names so serialize works
                            var name = document.getElementsByClassName('browse_select').item(i);
                            name = name.options[name.selectedIndex].value;
                            var operator = document.getElementsByClassName('browse_operators').item(i);
                            if (i != 0 ){
                            operator = operator.options[operator.selectedIndex].value+" ";
                            }
                            else{
                                    operator = "START ";
                            }
                            terms.item(i).name = operator + name;
                    }
                    //Remove previously appended
                    $('.appended').remove();
    
    
                    //Don't refresh page after submitting
                    event.preventDefault();
                    //Convert the form data into one string of key/value pairs for our python script to read
                    //Eg, "search_text='ABL1'&num_paths=4"
                    //console.log($("form#GenSearch .browse_searchbar"));-->
                    data = $("form#GenSearch .browse_searchbar").serialize();
                    //When the user submits the form, this function will be called
                    console.log(data);
                    CombinedGeneSearch(data);
            });
    });
    
    
    function CombinedGeneSearch(data) {
            //jquery to make ajax request to server
            $('#loading_image').show(); // show loading image, as request is about to start
            var start_time = new Date().getTime(); // Get time of request
            var request = $.ajax(
            {
                    type: "POST",
                    url: "/cgi-bin/VHFGenesSearch.py", //CGI script for general browse
                    //url: "/~dezhang/cgi-bin/VHFGenesSearch.py", //REMOVE FOR MOVE TO MASTER
                    data: data,
                    dataType: "json",
                    success: function(response) //run function once we get response
                    {
                            //console.log(response);-->
                            drawGenetable(response);
                            var request_time = new Date().getTime() - start_time;  // Calculate time response took in milliseconds
                            $(".gene_table_header").children().remove();  // Remove any previous row counts
                            // Prepend number of genes, append time search took
                            $(".gene_table_header").prepend("<b style='display:inline-block !important'>" + response.length + " </b> ");
                            $(".gene_table_header").append(" in <b style='display:inline-block !important'>" + request_time/1000 + "</b> seconds");
                            //console.log($(".gene_table_header").children());-->
                            $('#loading_image').hide(); //Hides loading image
            //console.log(request_time/1000);-->
                    },
                    error: function(data, status)
                    {
                            $('#loading_image').hide(); //Hides loading image
                            console.log(status);
                            console.log(data);
                            $("#error").html(data['responseText']);
                            //response(data);-->
                            console.log("Something went wrong");
                    },
            });
            request.fail(function( jqHXR, textStatus ) {
                    $("#error").html(jqHXR.responseText);
            });
    }
    //>
    // type = "text/javascript">
    //Combined Sample Search
    $(document).ready(function(){
            $( ".sample_search" ).on( "click", function (event) {
                    //set input names so serialize works
                    var name = document.getElementsByClassName('browse_select').item(0);
                    //console.log(name);-->
                    var name = document.getElementsByClassName('browse_select').item(1);
                    //console.log(name);-->
                    name = name.options[name.selectedIndex].value;
                    //Remove previously appended
                    $('.appended').remove();
    
    
                    //Don't refresh page after submitting
                    event.preventDefault();
                    //Convert the form data into one string of key/value pairs for our python script to read
                    //Eg, "search_text='ABL1'&num_paths=4"
                    //console.log($("form#SampSearch .browse_searchbar"));-->
                    data = $("form#SampSearch .browse_select").serialize();
                    //When the user submits the form, this function will be called
                    console.log(data);
                    SampleSearch(data);
    
            });
    });
    function SampleSearch(data) {
            //jquery to make ajax request to server
            $('#loading_image').show(); // show loading image, as request is about to start
            var start_time = new Date().getTime(); // Get time of request
            var request = $.ajax(
            {
                    type: "POST",
                    url: "/cgi-bin/VHFSampleSearch.py", //CGI script for general browse
                    //url: "/~dezhang/cgi-bin/VHFSampleSearch.py", //REMOVE FOR MOVE TO MASTER
                    data: data,
                    dataType: "json",
                    success: function(response) //run function once we get response
                    {
                            console.log(response);
                            drawSampletable(response);
                            var request_time = new Date().getTime() - start_time;  // Calculate time response took in milliseconds
                            $(".sample_table_header").children().remove();  // Remove any previous row counts
                            // Prepend number of genes, append time search took
                            $(".sample_table_header").prepend("<b style='display:inline-block !important'>" + response.length + " </b> ");
                            $(".sample_table_header").append(" in <b style='display:inline-block !important'>" + request_time/1000 + "</b> seconds");
                            //console.log($(".sample_table_header").children());-->
                            $('#loading_image').hide(); //Hides loading image
            //console.log(request_time/1000);-->
                    },
                    error: function(data, status)
                    {
                            $('#loading_image').hide(); //Hides loading image
                            console.log(status);
                            console.log(data);
                            $("#error").html(data['responseText']);
                            //response(data);-->
                            console.log("Something went wrong");
                    },
            });
            request.fail(function( jqHXR, textStatus ) {
                    $("#error").html(jqHXR.responseText);
            });
    }
    //>
    // type = "text/javascript">
    //Function to add new search area to browse
    function addsearch(){
            var div, sel, sel2, opt1, opt2, opt3, opt4, and, or, not, tn1, tn2, tn3, tn4, tn5, tn6, GO, inp1, inp2;
            // Create Select Menu
            div = document.createElement('div');
            sel = document.createElement('select');
            opt1 = document.createElement('option');
            opt2 = document.createElement('option');
            opt3 = document.createElement('option');
            opt4 = document.createElement('option');
            tn1 = document.createTextNode("Macaque Gene Symbol");
            tn2 = document.createTextNode("Human Gene Symbol");
            tn3 = document.createTextNode("Gene Description");
            GO = document.createTextNode("Gene Ontology Term");
            opt1.appendChild(tn1);
            opt1.appendChild(tn1);
            opt2.appendChild(tn2);
            opt3.appendChild(tn3);
            opt4.appendChild(GO);
            sel.appendChild(opt1);
            sel.appendChild(opt2);
            sel.appendChild(opt3);
            sel.appendChild(opt4);
            sel.setAttribute("class", "browse_select");
            // Create Text input
            inp1 = document.createElement('input');
            inp2 = document.createElement('input');
            inp1.setAttribute("type", "text");
            inp1.setAttribute("class", "browse_searchbar");
            inp2.setAttribute("type", "button");
            inp2.setAttribute("value", "Remove Search Term");
            inp2.setAttribute("onclick", "remove_search_term(this)");
            opt1.setAttribute("value", "MMUgenePart");
            opt2.setAttribute("value", "HumangenePart");
            opt3.setAttribute("value", "DescgenePart");
            opt4.setAttribute("value", "GOPart");
            // Create Operator Menu
            sel1 = document.createElement('select');
            and = document.createElement('option');
            or = document.createElement('option');
            not = document.createElement('option');
            tn4 = document.createTextNode("AND");
            tn5 = document.createTextNode("OR");
            tn6 = document.createTextNode("NOT");
            and.appendChild(tn4);
            or.appendChild(tn5);
            not.appendChild(tn6);
            sel1.appendChild(and);
            sel1.appendChild(or);
            sel1.appendChild(not);
            sel1.setAttribute("class", "browse_operators");
            // Add to div
            div.appendChild(sel1);
            div.appendChild(sel);
            div.appendChild(inp1);
            div.appendChild(inp2);
            div.setAttribute("class", "more_browse_search");
            $("#GenSearch").append(div);
    }
    //>
    // type = "text/javascript">
    // This draws the table for the general gene search
    function drawGenetable(array) {
    var arr = array;
    if (arr.length == 0){ // Check if result exists
            //console.log($(".browse_table").children());-->
            tab = document.getElementById("search_result_table");
            tr = document.createElement('tr');
            tn = document.createTextNode("No Matching Genes");
            //mt = document.createElement('td');-->
            //mt1 = document.createElement('td');-->
            //mt2 = document.createElement('td');-->
            //mt3 = document.createElement('td');-->
            td = document.createElement('td');
            td.appendChild(tn);
            td.setAttribute("colspan", $(".browse_table").children().length);
            td.setAttribute("class", "No_genes");
            tr.appendChild(td);
            //tr.appendChild(mt);-->
            //tr.appendChild(mt1);-->
            //tr.appendChild(mt2);-->
            //tr.appendChild(mt3);-->
            //tab.appendChild(tr);-->
            tab.insertBefore(tr, tab.firstChild);
            //console.log("test");-->
            //$("#search_result_table").html("No Matching Genes");-->
    }
    var tab, tr, td, tn, row, col, add, a;
    tab = document.getElementById("search_result_table");
    for (row=0; row < arr.length; row++){
            tr = document.createElement('tr');
            tr.setAttribute("class", "browse_row");
            for (col=0; col < arr[row].length; col++){
                    td = document.createElement('td');
                    tn = document.createTextNode(arr[row][col]);
                    a = document.createElement('a');
                    a.appendChild(tn);
                    if (col == 0){//Macaque Ensembl ID
                    //console.log("This is the MMU", arr[row][col]);
                    a.href = "http://useast.ensembl.org/Macaca_mulatta/Gene/Summary?db=core;g="+arr[row][col];
                    a.target = "_blank"; //Open link in new tab
                    }
                    if (col == 1){//Human Ensembl ID
                    //console.log("This is the MMU", arr[row][col]);
                    a.href = "http://useast.ensembl.org/Homo_sapiens/Gene/Summary?db=core;g="+arr[row][col];
                    a.target = "_blank"; //Open link in new tab
                    }
                    if (col ==2) { //Macaque Wikigene ID
                    var gene= arr[row][col];
                    var patt = new RegExp("LOC");
                    var res = patt.test(gene);
                    //console.log(res);-->
                            if (res == true) { /*Filters out LOC string for Macaque, since links to MMU LOC genes only
                            require numbers on NCBI and don't appear in Gene card*/
                                    gene = gene.replace(/[^0-9\.]+/g, "");
                                    //console.log(gene);-->
                                    a.href = "http://www.ncbi.nlm.nih.gov/gene/"+gene;
                                    a.target = "_blank";
                                    }
                            else {
                                    a.href = "http://www.genecards.org/cgi-bin/carddisp.pl?gene="+arr[row][col];
                                    a.target = "_blank";
                                    }
                            }
                    if (col ==3){ //Human Wikigene ID
                    a.href = "http://www.genecards.org/cgi-bin/carddisp.pl?gene="+arr[row][col];
                    a.target = "_blank";
                    }
                    if (col ==4){
                    a.title = arr[row][col];
                    }
                    td.appendChild(a);
                    tr.appendChild(td);
            }
            td = document.createElement('td');
            tn = document.createTextNode("Add");
            add = document.createElement('button');
            add.onclick = function(){
                    var MMUgene = $(this).closest('tr').children('td:eq(2)').text(); /*Sets variable gene as the text from the
                    second third column of that row*/
                    var HUMgene = $(this).closest('tr').children('td:eq(3)').text();
                    //console.log(gene);
                    if (MMUgene != "") { //Checks if Macaque gene symbol is not blank
                            //console.log("MMU Gene");
                            addtocart(MMUgene);
                    }
                    else { //If Macaque gene symbol is blank, uses human gene symbol instead
                            //console.log("Human Gene");
                            addtocart(HUMgene);
                    }
                    $(this).closest('button').attr("disabled", true);
                    //alert(gene);-->
                    //console.log(gene);-->
                    checkcart();
                    };
            add.appendChild(tn);
            td.appendChild(add)
            tr.appendChild(td);
            //tab.appendChild(tr);-->
            tab.insertBefore(tr, tab.firstChild); // Prepends rows
    }
    demarc = document.createElement('td');  // Add line at end of table to differentiate between previous searches
    demarctr = document.createElement('tr');
    demarc.setAttribute("colspan", $(".browse_table").children().length);  // Set row length as number of cols
    demarc.setAttribute("class", "demarcation"); // Set class for css coloring
    demarctr.appendChild(demarc);
            //tab.appendChild(demarctr);-->  // Prepends rows
            tab.insertBefore(demarctr, tab.firstChild);
            $("td button").addClass("add_button"); // Add classes for css shenanigans
            }
    
    function drawSampletable(array) {
            var arr = array;
            if (arr.length == 0){ // Check if result exists
                    //console.log($(".browse_table").children());-->
                    tab = document.getElementById("search_result_table_samp");
                    tr = document.createElement('tr');
                    tn = document.createTextNode("No Matching Datasets");
                    td = document.createElement('td');
                    td.appendChild(tn);
                    td.setAttribute("colspan", $(".browse_table").children().length);
                    td.setAttribute("class", "No_genes");
                    tr.appendChild(td);
    
                    tab.insertBefore(tr, tab.firstChild);
            }
            var tab, tr, td, tn, row, col, add, a;
            tab = document.getElementById("search_result_table_samp");
            for (row=0; row < arr.length; row++){
                    tr = document.createElement('tr');
                    tr.setAttribute("class", "browse_row");
                    for (col=0; col < arr[row].length; col++){
                            td = document.createElement('td');
                            tn = document.createTextNode(arr[row][col]);
                            a = document.createElement('a');
                            if (col == 0){
                                    a.style="display:none"
                                    td.style="display:none"
                            }
                            a.appendChild(tn);
                            td.appendChild(a);
                            tr.appendChild(td);
                            if (col == 7){
                                    a.href = "https://www.ncbi.nlm.nih.gov/pubmed/"+arr[row][col];
                                    a.target = "_blank"; //Open link in new tab
                            }
                    }
                    td = document.createElement('td');
                    tn = document.createTextNode("Add");
                    add = document.createElement('button');
                    add.onclick = function(){
                            var sampleName = $(this).closest('tr').children('td:eq(0)').text(); /*Sets variable gene as the text from the*/
                            addtosamplecart(sampleName);
                            $(this).closest('button').attr("disabled", true);
                            //alert(sampleName);-->
                            //console.log(sampleName);-->
                            checksamplecart();
                            carttosamples();
                            };
                    add.appendChild(tn);
                    td.appendChild(add)
                    tr.appendChild(td);
                    //tab.appendChild(tr);-->
                    tab.insertBefore(tr, tab.firstChild); // Prepends rows
            }
    demarc = document.createElement('td');  // Add line at end of table to differentiate between previous searches
    demarctr = document.createElement('tr');
    demarc.setAttribute("colspan", $(".browse_table").children().length);  // Set row length as number of cols
    demarc.setAttribute("class", "demarcation"); // Set class for css coloring
    demarctr.appendChild(demarc);
            //tab.appendChild(demarctr);-->  // Prepends rows
            tab.insertBefore(demarctr, tab.firstChild);
            $("td button").addClass("add_button"); // Add classes for css shenanigans
            }
    
            //Function to store genes of interest
            function addtocart(gene){
                    var existing_gene = getCookie("genes");
                    var patt1 = new RegExp("^" + gene + "$"); //set regex term as current gene added
                    var patt2 = new RegExp("^" + gene + " ");
                    var patt3 = new RegExp(" " + gene + " ");
                    var patt4 = new RegExp(" " + gene + "$");
                    //console.log(gene);-->
                    //console.log(existing_gene);-->
                    if (patt1.test(existing_gene) == true ||
                            patt2.test(existing_gene) == true ||
                            patt3.test(existing_gene) == true ||
                            patt4.test(existing_gene) == true   ) { //checks if gene is already in cart
                            //console.log("Already in Cart");-->
                    }
                    else {
                            //console.log("Not in Cart");-->
                            document.cookie ="genes=" + existing_gene +" "+ gene; // add next genes to cookie
                    }
            }
    
            //Function to store genes of interest
            function addtosamplecart(sample){
                    var existing_samples = getCookie("samples");
                    var patt1 = new RegExp("^" + sample + "$"); //set regex term as current gene added
                    var patt2 = new RegExp("^" + sample + " ");
                    var patt3 = new RegExp(" " + sample + " ");
                    var patt4 = new RegExp(" " + sample + "$");
                    //console.log(sample);-->
                    //console.log(existing_samples);-->
                    if (patt1.test(existing_samples) == true ||
                            patt2.test(existing_samples) == true ||
                            patt3.test(existing_samples) == true ||
                            patt4.test(existing_samples) == true   ) { //checks if gene is already in cart
                            //console.log("Already in sample Cart");-->
                    }
                    else {
                            //console.log("Not in sample Cart");-->
                            document.cookie ="samples=" + existing_samples +" "+ sample; // add next genes to cookie
                    }
            }
    
            //Checks selected genes from general search
            function checkcart() {
                    var genes=getCookie("genes");
                    var rem, br, div, txt, a, x, d;
                    if (genes!="") { //if genes exist in cookie, removes whitespace and adds newline and button to each gene
                            div = document.createElement('div');
                            //console.log(genes);-->
                            for (i=0; i < genes.split(" ").length; i++){
                                    txt = document.createTextNode(genes.split(" ")[i]);
                                    x = document.createTextNode('\u2716');
                                    a = document.createElement('a');
                                    a.appendChild(txt);
                                    br = document.createElement('br');
                                    rem = document.createElement('button');
                                    rem.onclick = function(){
                                            var gene = $(this).closest('a').text();
                                            //console.log(gene);-->
                                            specificdelete(gene);
                                            checkcart();
                                            };
                                    rem.appendChild(x);
                                    a.appendChild(rem);
                                    a.appendChild(br);
                                    div.appendChild(a);
                            }
                            genes2 = div;
                            $(".cart").html(genes2);
                            $("a button").addClass("xbutton");
                    }
                    else{
                            //console.log("The Cart is empty");-->
                            $(".cart").html("No Genes in Cart");
                    }
            return genes;
            }
            //Checks selected genes from general search
            function checksamplecart() {
                    var samples=getCookie("samples");
                    var rem, br, div, txt, a, x, d;
                    if (samples!="") { //if genes exist in cookie, removes whitespace and adds newline and button to each gene
                            div = document.createElement('div');
                            //console.log(samples);-->
                            for (i=0; i < samples.split(" ").length; i++){
                                    txt = document.createTextNode(samples.split(" ")[i]);
                                    x = document.createTextNode('\u2716');
                                    a = document.createElement('a');
                                    a.appendChild(txt);
                                    br = document.createElement('br');
                                    rem = document.createElement('button');
                                    rem.onclick = function(){
                                            var sample = $(this).closest('a').text();
                                            //console.log(sample);-->
                                            specificsampledelete(sample);
                                            checkcart();
                                            };
                                    rem.appendChild(x);
                                    a.appendChild(rem);
                                    a.appendChild(br);
                                    div.appendChild(a);
                            }
                            sample2 = div;
                            $(".samplecart").html(sample2);
                            $("a button").addClass("xbutton");
                    }
                    else{
                            //console.log("The Cart is empty");-->
                            $(".samplecart").html("No Datasets in Cart");
                    }
            return samples;
            }
    
            //Delete Specific Genes from Cart
            function specificdelete(gene){
                    var current = getCookie("genes");
                    del = gene.replace("\u2716",""); //input carries over "X" for some reason. This removes it.
                    //console.log(del);-->
                    var patt1 = new RegExp(" " + del + " "); //set regex term as current gene added
                    var patt2 = new RegExp("^" + del + "$");
                    var patt3 = new RegExp("^" + del + " ");
                    var patt4 = new RegExp(" " + del + "$");
                    //console.log(current);-->
                    if (patt1.test(current) == true) { //checks if gene is already in cart
                    //console.log("patt1");-->
                    current = current.replace(patt1," "); //deletes specific gene from cookie
                    }
                    if (patt2.test(current) == true) {
                    //console.log("patt2");-->
                    current = current.replace(patt2,"");
                    }
                    if (patt3.test(current) == true) {
                    //console.log("patt3");-->
                    current = current.replace(patt3,"");
                    }
                    if (patt4.test(current) == true) {
                    //console.log("patt4");-->
                    current = current.replace(patt4,"");
                    }
                    document.cookie ="genes=" + current;
                    //$("button").attr("disabled", false); //re-enable all disabled add to search buttons-->
                    //console.log($(".browse_row td a:contains('"+del+"')").closest("tr").find("button"));-->
                    $(".browse_row td a:contains('"+del+"')").closest("tr").find("button").attr("disabled", false); // Gene specific add button re-enable
            }
    
            //Delete Specific Genes from Cart
            function specificsampledelete(sample){
                    var current = getCookie("samples");
                    del = sample.replace("\u2716",""); //input carries over "X" for some reason. This removes it.
                    //console.log(del);-->
                    var patt1 = new RegExp(" " + del + " "); //set regex term as current gene added
                    var patt2 = new RegExp("^" + del + "$");
                    var patt3 = new RegExp("^" + del + " ");
                    var patt4 = new RegExp(" " + del + "$");
                    //console.log(current);-->
                    if (patt1.test(current) == true) { //checks if gene is already in cart
                    //console.log("patt1");-->
                    current = current.replace(patt1," "); //deletes specific gene from cookie
                    }
                    if (patt2.test(current) == true) {
                    //console.log("patt2");-->
                    current = current.replace(patt2,"");
                    }
                    if (patt3.test(current) == true) {
                    //console.log("patt3");-->
                    current = current.replace(patt3,"");
                    }
                    if (patt4.test(current) == true) {
                    //console.log("patt4");-->
                    current = current.replace(patt4,"");
                    }
                    document.cookie ="samples=" + current;
                    //$("button").attr("disabled", false); //re-enable all disabled add to search buttons-->
                    //console.log($(".browse_row td a:contains('"+del+"')").closest("tr").find("button"));-->
                    $(".browse_row td a:contains('"+del+"')").closest("tr").find("button").attr("disabled", false); // Gene specific add button re-enable
                    checksamplecart();
                    carttosamples();
            }
    
            //Reset cart
            function resetcart(){
            document.cookie ="genes="; // Set genes to null
                    $(".cart").html("No Genes");
                    $("button").attr("disabled", false); //re-enable all disabled add to search buttons
                    //var genes=getCookie("genes");-->
                    //console.log(genes);-->
            }
    
            function resetsamplecart(){
            document.cookie ="samples="; // Set genes to null
                    $(".samplecart").html("No Datasets");
                    $("button").attr("disabled", false); //re-enable all disabled add to search buttons
                    //var samples=getCookie("samples");-->
                    //console.log(samples);-->
            }
    
            //Add Current cart to Gene Symbol search box
            function carttosearch(){
                    var genes=getCookie("genes");
                    genes2 = genes.split(" ").join("\r\n"); //removes whitespace and adds newline to format for search
                    //console.log(genes2, "Success");-->
                    document.getElementById('gene_inner').value = genes2;
            }
    //BLAHBLAH
            function carttosamples(){
                    var samples=getCookie("samples");
                    samples2 = samples.split(" ").join("\r\n"); //removes whitespace and adds newline to format for search
                    //console.log(samples2, "Success");-->
                    document.getElementById('sample_inner').value = samples2;
            }
    
            // Delete all rows in general search
            function deleteresults(){
                    var nrow = document.getElementById("search_result_table").rows.length; // Javascript Way
                    //var nrow = $("#search_result_table tr").length;-->
                    for (x=1; x <= nrow-1; x++){
                            //console.log(x,nrow);-->
                            document.getElementById("search_result_table").deleteRow(nrow-x);
                    }
                    //$(".browse_row").remove(); // Jquery way-->
                    //$(".demarcation").remove();-->
                    $(".gene_table_header").html("Matching genes in the database");
            }
    
            // Delete all rows in sample search
            function deletesampleresults(){
                    var nrow = document.getElementById("search_result_table_samp").rows.length; // Javascript Way
                    //var nrow = $("#search_result_table_samp tr").length;-->
                    for (x=1; x <= nrow-1; x++){
                            //console.log(x,nrow);-->
                            document.getElementById("search_result_table_samp").deleteRow(nrow-x);
                    }
                    //$(".browse_row").remove(); // Jquery way-->
                    //$(".demarcation").remove();-->
                    $(".sample_table_header").html("Matching datasets in the database");
            }
    
            //Hide-unhide search sidebar
            $(document).ready(function(){
                    $("#gene_search").click(function(){
                            if ($("#sidebar_modifiers").css('display') == 'none'){
                            $("#sidebar_modifiers").toggle();
                            }
                    });
            });
    
            //Toggle count charts visible based on value of corresponding checkbox
            function RNA_check_Changed()
            {
                    $("#chartA").show();
            }
    
            function Microarr_check_Changed()
            {
                    $("#micro_chartA").show();
            }
    
            function Nanostring_check_Changed()
            {
                    $("#nano_chartA").show();
            }
            //>
            // type = "text/javascript">
            ///UPLOAD TEXT FILE INTO TEXT AREA///
            window.onload = function() {
            ///get the uploaded file from genetxt or ensembltxt///
    var fileInput = document.getElementById('genetxt');
    //              var fileInput2 = document.getElementById('ensembltxt');
    var fileDisplayArea = document.getElementById('gene_inner');
    //              var fileDisplayArea2 = document.getElementById('ensembl_inner');
    var fileDisplayArea3 = document.getElementById('sample_inner');
            ///genetxt///
    fileInput.addEventListener('change', function(e) {
            var file = fileInput.files[0];
            var textType = /text.*/;
    
                    if (fileInput.files[0].name.match(/\.(FASTA|fasta|FAST|fast)$/)){
                            alert('Fasta files not accepted yet.');
                    }
                    else{
                            if (file.type.match(textType)) {
                                    var reader = new FileReader();
    
                                    reader.onload = function(e) {
                                            fileDisplayArea.innerText = reader.result;
                                    }
    
                                    reader.readAsText(file);
                            } else {
                                    alert("File type not supported!");
                                    }
                            }
            });
    
            ///ensembltxt///
            fileInput2.addEventListener('change', function(e) {
            var file = fileInput2.files[0];
            var textType = /text.*/;
    
            if (file.type.match(textType)) {
            var reader = new FileReader();
    
            reader.onload = function(e) {
                    fileDisplayArea2.innerText = reader.result;
            }
    
            reader.readAsText(file);
            } else {
            alert("File type not supported!");
            }
            });
            }
            //>
            // type = "text/javascript">
            //Checks User Cookie
            function CheckLogin() {
                    var username=getCookie("username");
                    if (username!="") {
                            //console.log(username);-->
                            $("#makona_div").show();
                    }
                    else {
                            //console.log("No Login");-->
                    }
            //return username;-->
            }
            //>
            // type = "text/javascript">
            //Opens graph in new window
            function graph_window(type){
                    var type = type; //Specifies which chart should be created
                    sessionStorage.setItem("type", type); //Stores data type in sessionStorage
                    var myWindow =  window.open('graph.html','');
                    }
    
            //Function for top and bottom scroll bars
            function activate_scrollbars(){
                    //$(document).ready(function(){
                            //$('.double-scroll').doubleScroll();
                    //});
            }
    
            //Div toggles for example search
            function example_toggles(){
                    //console.log("function started;");-->
                            $('#chartA').show();
                            $('#searchGene').submit();
                            $(".Datatype").show();
                            //console.log($(".search_field_title.Datatype"));-->
                            $('#search_field_ebov').show();
                            $('#RNAbox').show();
                            $("#datatype_label").show();
                            $("#strain_label").show();
                            //console.log("function called");-->
            }
            //>
            // type = "text/javascript">
            function ClearStorage(){
                    sessionStorage.clear(); //Clears any previous data
                    }
            //>
            // type = "text/javascript">
            //Toggles Highcharts Legend
            function toggle_legend(chart){
                    if (chart == "A"){
                            var chart = $("#chartA").highcharts(); // Grabs highcharts plugin
                            //console.log(chartA);-->
                            //console.log($("#chartA.legend"));-->
                            chart.legend.toggle();
                            }
                    if (chart == "B"){
                            var chart = $("#chartB").highcharts();
                            //console.log(chartB);-->
                            //console.log($("#chartA.legend"));-->
                            chart.legend.toggle();
                            }
                    if (chart == "microA"){
                            var chart = $("#micro_chartA").highcharts();
                            //console.log(chartB);-->
                            //console.log($("#chartA.legend"));-->
                            chart.legend.toggle();
                            }
                    else{
                            console.log("argument passed to toggle_legend() is not A, B or microA");
                    }
            }
            //>
            // type= "text/javascript">
            //Moves add to search button to current lowest row
            function move_search_button(input){
                    // Create add search term button
                    var button = document.createElement("input");
                    button.setAttribute("value", "Add Search Term");
                    button.setAttribute("onclick", "addsearch(), move_search_button(this)");
                    button.setAttribute("type", "button");
                    // Remove old search button
                    var search_button = input
                    $(search_button).remove();
                    //console.log($(search_button));-->
                    // Add to newest row
                    //console.log($(".more_browse_search").last());-->
                    $(".more_browse_search").last().append(button);
    
            }
            //>
            // type = "text/javascript">
            // Removes search term
            function remove_search_term(input){
                    //console.log($(".more_browse_search").length);-->
                    // Create add search term button
                    var button = document.createElement("input");
                    button.setAttribute("value", "Add Search Term");
                    button.setAttribute("onclick", "addsearch(), move_search_button(this)");
                    button.setAttribute("type", "button");
                    // If the row contains the add search term button, add button to previous div
                    //console.log($(input).next());-->
                    if ($(input).next().val() == "Add Search Term"){
                            //console.log("Correct");-->
                            $(input).parent().prev().append(button);
                    }
                    // Remove row
                    $(input).parent().remove()
            }
            //>
            // Draws 1st heatmap
            function draw_Study_Heatmap (DPI_y_cats, DPI_hm, DPI_x_cat, legend, title, element) {
                    console.log(DPI_y_cats, DPI_hm, DPI_x_cat, legend, title, element);
                    $(function () {
                            $(element).highcharts({
                                    chart: {
                                            //reflow: false,-->
                                            type: 'heatmap',
                                            marginTop: 40,
                                            marginBottom: 120,
                                            //marginLeft:0,-->
                                            //marginRight:0,-->
    
                                            // Edit chart spacing
                                            spacingBottom: 0,
                                            spacingTop: 0,
                                            spacingLeft: 0,
                                            spacingRight: 0,
    
                                            // Explicitly tell the width and height of a chart
                                            //width: null,
                                            //height: null,
    
                                            plotBorderColor: '#000000',
                                            plotBorderWidth: 1,
                                            borderWidth:0
                                    },
    
                                    credits: {
                                            //enabled: false-->
                                    },
    
                                    title: {
                                            text: title,
                                            style: {
                                            //color: '#FF00FF',-->
                                            fontWeight: 'bold',
                                            fontSize: '1.3em'
                                            }
                                    },
    
                                    xAxis: [{
                                            categories: DPI_x_cat,
                                            visible: true,
                                            labels:{
                                                    rotation: -45,
                                                    style: {
                                                            //color: '#FF00FF',-->
                                                            //fontWeight: 'bold',-->
                                                            fontSize: '0.8em'
                                                    }
                                            }
                                    }],
    
                                    yAxis: {
                                            categories: DPI_y_cats,
                                            title: "Gene",
                                            reversed: true,
                                            //visible: false-->
                                            labels:{
                                                    style: {
                                                            //color: '#FF00FF',-->
                                                            //fontWeight: 'bold',-->
                                                            fontSize: '1em'
                                                    }
                                            }
                                    },
    
                                    // colorAxis: {
                                    //         stops: [
                                    //                 [0, '#3060cf'],
                                    //                 [0.5, '#ffffff'],
                                    //                 [0.9, '#c4463a']
                                    //         ],
                                    //         min: -legend,
                                    //         max: legend,
                                    //         //minorTickInterval: 1,-->
                                    //         endOnTick: 0,
                                    //         startOnTick: 0,
                                    //         reversed: false
                                    // },
    
                                    colorAxis: {
                                            stops: [
                                                    [-10, '#3060cf'],
                                                    [0, '#ffffff'],
                                                    [10, '#c4463a']
                                            ],
                                            min: -legend,
                                            max: legend,
                                            endOnTick: 0,
                                            startOnTick: 0,
                                            reversed: true
                                    },
    
                                    // colorAxis: {
                                    //         min: 0,
                                    //         minColor: '#FFFFFF',
                                    //         maxColor: Highcharts.getOptions().colors[0]
                                    //       },
    
                                    legend: {
                                            //enabled: false,-->
                                            align: 'right',
                                            layout: 'vertical',
                                            margin: 0,
                                            verticalAlign: 'top',
                                            y: 25,
                                            symbolHeight: 320
                                    },
    
                                    //tooltip: {
                                            //formatter: function () {
                                                    //return this.series.xAxis.categories[this.point.x] +"<br>" +
                                                    //this.series.yAxis.categories[this.point.y] + "<br>" + this.point.value;
                                            //}
                                    //},
    
                                    series: [{
                                            //name: 'Sales per employee',-->
                                            borderWidth: 1,
                                            data: DPI_hm,
                                            dataLabels: {
                                                    enabled: true,
                                                    color: 'black',
                                                    style: {
                                                            textShadow: 'none'
                                                    }
                                            }
                                    }]
    
                            });
                    });
            }