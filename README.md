Pickystats app is a simple project which receives a text file input and provides
some statistics regarding the entries of the text file. Its is modularized and can
be extended easly. 

# Getting started
1. Clone the repository
2. Checkout to develop branch
3. `pip install -r requirements`
4. `python manage.py rusnerver`
5. Navigate to the api docs of your choosing for more info:
    - Redoc: /api/v1/redoc/
    - Swagger: /api/v1/swagger/
    
# Adding more statistics
- If you want to add your own statistic you need to take two steps:
    1. Inherit from `pickystats.analyzer.BaseCustomStats` and Implement the
    `get_analysis` method. Let's call it `MyCustomPickStats`
       
    2. Next You have to add `MyCustomPickStats` to `pickystats.analyzer.PickyStat` `analyzer` list.
    That's it. Just note that you have to operate on self.normalized_data when inheriting form `BaseCustomStat`
       
# Adding more output formats
- Provided that you have implemented your own output formatting class, you can plug it in by
adding a method to `pickystats.analyzer.DataFormatters` and chose a name for the format and add 
  it to the `self._formats` dict. That's it. 
    
# Running Tests:
- Issue: 
    - `pytest -v`
    
# Roadmap 
The followings could enrich the quality of the codebase:
- A more robust validation of the uploaded text-file
- A better normalizer class to be able to parse and normalized more malformed element entries.
- Docs improvement to enable auto generation using tools such as sphinx
- If you want to go to extremes, you could add a data model to hold the hash value of input
text file to prevent processing of already-processed text inputs and simply return the cached results.
- Dockerization of project could be.

# Task Stats
- I put Almost 4 Hours to complete the task including designing high-level architecture, and coding.
- I put an extra 45 minutes to for documentation and improving annotations.