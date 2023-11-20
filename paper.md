---
title: 'An open source video annotation tool'
tags:
  - Python
  - OpenCV
  - GUI
  - Tkinter
  - Video annotation
authors:
  - name: Oussama Jlassi
    corresponding: true
    affiliation: 1
  - name: Philippe C. Dixon
    orcid: 0000-0003-3581-7259
    affiliation: 2
affiliations:
 - name: Department of Computer Science and Operations Research, Université de Montréal, Montréal, Québec, Canada
   index: 1
 - name: Department of Kinesiology and Physical Activity, McGill University, Montreal, Québec, Canada
   index: 2
date: 20 November 2023
bibliography: paper.bib

# Summary

The manual annotation and labelling of specific moments (events) within a video file
is a crucial step in several data processing pipelines, including the creation of 
machine learning training datasets. The software presented herein [@software] is developed 
using the Python programming language (v3.11) and generates comma separated files 
containing event names and timing (frame number and absolute time) from MP4 video files. 
Whether used in academic research or other multimedia-related fields, this tool allows 
users to efficiently and reliably annotate event data.

# Statement of need

In the landscape of open-source tools, there exists a notable absence of readily available
software solely dedicated to labelling key moments within videos. A related tool, entitled 
`MaD GUI` [@madgui], provides graphical annotation and computational analysis of time 
series data; however, it is difficult to annotate specific class events from a video. 
`MaD GUI` offers a wide range of features but lacks the simplicity and straightforwardness 
of our tool which provides a user-friendly environment for marking key moments within 
video sequences. Other tools, which (a) focus on the annotation of entire images or sections
of images, such as `labellmg` [@labelimg] or (b) are commercially available such as 
`Encord` [@encord] are not reviewed here as they do not address the stated need or are not
open-source.  

# Content

This software incorporates a multitude of features tailored to streamline the annotation 
process. It harnesses the capabilities of Python libraries such as `OpenCV` [@opencv] for 
video manipulation and `tkinter` [@tkinter] for the user interface. Users are provided with 
functionalities allowing video playback, frame navigation, skip options, speed adjustments, and 
the ability to add custom annotations to specified moments. The graphical user interface offers 
a straightforward design, rendering it accessible to users with varying levels of technical expertise. 

# Impact

By enabling users to label and categorize significant moments within video content 
effortlessly, the tool speeds up data creation, analysis, and interpretation. Its simplicity and 
efficiency significantly reduce the time and effort required for annotating videos. 

# Ongoing research using this software

This software constitutes an integral component of our ongoing research project which is focused on
human movement analysis, wherein its application is pivotal for the manual annotation of video footage. 
This annotation process is integral to a comprehensive study involving participants navigating diverse 
terrain surfaces while equipped with Inertial Measurement Unit (IMU) sensors. The primary objective 
is to synchronize the acquired sensor data with precise segments of the participants' walking on each 
distinct surface. The resulting synchronized dataset will serve as a foundational resource for the 
subsequent development and training of machine learning models. These models, once established, are 
anticipated to predict the different walking surfaces. 

# Future Work 

Looking ahead, potential enhancements for the tool could include the integration of a slider within 
the video player, offering users a more intuitive and fine-grained control over frame selection. 
Additionally, optimizing the software's performance through the implementation of threading mechanisms 
could significantly improve its speed and responsiveness. 

# Acknowledgements  

PCD acknowledges support from the fonds de recherche Québec Santé (FRQS) research scholar award 
(Junior 1) and funding from the Natural Sciences and Engineering Research Council of Canada (NSERC) 
discovery grant program (RGPIN-2022-04217).

# References