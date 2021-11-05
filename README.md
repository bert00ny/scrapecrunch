# Crunchbase scrape

There is still a lot of improvement 

## Table of contents
* [Technologies](#Technologies)
* [Results](#Results)
* [Setup](#Setup)
	
## Technologies
Project is created with:
* Python 3.8

## Results


| Features | Total_Road_Deaths | Area  | Population | Vehicle_ownership | Population_density  | GDP |
| --- | --- | --- | --- |--- |--- |---|
| Spearman correlation | 0.101848 | 0.015058 | 0.003833 | -0.271906 | -0.287514 | -0.774538 |

According to the Spearman correlation coefficients, the total number of road deaths, the size of a European country, and the number of people living in that country have a very weak and positive correlation with the number of road deaths per million inhabitants for that country. Vehicle ownership and population density (inhabitants per km2) have a weak and negative correlation with road deaths per million inhabitants. Finally, GDP has a strong (almost very strong) and negative correlation with road deaths per million inhabitants. This strong and negative correlation means that the higher the GPD is for a country, the smaller the number of road death per million inhabitants.


![Algorithm schema](./4m-carbon-fiberPIC.png)



For any interested reader, the correlation matrix above can be used to compare the correlations between all of the features in the CSV file.

| Spearman correlation coeficient| Strength of correlation |
| --- | --- |
| .00-.19 | very weak |
| .20-.39 | weak |
| .40-.59 | moderate |
| .60-.79 | strong |
| .80-1.0 | very strong |
	
## Setup
To run this project, download the project and run the following in Bash:

```
$ cd ../local_directory/
$ python3 normalization.py
```
