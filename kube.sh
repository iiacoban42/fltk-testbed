export POD_NAME=$(kubectl get pods -n default -l" app.kubernetes.io/name=kubernetes-dashboard,app.kubernetes.io/instance=kubernetes-dashboard" -o jsonpath="{.items[0].metadata.name}")

kubectl -n default port-forward $POD_NAME 8443:8443
