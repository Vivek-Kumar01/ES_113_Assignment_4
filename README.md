# ES_113_Assignment_4
This is the fourth assignment of the ES 113 course (Data-Centric and Computing)

To set up the website on your local computer:
1. Make a new Python project on your favourite code editor(VS Code)/IDE(Pycharm)
2. Download and extract the folders and files in the Electoral_Bonds folder and save them in your newly created project directory.
3. PIP install required libraries (that are imported by app.py)
4. Run app.py and go to the local URL. You can see the options for searching and analysing bonds.

There is also another folder named "PDF to CSV" with code used to convert PDF table data to CSV. (You can run this by following similar steps mentioned above) 

This csv is then imported in MySQL database. The front end and back end are connected through the Flask library, and SQLAlchemy is used to compute SQL queries.

The first link has a search/filter functionality to get bond-purchased data and shows the quantity.
The second link has a search/filter functionality to get bond-redeemed data and shows the quantity.
The third link joins the two tables and gives which bond was bought by which company and the party which redeemed it. And shows the total number of denominations for the given conditions.
