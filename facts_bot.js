var http = require('http');
var twit = require('twitter');
require('dotenv').config();
const quotes = require('./facts.json');
var quote_tweet = quotes[Math.floor(Math.random()*3)];

var client = new twit({
	consumer_key: process.env.CONSUMER_KEY,
	consumer_secret: process.env.CONSUMER_SECRET,
	access_token_key: process.env.ACCESS_TOKEN_KEY,
	access_token_secret: process.env.ACCESS_TOKEN_SECRET
});

client.post('statuses/update',{status: 'Facts Bot Tweeting \n' + quote_tweet + '\n #facts #learnings'},
                            function(error,tweet,response){
                                if(!error){
                                    console.log(tweet);
                                }
                               });