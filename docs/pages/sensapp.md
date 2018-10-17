---
layout: default
---

# Amplifying Microservice

We describe below how to use CAMP to amplify an integration test of a
microservice architecture. Initially, SensApp comes with a fixed
deployment described into a docker-compose file and will see how CAMP
can "mutate" this description and yields new ones.


## The SensApp Architecture

SensApp is a prototypical microservice applications. It is designed to
store reliably data coming from multiple IoT sensors. Sensapp follows
the microservice architecture and its logic is broken down into three
services, namely the receiver, the storage, and the registry.

 * The *registry* stores the metadata associated with sensors, such as
   their identifier, a short description and the unit of the
   measurement.
   
 * The *receiver* receives data directly from the sensors. It simply
   accepts sensors' data and places it in a message queue for later
   storage.
   
 * The *storage* picks up data from the message queue, check whether
   the sensor that pushed this data is properly registered, and
   eventually persists this data into a database specialized for
   time-series data.
      
The schema below illustrates the architecture of the system.

SensApp also includes a *smoke test* service (so called Tester) that
simulates a few sensors pushing data and later check that all data are
properly stored. 

