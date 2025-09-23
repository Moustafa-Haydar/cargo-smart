<img src="./readme/title1.svg"/>

<br><br>

<!-- project overview -->
<img src="./readme/title2.svg"/>

CargoSmart is an AI-powered intelligent logistics platform that leverages machine learning and agentic AI to autonomously optimize delivery routes, predict delays, and automate shipment management decisions in real-time.

<br><br>

<!-- System Design -->
<img src="./readme/title3.svg"/>

### Cargo Smart – Software Architecture

<p align="center">
  <img src="./readme/demo/tools/software architecture.png" width="500"/>
</p>

### Cargo Smart - Class diagram

[View on Eraser](https://app.eraser.io/workspace/hUhaIbwbfGFrjAfvHiIM)

<p align="center">
  <img src="./readme/demo/tools/eraser .png" width="400"/>
</p>

<br><br>

<!-- Project Highlights -->
<img src="./readme/title4.svg"/>

### Main Features

<p align="center">
  <img src="./readme/demo/tools/features.png" width="400"/>
</p>

- Machine Learning Model that analysis weather, and location data to forecast shipment delays with 86%+ accuracy. The machine learning classifier processes multiple environmental factors to provide both delay probability and ETA adjustments.
- AI Agent that generates optimal alternative routes using Dijkstra's algorithm when delays are predicted, and presents rerouting suggestions to operations managers for approval.
- N8N automation engine that monitors all active shipments every 5 minutes, identifies delayed routes using ML predictions, and automatically triggers the agentic AI for route regeneration, also sending real-time notifications to drivers.
- Interactive Google Maps-powered operations center that displays vehicle tracking, shipment locations, and route visualizations with dynamic filtering and hover tooltips. The live map provides route polylines, and multi-theme support (light, dark, satellite, terrain) for comprehensive logistics oversight.

<br><br>

<!-- Demo -->
<img src="./readme/title5.svg"/>

### Operations Manager Screens (Web)

<table style="width:100%; table-layout:fixed;">
  <tr>
    <td style="width:50%;">Login screen</td>
    <td style="width:50%;">Shipments screen</td>
  </tr>
  <tr>
    <td style="width:50%; vertical-align:top;">
      <img src="./readme/demo/screens - ops manager/login.png" style="width:100%; height:auto; object-fit:contain;"/>
    </td>
    <td style="width:50%; vertical-align:top;">
      <img src="./readme/demo/screens - ops manager/shipments.png" style="width:100%; height:auto; object-fit:contain;"/>
    </td>
  </tr>
</table>

<table style="width:100%; table-layout:fixed;">
  <tr>
    <td style="width:50%;">Map screen</td>
  </tr>
  <tr>
    <td style="width:50%; vertical-align:top;">
        <img src="./readme/demo/screens - ops manager/map.gif" style="width:100%; height:auto; object-fit:contain;"/>
    </td>
  </tr>
</table>

<table style="width:100%; table-layout:fixed;">
  <tr>
    <td>Vehicles screen</td>
    <td>Routes screen</td>
  </tr>
  <tr>
    <td>
      <img src="./readme/demo/screens - ops manager/vehicles.png" style="max-width:100%; height:auto;"/>
    </td>
    <td style="width:50%; vertical-align:top;">
      <img src="./readme/demo/screens - ops manager/routes.png" style="width:100%; height:auto; object-fit:contain;"/>
    </td>
  </tr>
</table>

<table style="width:100%; table-layout:fixed; margin-top:20px;">
  <tr>
    <td>Reroute screen</td>
  </tr>
  <tr>
    <td>
      <img src="./readme/demo/screens - ops manager/reroute gif.gif" style="max-width:100%; height:auto;"/>
    </td>
  </tr>
</table>

<br><br>

### User Screens (Mobile)

<table>
  <tr>
    <td>Login screen</td>
    <td>Shipments screen</td>
    <td>Mark As Delivered screen</td>
  </tr>
  <tr>
    <td><img src="./readme/demo/screens%20-%20mobile/mobile%20-%20login.png" width="250"/></td>
    <td><img src="./readme/demo/screens%20-%20mobile/mobile%20-%20shipments.png" width="250"/></td>
    <td><img src="./readme/demo/screens%20-%20mobile/mobile%20-%20mark%20as%20delivered.png" width="250"/></td>
  </tr>
</table>

### Admin Screens (Web)

<table style="width:100%; table-layout:fixed; margin-top:20px;">
  <tr>
    <td>Users screen</td>
    <td>Groups screen</td>
  </tr>
  <tr>
    <td>
      <img src="./readme/demo/screens - admin/users.png" style="max-width:100%; height:auto;"/>
    </td>
    <td>
      <img src="./readme/demo/screens - admin/groups.png" style="max-width:100%; height:auto;"/>
    </td>
  </tr>
</table>

<table style="width:100%; table-layout:fixed; margin-top:20px;">
  <tr>
    <td>Permissions screen</td>
    <td>Group Permissions screen</td>
  </tr>
  <tr>
    <td>
      <img src="./readme/demo/screens - admin/permissions.png" style="max-width:100%; height:auto;"/>
    </td>
    <td>
      <img src="./readme/demo/screens - admin/group permissions.png" style="max-width:100%; height:auto;"/>
    </td>
  </tr>
</table>

<br><br>

<!-- Development & Testing -->
<img src="./readme/title6.svg"/>

<table>
  <tr>
    <td>Services</td>
    <td>Validation</td>
    <td>Testing</td>
  </tr>
  <tr>
    <td><img src="./readme/demo/development/services.png" width="250"/></td>
    <td><img src="./readme/demo/development/validate login .png" width="250"/></td>
    <td><img src="./readme/demo/development/test.png" width="250"/></td>
  </tr>
</table>

### Machine Learning

<p align="center">
  <img src="./backend/models/plots/confusion_matrix.png" width="500"/>
</p>

#### Delay Prediction — Summary

`train_delay_model.py` trains a delay classifier using a Scikit‑learn `LogisticRegression` inside a preprocessing `Pipeline` (imputation + scaling for numeric, one‑hot for categorical). Features include geospatial distance, temporal signals, and simple weather flags. Data comes from `data/delivery_truck_data.xlsx` with an 80/20 stratified split. The trained model is saved to `models/delay_classifier.joblib` and plots to `models/plots/`.

- **ROC‑AUC**: 0.841 • **PR‑AUC**: 0.914 • **F1**: 0.797
- **Accuracy**: 0.75 (support: 1,278)
- Confusion matrix shown above (`confusion_matrix.png`).

### Dataset

The dataset used in this project is published: [Enhanced Delivery Truck Trips Dataset with Routes and Weather](https://zenodo.org/records/17185680).

This dataset contains enriched delivery truck trip records. The base data was originally obtained from the Kaggle Delivery Truck Trips Dataset.

To extend the dataset’s analytical value, two additional data sources were integrated:

- **Routes**: Calculated using the OpenRouteService API, providing geographical routing information.
- **Weather**: Historical weather data retrieved via the OpenWeatherMap API, giving environmental context to each trip.

This combination allows researchers and practitioners to explore the impact of routes and weather conditions on delivery logistics and performance.

### N8N Automation

<table>
  <tr>
    <td>N8N Automation</td>
  </tr>
  <tr>
    <td>
        <img src="./readme/demo/tools/n8n description .png" style="max-width:100%; height:auto;"/>
    </td>
  </tr>
  <tr>
    <td>
        <img src="./readme/demo/tools/n8n.png" style="max-width:100%; height:auto;"/>
    </td>
  </tr>
</table>

### Project Management (Linear)

- Overview of how tasks were organized and tracked throughout the project.

<table>
  <tr>
    <td>Linear</td>
  </tr>
  <tr>
    <td>
        <img src="./readme/demo/tools/linear .png" style="max-width:100%; height:auto;"/>
    </td>
  </tr>
</table>

<br><br>

<!-- Deployment -->
<img src="./readme/title7.svg"/>

### Swagger API Documentation

- Interactive API docs for backend services
- Groups: Web Authentication, User Management, Mobile Authentication, Mobile Shipments,...
- Tips:
  - Mobile: login to get a token, then Authorize with Bearer token
  - Web: get CSRF, then login; session cookies are used

<table style="width:100%; table-layout:fixed; margin-top:10px;">
  <tr>
    <td>Swagger API 1</td>
    <td>Swagger API 2</td>
    <td>Swagger API 3</td>
  </tr>
  <tr>
    <td><img src="./readme/demo/swagger apis/api 1.png" width="250"/></td>
    <td><img src="./readme/demo/swagger apis/api 2.png" width="250"/></td>
    <td><img src="./readme/demo/swagger apis/api 3.png" width="250"/></td>
  </tr>
</table>
