DOCKER_BUILDKIT=1 docker build . --tag gcr.io/focal-shape-325414/fltk
docker push gcr.io/focal-shape-325414/fltk
cd charts
helm uninstall -n test orchestrator
helm install orchestrator ./orchestrator --namespace test -f fltk-values.yaml
cd ..
