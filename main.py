import requests
from requests.auth import HTTPBasicAuth
import sys
import os

RANCHER_BASE_URL = os.environ.get("RANCHER_BASE_URL", "")
RANCHER_ACCESS_KEY = os.environ.get("RANCHER_ACCESS_KEY", "")
RANCHER_SECRET_KEY = os.environ.get("RANCHER_SECRET_KEY", "")
RANCHER_ENVIRONMENT = os.environ.get("RANCHER_ENVIRONMENT", "")

RANCHER_LIST_STACKS = "{}/projects/{}/projects/{}/stacks".format(RANCHER_BASE_URL, RANCHER_ENVIRONMENT,
                                                                 RANCHER_ENVIRONMENT)
SERVICES_TO_NOT_RESTART = os.environ.get("SERVICES_TO_NOT_RESTART", "").split(",")


def authenticated_get(url):
    print("[*] Getting URL: {}".format(url))
    response = requests.get(url, auth=HTTPBasicAuth(RANCHER_ACCESS_KEY, RANCHER_SECRET_KEY))
    print("[*] Response: {} {}".format(response.status_code, response.headers))
    return response.json()


def authenticated_post(url, body):
    print("[*] Posting to URL: {}".format(url))
    response = requests.post(url, body, auth=HTTPBasicAuth(RANCHER_ACCESS_KEY, RANCHER_SECRET_KEY))
    print("[*] Response: {} {}".format(response.status_code, response.headers))
    return response.json()


def get_all_stacks():
    print("[*] Getting all stacks")
    stacks = authenticated_get(RANCHER_LIST_STACKS)
    print("[*] Stacks: {}".format(len(stacks)))
    return stacks


def get_all_service_links(stack_name):
    stacks = get_all_stacks()
    print("[*] Finding wanted stack")
    wanted_stack = next(x for x in stacks["data"] if x["name"] == stack_name)
    print("[*] Found stack: {}".format(wanted_stack.get("name", "")))
    return authenticated_get(wanted_stack["links"]["services"])


def get_service(service):
    print("[*] Getting service link for: {}".format(service.get("name", "")))
    return authenticated_get(service["links"]["self"])


def get_restart_urls(stack_name):
    print("[*] Finding services for stack: {}".format(stack_name))
    stack_services = get_all_service_links(stack_name)
    print("[*] Services found: {}".format(len(stack_services)))
    services = list(get_service(x) for x in stack_services["data"])
    return list(x.get("actions", {}).get("restart", "") or x.get("actions", {}).get("activate", "") for x in services if
                x["state"] == "inactive" or x["name"] not in SERVICES_TO_NOT_RESTART)


def restart_service(url):
    payload = {"rollingRestartStrategy": {"batchSize": 1, "intervalMillis": 2000}}
    print("[*] Restarting service with payload: {} {}".format(url, payload))
    return authenticated_post(url, payload)


if __name__ == "__main__":
    print(sys.argv)
    urls = get_restart_urls(sys.argv[1])
    print("[*] URLS to restart: {}".format(urls))
    restarted = list(restart_service(x) for x in urls)
    print("[*] Restarted {} services".format(len(restarted)))
