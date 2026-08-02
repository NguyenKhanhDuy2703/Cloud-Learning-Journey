# ☸️ Kubernetes Pod Deep Dive — Devopscube Guide

> **Nguồn tham khảo:** [devopscube.com/kubernetes-pod](https://devopscube.com/kubernetes-pod/)

![Kubernetes Pod Header](./images/kubernetes-pod/hero-kubernetes-pod.png)

In this guide, I have coveredKubernetespod core concepts in detail using practical examples and use cases.

So if you want to understand,

1. Understand core Kubernetes Pod concepts
2. Learn the anatomy of a Pod
3. How to create a pod step by step
4. Ways to access and troubleshoot Pods
5. Understand Pod associated objects

This guide is for you.

The aim of this guide is tomake you understand the building blocksof the pod and do a practical implementation of deploying a pod and accessing the application running on it.

Also, there are many concepts associated with a Pod object. So I have given all the information andconcepts related to a Podto further build on the basics you have learned.


---

## What is a Kubernetes Pod?

Before getting into Kubernetes Pod concepts, let's understandcontainers.

A container as we all know, is aself-contained environmentwhere we package applications and their dependencies. Typically, a container runs a single process (Although there are ways to run multiple processes). Each container gets an IP address and can attach volumes and control CPU and memory resources, among other things. All these happen via the concepts of namespaces and control groups.

Kubernetes is a container orchestration system for deploying, scaling, and managing containerized applications, and it has its own way of running containers.We call it a pod. A pod is thesmallest deployable unit in Kubernetesthat represents a single instance of an application.

For example, if you want to run the Nginx application, you run it in a pod.

So how does it differ from a container?

A container is a single unit. However, a pod can contain more than one container. You can think ofpods as a box that can hold one or more containerstogether.

Pod provides a higher level of abstraction that allows you to manage multiple containers as a single unit. Here instead of each container getting an IP address, thepod gets a single unique IP addressand containers running inside the pod use localhost to connect to each other ondifferent ports.


![Kubernetes pod](./images/kubernetes-pod/multi-container-pod.gif)

It means containers inside the Kubernetes pod share the following

1. Network namespace- All containers inside a pod communicate via localhost.
2. IPC namespace: All containers use a shared interprocess communication namespace.
3. UTS namespace: All containers share the same hostname.

What is not shared between containers inside a pod?

1. By default, thePID namespaceis not shared however kubernetes provide options to enable process sharing between containers inside the pod usingshareProcessNamespaceOption.
2. The mount namespace is not shared between containers. Each container has its own private filesystem and directories. However, thepod mount volumesare shared between containers.

In a nutshell, here is what you should know about a pod:

1. Pods are the smallest deployable units in Kubernetes.
2. Pods are ephemeral in nature; they can be created, deleted, and updated.
3. A pod can have more than one container; there is no limit to how many containers you can run inside a pod.
4. Each pod gets a unique IP address.
5. Pods communicate with each other using the IP address.
6. Containers inside a pod connect using localhost on different ports.
7. Containers running inside a pod should have different port numbers to avoid port clashes.
8. You can set CPU and memory resources for each container running inside the pod.
9. Containers inside a pod can share the same volume mount if you mount the same volume into each container.
10. All the containers inside a pod are scheduled on the same node; It cannot span multiple nodes.
11. If there is more than one container, during the pod startup, there isno guaranteed start orderfor regular containers. Whereas the init containers inside the pod run in sequence.


---

## Pod YAML (Object Definition)

Now that we have a basic understanding of a Pod, let's have a look at how we define a Pod. Pod is a nativeKubernetes Objectand if you want to create a pod, you need to declare the pod requirements in YAML format. You can also create a pod using the kubectl imperative command. Which we will see in a later topic.

Here is an example Pod YAML that creates an Nginx web server pod. This YAML is nothing but a declarative desired state of a pod.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server-pod
  labels:
    app: web-server
    environment: production
  annotations:
    description: This pod runs the web server
spec:
  containers:
  - name: web-server
    image: nginx:latest
    ports:
    - containerPort: 80
```

Let's understand this pod YAML. Once you understand the basic YAML it will be easier for you to work with pods and associated objects likedeployment,daemonset, statefulset, etc.

As we discussed in theKubernetes Objectblog, every Kubernetes object has some common set of parameters. The values change as per the kind of object we are creating.

Let's take a look at the Kubernetes pod object.

We have now looked at a basic Pod YAML manifest. It's important to note that thismanifest supports many parameters. We will gradually explore these additional parameters with a hands-on, practical approach.

Now that we have some basic understanding of a Pod, let's create a pod.


---

## Creating Pod (Practical Examples)

You can create a pod in two ways

1. Using the kubectl imperative command:Primarily used for learning and testing purposes. The imperative command comes with its own limitations.
2. Declarative approach: Using YAML manifest. When working on projects, the YAML manifest is used to deploy pods.

Let's look at both options. We are going to create an NGINX pod with the following

1. The name of the pod is web-server-pod
2. It should have labelsapp: web-serverandenvironment: production
3. Add an annotation to describe the pod.
4. Usenginx:1.14.2container image.
5. Expose Container port80.


### Method 1: Create Pod Using Kubectl Command

For the discussed pod requirements, here is the kubectl command.

```bash
kubectl run web-server-pod \
  --image=nginx:1.14.2 \
  --restart=Never \
  --port=80 \
  --labels=app=web-server,environment=production \
  --annotations description="This pod runs the web server"
```

Here the pod gets deployed in the default namespace. You can get the status of the deployed pod kubectl.

```bash
kubectl get pods
```

Once the pod is deployed you will see the podRunningstatus as shown below. In our example, we have only one container inside the pod. So it shows1/1ready and running.


![listing kubernetes pods using kubectl](./images/kubernetes-pod/kubectl-get-pods.png)


### Describe a Pod

If you want to know all thedetails of the running pod, you can describe the pod using kubectl.

```bash
kubectl describe pod web-server-pod
```

In the following output, you can see all the details about the pod. Its IP address, namespace, container details, QoS class, etc.


![Kubernetes pod details using describe command](./images/kubernetes-pod/kubectl-describe-pod.png)

_*Hình: Click to view in HD*_

The following image shows the complete pod anotomy.


![Kubernetes Pod Anatomy](./images/kubernetes-pod/kubernetes-pod-anatomy.png)

Now let's delete the pod using the following command.

```bash
kubectl delete pod web-server-pod
```


### Method 1: Create Pod Using Declarative YAML

When working on real projects, you will have to create pods mostly through a declarative approach.

Let's see how we can create a pod using the YAML manifest.

Create a file namednginx.yamlwith the following contents.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server-pod
  labels:
    app: web-server
    environment: production
  annotations:
    description: This pod runs the web server
spec:
  containers:
  - name: web-server
    image: nginx:1.14.2
    ports:
    - containerPort: 80
```

Now, to deploy the manifest, you need to execute the following kubectl command with the file name.

```bash
kubectl create -f nginx.yaml
```

Should we remember each parameter to create the YAML? No. You can use the--dry-run flagto create the YAML file.

Here is an example.

```bash
kubectl run nginx-pod --image=nginx:1.14.2 --dry-run=client -o yaml
```

You can save the YAML output by redirecting the dry-run output to a file.

```bash
kubectl run nginx-pod --image=nginx:1.14.2 --dry-run=client -o yaml > nginx-pod.yaml
```


---

## Access Application Running In a Pod

Now we have a running pod with the Nginx web server. The whole idea is to deploy and access the application running inside the pod.

Kubectl offers aport-forwardcommand to access running pods in the Kubernetes cluster from the local workstation.

We have a running pod namedweb-server-pod. Let's access it via the port-forward command.

```bash
kubectl port-forward pod/web-server-pod 8080:80
```

You should see an output as shown below.


![kubectl port forward to access pod in local system](./images/kubernetes-pod/kubectl-port-forward.png)

Now if you go to the browser and accesshttp://localhost:8080, you should see the Nginx homepage as shown below. The webpage is served by our Nginx web server pod.


![kubectl port forward to access nginx pod](./images/kubernetes-pod/kubectl-port-forward-nginx.png)

Now you can disconnect port forwarding bypressing CTRL+C.

Here is what happens when you run kubectl port-forward

1. Kubectl binds the specified port in your local system. In our case, it's8080.
2. It then communicated with the Kubernetes cluster API to establish a tunnel (a single HTTP connection) to the required node and then to the specified pod and container port, ie 80.


---

## Access Pod Shell

We have learned how to access the application running inside the pod.

Now what if you want to get access to the pod shell?

There are many use cases where you need terminal access to the pod. One main use case is debugging andpod troubleshooting.

Here is wherekubectl execcommand comes in handy.

You can access the shell of web-server-pod using the following command.

```bash
kubectl exec -it web-server-pod -- /bin/sh
```

In the following output, I am executingwhoamicommand inside the pod.


![kubectl exect to pod shell](./images/kubernetes-pod/kubectl-exec-pod.png)


---

## Pod Lifecycle

Another important concept you should know about a pod is its lifecycle.

A pod is typically managed by a controller likeReplicaSetController, Deployment controller, etc. When you create a single pod using YAML, it is not managed by any controller. In both cases, a pod goes through different lifecycle phases.

Following are the pod lifecycle phases.

1. Pending: It means the pod creation request is successful, however, the scheduling is in process. For example, it is in the process of downloading the container image.
2. Running:The pod is successfully running and operating as expected. For example, the pod is service client requests.
3. Succeeded:All containers inside the pod have been successfully terminated. For example, the successful completion of a CronJob object.
4. Failed:All pods are terminated but at least one container has terminated in failure. For example, the application running inside the pod is unable to start due to a config issue and the container exits with a non-zero exit code.
5. Unknown:Unknown status of the pod. For example, the cluster is unable to monitor the status of the pod.

If you describe the pod, you can view the phase of the pod. Here is an example.


![pod lifecyle phases - pending pod](./images/kubernetes-pod/pod-lifecycle-phases.png)

If you want to know more information, check out the detailed blog onpod lifecycle.


---

## Pod Features

We have deployed a simple Nginx pod with very minimal configurations. However, a pod had a lot offeaturesfor resource management, configuration, secrets, availability, security, etc.

If you are a beginner, learning all these concepts in one go will be overkill. It makes more sense to learn all these concepts whenworking with pod-related objectslike Deployment with practical use cases.

Also, you need to understand every feature in detail with a practical use case.

Following are the key features related to the pod.

1. Resource Requests and Limits:Pod CPU/Memory Allocation
2. Labels: key-value pairs attached to pods to categorize resources.
3. Selectors:To group resources based on labels.
4. Liveness, Readiness, and Startup Probes:Container Health Checks
5. ConfigMaps: For Config Management
6. Secrets: For Secret management
7. Volumes: Persistent Data Storage
8. Init Containers:Containers that run before main containers.
9. Ephemeral Containers:Temporary containers added to the pod for debugging or troubleshooting purposes.
10. Service Account:To restrict access to Kubernetes objects & resources.
11. SecurityContext:Host permissions and Privileges.
12. Affinity and Anti-Affinity Rules: Pod Placement Control across nodes
13. Pod Preemption & Priority:Setting priorities for pod scheduling & eviction.
14. Pod Disruption Budget: The minimum number of pod replicas that need to be running during a voluntary disruption.
15. Container Life Cycle Hooks:Executing custom scripts based on the pod’s lifecycle phase changes.
16. dnsConfig:For custom DNS settings
17. dnsPolicy:Defines how DNS resolution works inside the Pod.


---

## Comprehensive Pod YAML Configuration

If you add the pod features I listed above, you will get a comprehensive pod YAML configuration as given below. Also, these options will be used along with objects like Deployment, Statefulset, etc.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: web-server-pod
spec:
  initContainers:
  - name: init-myservice
    image: busybox:1.28
    command: ['sh', '-c', 'echo "Init container started!"']
  containers:
  - name: web-server
    image: nginx:latest
    ports:
    - containerPort: 80
    volumeMounts:
    - name: shared-data
      mountPath: /usr/share/nginx/html
    - name: secret-volume
      mountPath: /etc/my-secret
    - name: configmap-volume
      mountPath: /etc/config
    securityContext:
      capabilities:
        add: ["NET_ADMIN", "SYS_TIME"]
    resources:
      requests:
        memory: "64Mi"
        cpu: "250m"
      limits:
        memory: "128Mi"
        cpu: "500m"
    readinessProbe:
      httpGet:
        path: /index.html
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 5
    livenessProbe:
      httpGet:
        path: /index.html
        port: 80
      initialDelaySeconds: 15
      periodSeconds: 20
    startupProbe:
      httpGet:
        path: /index.html
        port: 80
      failureThreshold: 30
      periodSeconds: 10
    lifecycle:
      postStart:
        exec:
          command: ["/bin/sh", "-c", "echo 'PostStart'"]
      preStop:
        exec:
          command: ["/bin/sh", "-c", "echo 'PreStop'"]
  serviceAccountName: nginx-service-account   
  securityContext:                        
    runAsUser: 1000
    runAsGroup: 3000
    fsGroup: 2000
  shareProcessNamespace: true
  volumes:
  - name: shared-data
    emptyDir: {}
  - name: secret-volume
    secret:
      secretName: nginx-secret
  - name: configmap-volume
    configMap:
      name: nginx-configmap
```


---

## Pod Associated Objects

When it comes to running applications on Kubernetes, we don't run an individual pod. Because Kubernetes is all aboutscaling and maintainingthe availability of pods.

So if you run a single pod, it will be asingle point of failure. Because the Pods themselves cannot be directly scaled.

As we discussed in theKubernetes Architecture, we need controllers like Replicaset to ensure the desired number of pods are running at all the time.

Kubernetes has different types of objects associated with pods for different use cases.


![Kubernetes objects that are associated with pod](./images/kubernetes-pod/pod-associated-objects.gif)

_*Hình: Click to view in HD*_

The following are important pod-associated objects.

1. Replicaset: To maintain a stable set of Pods replicas running at any given time.
2. Deployment: To run stateless applications like web servers, APIs, etc
3. StatefulSets: To run stateful applications like distributed databases.
4. Daemonsets:To run agents on all the Kubernetes nodes.
5. Jobs: For batch processing
6. CronJobs:Scheduled Jobs


---

## Conclusion

In this guide, we looked at all the core concepts of a Kubernetes Pod. As I mentioned in the introduction, a pod has a lot of features when it comes tokubernetes productionlevel implementation.

In the next series of blogs, we will look at each pod feature and associated objects in detail.

Also, look at theKubernetes tutorials, where I have listed comprehensive guides covering many concepts practically.
