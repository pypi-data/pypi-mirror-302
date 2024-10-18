[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/n9_1Qfip)
# Overview

Your team has been hired to develop a web application for a small logistics company, based on the requirements outlined in this document. Since these requirements are well understood and the project is relatively small, your team has chosen the **waterfall** process model for this project. The phases of the project, following the **waterfall** model, are detailed below.

# Communication Phase

## Overview

The project involves developing a web application for a logistics company to manage information about their facilities. This includes details such as the facility name, location, type (warehouse or distribution center), and operational status (active or inactive). Additionally, the application will track the costs of transporting goods between facilities. By optimizing these routes, the web application will help the company save money.

## Objectives 

* Manage facility information.
* Update tranportation costs between facilities.
* Calculate optimal routes between facilities.

## Requirements 

1. Users must be able to authenticate themselves.
2. Users should be able to list all facilities.
3. Users should be able to create, update, and delete facilities.
4. Users should be able to update the transportation costs between any pair of facilities.
5. Users should be able to retrieve the optimal routes between one facility and all others.

## Constraints 

* A working version of the web application is expected to be delivered in 3 weeks. 
* The implementation team is limited to 3 to 5 members. 
* The software must be implemented in Python, Flask, and SQLAlchemy. 

## Risks 

* The tight schedule may result in the system not meeting quality requirements. 

# Planning Phase

## Schedule 

Estimate a schedule for this project by completing the table below. 

|Phase|Task|Start|End|Duration|Deliverable|
|---|---|---|---|---|---|
|Modeling|Requirements Analysis|10/03/24|10/08/24|5 days|Use Case Diagram|
|Modeling|Data Model|10/03/24|10/08/24|5 days|Class Diagram|
|Construction|Coding|10/08/24|10/15/24|7 days|Code|
|Construction|Testing|10/15/24|10/17/24|2 days|Test Report|
|Deployment|Delivery|10/17/23|10/18/24|1 day|Final Commit/Push|

## Team Roles

Assign roles for each member of the team by completing the table below. Member can take more than one role. 

|Name|Role(s)|
|--|--|
|name|manager: Kyle Pineiro,developer: Samrawit Weldehawariyat, Manoj Budathoki tester:Phil Phronesius,documenter:Yujin|

# Modeling Phase

## Requirements Analysis 

Based on the description given for this project, complete the requirements analysis by building a use case diagram using UML.  

## Data Model 

Based on the model shared in **models.py**, document the data model by creating a UML class diagram. The model consists of the following entities:

* User: id, name, about, and password. 
* Facility: id, name, address, type, and active.
* TransportationCost: from_facility, to_facility, cost

Make sure that your class diagram shows the association between **Facility** and **TransportationCost**. 

## Baseline Implementation

A baseline for the web app is given in **Flask**. The project should be structured like the following: 

```
.venv
pics
src
|__app
|______init__.py
|____modes.py
|____routes.py
|____forms.py
|__instance
|____logistics.db
|__static
|____style.css
|__templates
|____base.html
|____index.html
uml
|__class.wsd
|__use_case.wsd
README.md
requirements.txt
Dockerfile
```

The **.venv** should NOT be pushed to the remote repository. Add an exception in your **.gitignore**. 

# Implementation Phase

Following software development collaboration best practices, create a **dev** branch for the beta versions of your project. Additionally, create local temporary branches for development and testing, assigned to individual team members. When the **dev** version of your project is stable, merge it into the **main** branch. 

The template code includes suggested routes that follow API development best practices. We strongly recommend adopting these suggested routes.

To compute the shortest path routes, we strongly recommend using the library you built in Homework #4.

Before starting the implementation, a team representative must meet with the instructor. This is a mandatory checkpoint. Be prepared to present the use case and class diagrams, a baseline implementation, a draft schedule, and the team roles assignment. 

# Testing Phase

At this point you are NOT expected to write automated tests.  Instead, you are asked to run manual tests and complete a report using the table below. 

|Functionality Tested|Date|Time|Result|
|--|--|--|--|
|Sign Up|99/99/23|99:99|passed|
|...|...|...|...|

# Deployment Phase

Commit and push your project using "final submission" as the commit message. Additionally, create a Docker image to enable the instructor to run your project as a container. To meet this requirement, you should create a Dockerfile that allows the instructor to build the image of your project and run it as a container.

# Team Evaluation 

Student will receive a form to evaluate the members of their team and to self-evaluate themselves.  

# Rubric 

+5 Planning: Schedule

+5 Planning: Team Roles 

+10 Modeling: Use Case Diagram 

+10 Modeling: Class Diagram

+10 Check-point

+40 Implementation

+10 Testing 

+10 Deployment

-25 Team/Self Evaluation

## Bonus

+5 incorporating a visual representation of the facilities and the transportation costs between them using a graph library.

# User Interface Suggestions

![pic1](pics/pic1.png)

![pic2](pics/pic2.png)

![pic3](pics/pic3.png)

![pic4](pics/pic4.png)

![pic5](pics/pic5.png)

![pic6](pics/pic6.png)

![pic7](pics/pic7.png)

![pic8](pics/pic8.png)
