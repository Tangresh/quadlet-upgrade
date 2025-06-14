#!/usr/bin/env python3

from podman import PodmanClient
import subprocess

# Provide a URI path for the libpod service.  In libpod, the URI can be a unix
# domain socket(UDS) or TCP.  The TCP connection has not been implemented in this
# package yet.

uri = "unix:///run/user/1000/podman/podman.sock"

def upgrade():
    with PodmanClient(base_url=uri) as client:
        for pod in client.pods.list():
            if pod.attrs.get("Labels").get("quadletName") is not None:
                quadlet_name = pod.attrs.get("Labels").get("quadletName")
            else:
                quadlet_name = pod.name

            print("Checking pod {}, quadlet {}".format(pod.name, quadlet_name))
            newer_images_available = False

            pod_containers = pod.attrs.get("Containers")
            pod_container: dict
            for pod_container in pod_containers:
                container_id = pod_container.get("Id")

                container = client.containers.get(container_id)
                if container.attrs.get("IsInfra"):
                    print("Skipping infra container")
                    continue

                container_image_id = container.attrs.get("Image")
                container_image_name = container.attrs.get("ImageName")

                client.images.pull(container_image_name)
                available_image = client.images.get(container_image_name)
                if available_image.id != container_image_id:
                    print("Newer image available for {}/{}".format(pod.name, container.name))
                    newer_images_available = True

            if newer_images_available:
                answer = input("Restart service {}? [y/N]".format(quadlet_name))
                if answer == "y":
                    subprocess.check_call(["systemctl", "--user", "restart", quadlet_name])

            print()

if __name__ == "__main__":
    upgrade()
