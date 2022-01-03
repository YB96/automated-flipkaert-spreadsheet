# Automated Flipkart spreadsheet
Flipkart is one such eCommerce company that promotes online sales in India. It is not only for accessories, but for a wide range of other daily use items as well, that Flipkart remains as the leading choice of online shoppers. Flipkart, the most prominent eCommerce website in India and is empowering tons of Indian businesses to venture into the competitive online shopping industry. This multi-vendor website serves as the platform for vendors to display their product to the website’s visitors. It was initiated in 2007 and recently achieved a similar web ranking of 133 globally and 9th amongst the top Indian websites. Flipkart is the first eCommerce website in India that has reached the $1 billion mark.

We will be creating a csv file which will contain all the `iPhones` data present in the flipkart and sending it through an automated mail using SMTP library. The web page we are going to scrape is this [page](https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3DAPPLE&page=).
![](https://imgur.com/TCcnDWE)<br>
In the csv file we will adding `Mobile names`,`Prices`,`Ratings` and `Description`

Here is an outline of all the steps we will follow:

1. Download the webpage using "request library
2. Parse the HTML source code using beautiful soup
3. Extract items description, rating, prices, review and image Urls from 8 pages 
4. Compile and extracted information into Python lists and dictionaries
5. Extract and combine data from multiple pages
6. Save the extracted information to a CSV file.


By the end of the project, we will created a CSV file in the similar format:<br> 
- Each record is located on a separate line, delimited by a line break (CRLF).  
For example:<br>
aaa,bbb,ccc CRLF <br>
zzz,yyy,xxx CRLF
