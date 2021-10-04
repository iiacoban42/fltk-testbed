cd charts

helm install extractor ./extractor -f fltk-values.yaml --namespace test

helm uninstall -n test orchestrator
helm install orchestrator ./orchestrator --namespace test -f fltk-values.yaml

sleep 20

export POD_NAME=$(kubectl get pods -n test -l "app.kubernetes.io/name=fltk.extractor" -o jsonpath="{.items[0].metadata.name}")

kubectl -n test port-forward $POD_NAME 6006:6006

cd ..
