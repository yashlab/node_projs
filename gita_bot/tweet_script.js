var http = require('http');
var twit = require('twitter');
require('dotenv').config();
const quotes = require('current_verse.json');

var client = new twit({
	consumer_key: process.env.CONSUMER_KEY,
	consumer_secret: process.env.CONSUMER_SECRET,
	access_token_key: process.env.ACCESS_TOKEN_KEY,
	access_token_secret: process.env.ACCESS_TOKEN_SECRET
});

console.log(quotes)