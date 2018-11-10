# cs490seniorproject
May we graduate with hope in our hearts.


Progress Updates:



Sage 9/30/18:
- Making pymongo work took some time today, but managed to get it working fine. I decided to work with Mongo Atlas, which is a cloud storage platform for us to not have to store data locally. I’ll be uploading my code and tidy it up in the coming days (as well as adding descriptions of how the parts work!).
    - The database is ready for CRUD operations via pymongo!

- It should be noted, users must be added to the project AND added as SCRAM users (SCRAM being an authentication method. They have to be added otherwise authentication will fail).

- Packages that will be needed are pymongo, pprint, and urllib.

- Working with Atlas means that its using Mongo 4.x. To work with that, we’ll need to use python 3.7 to avoid possible problems.

- Also, as much as I like the idea of forking and pull requests, it seems that
we are not allowed to fork a repository you own. So far I've just updated the
master repo, but I think I'll be working with branches as I add to the database manipulation.


Our web app is deployed to: https://data-sense.herokuapp.com/
