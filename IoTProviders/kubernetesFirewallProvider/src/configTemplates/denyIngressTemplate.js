const template = {
    "apiVersion": "networking.k8s.io/v1",
    "kind": "NetworkPolicy",
    "metadata": {
      "name": "default-deny"
    },
    "spec": {
      "podSelector": {
        "matchLabels": {
            "app": "servicename"
        }
      },
      "ingress": [
      ]
    }
  }

  module.exports = template;