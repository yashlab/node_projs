
> Written with [StackEdit](https://stackedit.io/).
NOTE: Make sure you are in the Gita bot directory before running any scripts. 
> ## Process:
 1. Verse_Tweeter.py
	- Dependency:
		* config.py
		* verse_process.py
	- Functions:
		* loads the verse data from source
		* generates html and images for verse and meanings
		* updates the register with today date and next verse URL
		 
2. mailstart.py
	- Dependency:
		- mailer_with_attach.py : 
		- data_details.py
		- ses_mailer.py
	- Functions:
		- fetches the recipients list from Google Sheets API.
		- sends emails to the recipients using either G-Mail or Amazon SES.

## Sample Outputs

![](quote.jpeg)
![](meaning.jpeg)
