# Automatic Test Sample Site
## Purpose
A site you can use to try out things with Automated Test frameworks.

## Setup & start test site - directly on your machine
After `git clone` run this...
```
cd automatic-test-sample-site
composer install
composer dump-autoload -o
```
Composer lock file is optimized for PHP 8.2

To start site...
```
cd automatic-test-sample-site
php -S localhost:8000
```
then open in browser: `http://localhost:8000`


## Setup & start test site - Docker, locally
After `git clone` and navigating inside `automatic-test-sample-site` directory build the container...
```
docker build --no-cache -t sample-site .
```

To start container...
```
docker run --name sample-site -p 8000:8000 -it sample-site:latest
```
then open in browser: `http://localhost:8000`

## Build & Push to Gitlab Container Registry

PART 1: Copy repo here into a GitLab repo

PART 2: Create container image of repo and push it to the GitLab Container Registry with this `.gitlab-ci.yml`:
```
image: docker:latest

services:
  - docker:dind

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: ""

stages:
  - build

build_image:
  stage: build
  before_script:
    - docker login -u "$CI_REGISTRY_USER" -p "$CI_JOB_TOKEN" "$CI_REGISTRY"
  script:
    - docker build -t $CI_REGISTRY_IMAGE:latest .
    - docker tag $CI_REGISTRY_IMAGE:latest $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_NAME
    - docker push $CI_REGISTRY_IMAGE:latest
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_REF_NAME
```

PART 3: Define pipeline jobs that start the test site container, followed by the automated UI tests.

See example here: https://github.com/andreasneuber/docker-based-e2e-tests/blob/master/.gitlab-ci.yml

Additional references:
- https://www.youtube.com/watch?v=ZJZGJTM23z0
- https://www.youtube.com/watch?v=fymJsLIwrFU


## Development - Add new controller and view - steps
1. Make sure you are in the root dir of the framework
2. Then run these console commands

```
// Create a new controller
php bin/console create:controller <name>

// Create a new view
php bin/console create:view <name>
```
3. In new controller file adjust the name of template - in method `renderView`
4. The new page can now be called via `index.php?action=<name>` (name = basically controller class name without `Controller`)


## PHP version
Goal is to keep things compatible with the latest released stable major PHP version.

## API
Site has also an API (very simple one and works only without Docker). You can use:
- `http://localhost:8000/api/allusers`
- `http://localhost:8000/api/user/1` or `http://localhost:8000/api/user/2`

### Docu
- https://medium.com/@miladev95/how-to-make-crud-rest-api-in-php-with-mysql-5063ae4cc89
- https://www.a2hosting.com/kb/developer-corner/sqlite/connect-to-sqlite-using-php/
- https://stackoverflow.com/questions/22049212/copying-files-from-docker-container-to-host
