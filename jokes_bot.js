var http = require('http');
var twit = require('twitter');
require('dotenv').config();
var axios = require('axios'); //https://github.com/axios/axios

var client = new twit({
	consumer_key: process.env.CONSUMER_KEY,
	consumer_secret: process.env.CONSUMER_SECRET,
	access_token_key: process.env.ACCESS_TOKEN_KEY,
	access_token_secret: process.env.ACCESS_TOKEN_SECRET
});

axios("https://official-joke-api.appspot.com/random_joke").then(Response => {
	return [Response.data.type, Response.data.setup, Response.data.punchline];
}).then(([type,setup, punch]) => {
	client.post('statuses/update', {status:  'Joke Bot Tweets.\nHere is a(n) '+ `${type}` +' joke.\n' + `${setup}\n\n\n${punch}` + '#joke #fun #covid #vaccine #lockdown 😁😆'}, function(error, tweet, response){
		if(!error){
			console.log(tweet);
		}
	})
});


