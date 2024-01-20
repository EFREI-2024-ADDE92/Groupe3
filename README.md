# Groupe3
Melis HARMANTEPE
Mathis DA CRUZ
Sarankan SIVANANTHAN
Ulysse BOUCHET
Kevin ESTEVES

#Créer l'application du modèle et faire une requete pour une prédiction
(Langer d'abord get_model.py)
curl -X POST "http://127.0.0.1:5000/predict?sepal_length=5.0&sepal_width=2.1&petal_length=2.4&petal_width=3.2"

#Build docker image
docker build -t model_groupe3 .

#Run l'image en local
docker run -p 5000:5000 model_groupe3

#Login to azure ACR
az login
az acr login --name efreibigdata.azurecr.io

#Tag the image
docker tag model_groupe3 efreibigdata.azurecr.io/model_groupe3:latest

#Push image to azure
docker push efreibigdata.azurecr.io/model_groupe3:latest
az acr repository list --name efreibigdata.azurecr.io --output table

#Test charge (k6 avec js)
k6 run -e MY_URL=https://group3-container.bluesmoke-5ac04595.francecentral.azurecontainerapps.io/predict/test_charge.js

#Test predict on the app
curl -X POST "https://group3-container.bluesmoke-5ac04595.francecentral.azurecontainerapps.io/predict?sepal_length=5.0&sepal_width=2.1&petal_length=2.4&petal_width=3.2"

#Faire 10 requetes pour tester l'autoscaling
for i in {1..10}; do curl -X POST "https://group3-container.bluesmoke-5ac04595.francecentral.azurecontainerapps.io/predict?sepal_length=5.0&sepal_width=2.1&petal_length=2.4&petal_width=3.2"; done

#Tester prometheus
curl https://group3-container.bluesmoke-5ac04595.francecentral.azurecontainerapps.io/metrics

#Filter les metrics
curl https://group3-container.bluesmoke-5ac04595.francecentral.azurecontainerapps.io/metrics | grep 'api_calls_total'
