# Golden set review

For each question below:

1. Read the **question**: would a real user ask this? Is it clear and about Kubernetes v1.33?
2. Read the **documentation excerpts**: do they really answer the question? Is an obviously
   better section missing?
3. Read the **reference answer**: is it correct *according to the excerpts*?
4. Tick **exactly one** box (replace `[ ]` with `[x]`). If you pick *Needs changes*, write what
   to change under **Notes**.

**Out-of-scope questions** are tests that the system *refuses* to answer. If the question really
is outside the Kubernetes docs, tick **Correct as written** (it stays in the set as a refusal
test). Tick **Reject** only if it should be removed from the set.

When done, run: `uv run driftrag-golden apply --reviewer "Your Name"`

---

### `resource-limits`

**Question** (en, task): How do I cap the CPU and memory a container is allowed to use?

**Reference answer:** Set `resources.limits.cpu` and `resources.limits.memory` on the container. CPU use above the limit is throttled; a container that exceeds its memory limit can be OOM-killed. `resources.requests` are what the scheduler uses to pick a node.

**Relevant documentation:**
- `concepts/configuration/manage-resources-containers.md`, section: *Resource Management for Pods and Containers > Requests and limits*
  > [Resource Management for Pods and Containers > Requests and limits]
  > If the node where a Pod is running has enough of a resource available, it's possible (and
  > allowed) for a container to use more resource than its `request` for that resource specifies.
  > For example, if you set a `memory` request of 256 MiB for a container, and that container is in
  > a Pod scheduled to a Node with 8GiB of memory and no other Pods, then the container can try to use
  > more RAM.
  > Limits are a different story. Both `cpu` and `memory` limits are applied by the kubelet (and
  > container runtime),
  > and are ultimately enforced by the kernel. On Linux nodes, the Linux kernel
  > enforces limits with
  > cgroups.
  > The behavior of `cpu` and `memory` limit enforcement is slightly different.
  > `cpu` limits are enforced by CPU throttling. When a container approaches
  > its `cpu` limit, the kernel will restrict access to the CPU corresponding to the
  > container's limit. Thus, a `cpu` limit is a hard limit the kernel enforces.
  > Containers may not use more CPU than is specified in their `cpu` limit.
  > `memory` limits are enforced by the kernel with out of memory (OOM) kills. When
  > a container uses more than its `memory` limit, the kernel may terminate it. However,
  > terminations only happen when the kernel detects memory pressure. Thus, a
  > container that over allocates memory may not be immediately killed. This means
  > `memory` limits are enforced reactively. A container may use more memory than
  > its `memory` limit, but if it does, it may get killed.
  > There is an alpha feature `MemoryQoS` which attempts to add more preemptive
  > limit enforcement for memory (as opposed to reactive enforcement by the OOM
  > killer). However, this effort is
  > stalled
  > due to a potential livelock situation a memory hungry can cause.
  > If you specify a limit for a resource, but do not specify any request, and no admission-time
  > mechanism has applied a default request for that resource, then Kubernetes copies the limit
  > you specified and uses it as the requested value for the resource.
- `concepts/configuration/manage-resources-containers.md`, section: *Resource Management for Pods and Containers > Container resources example*
  > [Resource Management for Pods and Containers > Container resources example {#example-1}]
  > The following Pod has two containers. Both containers are defined with a request for
  > 0.25 CPU
  > and 64MiB (2<sup>26</sup> bytes) of memory. Each container has a limit of 0.5
  > CPU and 128MiB of memory. You can say the Pod has a request of 0.5 CPU and 128
  > MiB of memory, and a limit of 1 CPU and 256MiB of memory.
  > ```yaml
  > ---
  > apiVersion: v1
  > kind: Pod
  > metadata:
  >   name: frontend
  > spec:
  >   containers:
  >   - name: app
  >     image: images.my-company.example/app:v4
  >     resources:
  >       requests:
  >         memory: "64Mi"
  >         cpu: "250m"
  >       limits:
  >         memory: "128Mi"
  >         cpu: "500m"
  >   - name: log-aggregator
  >     image: images.my-company.example/log-aggregator:v6
  >     resources:
  >       requests:
  >         memory: "64Mi"
  >         cpu: "250m"
  >       limits:
  >         memory: "128Mi"
  >         cpu: "500m"
  > ```
- `concepts/configuration/manage-resources-containers.md`, section: *Resource Management for Pods and Containers > How Pods with resource requests are scheduled*
  > [Resource Management for Pods and Containers > How Pods with resource requests are scheduled]
  > When you create a Pod, the Kubernetes scheduler selects a node for the Pod to
  > run on. Each node has a maximum capacity for each of the resource types: the
  > amount of CPU and memory it can provide for Pods. The scheduler ensures that,
  > for each resource type, the sum of the resource requests of the scheduled
  > containers is less than the capacity of the node.
  > Note that although actual memory
  > or CPU resource usage on nodes is very low, the scheduler still refuses to place
  > a Pod on a node if the capacity check fails. This protects against a resource
  > shortage on a node when resource usage later increases, for example, during a
  > daily peak in request rate.

*Drafting note:* Known partial answer in E0. | LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged | human review (Youssef Zemzem, 2026-11-07): added the scheduling section for the requests claim

**Decision** (tick one):
- [x ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `secret-encryption`

**Question** (en, concept): Are Kubernetes Secrets encrypted by default?

**Reference answer:** No. By default, Secrets are stored unencrypted in the API server's underlying data store (etcd). Enable encryption at rest and restrict access with least-privilege RBAC.

**Relevant documentation:**
- `concepts/configuration/secret.md`, section: *(whole document)*
  > [Secrets]
  > A Secret is an object that contains a small amount of sensitive data such as
  > a password, a token, or a key. Such information might otherwise be put in a
  >  specification or in a
  > container image. Using a
  > Secret means that you don't need to include confidential data in your
  > application code.
  > Because Secrets can be created independently of the Pods that use them, there
  > is less risk of the Secret (and its data) being exposed during the workflow of
  > creating, viewing, and editing Pods. Kubernetes, and applications that run in
  > your cluster, can also take additional precautions with Secrets, such as avoiding
  > writing sensitive data to nonvolatile storage.
  > Secrets are similar to ConfigMaps
  > but are specifically intended to hold confidential data.
  > Kubernetes Secrets are, by default, stored unencrypted in the API server's underlying data store
  > (etcd). Anyone with API access can retrieve or modify a Secret, and so can anyone with access to etcd.
  > Additionally, anyone who is authorized to create a Pod in a namespace can use that access to read
  > any Secret in that namespace; this includes indirect access such as the ability to create a
  > Deployment.
  > In order to safely use Secrets, take at least the following steps:
  > 1. Enable Encryption at Rest for Secrets.
  > 1. Enable or configure RBAC rules with
  >    least-privilege access to Secrets.
  > 1. Restrict Secret access to specific containers.
  > 1. Consider using external Secret store providers.
  > For more guidelines to manage and improve the security of your Secrets, refer to
  > Good practices for Kubernetes Secrets.
  > See Information security for Secrets for more details.
  > [Secrets > Uses for Secrets]
  > You can use Secrets for purposes such as the following:
  > - Set environment variables for a container.
  > - Provide credentials such as SSH keys or passwords to Pods.
  > - Allow the kubelet to pull container images from private registries.
  > The Kubernetes control plane also uses Secrets; for example,
  > bootstrap token Secrets are a mechanism to
  > help automate node registration.
  > [Secrets > Uses for Secrets > Use case: dotfiles in a secret volume]
  > You can make your data "hidden" by defining a key that begins with a dot.
  > This key represents a dotfile or "hidden" file. For example, when the following Secret
  > is mounted into a volume, `secret-volume`, the volume will contain a single file,
  > called `.secret-file`, and the `dotfile-test-container` will have this file
  > present at the path `/etc/secret-volume/.secret-file`.
  > Files beginning with dot characters are hidden from the output of `ls -l`;
  > you must use `ls -la` to see them when listing directory contents.
  > [Secrets > Uses for Secrets > Use case: Secret visible to one container in a Pod]
  > Consider a program that needs to handle HTTP requests, do some complex business
  > logic, and then sign some messages with an HMAC. Because it has complex
  > application logic, there might be an unnoticed remote file reading exploit in
  > the server, which could expose the private key to an attacker.
  > This could be divided into two processes in two containers: a frontend container
  > which handles user interaction and business logic, but which cannot see the
  > private key; and a signer container that can see the private key, and responds
  > to simple signing requests from the frontend (for example, over localhost networking).
  > With this partitioned approach, an attacker now has to trick the application
  > server into doing something rather arbitrary, which may be harder than getting
  > it to read a file.
  > [Secrets > Uses for Secrets > Alternatives to Secrets]
  > Rather than using a Secret to protect confidential data, you can pick from alternatives.
  > Here are some of your options:
  > - If your cloud-native component needs to authenticate to another application that you
  >   know is running within the same Kubernetes cluster, you can use a
  >   ServiceAccount
  >   and its tokens to identify your client.
  > - There are third-party tools that you can run, either within or outside your cluster,
  >   that manage sensitive data. For example, a service that Pods access over HTTPS,
  >   that reveals a Secret if the client correctly authenticates (for example, with a ServiceAccount
  >   token).
  > - For authentication, you can implement a custom signer for X.509 certificates, and use
  >   CertificateSigningRequests
  >   to let that custom signer issue certificates to Pods that need them.
  > - You can use a device plugin
  >   to expose node-local encryption hardware to a specific Pod. For example, you can schedule
  >   trusted Pods onto nodes that provide a Trusted Platform Module, configured out-of-band.
  > You can also combine two or more of those options, including the option to use Secret objects themselves.
  > You can also combine two or more of those options, including the option to use Secret objects themselves.
  > For example: implement (or deploy) an operator
  > that fetches short-lived session tokens from an external service, and then creates Secrets based
  > on those short-lived session tokens. Pods running in your cluster can make use of the session tokens,
  > and operator ensures they are valid. This separation means that you can run Pods that are unaware of
  > the exact mechanisms for issuing and refreshing those session tokens.
  > [Secrets > Types of Secret {#secret-types}]
  > When creating a Secret, you can specify its type using the `type` field of
  > the Secret
  > resource, or certain equivalent `kubectl` command line flags (if available).
  > The Secret type is used to facilitate programmatic handling of the Secret data.
  > Kubernetes provides several built-in types for some common usage scenarios.
  > These types vary in terms of the validations performed and the constraints
  > Kubernetes imposes on them.
  > Kubernetes provides several built-in types for some common usage scenarios.
  > These types vary in terms of the validations performed and the constraints
  > Kubernetes imposes on them.
  > | Built-in Type                         | Usage                                   |
  > | ------------------------------------- |---------------------------------------- … (section continues)

*Drafting note:* Common misconception; checks that the answer doesn't claim base64 is encryption. | LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged | human review (Youssef Zemzem, 2026-11-07): removed the base64 claim (not supported for Secret values in general)

**Decision** (tick one):
- [ x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `rollback-deployment`

**Question** (en, task): I deployed a broken version of my app. How do I go back to the previous version?

**Reference answer:** `kubectl rollout undo deployment/<name>` (optionally `--to-revision=<n>`); `kubectl rollout history` lists revisions.

**Relevant documentation:**
- `concepts/workloads/controllers/deployment.md`, section: *Deployments > Rolling Back a Deployment > Rolling Back to a Previous Revision*
  > [Deployments > Rolling Back a Deployment > Rolling Back to a Previous Revision]
  > Follow the steps given below to rollback the Deployment from the current version to the previous version, which is version 2.
  > 1. Now you've decided to undo the current rollout and rollback to the previous revision:
  >    ```shell
  >    kubectl rollout undo deployment/nginx-deployment
  >    ```
  >    The output is similar to this:
  >    ```
  >    deployment.apps/nginx-deployment rolled back
  >    ```
  >    Alternatively, you can rollback to a specific revision by specifying it with `--to-revision`:
  >    ```shell
  >    kubectl rollout undo deployment/nginx-deployment --to-revision=2
  >    ```
  >    The output is similar to this:
  >    ```
  >    deployment.apps/nginx-deployment rolled back
  >    ```
  >    For more details about rollout related commands, read `kubectl rollout`.
  >    The Deployment is now rolled back to a previous stable revision. As you can see, a `DeploymentRollback` event
  >    for rolling back to revision 2 is generated from Deployment controller.
  > 2. Check if the rollback was successful and the Deployment is running as expected, run:
  >    ```shell
  >    kubectl get deployment nginx-deployment
  >    ```
  >    The output is similar to this:
  >    ```
  >    NAME               READY   UP-TO-DATE   AVAILABLE   AGE
  >    nginx-deployment   3/3     3            3           30m
  >    ```
  > 3. Get the description of the Deployment:
  >    ```shell
  >    kubectl describe deployment nginx-deployment
  >    ```
  >    The output is similar to this:
  >    ```
  >    Name:                   nginx-deployment
  >    Namespace:              default
  >    CreationTimestamp:      Sun, 02 Sep 2018 18:17:55 -0500
  >    Labels:                 app=nginx
  >    Annotations:            deployment.kubernetes.io/revision=4
  >                            kubernetes.io/change-cause=kubectl set image deployment/nginx-deployment nginx=nginx:1.16.1
  >    Selector:               app=nginx
  >    Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
  >    StrategyType:           RollingUpdate
  >    MinReadySeconds:        0
  >    RollingUpdateStrategy:  25% max unavailable, 25% max surge
  >    Pod Template:
  >      Labels:  app=nginx
  >      Containers:
  >       nginx:
  >        Image:        nginx:1.16.1
  >        Port:         80/TCP
  >        Host Port:    0/TCP
  >        Environment:  <none>
  >        Mounts:       <none>
  >      Volumes:        <none>
  >    Conditions:
  >      Type           Status  Reason
  >      ----           ------  ------
  >      Available      True    MinimumReplicasAvailable
  >      Progressing    True    NewReplicaSetAvailable
  >    OldReplicaSets:  <none>
  >    NewReplicaSet:   nginx-deployment-c4747d96c (3/3 replicas created)
  >    Events:
  >      Type    Reason              Age   From                   Message
  >      ----    ------              ----  ----                   -------
  >      Normal  ScalingReplicaSet   12m   deployment-controller  Scaled up replica set nginx-deployment-75675f5897 to 3
  >      Normal  ScalingReplicaSet   11m   deployment-controller  Scaled up replica set nginx-deployment-c4747d96c to 1
  >      Normal  ScalingReplicaSet   11m   deployment-controller  Scaled down replica set nginx-deployment-75675f5897 to 2
  >      Normal  ScalingReplicaSet   11m   deployment-controller  Scaled up replica set nginx-deployment-c4747d96c to 2
  >      Normal  ScalingReplicaSet   11m   deployment-controller  Scaled down replica set nginx-deployment-75675f5897 to 1
  >      Normal  ScalingReplicaSet   11m   deployment-controller  Scaled up replica set nginx-deployment-c4747d96c to 3
  >      Normal  ScalingReplicaSet   11m   deployment-controller  Scaled down replica set nginx-deployment-75675f5897 to 0
  >      Normal  ScalingReplicaSet   11m   deployment-controller  Scaled up replica set nginx-deployment-595696685f to 1
  >      Normal  DeploymentRollback  15s   deployment-controller  Rolled back deployment "nginx-deployment" to revision 2
  >      Normal  ScalingReplicaSet   15s   deployment-controller  Scaled down replica set nginx-deployment-595696685f to 0
  >    ```
- `concepts/workloads/controllers/deployment.md`, section: *Deployments > Rolling Back a Deployment > Checking Rollout History of a Deployment*
  > [Deployments > Rolling Back a Deployment > Checking Rollout History of a Deployment]
  > Follow the steps given below to check the rollout history:
  > 1. First, check the revisions of this Deployment:
  >    ```shell
  >    kubectl rollout history deployment/nginx-deployment
  >    ```
  >    The output is similar to this:
  >    ```
  >    deployments "nginx-deployment"
  >    REVISION    CHANGE-CAUSE
  >    1           kubectl apply --filename=https://k8s.io/examples/controllers/nginx-deployment.yaml
  >    2           kubectl set image deployment/nginx-deployment nginx=nginx:1.16.1
  >    3           kubectl set image deployment/nginx-deployment nginx=nginx:1.161
  >    ```
  >    `CHANGE-CAUSE` is copied from the Deployment annotation `kubernetes.io/change-cause` to its revisions upon creation. You can specify the`CHANGE-CAUSE` message by:
  >    * Annotating the Deployment with `kubectl annotate deployment/nginx-deployment kubernetes.io/change-cause="image updated to 1.16.1"`
  >    * Manually editing the manifest of the resource.
  > 2. To see the details of each revision, run:
  >    ```shell
  >    kubectl rollout history deployment/nginx-deployment --revision=2
  >    ```
  > 2. To see the details of each revision, run:
  >    ```shell
  >    kubectl rollout history deployment/nginx-deployment --revision=2
  >    ```
  >    The output is similar to this:
  >    ```
  >    deployments "nginx-deployment" revision 2
  >      Labels:       app=nginx
  >              pod-template-hash=1159050644
  >      Annotations:  kubernetes.io/change-cause=kubectl set image deployment/nginx-deployment nginx=nginx:1.16.1
  >      Containers:
  >       nginx:
  >        Image:      nginx:1.16.1
  >        Port:       80/TCP
  >         QoS Tier:
  >            cpu:      BestEffort
  >            memory:   BestEffort
  >        Environment Variables:      <none>
  >      No volumes.
  >    ```

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged | human review (Youssef Zemzem, 2026-11-07): pointed to the subsections that contain the commands

**Decision** (tick one):
- [ x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `service-types`

**Question** (en, concept): When should I use a NodePort Service instead of ClusterIP or LoadBalancer?

**Reference answer:** ClusterIP (the default) is only reachable inside the cluster. NodePort exposes the Service on a static port on each node; it lets you set up your own load-balancing solution, configure environments not fully supported by Kubernetes, or expose nodes' IPs directly. LoadBalancer uses an external load balancer.

**Relevant documentation:**
- `concepts/services-networking/service.md`, section: *Service > Service type*
  > [Service > Service type  {#publishing-services-service-types}]
  > For some parts of your application (for example, frontends) you may want to expose a
  > Service onto an external IP address, one that's accessible from outside of your
  > cluster.
  > Kubernetes Service types allow you to specify what kind of Service you want.
  > The available `type` values and their behaviors are:
  > `ClusterIP`
  > : Exposes the Service on a cluster-internal IP. Choosing this value
  >   makes the Service only reachable from within the cluster. This is the
  >   default that is used if you don't explicitly specify a `type` for a Service.
  >   You can expose the Service to the public internet using an
  >   Ingress or a
  >   Gateway.
  > `NodePort`
  > : Exposes the Service on each Node's IP at a static port (the `NodePort`).
  >   To make the node port available, Kubernetes sets up a cluster IP address,
  >   the same as if you had requested a Service of `type: ClusterIP`.
  > `LoadBalancer`
  > : Exposes the Service externally using an external load balancer. Kubernetes
  >   does not directly offer a load balancing component; you must provide one, or
  >   you can integrate your Kubernetes cluster with a cloud provider.
  > `ExternalName`
  > : Maps the Service to the contents of the `externalName` field (for example,
  >   to the hostname `api.foo.bar.example`). The mapping configures your cluster's
  >   DNS server to return a `CNAME` record with that external hostname value.
  >   No proxying of any kind is set up.
  > The `type` field in the Service API is designed as nested functionality - each level
  > adds to the previous. However there is an exception to this nested design. You can
  > define a `LoadBalancer` Service by
  > disabling the load balancer `NodePort` allocation.
  > [Service > Service type  {#publishing-services-service-types} > `type: ClusterIP` {#type-clusterip}]
  > This default Service type assigns an IP address from a pool of IP addresses that
  > your cluster has reserved for that purpose.
  > Several of the other types for Service build on the `ClusterIP` type as a
  > foundation.
  > If you define a Service that has the `.spec.clusterIP` set to `"None"` then
  > Kubernetes does not assign an IP address. See headless Services
  > for more information.
  > [Service > Service type  {#publishing-services-service-types} > `type: ClusterIP` {#type-clusterip} > Choosing your own IP address]
  > You can specify your own cluster IP address as part of a `Service` creation
  > request.  To do this, set the `.spec.clusterIP` field. For example, if you
  > already have an existing DNS entry that you wish to reuse, or legacy systems
  > that are configured for a specific IP address and difficult to re-configure.
  > The IP address that you choose must be a valid IPv4 or IPv6 address from within the
  > `service-cluster-ip-range` CIDR range that is configured for the API server.
  > If you try to create a Service with an invalid `clusterIP` address value, the API
  > server will return a 422 HTTP status code to indicate that there's a problem.
  > Read avoiding collisions
  > to learn how Kubernetes helps reduce the risk and impact of two different Services
  > both trying to use the same IP address.
  > [Service > Service type  {#publishing-services-service-types} > `type: NodePort` {#type-nodeport}]
  > If you set the `type` field to `NodePort`, the Kubernetes control plane
  > allocates a port from a range specified by `--service-node-port-range` flag (default: 30000-32767).
  > Each node proxies that port (the same port number on every Node) into your Service.
  > Your Service reports the allocated port in its `.spec.ports[*].nodePort` field.
  > Using a NodePort gives you the freedom to set up your own load balancing solution,
  > to configure environments that are not fully supported by Kubernetes, or even
  > to expose one or more nodes' IP addresses directly.
  > For a node port Service, Kubernetes additionally allocates a port (TCP, UDP or
  > SCTP to match the protocol of the Service). Every node in the cluster configures
  > itself to listen on that assigned port and to forward traffic to one of the ready
  > endpoints associated with that Service. You'll be able to contact the `type: NodePort`
  > Service, from outside the cluster, by connecting to any node using the appropriate
  > protocol (for example: TCP), and the appropriate port (as assigned to that Service).
  > [Service > Service type  {#publishing-services-service-types} > `type: NodePort` {#type-nodeport} > Choosing your own port {#nodeport-custom-port}]
  > If you want a specific port number, you can specify a value in the `nodePort`
  > field. The control plane will either allocate you that port or report that
  > the API transaction failed.
  > This means that you need to take care of possible port collisions yourself.
  > You also have to use a valid port number, one that's inside the range configured
  > for NodePort use.
  > Here is an example manifest for a Service of `type: NodePort` that specifies
  > a NodePort value (30007, in this example):
  > ```yaml
  > apiVersion: v1
  > kind: Service
  > metadata:
  >   name: my-service
  > spec:
  >   type: NodePort
  >   selector:
  >     app.kubernetes.io/name: MyApp
  >   ports:
  >     - port: 80
  >       # By default and for convenience, the `targetPort` is set to
  >       # the same value as the `port` field.
  >       targetPort: 80
  >       # Optional field
  >       # By default and for convenience, the Kubernetes control plane
  >       # will allocate a port from a range (default: 30000-32767)
  >       nodePort: 30007
  > ```
  > [Service > Service type  {#publishing-services-service-types} > `type: NodePort` {#type-nodeport} > Reserve Nodeport ranges to avoid collisions  {#avoid-nodeport-collisions}]
  > The policy for assigning ports to NodePort services applies to both the auto-assignment and
  > the manual assignment scenarios. When a user wants to create a NodePort service that
  > uses a specific port, the target port may conflict with another port that has already been assigned.
  > To avoid this problem, the port range for NodePort services is divided into two bands.
  > Dynamic port assignment uses the upper band by default, and it may use the lower band once the
  > upper band has been exhausted. Users … (section continues)

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged | human review (Youssef Zemzem, 2026-11-07): added the documented NodePort use cases

**Decision** (tick one):
- [ x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `node-selector-ssd`

**Question** (en, task): How do I make a pod run only on nodes that have an SSD?

**Reference answer:** Attach a label to the nodes that have an SSD (labels can be attached manually, e.g. `disktype=ssd`) and add a matching `nodeSelector` (or node affinity rule) to the Pod spec, so it's only scheduled on nodes with that label.

**Relevant documentation:**
- `concepts/scheduling-eviction/assign-pod-node.md`, section: *Assigning Pods to Nodes > Node labels*
  > [Assigning Pods to Nodes > Node labels {#built-in-node-labels}]
  > Like many other Kubernetes objects, nodes have
  > labels. You can
  > attach labels manually.
  > Kubernetes also populates a standard set of labels
  > on all nodes in a cluster.
  > The value of these labels is cloud provider specific and is not guaranteed to be reliable.
  > For example, the value of `kubernetes.io/hostname` may be the same as the node name in some environments
  > and a different value in other environments.
  > [Assigning Pods to Nodes > Node labels {#built-in-node-labels} > Node isolation/restriction]
  > Adding labels to nodes allows you to target Pods for scheduling on specific
  > nodes or groups of nodes. You can use this functionality to ensure that specific
  > Pods only run on nodes with certain isolation, security, or regulatory
  > properties.
  > If you use labels for node isolation, choose label keys that the kubelet
  > cannot modify. This prevents a compromised node from setting those labels on
  > itself so that the scheduler schedules workloads onto the compromised node.
  > The `NodeRestriction` admission plugin
  > prevents the kubelet from setting or modifying labels with a
  > `node-restriction.kubernetes.io/` prefix.
  > To make use of that label prefix for node isolation:
  > 1. Ensure you are using the Node authorizer and have _enabled_ the `NodeRestriction` admission plugin.
  > 2. Add labels with the `node-restriction.kubernetes.io/` prefix to your nodes, and use those labels in your node selectors.
  >    For example, `example.com.node-restriction.kubernetes.io/fips=true` or `example.com.node-restriction.kubernetes.io/pci-dss=true`.
- `concepts/scheduling-eviction/assign-pod-node.md`, section: *Assigning Pods to Nodes > nodeSelector*
  > [Assigning Pods to Nodes > nodeSelector]
  > `nodeSelector` is the simplest recommended form of node selection constraint.
  > You can add the `nodeSelector` field to your Pod specification and specify the
  > node labels you want the target node to have.
  > Kubernetes only schedules the Pod onto nodes that have each of the labels you
  > specify.
  > See Assign Pods to Nodes for more
  > information.
- `concepts/scheduling-eviction/assign-pod-node.md`, section: *Assigning Pods to Nodes > Affinity and anti-affinity*
  > [Assigning Pods to Nodes > Affinity and anti-affinity]
  > `nodeSelector` is the simplest way to constrain Pods to nodes with specific
  > labels. Affinity and anti-affinity expand the types of constraints you can
  > define. Some of the benefits of affinity and anti-affinity include:
  > - The affinity/anti-affinity language is more expressive. `nodeSelector` only
  >   selects nodes with all the specified labels. Affinity/anti-affinity gives you
  >   more control over the selection logic.
  > - You can indicate that a rule is *soft* or *preferred*, so that the scheduler
  >   still schedules the Pod even if it can't find a matching node.
  > - You can constrain a Pod using labels on other Pods running on the node (or other topological domain),
  >   instead of just node labels, which allows you to define rules for which Pods
  >   can be co-located on a node.
  > The affinity feature consists of two types of affinity:
  > - *Node affinity* functions like the `nodeSelector` field but is more expressive and
  >   allows you to specify soft rules.
  > - *Inter-pod affinity/anti-affinity* allows you to constrain Pods against labels
  >   on other Pods.
  > [Assigning Pods to Nodes > Affinity and anti-affinity > Node affinity]
  > Node affinity is conceptually similar to `nodeSelector`, allowing you to constrain which nodes your
  > Pod can be scheduled on based on node labels. There are two types of node
  > affinity:
  > - `requiredDuringSchedulingIgnoredDuringExecution`: The scheduler can't
  >   schedule the Pod unless the rule is met. This functions like `nodeSelector`,
  >   but with a more expressive syntax.
  > - `preferredDuringSchedulingIgnoredDuringExecution`: The scheduler tries to
  >   find a node that meets the rule. If a matching node is not available, the
  >   scheduler still schedules the Pod.
  > In the preceding types, `IgnoredDuringExecution` means that if the node labels
  > change after Kubernetes schedules the Pod, the Pod continues to run.
  > You can specify node affinities using the `.spec.affinity.nodeAffinity` field in
  > your Pod spec.
  > For example, consider the following Pod spec:
  > In this example, the following rules apply:
  > - The node *must* have a label with the key `topology.kubernetes.io/zone` and
  >   the value of that label *must* be either `antarctica-east1` or `antarctica-west1`.
  > - The node *preferably* has a label with the key `another-node-label-key` and
  >   the value `another-node-label-value`.
  > You can use the `operator` field to specify a logical operator for Kubernetes to use when
  > interpreting the rules. You can use `In`, `NotIn`, `Exists`, `DoesNotExist`,
  > `Gt` and `Lt`.
  > Read Operators
  > to learn more about how these work.
  > `NotIn` and `DoesNotExist` allow you to define node anti-affinity behavior.
  > Alternatively, you can use node taints
  > to repel Pods from specific nodes.
  > If you specify both `nodeSelector` and `nodeAffinity`, *both* must be satisfied
  > for the Pod to be scheduled onto a node.
  > If you specify multiple terms in `nodeSelectorTerms` associated with `nodeAffinity`
  > types, then the Pod can be scheduled onto a node if one of the specified terms
  > can be satisfied (terms are ORed).
  > If you specify multiple expressions in a single `matchExpressions` field associated with a
  > term in `nodeSelectorTerms`, then the Pod can be scheduled onto a node only
  > if all the expressions are satisfied (expressions are ANDed).
  > See Assign Pods to Nodes using Node Affinity
  > for more information.
  > [Assigning Pods to Nodes > Affinity and anti-affinity > Node affinity > Node affinity weight]
  > You can specify a `weight` between 1 and 100 for each instance of the
  > `preferredDuringSchedulingIgnoredDuringExecution` affinity type. When the
  > scheduler finds nodes that meet all the other scheduling requirements of the Pod, the
  > scheduler iterates through every preferred rule that the node satisfies and adds the
  > value of the `weight` for that expression to a sum.
  > The final sum is added to the score of other priority functions for the node.
  > Nodes with the highest total score are prioritized when the scheduler makes a
  > scheduling decision for the Pod.
  > For example, consider the following Pod spec:
  > If there are two possible nodes that match the
  > `preferredDuringSchedulingIgnoredDuringExecution` rule, one with the
  > `label-1:key-1` label and another with the `label-2:key-2` label, the scheduler
  > considers the `weight` of each node and adds the weight to the other scores for
  > that node, and schedules the Pod onto the node with the highest final score.
  > If you want Kubernetes to successfully schedule the Pods in this example, you
  > must have existing nodes with the `kubernetes.io/os=linux` label.
  > [Assigning Pods to Nodes > Affinity and anti-affinity > Node affinity > Node affinity per scheduling profile]
  > When configuring multiple scheduling profiles, you can associate
  > a profile with a node affinity, which is useful if a profile only applies to a specific set of nodes.
  > To do so, add an `addedAffinity` to the `args` field of the `NodeAffinity` plugin
  > in the scheduler configuration. For example:
  > ```yaml
  > apiVersion: kubescheduler.config.k8s.io/v1
  > kind: KubeSchedulerConfiguration
  > profiles:
  >   - schedulerName: default-scheduler
  >   - schedulerName: foo-scheduler
  >     pluginConfig:
  >       - name: NodeAffinity
  >         args:
  >           addedAffinity:
  >             requiredDuringSchedulingIgnoredDuringExecution:
  >               nodeSelectorTerms:
  >               - matchExpressions:
  >                 - key: scheduler-profile
  >                   operator: In
  >                   values:
  >                   - foo
  > ```
  > The `addedAffinity` is applied to all Pods that set `.spec.schedulerName` to `foo-scheduler`, in addition to the
  > NodeAffinity specified in the PodSpec.
  > That is, in order to match the Pod, nodes need to satisfy `addedAffinity` and
  > the Pod's `.spec.NodeAffinity`.
  > Since the `addedAffinity` is not visible to end users, its behavior might be
  > unexpected to them. Use node labels that have a clear correlation to the
  > scheduler profile name.
  > The DaemonSet controller, which creates Pods for DaemonSets,
  > does not support scheduling … (section continues)

*Drafting note:* human review (Youssef Zemzem, 2026-11-07): added the node-labels section; no kubectl command claimed

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
Specify that only requiredDuringSchedulingIgnoredDuringExecution node affinity guarantees scheduling exclusively on SSD-labelled nodes. Preferred node affinity is a soft preference and does not guarantee this. nodeSelector is also a valid strict constraint.

---

### `statefulset-database`

**Question** (en, concept): Why would I use a StatefulSet instead of a Deployment for a database?

**Reference answer:** Use a StatefulSet when the application needs stable network identities, stable persistent storage, or ordered, graceful deployment and scaling; databases that need these properties are a typical fit.

**Relevant documentation:**
- `concepts/workloads/controllers/statefulset.md`, section: *StatefulSets > Using StatefulSets*
  > [StatefulSets > Using StatefulSets]
  > StatefulSets are valuable for applications that require one or more of the
  > following.
  > * Stable, unique network identifiers.
  > * Stable, persistent storage.
  > * Ordered, graceful deployment and scaling.
  > * Ordered, automated rolling updates.
  > In the above, stable is synonymous with persistence across Pod (re)scheduling.
  > If an application doesn't require any stable identifiers or ordered deployment,
  > deletion, or scaling, you should deploy your application using a workload object
  > that provides a set of stateless replicas.
  > Deployment or
  > ReplicaSet may be better suited to your stateless needs.
- `concepts/workloads/controllers/statefulset.md`, section: *StatefulSets > Pod Identity*
  > [StatefulSets > Pod Identity]
  > StatefulSet Pods have a unique identity that consists of an ordinal, a
  > stable network identity, and stable storage. The identity sticks to the Pod,
  > regardless of which node it's (re)scheduled on.
  > [StatefulSets > Pod Identity > Ordinal Index]
  > For a StatefulSet with N replicas, each Pod in the StatefulSet
  > will be assigned an integer ordinal, that is unique over the Set. By default,
  > pods will be assigned ordinals from 0 up through N-1. The StatefulSet controller
  > will also add a pod label with this index: `apps.kubernetes.io/pod-index`.
  > [StatefulSets > Pod Identity > Start ordinal]
  > `.spec.ordinals` is an optional field that allows you to configure the integer
  > ordinals assigned to each Pod. It defaults to nil. Within the field, you can
  > configure the following options:
  > * `.spec.ordinals.start`: If the `.spec.ordinals.start` field is set, Pods will
  >   be assigned ordinals from `.spec.ordinals.start` up through
  >   `.spec.ordinals.start + .spec.replicas - 1`.
  > [StatefulSets > Pod Identity > Stable Network ID]
  > Each Pod in a StatefulSet derives its hostname from the name of the StatefulSet
  > and the ordinal of the Pod. The pattern for the constructed hostname
  > is `$(statefulset name)-$(ordinal)`. The example above will create three Pods
  > named `web-0,web-1,web-2`.
  > A StatefulSet can use a Headless Service
  > to control the domain of its Pods. The domain managed by this Service takes the form:
  > `$(service name).$(namespace).svc.cluster.local`, where "cluster.local" is the
  > cluster domain.
  > As each Pod is created, it gets a matching DNS subdomain, taking the form:
  > `$(podname).$(governing service domain)`, where the governing service is defined
  > by the `serviceName` field on the StatefulSet.
  > Depending on how DNS is configured in your cluster, you may not be able to look up the DNS
  > name for a newly-run Pod immediately. This behavior can occur when other clients in the
  > cluster have already sent queries for the hostname of the Pod before it was created.
  > Negative caching (normal in DNS) means that the results of previous failed lookups are
  > remembered and reused, even after the Pod is running, for at least a few seconds.
  > If you need to discover Pods promptly after they are created, you have a few options:
  > If you need to discover Pods promptly after they are created, you have a few options:
  > - Query the Kubernetes API directly (for example, using a watch) rather than relying on DNS lookups.
  > - Decrease the time of caching in your Kubernetes DNS provider (typically this means editing the
  >   config map for CoreDNS, which currently caches for 30 seconds).
  > As mentioned in the limitations section, you are responsible for
  > creating the Headless Service
  > responsible for the network identity of the pods.
  > Here are some examples of choices for Cluster Domain, Service name,
  > StatefulSet name, and how that affects the DNS names for the StatefulSet's Pods.
  > Here are some examples of choices for Cluster Domain, Service name,
  > StatefulSet name, and how that affects the DNS names for the StatefulSet's Pods.
  > Cluster Domain | Service (ns/name) | StatefulSet (ns/name)  | StatefulSet Domain  | Pod DNS | Pod Hostname |
  > -------------- | ----------------- | ----------------- | -------------- | ------- | ------------ |
  >  cluster.local | default/nginx     | default/web       | nginx.default.svc.cluster.local | web-{0..N-1}.nginx.default.svc.cluster.local | web-{0..N-1} |
  >  cluster.local | foo/nginx         | foo/web           | nginx.foo.svc.cluster.local     | web-{0..N-1}.nginx.foo.svc.cluster.local     | web-{0..N-1} |
  >  kube.local    | foo/nginx         | foo/web           | nginx.foo.svc.kube.local        | web-{0..N-1}.nginx.foo.svc.kube.local        | web-{0..N-1} |
  > Cluster Domain will be set to `cluster.local` unless
  > otherwise configured.
  > [StatefulSets > Pod Identity > Stable Storage]
  > For each VolumeClaimTemplate entry defined in a StatefulSet, each Pod receives one
  > PersistentVolumeClaim. In the nginx example above, each Pod receives a single PersistentVolume
  > with a StorageClass of `my-storage-class` and 1 GiB of provisioned storage. If no StorageClass
  > is specified, then the default StorageClass will be used. When a Pod is (re)scheduled
  > onto a node, its `volumeMounts` mount the PersistentVolumes associated with its
  > PersistentVolume Claims. Note that, the PersistentVolumes associated with the
  > Pods' PersistentVolume Claims are not deleted when the Pods, or StatefulSet are deleted.
  > This must be done manually.
  > [StatefulSets > Pod Identity > Pod Name Label]
  > When the StatefulSet controller creates a Pod,
  > it adds a label, `statefulset.kubernetes.io/pod-name`, that is set to the name of
  > the Pod. This label allows you to attach a Service to a specific Pod in
  > the StatefulSet.
  > [StatefulSets > Pod Identity > Pod index label]
  > When the StatefulSet controller creates a Pod,
  > the new Pod is labelled with `apps.kubernetes.io/pod-index`. The value of this label is the ordinal index of
  > the Pod. This label allows you to route traffic to a particular pod index, filter logs/metrics
  > using the pod index label, and more. Note the feature gate `PodIndexLabel` is enabled and locked by default for this
  > feature, in order to disable it, users will have to use server emulated version v1.31.

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): removed the unsupported comparison with Deployments | human review (Youssef Zemzem, 2026-11-07): qualified the claim about databases

**Decision** (tick one):
- [ ] ✅ Correct as written
- [x ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**
The documentation supports stable network identities, persistent storage, and ordered deployment and scaling as reasons to use StatefulSets. However, it does not explicitly identify databases as a typical use case. Remove the database-specific generalization or clearly qualify it as an inference.

---

### `cronjob-nightly`

**Question** (en, task): How do I run a job every night at 2 am?

**Reference answer:** Create a CronJob with `schedule: "0 2 * * *"` (cron syntax; `timeZone` can set the time zone).

**Relevant documentation:**
- `concepts/workloads/controllers/cron-jobs.md`, section: *CronJob > Writing a CronJob spec > Schedule syntax*
  > [CronJob > Writing a CronJob spec > Schedule syntax]
  > The `.spec.schedule` field is required. The value of that field follows the Cron syntax:
  > ```
  > # ┌───────────── minute (0 - 59)
  > # │ ┌───────────── hour (0 - 23)
  > # │ │ ┌───────────── day of the month (1 - 31)
  > # │ │ │ ┌───────────── month (1 - 12)
  > # │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
  > # │ │ │ │ │                                   OR sun, mon, tue, wed, thu, fri, sat
  > # │ │ │ │ │
  > # │ │ │ │ │
  > # * * * * *
  > ```
  > For example, `0 3 * * 1` means this task is scheduled to run weekly on a Monday at 3 AM.
  > The format also includes extended "Vixie cron" step values. As explained in the
  > FreeBSD manual:
  > > Step values can be used in conjunction with ranges. Following a range
  > > with `/<number>` specifies skips of the number's value through the
  > > range. For example, `0-23/2` can be used in the hours field to specify
  > > command execution every other hour (the alternative in the V7 standard is
  > > `0,2,4,6,8,10,12,14,16,18,20,22`). Steps are also permitted after an
  > > asterisk, so if you want to say "every two hours", just use `*/2`.
  > A question mark (`?`) in the schedule has the same meaning as an asterisk `*`, that is,
  > it stands for any of available value for a given field.
  > A question mark (`?`) in the schedule has the same meaning as an asterisk `*`, that is,
  > it stands for any of available value for a given field.
  > Other than the standard syntax, some macros like `@monthly` can also be used:
  > | Entry 										| Description																									| Equivalent to |
  > | ------------- 						| ------------- 																							|-------------  |
  > | @yearly (or @annually)		| Run once a year at midnight of 1 January										| 0 0 1 1 * 		|
  > | @monthly 									| Run once a month at midnight of the first day of the month	| 0 0 1 * * 		|
  > | @weekly 									| Run once a week at midnight on Sunday morning								| 0 0 * * 0 		|
  > | @daily (or @midnight)			| Run once a day at midnight																	| 0 0 * * * 		|
  > | @hourly 									| Run once an hour at the beginning of the hour								| 0 * * * * 		|
  > To generate CronJob schedule expressions, you can also use web tools like crontab.guru.
- `concepts/workloads/controllers/cron-jobs.md`, section: *CronJob > Writing a CronJob spec > Time zones*
  > [CronJob > Writing a CronJob spec > Time zones]
  > For CronJobs with no time zone specified, the kube-controller-manager
  > interprets schedules relative to its local time zone.
  > You can specify a time zone for a CronJob by setting `.spec.timeZone` to the name
  > of a valid time zone.
  > For example, setting `.spec.timeZone: "Etc/UTC"` instructs Kubernetes to interpret
  > the schedule relative to Coordinated Universal Time.
  > A time zone database from the Go standard library is included in the binaries and used as a fallback in case an external database is not available on the system.

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged | human review (Youssef Zemzem, 2026-11-07): pointed to the schedule-syntax and time-zone subsections

**Decision** (tick one):
- [x ] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `image-pull-policy`

**Question** (en, concept): When does the kubelet pull an image again instead of using the cached one?

**Reference answer:** It depends on `imagePullPolicy`. `IfNotPresent`: pull only if the image isn't already present locally. `Always`: each time a container starts, the kubelet asks the registry for the image digest and pulls only if that exact digest isn't cached. `Never`: never pull. If the policy is omitted and the tag is `:latest` (or there is no tag), the default is `Always`.

**Relevant documentation:**
- `concepts/containers/images.md`, section: *Images > Updating images*
  > [Images > Updating images]
  > When you first create a Deployment,
  > StatefulSet, Pod, or other
  > object that includes a PodTemplate, and a pull policy was not explicitly specified,
  > then by default the pull policy of all containers in that Pod will be set to
  > `IfNotPresent`. This policy causes the
  > kubelet to skip pulling an
  > image if it already exists.
  > [Images > Updating images > Image pull policy]
  > The `imagePullPolicy` for a container and the tag of the image both affect _when_ the
  > kubelet attempts to pull
  > (download) the specified image.
  > Here's a list of the values you can set for `imagePullPolicy` and the effects
  > these values have:
  > `IfNotPresent`
  > : the image is pulled only if it is not already present locally.
  > `Always`
  > : every time the kubelet launches a container, the kubelet queries the container
  >   image registry to resolve the name to an image
  >   digest.
  >   If the kubelet has a container image with that exact digest cached locally, the kubelet uses its
  >   cached image; otherwise, the kubelet pulls the image with the resolved digest, and uses that image
  >   to launch the container.
  > `Never`
  > : the kubelet does not try fetching the image. If the image is somehow already present
  >   locally, the kubelet attempts to start the container; otherwise, startup fails.
  >   See pre-pulled images for more details.
  > The caching semantics of the underlying image provider make even
  > `imagePullPolicy: Always` efficient, as long as the registry is reliably accessible.
  > Your container runtime can notice that the image layers already exist on the node
  > so that they don't need to be downloaded again.
  > You should avoid using the `:latest` tag when deploying containers in production as
  > it is harder to track which version of the image is running and more difficult to
  > roll back properly.
  > Instead, specify a meaningful tag such as `v1.42.0` and/or a digest.
  > To make sure the Pod always uses the same version of a container image, you can specify
  > the image's digest;
  > replace `<image-name>:<tag>` with `<image-name>@<digest>`
  > (for example, `image@sha256:45b23dee08af5e43a7fea6c4cf9c25ccf269ee113168c19722f87876677c5cb2`).
  > When using image tags, if the image registry were to change the code that the tag on that image
  > represents, you might end up with a mix of Pods running the old and new code. An image digest
  > uniquely identifies a specific version of the image, so Kubernetes runs the same code every time
  > it starts a container with that image name and digest specified. Specifying an image by digest
  > pins the code that you run so that a change at the registry cannot lead to that mix of versions.
  > There are third-party admission controllers
  > that mutate Pods (and PodTemplates) when they are created, so that the
  > running workload is defined based on an image digest rather than a tag.
  > That might be useful if you want to make sure that your entire workload is
  > running the same code no matter what tag changes happen at the registry.
  > [Images > Updating images > Image pull policy > Default image pull policy {#imagepullpolicy-defaulting}]
  > When you (or a controller) submit a new Pod to the API server, your cluster sets the
  > `imagePullPolicy` field when specific conditions are met:
  > - if you omit the `imagePullPolicy` field, and you specify the digest for the
  >   container image, the `imagePullPolicy` is automatically set to `IfNotPresent`.
  > - if you omit the `imagePullPolicy` field, and the tag for the container image is
  >   `:latest`, `imagePullPolicy` is automatically set to `Always`.
  > - if you omit the `imagePullPolicy` field, and you don't specify the tag for the
  >   container image, `imagePullPolicy` is automatically set to `Always`.
  > - if you omit the `imagePullPolicy` field, and you specify a tag for the container
  >   image that isn't `:latest`, the `imagePullPolicy` is automatically set to
  >   `IfNotPresent`.
  > The value of `imagePullPolicy` of the container is always set when the object is
  > first _created_, and is not updated if the image's tag or digest later changes.
  > The value of `imagePullPolicy` of the container is always set when the object is
  > first _created_, and is not updated if the image's tag or digest later changes.
  > For example, if you create a Deployment with an image whose tag is _not_
  > `:latest`, and later update that Deployment's image to a `:latest` tag, the
  > `imagePullPolicy` field will _not_ change to `Always`. You must manually change
  > the pull policy of any object after its initial creation.
  > [Images > Updating images > Image pull policy > Required image pull]
  > If you would like to always force a pull, you can do one of the following:
  > - Set the `imagePullPolicy` of the container to `Always`.
  > - Omit the `imagePullPolicy` and use `:latest` as the tag for the image to use;
  >   Kubernetes will set the policy to `Always` when you submit the Pod.
  > - Omit the `imagePullPolicy` and the tag for the image to use;
  >   Kubernetes will set the policy to `Always` when you submit the Pod.
  > - Enable the AlwaysPullImages
  >   admission controller.
  > [Images > Updating images > ImagePullBackOff]
  > When a kubelet starts creating containers for a Pod using a container runtime,
  > it might be possible the container is in Waiting
  > state because of `ImagePullBackOff`.
  > The status `ImagePullBackOff` means that a container could not start because Kubernetes
  > could not pull a container image (for reasons such as invalid image name, or pulling
  > from a private registry without `imagePullSecret`). The `BackOff` part indicates
  > that Kubernetes will keep trying to pull the image, with an increasing back-off delay.
  > Kubernetes raises the delay between each attempt until it reaches a compiled-in limit,
  > which is 300 seconds (5 minutes).
  > [Images > Updating images > Image pull per runtime class]
  > Kubernetes includes alpha support for performing image pulls based on the RuntimeClass of a Pod.
  > If you enable the `RuntimeClassInImageCriApi` feature gate,
  > the kubelet references container images by a tuple of image name and runtime handler
  > rather than just the image name or digest. Your
  > container … (section continues)

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged | human review (Youssef Zemzem, 2026-11-07): corrected Always (resolve digest, pull only if not cached)

**Decision** (tick one):
- [ x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-rollback`

**Question** (fr, task): Comment revenir à la version précédente d'un déploiement ?

**Reference answer:** `kubectl rollout undo deployment.v1.apps/<nom>` (option `--to-revision` pour une révision précise).

**Relevant documentation:**
- `concepts/workloads/controllers/deployment.md`, section: *Déploiements > Annulation d'un déploiement > Revenir à une révision précédente*
  > [Déploiements > Annulation d'un déploiement > Revenir à une révision précédente]
  > Suivez les étapes ci-dessous pour restaurer le déploiement de la version actuelle à la version précédente, qui est la version 2.
  > 1. Vous avez maintenant décidé d'annuler le déploiement actuel et le retour à la révision précédente:
  >     ```shell
  >     kubectl rollout undo deployment.v1.apps/nginx-deployment
  >     ```
  >     La sortie est similaire à ceci:
  >     ```text
  >     deployment.apps/nginx-deployment
  >     ```
  >     Alternativement, vous pouvez revenir à une révision spécifique en la spécifiant avec `--to-revision`:
  >     ```shell
  >     kubectl rollout undo deployment.v1.apps/nginx-deployment --to-revision=2
  >     ```
  >     La sortie est similaire à ceci:
  >     ```text
  >     deployment.apps/nginx-deployment
  >     ```
  >     Pour plus de détails sur les commandes liées au déploiement, lisez `kubectl rollout`.
  >     Le déploiement est maintenant rétabli à une précédente révision stable.
  >     Comme vous pouvez le voir, un événement `DeploymentRollback` pour revenir à la révision 2 est généré à partir du contrôleur de déploiement.
  > 2. Vérifiez si la restauration a réussi et que le déploiement s'exécute comme prévu, exécutez:
  >     ```shell
  >     kubectl get deployment nginx-deployment
  >     ```
  >     ```shell
  >     kubectl get deployment nginx-deployment
  >     ```
  >     La sortie est similaire à ceci:
  >     ```text
  >     NAME               READY   UP-TO-DATE   AVAILABLE   AGE
  >     nginx-deployment   3/3     3            3           30m
  >     ```
  > 3. Obtenez la description du déploiement:
  >     ```shell
  >     kubectl describe deployment nginx-deployment
  >     ```
  >     La sortie est similaire à ceci:
  >     La sortie est similaire à ceci:
  >     ```text
  >     Name:                   nginx-deployment
  >     Namespace:              default
  >     CreationTimestamp:      Sun, 02 Sep 2018 18:17:55 -0500
  >     Labels:                 app=nginx
  >     Annotations:            deployment.kubernetes.io/revision=4
  >                             kubernetes.io/change-cause=kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.9.1 --record=true
  >     Selector:               app=nginx
  >     Replicas:               3 desired | 3 updated | 3 total | 3 available | 0 unavailable
  >     StrategyType:           RollingUpdate
  >     MinReadySeconds:        0
  >     RollingUpdateStrategy:  25% max unavailable, 25% max surge
  >     Pod Template:
  >       Labels:  app=nginx
  >       Containers:
  >        nginx:
  >         Image:        nginx:1.9.1
  >         Port:         80/TCP
  >         Host Port:    0/TCP
  >         Environment:  <none>
  >         Mounts:       <none>
  >       Volumes:        <none>
  >     Conditions:
  >       Type           Status  Reason
  >       ----           ------  ------
  >       Available      True    MinimumReplicasAvailable
  >       Progressing    True    NewReplicaSetAvailable
  >     OldReplicaSets:  <none>
  >     NewReplicaSet:   nginx-deployment-c4747d96c (3/3 replicas created)
  >     Events:
  >       Type    Reason              Age   From                   Message
  >       ----    ------              ----  ----                   -------
  >       Normal  ScalingReplicaSet   12m   deployment-controller  Scaled up replica set nginx-deployment-75675f5897 to 3
  >       Normal  ScalingReplicaSet   11m   deployment-controller  Scaled up replica set nginx-deployment-c4747d96c to 1
  >       Normal  ScalingReplicaSet   11m   deployment-controller  Scaled down replica set nginx-deployment-75675f5897 to 2
  >       Normal  ScalingReplicaSet   11m   deployment-controller  Scaled up replica set nginx-deployment-c4747d96c to 2
  >       Normal  ScalingReplicaSet   11m   deployment-controller  Scaled down replica set nginx-deployment-75675f5897 to 1
  >       Normal  ScalingReplicaSet   11m   deployment-controller  Scaled up replica set nginx-deployment-c4747d96c to 3
  >       Normal  ScalingReplicaSet   11m   deployment-controller  Scaled down replica set nginx-deployment-75675f5897 to 0
  >       Normal  ScalingReplicaSet   11m   deployment-controller  Scaled up replica set nginx-deployment-595696685f to 1
  >       Normal  DeploymentRollback  15s   deployment-controller  Rolled back deployment "nginx-deployment" to revision 2
  >       Normal  ScalingReplicaSet   15s   deployment-controller  Scaled down replica set nginx-deployment-595696685f to 0
  >     ```
- `concepts/workloads/controllers/deployment.md`, section: *Déploiements > Annulation d'un déploiement > Vérification de l'historique de déploiement d'un déploiement*
  > [Déploiements > Annulation d'un déploiement > Vérification de l'historique de déploiement d'un déploiement]
  > Suivez les étapes ci-dessous pour vérifier l'historique de déploiement:
  > 1. Tout d'abord, vérifiez les révisions de ce déploiement:
  >     ```shell
  >     kubectl rollout history deployment.v1.apps/nginx-deployment
  >     ```
  >     La sortie est similaire à ceci:
  >     ```text
  >     deployments "nginx-deployment"
  >     REVISION    CHANGE-CAUSE
  >     1           kubectl apply --filename=https://k8s.io/examples/controllers/nginx-deployment.yaml --record=true
  >     2           kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.9.1 --record=true
  >     3           kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.91 --record=true
  >     ```
  >     `CHANGE-CAUSE` est copié de l'annotation de déploiement `kubernetes.io/change-cause` dans ses révisions lors de la création.
  >     Vous pouvez spécifier le message`CHANGE-CAUSE` en:
  >     * Annoter le déploiement avec `kubectl annotate deployment.v1.apps/nginx-deployment kubernetes.io/change-cause="image mis à jour en 1.9.1"`
  >     * Ajoutez le drapeau `--record` pour enregistrer la commande `kubectl` qui apporte des modifications à la ressource.
  >     * Modification manuelle du manifeste de la ressource.
  > 2. Pour voir les détails de chaque révision, exécutez:
  >     ```shell
  >     kubectl rollout history deployment.v1.apps/nginx-deployment --revision=2
  >     ```
  >     La sortie est similaire à ceci:
  >     ```text
  >     deployments "nginx-deployment" revision 2
  >       Labels:       app=nginx
  >               pod-template-hash=1159050644
  >       Annotations:  kubernetes.io/change-cause=kubectl set image deployment.v1.apps/nginx-deployment nginx=nginx:1.9.1 --record=true
  >       Containers:
  >        nginx:
  >         Image:      nginx:1.9.1
  >         Port:       80/TCP
  >          QoS Tier:
  >             cpu:      BestEffort
  >             memory:   BestEffort
  >         Environment Variables:      <none>
  >       No volumes.
  >     ```

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged | human review (Youssef Zemzem, 2026-11-07): pointed to the subsections with the commands; exact documented syntax

**Decision** (tick one):
- [ x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---

### `fr-service-types`

**Question** (fr, concept): Quels types de Service permettent d'exposer une application en dehors du cluster ?

**Reference answer:** `NodePort` et `LoadBalancer` exposent le service à l'extérieur du cluster ; `ClusterIP` (par défaut) reste interne ; `ExternalName` associe le service à un nom DNS (CNAME), sans proxy.

**Relevant documentation:**
- `concepts/services-networking/service.md`, section: *Service > Services de publication (ServiceTypes)*
  > [Service > Services de publication (ServiceTypes) {#publishing-services-service-types}]
  > Pour certaines parties de votre application (par exemple, les frontaux), vous souhaiterez peut-être exposer un service sur une adresse IP externe, qui est en dehors de votre cluster.
  > Les «ServiceTypes» de Kubernetes vous permettent de spécifier le type de service que vous souhaitez.
  > La valeur par défaut est «ClusterIP».
  > Les valeurs de `Type` et leurs comportements sont:
  > Les valeurs de `Type` et leurs comportements sont:
  >    * `ClusterIP`: Expose le service sur une IP interne au cluster.
  >      Le choix de cette valeur rend le service uniquement accessible à partir du cluster.
  >      Il s'agit du `ServiceType` par défaut.
  >    * `NodePort`: Expose le service sur l'IP de chaque nœud sur un port statique (le `NodePort`).
  >      Un service `ClusterIP`, vers lequel le service `NodePort` est automatiquement créé.
  >      Vous pourrez contacter le service `NodePort`, depuis l'extérieur du cluster, en demandant `<NodeIP>: <NodePort>`.
  >    * `LoadBalancer`: Expose le service en externe à l'aide de l'équilibreur de charge d'un fournisseur de cloud.
  >      Les services `NodePort` et `ClusterIP`, vers lesquels les itinéraires de l'équilibreur de charge externe, sont automatiquement créés.
  >    * `ExternalName`: Mappe le service au contenu du champ `externalName` (par exemple `foo.bar.example.com`), en renvoyant un enregistrement `CNAME` avec sa valeur.
  >      Aucun proxy d'aucune sorte n'est mis en place.
  >      Vous avez besoin de CoreDNS version 1.7 ou supérieure pour utiliser le type `ExternalName`.
  >      Vous avez besoin de CoreDNS version 1.7 ou supérieure pour utiliser le type `ExternalName`.
  > Vous pouvez également utiliser Ingress pour exposer votre service.
  > Ingress n'est pas un type de service, mais il sert de point d'entrée pour votre cluster.
  > Il vous permet de consolider vos règles de routage en une seule ressource car il peut exposer plusieurs services sous la même adresse IP.
  > [Service > Services de publication (ServiceTypes) {#publishing-services-service-types} > Type NodePort {#type-nodeport}]
  > Si vous définissez le champ `type` sur` NodePort`, le plan de contrôle Kubernetes alloue un port à partir d'une plage spécifiée par l'indicateur `--service-node-port-range` (par défaut: 30000-32767).
  > Chaque nœud assure le proxy de ce port (le même numéro de port sur chaque nœud) vers votre service.
  > Votre service signale le port alloué dans son champ `.spec.ports[*].nodePort`.
  > Si vous souhaitez spécifier une ou des adresses IP particulières pour proxyfier le port, vous pouvez définir l'indicateur `--nodeport-addresses` dans kube-proxy sur des blocs IP particuliers; cela est pris en charge depuis Kubernetes v1.10.
  > Cet indicateur prend une liste délimitée par des virgules de blocs IP (par exemple 10.0.0.0/8, 192.0.2.0/25) pour spécifier les plages d'adresses IP que kube-proxy doit considérer comme locales pour ce nœud.
  > Par exemple, si vous démarrez kube-proxy avec l'indicateur `--nodeport-addresses=127.0.0.0/8`, kube-proxy sélectionne uniquement l'interface de boucle locale pour les services NodePort.
  > La valeur par défaut pour `--nodeport-addresses` est une liste vide.
  > Cela signifie que kube-proxy doit prendre en compte toutes les interfaces réseau disponibles pour NodePort (qui est également compatible avec les versions antérieures de Kubernetes).
  > Si vous voulez un numéro de port spécifique, vous pouvez spécifier une valeur dans le champ `nodePort`.
  > Le plan de contrôle vous attribuera ce port ou signalera l'échec de la transaction API.
  > Cela signifie que vous devez vous occuper vous-même des éventuelles collisions de ports.
  > Vous devez également utiliser un numéro de port valide, celui qui se trouve dans la plage configurée pour l'utilisation de NodePort.
  > L'utilisation d'un NodePort vous donne la liberté de configurer votre propre solution d'équilibrage de charge, de configurer des environnements qui ne sont pas entièrement pris en charge par Kubernetes, ou même d'exposer directement les adresses IP d'un ou plusieurs nœuds.
  > Notez que ce service est visible en tant que `<NodeIP>: spec.ports[*].nodePort` et `.spec.clusterIP: spec.ports[*].Port`.
  > (Si l'indicateur `--nodeport-addresses` dans kube-proxy est défini, <NodeIP> serait filtré NodeIP(s).)
  > [Service > Services de publication (ServiceTypes) {#publishing-services-service-types} > Type LoadBalancer {#loadbalancer}]
  > Sur les fournisseurs de cloud qui prennent en charge les load balancers externes, la définition du champ `type` sur` LoadBalancer` provisionne un load balancer pour votre service.
  > La création réelle du load balancer se produit de manière asynchrone et les informations sur le load balancer provisionné sont publiées dans le champ `.status.loadBalancer`.
  > Par exemple:
  > ```yaml
  > apiVersion: v1
  > kind: Service
  > metadata:
  >   name: my-service
  > spec:
  >   selector:
  >     app.kubernetes.io/name: MyApp
  >   ports:
  >     - protocol: TCP
  >       port: 80
  >       targetPort: 9376
  >   clusterIP: 10.0.171.239
  >   type: LoadBalancer
  > status:
  >   loadBalancer:
  >     ingress:
  >     - ip: 192.0.2.127
  > ```
  > Le trafic provenant du load balancer externe est dirigé vers les Pods backend.
  > Le fournisseur de cloud décide de la répartition de la charge.
  > Le trafic provenant du load balancer externe est dirigé vers les Pods backend.
  > Le fournisseur de cloud décide de la répartition de la charge.
  > Certains fournisseurs de cloud vous permettent de spécifier le `loadBalancerIP`.
  > Dans ces cas, le load balancer est créé avec le `loadBalancerIP` spécifié par l'utilisateur.
  > Si le champ `loadBalancerIP` n'est pas spécifié, le loadBalancer est configuré avec une adresse IP éphémère.
  > Si vous spécifiez un `loadBalancerIP` mais que votre fournisseur de cloud ne prend pas en charge la fonctionnalité, le champ `loadBalancerIP` que vous définissez est ignoré.
  > Si vous utilisez SCTP, voir le caveat ci-dessous sur le type de service `LoadBalancer`.
  > Sur **Azure**, si vous souhaitez utiliser un type public spécifié par l'utilisateur … (section continues)

*Drafting note:* LLM pre-review (ChatGPT, 2026-11-07): claims confirmed in the full section text; answer unchanged | human review (Youssef Zemzem, 2026-11-07): ExternalName no longer described as external exposure

**Decision** (tick one):
- [ x] ✅ Correct as written
- [ ] ✏️ Needs changes (say what under Notes)
- [ ] ❌ Reject

**Notes:**


---
