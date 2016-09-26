/*
Javascript for job dashboard app
*/

function search() {

    var jobtitle = $('#jobtitleInput').val();
    var company = $('#companyInput').val();
    var location = $('#locationInput').val();
 
 	var inputData = {'jobtitle': jobtitle, 'company': company, 'location': location};

 	console.log("inputData: " + inputData);


    $.ajax({
        url: '/search',
        //data: $('form').serialize(),
        contentType : 'application/json; charset=utf-8',
        data : JSON.stringify(inputData),
        type: 'POST',
        success: function(response) {
            //console.log("response typeof: " + typeof response)
            
	    //var responseObj = JSON.stringify(eval("(" + response + ")"));
            var responseObj = JSON.parse(response);
            //console.log("responseObj:" + responseObj + ", responseObj typeof: " + typeof responseObj);
	    //console.log("responseObj:" + JSON.stringify(responseObj))	

            var jobsArray = responseObj.resJSON;
	    var jobtitle = "";
            var company = "";
            var location = "";
            var date = "";
            var url = "";
            var snippet = "";
            console.log("jobsArray length:" + jobsArray.length )
       
            for (var i=0; i<jobsArray.length; i++) {

                jobtitle = jobsArray[i]._source.jobtitle;
                company = jobsArray[i]._source.company;
                location = jobsArray[i]._source.location;
                snippet = jobsArray[i]._source.snippet;
                url = jobsArray[i]._source.url;
                //date = jobsArray[i]._source.day.toString() + ' - ' +  jobsArray[i]._source.month.toString() + ' - ' + jobsArray[i]._source.year.toString()   
                //console.log("row: " + i + ", jobtitle:" + jobtitle + ", company:" + company + ", location:" + location + ", date:" + date + ", url:" + url + ", snippet:" + snippet);

		$jobRow = $(".jobsResultsSection .jobRowTemplate").clone();
            	$jobRow.removeClass("jobRowTemplate");
                $jobRow.find(".jobtitleCompanyCol").text(jobtitle + " at " + company); 
                $jobRow.find(".snippetCol").text(snippet); 
                $jobRow.find(".urlLink").attr("href", url); 

                $(".jobsResultsSection").append('<div class="row jobRow">' + $jobRow.html() + '</div>');

            }
        },
        error: function(error) {
            console.log(error);
        }
    });


}
