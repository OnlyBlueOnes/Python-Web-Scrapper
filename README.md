IKEA & Jysk product comparison researcher

1.	Project description:

The project was created in order to facilitate the product research process on the websites of the well known furniture stores: IKEA and Jysk. The program compares the offer of both stores within the chosen category (the carpets in presented sample) and display the results according to specified conditions (dimensions of the product in the case of presented program.

2.	Project implementation:

Project was written in Python language with use of the Mongo DB  and is the example of web scraping. The primary data was captured from the Polish version of IKEA and Jysk websites. Information needed to create the project was the names of products, their prices and dimensions as well as their localization on the source websites.
Program executes the research within the specified category. The results of the processing are following: if the requested data is found (dimensions of the product in presented sample), program checks the price and dimensions of all matching product and saves the data in file with .csv extension. In the next step, the data are transferred to Mongo DB. Data in .csv file is presented in form of five-column indexed table. In order to change the results, variable ‘ key_word’ should be changed for another string. If the specified name is missing, program displays the information in appropriate CLI. 
