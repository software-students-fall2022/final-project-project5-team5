[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9565447&assignment_repo_type=AssignmentRepo)
<br />
![ML Tests](https://github.com/software-students-fall2022/final-project-project5-team5/actions/workflows/ml-tests.yaml/badge.svg)
![Web App Tests](https://github.com/software-students-fall2022/final-project-project5-team5/actions/workflows/web-app-tests.yaml/badge.svg)
![Docker Hub CD](https://github.com/software-students-fall2022/final-project-project5-team5/workflows/ci/badge.svg)

# Final Project
## Project Description

Our app has three subsystems:

**Machine Learning Client:** Allows the user to apply one image's style to another image.

**Web App:** Displays the result images along with the content and style images used.

**MongoDB Database:** Stores all the images.

Content and style images are uploaded to the Machine Learning client and converted into one resultant image. For this, Tensorflow's ML package is used. The Web App works as a gallery of all images created as well as content and style images used for the resultant images.


## Product Vision Statement
Simple image processing web app that applies style of one image onto another.


## Running the Project
1. Navigate to the root folder of this project, then run:
   ```
   docker compose up
   ```
   
2. The ML client (if run by Docker) will run at `127.0.0.1:3000`. The web-app will run at `127.0.0.1:4000`. A database container will also be created.
   
3. In the ML client, you can take upload the images or provide an URL of images. After you submit, the machine-learning algorithm will run for 2~3 seconds, show the result image and also upload it to the database.

4. After you have created a few images in the ML client, you can view results in the web-app by going to `127.0.0.1:4000`.

5. URL examples for images:
      - https://jpeg.org/images/jpeg-home.jpg
      - https://fileinfo.com/img/ss/xl/jpeg_43.png


## Digital Ocean

Photo Gallery for Transformation Process - [Link](https://transformationprocess-ohmxo.ondigitalocean.app/zackdan-project-5-team-5-deploy)

Machine Learning Client - [Link](https://transformationprocess-ohmxo.ondigitalocean.app/)


## Docker Hub

Docker Hub Image - [Link](https://hub.docker.com/repository/docker/zackdan/project5-team5-deploy)


## Team Members

-Amaan Khwaja ([Amaan Khwaja](https://github.com/Amaanmkhwaja))

-Manny Soto Ruiz ([MannySotoRuiz](https://github.com/MannySotoRuiz))

-Kedan Zha ([Kedan Zha](https://github.com/Zackdan0227))

-Wuji Cao ([Wuji Cao](https://github.com/cwj2099))

-Kevin Gong ([Kevin Gong](https://github.com/kxg202))

-Sagynbek Talgatuly ([Sagynbek Talgatuly](https://github.com/sagynbek001))
