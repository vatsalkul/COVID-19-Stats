![Blue, Yellow and Red Technology Facebook Cover](https://user-images.githubusercontent.com/30840527/77793080-7bed3980-708f-11ea-969e-490a067f0f4d.png)

# know-Corona

An attempt to raise awareness around the Covid-19 pandemic amongst the community.

- 🌏 Get worldwide Coronavirus disease (COVID-19) stats.
- 🇮🇳 Indian State wise data of Coronavirus disease.
- 💫 Country wise stats.
- 🗃️ Data: Country, Cases, Deaths, Recovered, Active, Critical, Per Million
- 🔔 Latest notifications by Indian Government related to COVID-19.
- 🥁 Announcements by reliable organisations like WHO.
- 🎯 Guidance on how to be safe (issued by WHO)

## Install

The project runs on Python 3.

1. Create a virtual environment:
`virtualenv venv --python=python3`

2. Activate the virtual environment:
`source ./venv/bin/activate`

3. Install all the dependencies in `requirements.txt` file:
`pip install -r requirements.txt`

4. Make sure you exported the following environment variables:
```
export DB_TYPE=<database_type>
export DB_USERNAME=<database_username>
export DB_PASSWORD=<database_password>
export DB_ENDPOINT=<database_endpoint>
export DB_NAME=<database_name>
```

5. Run the app:
`python app.py`

6. Navigate to http://localhost:5000 in your browser 

7. When you are done using the app, deactivate the virtual environment:
`deactivate`

## APIs
You can access the following routes to get data.

- **/home** : Overall World wide stats.
- **/world** : Country wise report
- **/india** : Indian State wise report.
- **/announcements** : Get announcements by WHO.
- **/notifications** : Get notifications from Indian government.
- **/guide** : Get guidance to fight COVID-19, posted by WHO.

**NOTE:** Announcements and Guidance need to be added to the database. Deployed version of know-Corona have all the data.

### Deployment
This app is deployed on Heroku and you can access the above mentioned api using http://know-corona.herokuapp.com/ (abovementioned api)

## Contribution
Feel free to play with the project and raise issue to introduce new feature.

## Contact
You can reach out to me at vatsalkulshreshtha@gmail.com

## License
Licensed under the [MIT License](https://github.com/vatsalkul/COVID-19-Stats/blob/master/LICENSE).
