# Manganace - Manipulate GAN Face

The project is made by Mantas Makelis for bachelor's thesis of Artificial Intelligence at Radboud University.
The key idea of the project was to establish a base project with User Interface (UI) to allow a user to explore the latent space of the Generative Adversarial Network (GAN).
The [GAN implementation](https://github.com/NVlabs/stylegan2) is provided by NVidia and this project utilizes the pretrained [FFHQ model](https://nvlabs-fi-cdn.nvidia.com/stylegan2/networks/stylegan2-ffhq-config-f.pkl).

The main established requirement of the project was to make a web-based UI which could be distributed to users using a containerization technology e.g. Docker and/or to be able to host it on a server.
Another requirement was to make it easily expandable, hence the approach to the architecture was an important aspect. 

The project contains two essential parts i.e. backend and frontend.
Backend is written in Python while the frontend is utilizing a Javascript framework Vue version 3 with utilization of the (at that moment) brand new Composition API.
It is worth mentioning that the backend is using an SQL database to keep track of everything, at the moment of writing it is SQLite but any SQL database can easily be configured.

Both projects, backend and frontend, are connected via HTTP calls.
Namely, the backend is hosting API endpoints and is encapsulating the GAN model while the frontend is interacting with it by calling the hosted API and getting and sending the data through it.

As of December 2020, the following **main** usability features are implemented:

1. Generate an image from a seed.
2. Apply emotion vectors to an image/seed (mixing is allowed).
3. Memorize and track all generated images.
4. Create custom collections of images.
5. Tag images for easy tracking/searching in collections.
6. Create separated image generation sessions.
7. Create research sessions which generates an array of images using preexisting hand-selected good seeds (looking straight with neutral emotion)
Generation contains the possibility to configure the session with desirable amount of images, overlapping image count, gender equalization, and arbitrary emotion vector steps amount.
This action, for each seed and each emotion vector (cartesian product), generates images by applying calculated emotion vector steps according to the selected amount of these steps.
Hence, it generates _[image_count * vector_count * vector_steps]_ amount of images.
8. Execute a research session where a participant is asked to enter a minimal demographic information, and then for each seed and vector combination is shown an image with a slider, and vector effect name i.e happy, sad, etc.
By moving the slider participant applies the vector either weakly (left) or strongly (right) and sees the image changing.
The goal is to place the slider where the participant deems to be the natural looking emotion on this particular seed.
9. Inspect the results of separate research sessions.
This includes the bar chart for each vector selection and chosen images with tags so all images of the same vector could be filtered easily.
10. Overall results of research sessions which includes only the bar chart for each vector.

For deeper dive into the tech-stack and architectural decisions please check out the following:

[Backend documentation](backend/README.md)

[Frontend documentation](frontend/README.md)

In case *you* have any questions or are continuing the work on this project and require assistance, please do not hesitate to contact me via [my student email](mailto:m.makelis@student.ru.nl).