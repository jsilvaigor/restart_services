# Restart Service

This project is intended to restart stopped and/or frozen services from a Rancher stack.
You have to pass 4 environment variables (example bellow) and the name of the stack you want to restart.

    RANCHER_BASE_URL=http://hostancher.com/v2-beta
    RANCHER_ACCESS_KEY=accesskey  
    RANCHER_SECRET_KEY=secretkey  
    RANCHER_ENVIRONMENT=1a5
    
If you don't want to restart some specific service, like a database, you can pass a comma separated list as a environment variable:

    SERVICES_TO_NOT_RESTART=redis,mongodb

You can run from a shell environment  like this

    RANCHER_BASE_URL=http://hostancher.com/v2-beta RANCHER_ACCESS_KEY=accesskey \
    RANCHER_SECRET_KEY=secretkey RANCHER_ENVIRONMENT=1a5 SERVICES_TO_NOT_RESTART=redis \
    python main.py stackName
    
Or run from a docker container passing the environment variables

    docker run -it --rm -e RANCHER_BASE_URL=http://hostancher.com/v2-beta \
    -e RANCHER_ACCESS_KEY=accesskey -e RANCHER_SECRET_KEY=secretkey \
    -e RANCHER_ENVIRONMENT=1a5 -e SERVICES_TO_NOT_RESTART=redis \
    jsilvaigor/restart_service stackName

Or be a more secure person and utilize a `.env` file

     docker run -it --rm --env-file .env jsilvaigor/restart_services stackName
