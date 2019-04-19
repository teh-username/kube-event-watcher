from functools import partial
import os
import queue
import threading

from kubernetes import client, config, watch

try:
    config.load_incluster_config()
except config.config_exception.ConfigException:
    config.load_kube_config()

namespace = os.environ.get('NAMESPACE', 'default')

kinds_lookup = {
    'pods': {
        'should_watch': os.environ.get('WATCH_PODS', False),
        'stream': partial(client.CoreV1Api().list_namespaced_pod, namespace=namespace)
    },
    'deployments': {
        'should_watch': os.environ.get('WATCH_DEPLOYMENTS', True),
        'stream': partial(client.AppsV1beta2Api().list_namespaced_deployment, namespace=namespace)
    },
    'services': {
        'should_watch': os.environ.get('WATCH_SERVICES', False),
        'stream': partial(client.CoreV1Api().list_namespaced_service, namespace=namespace)
    },
    'configmaps': {
        'should_watch': os.environ.get('WATCH_CONFIGMAPS', False),
        'stream': partial(client.CoreV1Api().list_namespaced_config_map, namespace=namespace)
    },
    'secrets': {
        'should_watch': os.environ.get('WATCH_SECRETS', False),
        'stream': partial(client.CoreV1Api().list_namespaced_secret, namespace=namespace)
    },
    'serviceaccounts': {
        'should_watch': os.environ.get('WATCH_SERVICEACCOUNTS', False),
        'stream': partial(client.CoreV1Api().list_namespaced_service_account, namespace=namespace)
    }
}

def webhook(q):
    while True:
        event = q.get()

        kind = event['object']['kind'].lower()
        namespace = event['object']['metadata']['namespace']
        type = event['type'].lower()
        name = event['object']['metadata']['name']

        print('='*50)
        print(f'A {kind} in namespace {namespace} has been {type}: {name}')
        print('='*50)

def create_watcher(q, w, stream):
    def watcher():
        for event in w.stream(stream):
            q.put(event)
    return watcher


if __name__ == "__main__":
    q = queue.Queue()
    w = watch.Watch()

    for key, values in kinds_lookup.items():
        if values['should_watch']:
            threading.Thread(
                target=create_watcher(q, w, values['stream']),
                daemon=True
            ).start()

    m = threading.Thread(
        target=partial(webhook, q=q),
        daemon=True
    )

    m.start()
    m.join()
