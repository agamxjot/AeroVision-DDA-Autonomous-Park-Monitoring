# 1. Project Overview

## 1.1 Introduction

The DDA Autonomous Park Monitoring System is a drone-assisted monitoring framework designed to support the inspection and maintenance of public parks. The system combines computer vision, geospatial analysis, coverage optimization, and multi-drone mission planning to automate the identification of park conditions and improve inspection efficiency.

The project focuses on monitoring multiple parks through aerial imagery and video, identifying maintenance-related conditions, and generating structured reports that can assist park management authorities.

## 1.2 Problem Statement

Traditional park inspection relies heavily on manual observation and ground-level inspection. This approach can be time-consuming, difficult to scale across multiple parks, and may not provide consistent coverage of large areas.

The proposed system addresses these challenges through:
- Automated detection of park conditions using drone imagery.
- Geospatial division of park areas into inspection nodes.
- Optimized coverage and waypoint planning.
- Multi-drone mission allocation and simulation.
- Automated generation of annotated videos and Excel reports.

## 1.3 Project Objectives

1. Develop a computer vision model to identify park maintenance conditions.
2. Generate optimized inspection points using a geospatial coverage approach.
3. Plan drone routes for systematic park inspection.
4. Support multi-drone deployment through battery-aware mission allocation.
5. Simulate drone movement and verify mission execution.
6. Generate visual and tabular reports for inspection results.

## 1.4 Monitoring Categories

The computer vision model identifies seven categories:

- BROKEN_TREES
- DRY_AREA
- PATHWAYS
- ROOFTOPS
- VEGETATION
- WATERBODY
- WATER_CLOGGING

## 1.5 Project Scope

The framework has been developed for seven park locations:

- Asaf Ali Park
- Lala Hardyal Park
- Rohini Park
- Sanjay Lake
- Smriti Van
- Vasant Udyan
- Vasant Vatika

For each park, the project maintains relevant processing outputs, including detection results, coverage maps, mission-planning results, and analytical reports.

## 1.6 Expected Outcomes

The system aims to provide a repeatable workflow for aerial park inspection, combining automated visual analysis with optimized geographical coverage and structured reporting.