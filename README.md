# kube-event-watcher
// TBD

## Installation

`kubectl apply -f <(helm template chart/)`

![sample](./docs/sample.png)

## Building from source

```
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python app/main.py
```

## Usage
// TBD

## Configuration

| **Name**                      | **Description**                                                        | **Optional** |
| :---------------------------- | :--------------------------------------------------------------------- | :----------- |
| `NAMESPACE`                   | Target namespace to watch. Defaults to `default`.                      | Yes          |
| `WATCH_PODS`                  | Toggle to whether watch pod changes. Defaults to `False`.              | Yes          |
| `WATCH_DEPLOYMENTS`           | Toggle to whether watch deployment changes. Defaults to `True`.        | Yes          |
| `WATCH_SERVICES`              | Toggle to whether watch service changes. Defaults to `False`.          | Yes          |
| `WATCH_CONFIGMAPS`            | Toggle to whether watch configmap changes. Defaults to `False`.        | Yes          |
| `WATCH_SECRETS`               | Toggle to whether watch secret changes. Defaults to `False`.           | Yes          |
| `WATCH_SERVICEACCOUNTS`       | Toggle to whether watch serviceaccount changes. Defaults to `False`.   | Yes          |
