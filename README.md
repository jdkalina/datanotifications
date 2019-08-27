# datanotifications
The goal is to create an automated collection of change notifications using Selemium. Change notifications are a series of weekly spreadsheets only exposed on a credentialed website and disseminated by Refinitiv on their support website.

To this end we'll use Python and a specific package called Selenium, which is an adapted package for website automation and testing. 

Important: You can't just download the selenium package, newer versions of the package require that you also install and webdriver from either chrome or firefox. Some easy Google-fu for 'Chrome Webdriver' should do the trick. You'll need to create a path to the webdriver after you've installed it on your cpu. Working on a future iteration where this is ported with a headless driver to a cloud instance.
