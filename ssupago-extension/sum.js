// get text from document
text = document.body.innerHTML;
text = "Son Heung-min (Korean: 손흥민 /ˈsɒn ˈhʊŋ.mɪn/; born 8 July 1992) is a South Korean professional footballer who plays as a forward for the Premier League club Tottenham Hotspur and captains the South Korea national team.[5] Widely regarded as one of the best wingers in the world, as well as one of the best Asian footballers in history, Son was the first Asian player to score more than 50 goals in the Premier League, and was nominated for the Ballon d'Or in 2019.[9][10][11][12][13]Born in Chuncheon, Gangwon Province, Son relocated to Germany to join Hamburger SV at age 16, for which he made his debut in the German Bundesliga in 2010. In 2013, he moved to Bayer Leverkusen for a club record €10 million before signing for Tottenham for £22 million two years later, becoming the most expensive Asian player in history.[14] While at Tottenham, Son became the top Asian goalscorer in both Premier League and Champions League history,[15] and surpassed Cha Bum-kun's record for most goals scored by a Korean player in European competition.[16][17][18] In 2019, he became the second Asian in history to reach and start a UEFA Champions League final after fellow countryman Park Ji-sung.[19]";

// send text to server and get result
ssupago_url = "http://127.0.0.1:8000/"
$.ajax({
    type: 'POST',
    // type: 'GET',
    url: ssupago_url,
    data: { 'content': text },
    Headers: {
        'Access-Control-Allow-Origin': '*',
    },
    beforeSend: function(){
        console.log("before:\n" + text);
    },
    success: function(data, status){
        console.log("after:\n" + data);
    },
    error: function(xhr, status, error){
        console.log(error);
    }
});


// print result
// console.log(result);
