# closed-domain-faq
# My Docker File for Automated build for closed domain FAQ serach interface

Visit [My DockerHub Account](https://hub.docker.com/u/keshv)

To use the application follow below mwntioned steps:

* Pull docker image from docker hub

        docker pull keshv/closed-domain-faq:latest

    ![](https://github.com/solidate/closed-domain-faq/blob/main/screenshots/1.png)

* Create a Data Folder on your pwd

        mkdir Data

    ![](https://github.com/solidate/closed-domain-faq/blob/main/screenshots/2.png)

* Add faq.csv file to Data Folder

    ![](https://github.com/solidate/closed-domain-faq/blob/main/screenshots/3.png)

* Start the container using image and mount the Data folder to the container, map port 80 to 8000

        docker run --mount type=bind,source="$(pwd)/Data",target="$(pwd)" -p 80:8000 --name <add-container-name> keshv/closed-domain-faq

    ![](https://github.com/solidate/closed-domain-faq/blob/main/screenshots/4.png)


## Screenshot

![](https://github.com/solidate/closed-domain-faq/blob/main/screenshots/record.gif)

