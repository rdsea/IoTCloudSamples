var template = {
    "apiVersion": "extensions/v1beta1",
    "kind": "Deployment",
    "metadata": {
      "name": "sensor"
    },
    "spec": {
      "replicas": 1,
      "template": {
        "metadata": {
          "labels": {
            "app": "sensor",
            "role": "test",
            "tier": "bts"
          }
        },
        "spec": {
          "volumes":[],
          "containers": [
            {
              "name": "sensor",
              "image": "rdsea/sensor",
              "command":["java"],
              "args": ["-jar", "sdsensor-0.0.1-SNAPSHOT-jar-with-dependencies.jar", "config/config.json", "data.csv", "test"],
              "volumeMounts":[],
              "resources": {
                "requests": {
                  "cpu": "100m",
                  "memory": "100Mi"
                }
              }
            }
          ]
        }
      }
    }
  }

  export default template;