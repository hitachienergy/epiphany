#!/bin/bash
echo 'Running SonarQube'
sonar-scanner -Dsonar.projectKey=$SONAR_PROJECT_KEY -Dsonar.host.url=$SONAR_HOST_URL -Dsonar.login=$SONAR_LOGIN