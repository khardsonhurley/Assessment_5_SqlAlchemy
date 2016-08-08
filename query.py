"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise directions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()

# -------------------------------------------------------------------
# Part 2: Write queries


#1. Get the brand with the **id** of 8.
## Can do .get(8) here because id is the primary key for the brands table. 
query1 = Brand.query.get(8)

#2. Get all models with the **name** Corvette and the **brand_name** Chevrolet.
##Remember that and operator only allowed with filter not filter_by.

query2 = Model.query.filter(Model.name=='Corvette',
                            Model.brand_name=='Chevrolet').all()
#OR#

query2 = db.session.query(Model).filter(Model.name=='Corvette',
                                        Model.brand_name=='Chevrolet').all()

#3. Get all models that are older than 1960.
##Remember if you want a list, you need to include ".all()" otherwise, you just 
#get an object back. 

query3 = Model.query.filter(Model.year > 1960).all()

#OR#

query3 = db.session.query(Model).filter(Model.year > 1960).all()

#4. Get all brands that were founded after 1920.

#Returns a list in the __repr__ format. 
query4= Brand.query.filter(Brand.founded > 1920).all()

#OR#

query4= db.session.query(Brand).filter(Brand.founded > 1920).all()

#5. Get all models with names that begin with "Cor".

query5= Model.query.filter(Model.name.like('%Cor%')).all()

#OR#

query5= db.session.query(Model).filter(Model.name.like('%Cor%')).all()

#6. Get all brands that were founded in 1903 and that are not yet discontinued.

query6 = Brand.query.filter(Brand.founded==1903, Brand.discontinued==None).all()

#OR#

query6 = db.session.query(Brand).filter(Brand.founded==1903, 
                                        Brand.discontinued==None).all()

#7. Get all brands that are either 1) discontinued (at any time) or 2) founded 
# before 1950.

query7=Brand.query.filter((Brand.discontinued!=None)|(Brand.founded < 1950)).all() 

#OR#

query7=db.session.query(Brand).filter((Brand.discontinued!=None)|
                                      (Brand.founded < 1950)).all() 

#OR# -- Using db.or_

query7=Brand.query.filter(db.or_(Brand.discontinued!=None,
                                Brand.founded < 1950)).all() 

#OR#

query7=db.session.query(Brand).filter(db.or_(Brand.discontinued!=None,
                                        Brand.founded < 1950)).all() 

#8. Get any model whose brand_name is not Chevrolet.
#Used .first() because it said 'any model'. '.all()' would also suffice. 

query8 = Model.query.filter(Model.brand_name !='Chevrolet').first()

#OR#

query8 = db.session.query(Model).filter(Model.brand_name !='Chevrolet').first()

# Fill in the following functions. (See directions for more info.)

def get_model_info(year):
    '''Takes in a year, and prints out each model, brand_name, and brand
    headquarters for that year using only ONE database query.'''

    #Query the database for all models that have that year. 
    model_list = Model.query.filter(Model.year == year)

    #Iterating over the model_list to get all relevant information. 
    for model in model_list:
        print model.name, model.brand_name, model.brand.headquarters #using the relationship.
    

def get_brands_summary():
    '''Prints out each brand name, and each model name for that brand
     using only ONE database query.'''

    brands_list = Brand.query

    # ONE APPROACH WITH LISTS:
    #for brand in brands_list:
    #     print "Brand Name: " + brand.name
    #     model_list = ""
    #     for model in brand.model:
    #             model_list = model_list + model.name + " "
    #     print "\tModels: " + model_list
    
    # OTHER APPROACH WITH DICTIONARIES:      
    #empty dictionary to add keys and values to. 
    brand_dict = {}

    #iterate over the results from the query. Add each brand as a key in the 
    #dictionary.
    for brand in brands_list:
        #Set the value to an empty list.
        brand_dict[brand.name] = []
        #Add the models to the value list. 
        for model in brand.model:
            brand_dict[brand.name].append(model.name)
    
    #Formatting the output. Iterate over keys in the dictionary
    for key in brand_dict:
        model_string = ""
        #add all models to a string. 
        for model in brand_dict[key]:
            model_string = model_string + "\t" + model + "\n"
        #print the key (brand) and the string that contains all the models.
        if model_string =="":
            print key + ": \n" + "\tNo models\n"
        else:
            print key + ": \n" + model_string
        

    

# -------------------------------------------------------------------
# Part 2.5: Discussion Questions (Include your answers as comments.)

# 1. What is the returned value and datatype of ``Brand.query.filter_by(name='Ford')``?
"""This query returns a sqlAlchemy object. When I put this into the model.py 
interactive mode, the return value was <flask_sqlalchemy.BaseQuery object at 
0x7f7188f4df10>. If I actually wanted to the formatted __repr__, I would need 
use one of the fetching records suffixes (.all(), .first(), .one())."""

# 2. In your own words, what is an association table, and what *type* of relationship
# does an association table manage?
"""An association table is a table that is used to show how elements in two 
tables are connected, without storing any other meaningful data in that table.
For example, lets say you have a table that has "Teachers" [names of teachers]
and one that has "Subjects" [all the subjects possible to teach.] An Association
Table called "TeacherSubjects" could be used here to show the subjects teachers
are teaching. We don't need a middle table here because no additional information
is being stored.

If, however, if we wanted to store the teachers, subject and the period the class
occurs, then a middle table would be more appropriate."""

# -------------------------------------------------------------------
# Part 3

def search_brands_by_name(mystr):
    mysearch = Brand.query.filter(Brand.name.like('%'+mystr+'%')).all()
    return mysearch

def get_models_between(start_year, end_year):
    modelsbetween = Model.query.filter((Model.year>=start_year) & 
                                        (Model.year<end_year)).all()
    return modelsbetween
