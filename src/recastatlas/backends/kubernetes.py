
import json

class KubernetesBackend:
    def submit(self, name, spec):
        workflow = {
            "apiVersion": "yadage.github.io/v1",
            "kind": "Workflow",
            "metadata": {"name": name},
            "spec": spec,
        }
        from kubernetes import client as k8sclient
        from kubernetes import config as k8sconfig

        k8sconfig.load_kube_config()
        _, rc, _ = k8sclient.ApiClient().call_api(
            "/apis/yadage.github.io/v1/namespaces/default/workflows",
            "POST",
            body=workflow,
        )
        return rc

    def check_workflow(self, name):
        from kubernetes import client as k8sclient
        from kubernetes import config as k8sconfig

        k8sconfig.load_kube_config()
        a, rc, d = k8sclient.ApiClient().call_api(
            "/apis/yadage.github.io/v1/namespaces/default/workflows/{}".format(name),
            "GET",
            _preload_content=False,
        )
        try:
            status = json.loads(a.read())["status"]["workflow"]
        except:
            return {"status": "UNKNOWN"}

        if status.get("succeeded") == 1:
            return {"status": "SUCCEEDED"}
        if status.get("active") == 1:
            return {"status": "INPROGRESS"}
        if status.get("failed") == 1:
            return {"status": "FAILED"}
        return {"status": "UNKNOWN"}

    def check_backend(self):
        try:
            from kubernetes import client as k8sclient
            from kubernetes import config as k8sconfig

            k8sconfig.load_kube_config()
            _, rc, _ = k8sclient.ApiClient().call_api(
                "/apis/yadage.github.io/v1/namespaces/default/workflows", "GET"
            )
            return rc == 200
        except ImportError:
            pass
        except k8sclient.rest.ApiException:
            pass
        return False        