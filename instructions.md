# Final Project

An exercise to put to practice software development teamwork, subsystem communication, containers, deployment, and CI/CD pipelines.

## Requirements

This is an open-ended exercise for you to show your mastery of software engineering, with some specific requirements:

- Your software must be composed of at least 3 different subsystems
- One of those subsystems must be a MongoDB database - you do not need to create this yourself!
- At least one subsystem must be a custom web application, written in Python using [flask](https://flask.palletsprojects.com/) and hosted with [Digital Ocean](https://m.do.co/c/4d1066078eb0) (this link will give you a free referral credit of $200 to use within 60 days).
- The other subsystem(s) can be anything of your choosing, but code must be primarily written in Python.
- Each custom subsystem's code must reside within its own subdirectory within this "mono-repo".
- Each custom subsystem must be a containerized application, each having their own `Dockerfile`.
- Each custom subsystem must have its own CI/CD pipeline using GitHub Actions, with a separate workflow files for each subsystem. These workflows must be triggered by any code change to the `main` or `master` branch. The workflows must build, test, deliver to DockerHub, and deploy the web app (and any other online subsystems) to Digital Ocean.
- Each custom subsystem must contain unit tests that provide at least 80% code coverage.
- You are welcome to use computing platforms such as Raspberry Pi or other embedded or mobile devices you have available, if they make sense for your project.

## Documentation

Replace the contents of the [README.md](./README.md) file with a beautifully-formatted Markdown file including

- a plain-language **description** of your project, including:
- [badges](https://docs.github.com/en/actions/monitoring-and-troubleshooting-workflows/adding-a-workflow-status-badge) at the top of the `README.md` file showing the result of the latest CI/CD of each subsystem.
- links to the container images for each custom subsystem, hosted on [DockerHub](https://hub.docker.com).
- the names of all teammates as links to their GitHub profiles.
- instructions for how to configure and run all parts of your project for any developer on any platform - these instructions must work!
- instructions for how to import any starter data into the database, if necessary for the system to operate correctly at first.
