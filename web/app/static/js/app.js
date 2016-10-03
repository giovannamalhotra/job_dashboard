/*
Javascript for job dashboard app
*/
var companyTweetsMap = {};


function getNumTweets(companyName) {

    var totalNum = 0;
    companyName = companyName.toLowerCase();
    if ( companyTweetsMap[companyName] ) {
        totalNum = companyTweetsMap[companyName].length;
    }    
    return totalNum;
}


function getArrayOfTweets(companyName) {

    companyName = companyName.toLowerCase();
    var tweetsArray = [];

    if ( companyTweetsMap[companyName] ) {
        tweetsArray = companyTweetsMap[companyName];
    }    
    return tweetsArray;
}



function search() {

    var jobtitle = $('#jobtitleInput').val();
    var company = $('#companyInput').val();
    var location = $('#locationInput').val();
 
 	var inputData = {'jobtitle': jobtitle, 'company': company, 'location': location};

 	console.log("inputData: " + JSON.stringify(inputData));

    $.ajax({
        url: '/search',
        //data: $('form').serialize(),
        contentType : 'application/json; charset=utf-8',
        data : JSON.stringify(inputData),
        type: 'POST',
        success: function(response) {
            //console.log("response typeof: " + typeof response)

            // Hide any error message that might be displayed
            $(".errorMsg").text(" ").hide();

                
            //var responseObj = JSON.stringify(eval("(" + response + ")"));
            var responseObj = JSON.parse(response);
            //console.log("responseObj:" + responseObj + ", responseObj typeof: " + typeof responseObj);
            //console.log("responseObj:" + JSON.stringify(responseObj))	

            /* Load tweets for each company */    
            tweetsArray = responseObj.res_tweets_json;
            companyTweetsMap = {};

            console.log("tweetsArray:" + JSON.stringify(tweetsArray));

            for (var i=0; i<tweetsArray.length; i++) {

                if (tweetsArray[i]._source) {

                    var company = tweetsArray[i]._source.company.toLowerCase();    
                    var tweet = tweetsArray[i]._source.tweet;
                    
                    if ( !companyTweetsMap[company] ) {

                        companyTweetsMap[company] = [tweet];    
                    } else {
                        companyTweetsMap[company].push(tweet);  
                    }
                }    
            }    

            console.log("companyTweetsMap:" + JSON.stringify(companyTweetsMap));
            
            var jobsArray = responseObj.res_jobs_json;
            var jobtitle = "";
            var company = "";
            var location = "";
            var date = "";
            var url = "";
            var snippet = "";
            console.log("jobsArray length:" + jobsArray.length);
           
            $(".jobsResultsSection .jobRow").not(".jobRowTemplate").remove();
            $(".jobsResultsSection .tweetsRow").remove();

            if (jobsArray.length > 0) {

                /* Sort jobs by Tweets */    

                jobsArray.sort(function(a, b) {

                    var companyA_tweetsNum = 0;
                    var companyB_tweetsNum = 0;

                    if ( companyTweetsMap[a._source.company] )  {
                        companyA_tweetsNum = companyTweetsMap[a_source.company].length;
                    }

                    if ( companyTweetsMap[b._source.company] )  {
                        companyB_tweetsNum = companyTweetsMap[b_source.company].length;
                    }
                    return companyA_tweetsNum - companyB_tweetsNum;
                });    


                $("body").removeClass("landing_background");
                $(".landing_box").fadeOut("normal", function() {
                    $(".jobsResultsSection").show("slow");
                });

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
                    $jobRow.find(".jobtitle").text(jobtitle); 
                    $jobRow.find(".company").text(company); 
                    $jobRow.find(".location").text(location); 
                    $jobRow.find(".urlLink").attr("href", url); 
                    $jobRow.find(".snippet").html(snippet); 

                    // Populate tweets
                    console.log("company:" + company + ", num Tweets:" + getNumTweets(company));
                    $jobRow.find(".tweetsNum").text(getNumTweets(company) + " tweets");
                    $jobRow.find(".tweetsNum").attr("data-company", company); 

                    $(".jobsResultsSection").append('<div class="row jobRow">' + $jobRow.html() + '</div>');

                }
            } else {
                $(".errorMsg").text("No results were found").show();
            }    
        },
        error: function(error) {
            console.log(error);
        }
    });

}


function displayLanding() {
    $(".jobsResultsSection").hide();
    $("body").addClass("landing_background");
    $(".landing_box").slideDown();
}



function changeStarStyle(thisObj) {

    $star = thisObj.find("i");
    if ( $star.hasClass("fa-star-o") ) {

        $star.removeClass("fa-star-o");
        $star.addClass("fa-star");

    } else {

        $star.removeClass("fa-star");
        $star.addClass("fa-star-o");
    }
}


function closeTweetsSection(thisObj) {

    thisObj.closest(".tweetsRow").slideUp("normal");
}



function displayTweets(thisObj) {

    $jobRowParent = thisObj.closest(".jobRow");

    if ( !$jobRowParent.next(".tweetsRow").length ) {

        var company = thisObj.find(".tweetsNum").attr("data-company");
        var tweetsArray = getArrayOfTweets(company);
        console.log("Inside displayTweets... company:" + company + ", tweetsArray:" + tweetsArray);

        var tweetsHTML = '<div class="tweetsRow row">' + 
                            '<div class="col-xs-10 tweetsSectionCol">' + 
                                '<div class="tweetsSectionTitle">Tweets</div>' +
                                 '<ul>';   



        for (var i=0; i<tweetsArray.length; i++) {
            tweetsHTML = tweetsHTML + 
                         '<li class="tweetElem">' + tweetsArray[i] + '</li>';
        }

        tweetsHTML = tweetsHTML +  '</ul>' + 
                            '</div>' + 
                            '<div class="col-xs-2">' + 
                                '<a href="javascript:void(0)" onclick="closeTweetsSection($(this))">' + 
                                    '<i class="fa fa-times closeTweetsBtn" aria-hidden="true"></i>' + 
                                '</a>' +
                            '</div>' + 
                        '</div>';    


        $jobRowParent.after(tweetsHTML);
    }


    if ( $jobRowParent.next(".tweetsRow").css("display") !== "none" ) { // Tweets section is visible
        $jobRowParent.next(".tweetsRow").slideUp("normal");

    } else {    
        $jobRowParent.next(".tweetsRow").slideDown("normal");     

    }
}


$(".form-control").keypress(function(e){
      if(e.keyCode==13) { $('#searchBtnId').click(); }
});

