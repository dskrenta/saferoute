#!/bin/bash

curl 'https://maps.googleapis.com/maps/api/directions/json?origin=40.763483,-73.9672732&destination=40.7706274,-73.9809601&alternatives=true&avoid=highways&mode=walking&key=AIzaSyAs4DpgjVRXUMRvj3oTxdXHSaB2T0O17wM' > result.json
