# Testing

<!-- TOC -->

- [Test Approach](#testaproach)
  - [Welcome](#welcome)
  - [Tool](#tool)
  - [Test Item](#testitem)
  - [Report](#report)
  - [Integration](#integration)

<!-- /TOC -->

## Welcome

This documentation describe approach in testing for open-source project 'epiphany-platform'.
In this section you can find test strategy, tools used for test management and terminology.

## Tool

For test management we are using  TestQuality, which extends Github to provide modern, powerful, test plan management.
All test activities are reported under dedicated project:

**https://epiphany-platform.testquality.com**

On-line help documentation is located: https://epiphany-platform.testquality.com/help/what

To get there, you need to ask for access one of [Administrators](#Administrators)

## Test Item

In TestQuality toll we are using such a testing terminology:  
**Test Project** - A project is used to organize testing and allows your team to coordinate their testing effort. A project can contain milestones and test cases organized into test plans.  
f.e. _Epiphany-platform_  
**Test Plan** - A test plan includes a set of test cases that help guide a specific testing effort against a product. It is a blueprint of what and how testing should be done. There are different test plans for different purposes, such as Acceptance test plan, Unit test plan, System test plan, Performance Test plan. A Test Plan is usually used to organize a testing activity. It contains a number of Test Cases grouped by Test Suites that together accomplish a particular goal in your overall repository of tests 
f.e _Automatic Deployment Smoke Test_, _Performance Test_ 

**Milestone** - A milestone is a time based goal, such as version release, patch, beta, iteration, etc. Milestones can track testing effort against a specific goal and are used to indicate what be and has been tested for goal.
f.e. _Sprint_20190328_, _Release19.2_

**Test Suite** - Allow to group Test Cases in larger common package, that is generally connected with one funcionality, platform or goal.
f.e _rspecRhel_, _specUbuntu_, _LongRunTest_

**Test Case** - A set of conditions when evaluated determine whether a system under test is working correctly. Test that are added to a Test Plan are later executed via a Test Plan Run. The bases of any Test Case are the steps, each step has the action to be performed and the expected results. These two parts of a step together with sequence allow to determine if your system under test is working.
f.e _Checking if RabbitMQ service is running_

**Test Plan Run** - A Test Plan Run is a way of creating a branch or version of your Test Plan that contains the tests you want to preform against a sytem under test. Results of Test Plan Run is indicated by Status.
Status gives us a indicator of how the test performed or whether it has even been executed.
f.e _Automatic Deployment Smoke Test Friday 5th of April 2019 08:07:15 AM_

## Report - TBD

## Integration - TBD

## Administrators of testquality
[Pawel](mailto:erzetpe@gmail.com)  
[Marek](mailto:marek.peszt@pl.abb.com)  
[Przemek](mailto:przemyslaw.dyrda@pl.abb.com