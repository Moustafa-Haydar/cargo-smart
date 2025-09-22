<img src="./readme/title1.svg"/>

<br><br>

<!-- project overview -->
<img src="./readme/title2.svg"/>

CargoSmart is an AI-powered intelligent logistics platform that leverages machine learning and agentic AI to autonomously optimize delivery routes, predict delays, and automate shipment management decisions in real-time.

<br><br>

<!-- System Design -->
<img src="./readme/title3.svg"/>

### Cargo Smart – Software Architecture

<img src="./readme/demo/tools/software architecture.png"/>

### Cargo Smart - Class diagram

[View on Eraser](https://app.eraser.io/workspace/hUhaIbwbfGFrjAfvHiIM)

<img src="./readme/demo/tools/eraser .png"/>

<br><br>

<!-- Project Highlights -->
<img src="./readme/title4.svg"/>

### Main Features

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

### Add Title Here

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

<table>
  <tr>
    <td>Machine Learning</td>
  </tr>
  <tr>
    <td>
        <img src="./backend/models/plots/confusion_matrix.png" style="max-width:40%; height:auto;"/>
    </td>
  </tr>
</table>

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

<!-- ### Add Title Here

- Description here. -->

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
