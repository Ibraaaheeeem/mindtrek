# alx-project-mmcq

# MedQuiz Project

Welcome to the MedQuiz project! This is a medical quiz application being designed to provide users with a platform for learning and testing their knowledge in the field of medical sciences. This README.md file will update you about the status of the project

## Table of Contents

- [Project Overview](#project-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

MedQuiz is aimed at offering an engaging and educational experience for medical students, professionals, and enthusiasts. The application will include a variety of quiz questions on medical subjects, adaptive learning features, and up-to-date content. 
It aims to include static content as well as dynamic content utilizing artificial intelligence to generate multiple choice questions that are user-tailored.

## Status Update

### Models

Flask app is been setup
Database models created. Models used
+ Category (Highest level of categorisation of questions)
+ Subcategory (under Category)
+ Subject (under Subcategory)
+ Unit(under Subject, lowest level of categorisation of questions)
+ Question(has a question_text, 5 options, correct option and explanation fields)
+ Attempt(represents a mock exam to be attempted by a user)
+ ExamSubject(represents a subject in a mock exam)


### Registration and Login api
+ Created a /auth/register endpoint for registration with username, email and password
+ Created a /auth/login endpoint for sigining in with username and password which returns a jwt
+ Created a /auth/profile endpoint for retrieval of user data

### Quiz api
1. [Get Categories](#get-categories)
2. [Get Subcategories](#get-subcategories)
3. [Get Subjects](#get-subjects)
4. [Get Units](#get-units)
5. [Get Questions](#get-questions)

### Admin api
1. [Add Category](#post-categories)
2. [Add Subcategory](#post-subcategories)
3. [Add Subject](#post-subjects)
4. [Add Unit](#post-units)
5. [Add Questions](#post-questions)
