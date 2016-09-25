/*
Javascript for job dashboard app
*/

console.log("Hello from app.js")


function displayResults(jsonList) {
	console.log(jsonList)
}


function search() {

    var jobtitle = $('#jobtitleInput').val();
    var company = $('#companyInput').val();
    var location = $('#locationInput').val();
 
 	var inputData = {'jobtitle': jobtitle, 'company': company, 'location': location};

 	console.log("inputData: " + inputData)


    $.ajax({
        url: '/search',
        //data: $('form').serialize(),
        contentType : 'application/json; charset=utf-8',
        data : JSON.stringify(inputData),
        type: 'POST',
        success: function(response) {
            console.log("Ajax response:" + response);
        },
        error: function(error) {
            console.log(error);
        }
    });


}
