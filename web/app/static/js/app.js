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

            /* Load tweets for each company */    
            tweetsArray = responseObj.res_tweets_json;

            console.log("tweetsArray:" + tweetsArray);

            for (var i=0; i<tweetsArray.length; i++) {

                if (tweetsArray[i]._source) {

                    var company = tweetsArray[i]._source.company.toLowerCase();    
                    var tweet = tweetsArray[i]._source.tweet;
                    
                    if ( !companyTweetsMap[company] ) {

                        var tweetsArray = [];
                        tweetsArray.push();    
                        companyTweetsMap[company] = tweetsArray;    
                    } else {
                       companyTweetsMap[company].push(tweet);  
                    }
                }    
            }    

            console.log("companyTweetsMap:" + companyTweetsMap);
            
            var jobsArray = responseObj.res_jobs_json;
            var jobtitle = "";
            var company = "";
            var location = "";
            var date = "";
            var url = "";
            var snippet = "";
            console.log("jobsArray length:" + jobsArray.length);
           
            $(".jobsResultsSection .jobRow").not(".jobRowTemplate").remove();

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
                $(".landing_box").slideUp("normal", function() {
                    $(".jobsResultsSection").show("normal");
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

                    $(".jobsResultsSection").append('<div class="row jobRow">' + $jobRow.html() + '</div>');

                    console.log("company:" + company + ", num Tweets:" + getNumTweets(company));

                    // Populate tweets
                    $jobRow.find(".TweetsNum").text(getNumTweets(company));
                    $jobRow.find(".TweetsNum").attr("data-company", company); 

                }
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
