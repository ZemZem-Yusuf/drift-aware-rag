> **LLM pre-review, not a human verification.** The decisions and notes below were produced by ChatGPT and were not checked by a person. They were used only to tighten the drafts (see each item's notes in `k8s-1.33.jsonl`); no item was marked verified from this pass.

# Golden set review

For each question below:

1. Read the **question**: would a real user ask this? Is it clear and about Kubernetes v1.33?

2. Read the **documentation excerpts**: do they really answer the question? Is an obviously

   better section missing?

3. Read the **reference answer**: is it correct *according to the excerpts*?

4. Tick **exactly one** box (replace `[ ]` with `[x]`). If you pick *Needs changes*, write what

   to change under **Notes**.

Out-of-scope questions only need a check that they really are outside the Kubernetes docs.

When done, run: `uv run driftrag-golden apply --reviewer "Your Name"`

---

### `restart-deployment`

**Question** (en, command): How do I restart all the pods of a Deployment without changing its spec?

**Reference answer:** Run `kubectl rollout restart deployment/<name>`. It triggers a rolling restart: Pods are replaced gradually with new ones using the same spec.

**Relevant documentation:**

- `reference/kubectl/generated/kubectl_rollout/kubectl_rollout_restart.md`, section: *(whole document)*

  > ##

  > Restart a resource.

  >         Resource rollout will be restarted.

  > ```

  > kubectl rollout restart RESOURCE

  > ```

  > ##

  > ```

  >   # Restart all deployments in the test-namespace namespace

  >   kubectl rollout restart deployment -n test-namespace

  >   # Restart a deployment

  >   kubectl rollout restart deployment/nginx

  >   # Restart a daemon set

  >   kubectl rollout restart daemonset/abc

  >   # Restart deployments with the app=nginx label

  >   kubectl rollout restart deployment --selector=app=nginx

  > ```

  > ##

  >    <table style="width: 100%; table-layout: fixed;">

  > <colgroup>

  > <col span="1" style="width: 10px;" />

  > <col span="1" />

  > </colgroup>

  > <tbody>

  > <tr>

  > <td …

*Drafting note:* Known hard case (E0): task wording vs command reference page.

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt documents the kubectl rollout restart command, but does not say that the Deployment spec remains unchanged or that Pods are replaced gradually using the same spec. Reword the question to ask how to trigger a Deployment restart, and remove those behavioral claims or add a supporting excerpt.

---

### `resource-limits`

**Question** (en, task): How do I cap the CPU and memory a container is allowed to use?

**Reference answer:** Set `resources.limits.cpu` and `resources.limits.memory` on the container (and usually `resources.requests` for scheduling). CPU above the limit is throttled; a container that exceeds its memory limit can be OOM-killed.

**Relevant documentation:**

- `concepts/configuration/manage-resources-containers.md`, section: *Resource Management for Pods and Containers > Requests and limits*

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

  > `cpu` limits …

- `concepts/configuration/manage-resources-containers.md`, section: *Resource Management for Pods and Containers > Container resources example*

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

  >   name: frontend

  > spec:

  >   containers:

  >   - name: app

  >     image: images.my-company.example/app:v4

  >     resources:

  >       requests:

  >         memory: "64Mi"

  >         cpu: "250m"

  >       limits:

  >         memory: "128Mi"

  >         cpu: "500m"

  >   - name: log-aggregator

  >     image: images.my-company.example/log-aggregator:v6

  >     resources:

  >       requests:

  >      …

*Drafting note:* Known partial answer in E0.

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The example supports setting resources.limits.cpu and resources.limits.memory. The supplied excerpt does not establish CPU throttling, memory OOM-kill behavior, or that requests are used for scheduling. Add the missing enforcement/scheduling excerpts or remove those claims.

---

### `probes-difference`

**Question** (en, concept): What's the difference between a liveness probe and a readiness probe?

**Reference answer:** A failing liveness probe makes the kubelet restart the container; a failing readiness probe removes the Pod from Service endpoints so it gets no traffic, without restarting it.

**Relevant documentation:**

- `concepts/configuration/liveness-readiness-startup-probes.md`, section: *(whole document)*

  > Kubernetes has various types of probes:

  > - Liveness probe

  > - Readiness probe

  > - Startup probe

- `concepts/workloads/pods/pod-lifecycle.md`, section: *Pod Lifecycle > Container probes*

  > A _probe_ is a diagnostic performed periodically by the kubelet

  > on a container. To perform a diagnostic, the kubelet either executes code within the container,

  > or makes a network request.

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

These excerpts only list probe types and define a probe as a periodic diagnostic. They do not explain the different effects of liveness and readiness failures (container restart versus removal from Service endpoints). Add the specific documentation paragraphs describing those behaviors.

---

### `configmap-env`

**Question** (en, task): How can I turn every key of a ConfigMap into environment variables in my container?

**Reference answer:** Use `envFrom` with a `configMapRef` naming the ConfigMap in the container spec.

**Relevant documentation:**

- `tasks/configure-pod-container/configure-pod-configmap.md`, section: *Configure a Pod to Use a ConfigMap > Configure all key-value pairs in a ConfigMap as container environment variables*

  > * Create a ConfigMap containing multiple key-value pairs.

  >   Create the ConfigMap:

  >   ```shell

  >   kubectl create -f https://kubernetes.io/examples/configmap/configmap-multikeys.yaml

  >   ```

  > * Use `envFrom` to define all of the ConfigMap's data as container environment variables. The

  >   key from the ConfigMap becomes the environment variable name in the Pod.

  >   Create the Pod:

  >   ```shell

  >   kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-envFrom.yaml

  >   ```

  >   Now, the Pod's output includes environment variables `SPECIAL_LEVEL=very` and

  >   `SPECIAL_TYPE=charm`.

  >   Once you're happy to move on, delete that Pod:

  >   ```shell

  >   kubectl delete pod dapi-test-pod --now

  >   ```

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt supports using envFrom to expose all ConfigMap keys as environment variables, but the configMapRef field and its YAML structure are not shown; the referenced example manifest is not quoted. Add the relevant YAML excerpt, or narrow the answer to the envFrom behavior explicitly documented here.

---

### `secret-encryption`

**Question** (en, concept): Are Kubernetes Secrets encrypted by default?

**Reference answer:** No. By default Secrets are stored unencrypted in etcd (values are only base64-encoded). Enable encryption at rest and restrict access with RBAC.

**Relevant documentation:**

- `concepts/configuration/secret.md`, section: *(whole document)*

  > A Secret is an object that contains a small amount of sensitive data such as

  > a password, a token, or a key. Such information might otherwise be put in a

  >  specification or in a

  > container image. Using a

  > Secret means that you don't need to include confidential data in your

  > application code.

  > Because Secrets can be created independently of the Pods that use them, there

  > is less risk of the Secret (and its data) being exposed during the workflow of

  > creating, viewing, and editing Pods. Kubernetes, and applications that run in

  > your cluster, can also take additional precautions with Secrets, such as avoiding

  > writing sensitive data to nonvolatile storage.

  > Secrets are similar to ConfigMaps

  > but are …

*Drafting note:* Common misconception; checks that the answer doesn't claim base64 is encryption.

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The supplied Secret excerpt describes sensitive data and general precautions, but does not say whether Secrets are stored unencrypted in etcd, whether values are base64-encoded, or how encryption at rest and RBAC apply. Add excerpts that directly support those claims, or remove them.

---

### `scale-deployment`

**Question** (en, command): How do I change the number of replicas of a Deployment from the command line?

**Reference answer:** `kubectl scale deployment/<name> --replicas=<n>`.

**Relevant documentation:**

- `concepts/workloads/controllers/deployment.md`, section: *Deployments > Scaling a Deployment*

  > You can scale a Deployment by using the following command:

  > ```shell

  > kubectl scale deployment/nginx-deployment --replicas=10

  > ```

  > The output is similar to this:

  > ```

  > deployment.apps/nginx-deployment scaled

  > ```

  > Assuming horizontal Pod autoscaling is enabled

  > in your cluster, you can set up an autoscaler for your Deployment and choose the minimum and maximum number of

  > Pods you want to run based on the CPU utilization of your existing Pods.

  > ```shell

  > kubectl autoscale deployment/nginx-deployment --min=10 --max=15 --cpu-percent=80

  > ```

  > The output is similar to this:

  > ```

  > deployment.apps/nginx-deployment scaled

  > ```

**Decision** (tick one):

- [x] ✅ Correct as written

- [ ] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

---

### `rollback-deployment`

**Question** (en, task): I deployed a broken version of my app. How do I go back to the previous version?

**Reference answer:** `kubectl rollout undo deployment/<name>` (optionally `--to-revision=<n>`); `kubectl rollout history` lists revisions.

**Relevant documentation:**

- `concepts/workloads/controllers/deployment.md`, section: *Deployments > Rolling Back a Deployment*

  > Sometimes, you may want to rollback a Deployment; for example, when the Deployment is not stable, such as crash looping.

  > By default, all of the Deployment's rollout history is kept in the system so that you can rollback anytime you want

  > (you can change that by modifying revision history limit).

  > A Deployment's revision is created when a Deployment's rollout is triggered. This means that the

  > new revision is created if and only if the Deployment's Pod template (`.spec.template`) is changed,

  > for example if you update the labels or container images of the template. Other updates, such as scaling the Deployment,

  > do not create a Deployment revision, so that you can facilitate simultaneous manual- …

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt explains when Deployment revisions are created and that rollout history is retained, but it does not show kubectl rollout undo, --to-revision, or kubectl rollout history. Add the relevant command examples, or limit the answer to the revision-history facts shown.

---

### `service-types`

**Question** (en, concept): When should I use a NodePort Service instead of ClusterIP or LoadBalancer?

**Reference answer:** ClusterIP is reachable only inside the cluster (default). NodePort opens a static port on every node for external access. LoadBalancer provisions an external load balancer from the cloud provider.

**Relevant documentation:**

- `concepts/services-networking/service.md`, section: *Service > Service type*

  > For some parts of your application (for example, frontends) you may want to expose a

  > Service onto an external IP address, one that's accessible from outside of your

  > cluster.

  > Kubernetes Service types allow you to specify what kind of Service you want.

  > The available `type` values and their behaviors are:

  > `ClusterIP`

  > : Exposes the Service on a cluster-internal IP. Choosing this value

  >   makes the Service only reachable from within the cluster. This is the

  >   default that is used if you don't explicitly specify a `type` for a Service.

  >   You can expose the Service to the public internet using an

  >   Ingress or a

  >   Gateway.

  > `NodePort`

  > : Exposes the Service on each Node's IP at a static port (the …

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt supports that ClusterIP is internal and the default, but the NodePort definition is cut off and no LoadBalancer definition is included. Add the complete NodePort and LoadBalancer excerpts before retaining those descriptions.

---

### `pod-pending`

**Question** (en, troubleshooting): My pod has been stuck in Pending for a long time. What can cause that?

**Reference answer:** The Pod can't be scheduled: usually not enough CPU or memory on any node, or a hostPort conflict. `kubectl describe pod` shows the scheduler's events explaining why.

**Relevant documentation:**

- `tasks/debug/debug-application/debug-pods.md`, section: *Debug Pods > Diagnosing the problem*

  > The first step in troubleshooting is triage. What is the problem?

  > Is it your Pods, your Replication Controller or your Service?

  >    * Debugging Pods

  >    * Debugging Replication Controllers

  >    * Debugging Services

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The quoted text only introduces Pod troubleshooting triage. It does not identify scheduling failures, CPU/memory shortages, hostPort conflicts, or the use of kubectl describe pod to inspect scheduler events. Add the relevant scheduling/troubleshooting excerpts.

---

### `crashloop`

**Question** (en, troubleshooting): My container keeps crashing and restarting in a loop. How do I find out why?

**Reference answer:** Check `kubectl describe pod` for the last state and exit code, and the logs of the crashed instance with `kubectl logs <pod> --previous`. The kubelet restarts it with an exponential back-off (CrashLoopBackOff).

**Relevant documentation:**

- `tasks/debug/debug-application/debug-pods.md`, section: *Debug Pods > Diagnosing the problem*

  > The first step in troubleshooting is triage. What is the problem?

  > Is it your Pods, your Replication Controller or your Service?

  >    * Debugging Pods

  >    * Debugging Replication Controllers

  >    * Debugging Services

- `concepts/workloads/pods/pod-lifecycle.md`, section: *Pod Lifecycle > How Pods handle problems with containers*

  > Kubernetes manages container failures within Pods using a `restartPolicy` defined in the Pod `spec`. This policy determines how Kubernetes reacts to containers exiting due to errors or other reasons, which falls in the following sequence:

  > 1. **Initial crash**: Kubernetes attempts an immediate restart based on the Pod `restartPolicy`.

  > 1. **Repeated crashes**: After the initial crash Kubernetes applies an exponential

  >    backoff delay for subsequent restarts, described in `restartPolicy`.

  >    This prevents rapid, repeated restart attempts from overloading the system.

  > 1. **CrashLoopBackOff state**: This indicates that the backoff delay mechanism is currently

  >    in effect for a given container …

- `tasks/debug/debug-application/debug-running-pod.md`, section: *Debug Running Pods > Examining pod logs*

  > First, look at the logs of the affected container:

  > ```shell

  > kubectl logs ${POD_NAME} ${CONTAINER_NAME}

  > ```

  > If your container has previously crashed, you can access the previous container's crash log with:

  > ```shell

  > kubectl logs --previous ${POD_NAME} ${CONTAINER_NAME}

  > ```

*Drafting note:* User says 'crashing in a loop'; docs say CrashLoopBackOff.

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpts support exponential backoff/CrashLoopBackOff and kubectl logs --previous. They do not support the advice to use kubectl describe pod to inspect the last state and exit code. Add an excerpt for that diagnostic or remove it; keep the backoff wording aligned with the source.

---

### `pvc-request-storage`

**Question** (en, concept): How does a pod ask for persistent storage that survives restarts?

**Reference answer:** Create a PersistentVolumeClaim (size, access mode, optional StorageClass) and reference it as a volume in the Pod spec; it binds to a matching PersistentVolume.

**Relevant documentation:**

- `concepts/storage/persistent-volumes.md`, section: *Persistent Volumes > PersistentVolumeClaims*

  > Each PVC contains a spec and status, which is the specification and status of the claim.

  > The name of a PersistentVolumeClaim object must be a valid

  > DNS subdomain name.

  > ```yaml

  > apiVersion: v1

  > kind: PersistentVolumeClaim

  > metadata:

  >   name: myclaim

  > spec:

  >   accessModes:

  >     - ReadWriteOnce

  >   volumeMode: Filesystem

  >   resources:

  >     requests:

  >       storage: 8Gi

  >   storageClassName: slow

  >   selector:

  >     matchLabels:

  >       release: "stable"

  >     matchExpressions:

  >       - {key: environment, operator: In, values: [dev]}

  > ```

- `concepts/storage/persistent-volumes.md`, section: *Persistent Volumes > Claims As Volumes*

  > Pods access storage by using the claim as a volume. Claims must exist in the

  > same namespace as the Pod using the claim. The cluster finds the claim in the

  > Pod's namespace and uses it to get the PersistentVolume backing the claim.

  > The volume is then mounted to the host and into the Pod.

  > ```yaml

  > apiVersion: v1

  > kind: Pod

  > metadata:

  >   name: mypod

  > spec:

  >   containers:

  >     - name: myfrontend

  >       image: nginx

  >       volumeMounts:

  >       - mountPath: "/var/www/html"

  >         name: mypd

  >   volumes:

  >     - name: mypd

  >       persistentVolumeClaim:

  >         claimName: myclaim

  > ```

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpts support the PVC fields shown (storage request, access mode, and StorageClass) and using a claim as a Pod volume. They do not explicitly explain matching-PersistentVolume binding or state that the data survives restarts. Add documentation excerpts for those claims, or narrow the answer to the demonstrated PVC/volume workflow.

---

### `namespaces-when`

**Question** (en, concept): When does it make sense to split a cluster into multiple namespaces?

**Reference answer:** When many users or teams share a cluster; namespaces scope names and let you apply quotas and access policies. Not needed to separate slightly different versions of an app.

**Relevant documentation:**

- `concepts/overview/working-with-objects/namespaces.md`, section: *Namespaces > When to Use Multiple Namespaces*

  > Namespaces are intended for use in environments with many users spread across multiple

  > teams, or projects.  For clusters with a few to tens of users, you should not

  > need to create or think about namespaces at all.  Start using namespaces when you

  > need the features they provide.

  > Namespaces provide a scope for names.  Names of resources need to be unique within a namespace,

  > but not across namespaces. Namespaces cannot be nested inside one another and each Kubernetes

  > resource can only be in one namespace.

  > Namespaces are a way to divide cluster resources between multiple users (via resource quota).

  > It is not necessary to use multiple namespaces to separate slightly different

  > resources, such …

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpts support multiple teams/users, name scoping, and resource quotas. They do not mention access policies. Remove “access policies” or add a relevant RBAC/authorization excerpt.

---

### `taint-dedicated-node`

**Question** (en, concept): How can I keep ordinary pods from being scheduled on a particular node?

**Reference answer:** Taint the node (e.g. `kubectl taint nodes <node> key=value:NoSchedule`); only Pods with a matching toleration can be scheduled there.

**Relevant documentation:**

- `concepts/scheduling-eviction/taint-and-toleration.md`, section: *(whole document)*

  > _Node affinity_

  > is a property of Pods that *attracts* them to

  > a set of nodes (either as a preference or a

  > hard requirement). _Taints_ are the opposite -- they allow a node to repel a set of pods.

  > _Tolerations_ are applied to pods. Tolerations allow the scheduler to schedule pods with matching

  > taints. Tolerations allow scheduling but don't guarantee scheduling: the scheduler also

  > evaluates other parameters

  > as part of its function.

  > Taints and tolerations work together to ensure that pods are not scheduled

  > onto inappropriate nodes. One or more taints are applied to a node; this

  > marks that the node should not accept any pods that do not tolerate the taints.

*Drafting note:* Vocabulary gap: user doesn't say 'taint'.

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt explains that taints repel Pods without matching tolerations and that tolerations permit scheduling, but it does not show the kubectl taint nodes ... command. Add the command example. Also avoid implying a toleration guarantees placement: the excerpt says the scheduler evaluates other parameters too.

---

### `node-selector-ssd`

**Question** (en, task): How do I make a pod run only on nodes that have an SSD?

**Reference answer:** Label the SSD nodes (e.g. `disktype=ssd`) and set `nodeSelector` (or node affinity) in the Pod spec to that label.

**Relevant documentation:**

- `concepts/scheduling-eviction/assign-pod-node.md`, section: *Assigning Pods to Nodes > nodeSelector*

  > `nodeSelector` is the simplest recommended form of node selection constraint.

  > You can add the `nodeSelector` field to your Pod specification and specify the

  > node labels you want the target node to have.

  > Kubernetes only schedules the Pod onto nodes that have each of the labels you

  > specify.

  > See Assign Pods to Nodes for more

  > information.

- `concepts/scheduling-eviction/assign-pod-node.md`, section: *Assigning Pods to Nodes > Affinity and anti-affinity*

  > `nodeSelector` is the simplest way to constrain Pods to nodes with specific

  > labels. Affinity and anti-affinity expand the types of constraints you can

  > define. Some of the benefits of affinity and anti-affinity include:

  > - The affinity/anti-affinity language is more expressive. `nodeSelector` only

  >   selects nodes with all the specified labels. Affinity/anti-affinity gives you

  >   more control over the selection logic.

  > - You can indicate that a rule is *soft* or *preferred*, so that the scheduler

  >   still schedules the Pod even if it can't find a matching node.

  > - You can constrain a Pod using labels on other Pods running on the node (or other topological domain),

  >   instead of just node labels, …

**Decision** (tick one):

- [x] ✅ Correct as written

- [ ] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

---

### `hpa-cpu`

**Question** (en, concept): How can Kubernetes add more pods automatically when CPU usage goes up?

**Reference answer:** A HorizontalPodAutoscaler periodically compares observed metrics (e.g. average CPU utilisation) with a target and adjusts the replicas of the Deployment.

**Relevant documentation:**

- `tasks/run-application/horizontal-pod-autoscale.md`, section: *(whole document)*

  > In Kubernetes, a _HorizontalPodAutoscaler_ automatically updates a workload resource (such as

  > a Deployment or

  > StatefulSet), with the

  > aim of automatically scaling the workload to match demand.

  > Horizontal scaling means that the response to increased load is to deploy more

  > Pods.

  > This is different from _vertical_ scaling, which for Kubernetes would mean

  > assigning more resources (for example: memory or CPU) to the Pods that are already

  > running for the workload.

  > If the load decreases, and the number of Pods is above the configured minimum,

  > the HorizontalPodAutoscaler instructs the workload resource (the Deployment, StatefulSet,

  > or other similar resource) to scale back down.

  > Horizontal pod …

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt supports that an HPA automatically scales a workload to match demand, but it does not describe periodic metric comparison, CPU utilization, or a target value. Add the relevant metrics/algorithm passage or narrow the answer to the automatic workload-scaling behavior shown.

---

### `ingress-vs-service`

**Question** (en, concept): What is an Ingress and how is it different from a Service?

**Reference answer:** An Ingress exposes HTTP(S) routes from outside the cluster to Services, with host/path rules and TLS; it needs an ingress controller. A Service gives a stable endpoint for a set of Pods.

**Relevant documentation:**

- `concepts/services-networking/ingress.md`, section: *Ingress > What is Ingress?*

  > Ingress

  > exposes HTTP and HTTPS routes from outside the cluster to

  >  within the cluster.

  > Traffic routing is controlled by rules defined on the Ingress resource.

  > Here is a simple example where an Ingress sends all its traffic to one Service:

  > An Ingress may be configured to give Services externally-reachable URLs,

  > load balance traffic, terminate SSL / TLS, and offer name-based virtual hosting.

  > An Ingress controller

  > is responsible for fulfilling the Ingress, usually with a load balancer, though

  > it may also configure your edge router or additional frontends to help handle the traffic.

  > An Ingress does not expose arbitrary ports or protocols. Exposing services other than HTTP and HTTPS to the …

- `concepts/services-networking/ingress.md`, section: *Ingress > Terminology*

  > For clarity, this guide defines the following terms:

  > * Node: A worker machine in Kubernetes, part of a cluster.

  > * Cluster: A set of Nodes that run containerized applications managed by Kubernetes.

  >   For this example, and in most common Kubernetes deployments, nodes in the cluster

  >   are not part of the public internet.

  > * Edge router: A router that enforces the firewall policy for your cluster. This

  >   could be a gateway managed by a cloud provider or a physical piece of hardware.

  > * Cluster network: A set of links, logical or physical, that facilitate communication

  >   within a cluster according to the Kubernetes networking model.

  > * Service: A Kubernetes  that identifies

  >   a set of Pods using …

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpts support HTTP(S) exposure, Ingress rules/controller, and TLS termination. They do not fully establish host/path rule behavior or that a Service provides a stable endpoint for a set of Pods (the Service definition is truncated). Add the corresponding Ingress-rules and Service-definition excerpts, or remove those unsupported details.

---

### `netpol-default-deny`

**Question** (en, task): How do I block all incoming traffic to the pods in a namespace by default?

**Reference answer:** Create a NetworkPolicy with an empty `podSelector` and `policyTypes: [Ingress]` and no ingress rules. Requires a network plugin that enforces NetworkPolicy.

**Relevant documentation:**

- `concepts/services-networking/network-policies.md`, section: *Network Policies > Default policies*

  > By default, if no policies exist in a namespace, then all ingress and egress traffic is allowed to

  > and from pods in that namespace. The following examples let you change the default behavior

  > in that namespace.

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt only states that, when no policies exist, ingress and egress are allowed by default. It does not show the default-deny policy YAML (podSelector, policyTypes, and absent ingress rules) or the network-plugin enforcement caveat. Add excerpts for the example and implementation requirement.

---

### `daemonset-agent`

**Question** (en, concept): How do I run exactly one copy of a log collector on every node of the cluster?

**Reference answer:** Use a DaemonSet: it runs one Pod per (matching) node and adds Pods to new nodes automatically.

**Relevant documentation:**

- `concepts/workloads/controllers/daemonset.md`, section: *(whole document)*

  > A _DaemonSet_ ensures that all (or some) Nodes run a copy of a Pod.  As nodes are added to the

  > cluster, Pods are added to them.  As nodes are removed from the cluster, those Pods are garbage

  > collected.  Deleting a DaemonSet will clean up the Pods it created.

  > Some typical uses of a DaemonSet are:

  > - running a cluster storage daemon on every node

  > - running a logs collection daemon on every node

  > - running a node monitoring daemon on every node

  > In a simple case, one DaemonSet, covering all nodes, would be used for each type of daemon.

  > A more complex setup might use multiple DaemonSets for a single type of daemon, but with

  > different flags and/or different memory and cpu requests for different …

*Drafting note:* Vocabulary gap: user doesn't say 'DaemonSet'.

**Decision** (tick one):

- [x] ✅ Correct as written

- [ ] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

---

### `statefulset-database`

**Question** (en, concept): Why would I use a StatefulSet instead of a Deployment for a database?

**Reference answer:** StatefulSets give each Pod a stable identity (name, network ID) and its own persistent storage, with ordered deployment and scaling; Deployments treat Pods as interchangeable.

**Relevant documentation:**

- `concepts/workloads/controllers/statefulset.md`, section: *StatefulSets > Using StatefulSets*

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

  > StatefulSet Pods have a unique identity that consists of an ordinal, a

  > stable network identity, and stable storage. The identity sticks to the Pod,

  > regardless of which node it's (re)scheduled on.

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpts support stable network identity, stable storage, and ordered deployment/scaling. They do not state that Deployments treat Pods as interchangeable. Remove that comparison or add a Deployment excerpt that supports it.

---

### `cronjob-nightly`

**Question** (en, task): How do I run a job every night at 2 am?

**Reference answer:** Create a CronJob with `schedule: "0 2 * * *"` (cron syntax; `timeZone` can set the time zone).

**Relevant documentation:**

- `concepts/workloads/controllers/cron-jobs.md`, section: *CronJob > Writing a CronJob spec*

  > The `.spec.schedule` field is required. The value of that field follows the Cron syntax:

  > ```

  > # ┌───────────── minute (0 - 59)

  > # │ ┌───────────── hour (0 - 23)

  > # │ │ ┌───────────── day of the month (1 - 31)

  > # │ │ │ ┌───────────── month (1 - 12)

  > # │ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)

  > # │ │ │ │ │                                   OR sun, mon, tue, wed, thu, fri, sat

  > # │ │ │ │ │

  > # │ │ │ │ │

  > # * * * * *

  > ```

  > For example, `0 3 * * 1` means this task is scheduled to run weekly on a Monday at 3 AM.

  > The format also includes extended "Vixie cron" step values. As explained in the

  > FreeBSD manual:

  > > Step values can be used in conjunction with ranges. Following a range

  > > …

- `concepts/workloads/controllers/cron-jobs.md`, section: *CronJob > Example*

  > This example CronJob manifest prints the current time and a hello message every minute:

  > (Running Automated Tasks with a CronJob

  > takes you through this example in more detail).

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt documents the five-field Cron schedule syntax, but it does not document the timeZone field. Remove the timezone aside or add the Kubernetes v1.33 timeZone documentation excerpt. An explicit daily-at-2-AM schedule example would also make the expression directly verifiable.

---

### `rbac-role-clusterrole`

**Question** (en, concept): What is the difference between a Role and a ClusterRole?

**Reference answer:** A Role grants permissions within one namespace; a ClusterRole is cluster-wide and can cover cluster-scoped resources or be reused across namespaces via RoleBindings.

**Relevant documentation:**

- `reference/access-authn-authz/rbac.md`, section: *Using RBAC Authorization > API objects*

  > The RBAC API declares four kinds of Kubernetes object: _Role_, _ClusterRole_,

  > _RoleBinding_ and _ClusterRoleBinding_. You can describe or amend the RBAC

  > objects

  > using tools such as `kubectl`, just like any other Kubernetes object.

  > These objects, by design, impose access restrictions. If you are making changes

  > to a cluster as you learn, see

  > privilege escalation prevention and bootstrapping

  > to understand how those restrictions can prevent you making some changes.

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt only lists Role, ClusterRole, RoleBinding, and ClusterRoleBinding as RBAC API objects. It does not define namespace versus cluster scope or explain reusing a ClusterRole through RoleBindings. Add the API-object definitions excerpt.

---

### `drain-node`

**Question** (en, command): How do I safely take a node offline for maintenance?

**Reference answer:** `kubectl drain <node> --ignore-daemonsets` evicts Pods (respecting PodDisruptionBudgets) and cordons the node; `kubectl uncordon <node>` afterwards.

**Relevant documentation:**

- `tasks/administer-cluster/safely-drain-node.md`, section: *Safely Drain a Node > Use `kubectl drain` to remove a node from service*

  > You can use `kubectl drain` to safely evict all of your pods from a

  > node before you perform maintenance on the node (e.g. kernel upgrade,

  > hardware maintenance, etc.). Safe evictions allow the pod's containers

  > to gracefully terminate

  > and will respect the PodDisruptionBudgets you have specified.

  > By default `kubectl drain` ignores certain system pods on the node

  > that cannot be killed; see

  > the kubectl drain

  > documentation for more details.

  > When `kubectl drain` returns successfully, that indicates that all of

  > the pods (except the ones excluded as described in the previous paragraph)

  > have been safely evicted (respecting the desired graceful termination period,

  > and respecting the …

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt supports safely evicting Pods and respecting PodDisruptionBudgets, but it does not show --ignore-daemonsets, state that drain cordons the node, or provide kubectl uncordon. Add the relevant command/options and cordon/uncordon excerpts, or remove those claims.

---

### `init-container-setup`

**Question** (en, concept): How can I make sure a setup step finishes before my app container starts?

**Reference answer:** Use init containers: they run to completion, one after another, before the app containers start.

**Relevant documentation:**

- `concepts/workloads/pods/init-containers.md`, section: *(whole document)*

  > This page provides an overview of init containers: specialized containers that run

  > before app containers in a Pod.

  > Init containers can contain utilities or setup scripts not present in an app image.

  > You can specify init containers in the Pod specification alongside the `containers`

  > array (which describes app containers).

  > In Kubernetes, a sidecar container is a container that

  > starts before the main application container and _continues to run_. This document is about init containers:

  > containers that run to completion during Pod initialization.

*Drafting note:* Vocabulary gap: user doesn't say 'init container'.

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt supports that init containers run before app containers and run to completion during Pod initialization. It does not state that they run one after another. Remove the sequential-order claim or add the excerpt that documents the ordering.

---

### `image-pull-policy`

**Question** (en, concept): When does the kubelet pull an image again instead of using the cached one?

**Reference answer:** It depends on `imagePullPolicy`: `Always` pulls each time, `IfNotPresent` uses the local copy, `Never` never pulls. With the `:latest` tag or no tag the default is `Always`.

**Relevant documentation:**

- `concepts/containers/images.md`, section: *Images > Updating images*

  > When you first create a Deployment,

  > StatefulSet, Pod, or other

  > object that includes a PodTemplate, and a pull policy was not explicitly specified,

  > then by default the pull policy of all containers in that Pod will be set to

  > `IfNotPresent`. This policy causes the

  > kubelet to skip pulling an

  > image if it already exists.

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt only documents the default IfNotPresent policy when no policy is specified and says it skips pulling an image that already exists. It does not support the Always/`Never` behavior or the :latest/untagged default claim. Add the relevant policy/defaulting excerpts or narrow the answer to what is shown.

---

### `pdb-keep-replicas`

**Question** (en, task): How do I make sure at least two replicas stay up while nodes are being drained?

**Reference answer:** Create a PodDisruptionBudget with `minAvailable: 2` selecting the Pods; voluntary evictions such as `kubectl drain` respect it.

**Relevant documentation:**

- `concepts/workloads/pods/disruptions.md`, section: *Disruptions > Pod disruption budgets*

  > Kubernetes offers features to help you run highly available applications even when you

  > introduce frequent voluntary disruptions.

  > As an application owner, you can create a PodDisruptionBudget (PDB) for each application.

  > A PDB limits the number of Pods of a replicated application that are down simultaneously from

  > voluntary disruptions. For example, a quorum-based application would

  > like to ensure that the number of replicas running is never brought below the

  > number needed for a quorum. A web front end might want to

  > ensure that the number of replicas serving load never falls below a certain

  > percentage of the total.

  > Cluster managers and hosting providers should use tools which

  > respect …

- `tasks/administer-cluster/safely-drain-node.md`, section: *Safely Drain a Node > (Optional) Configure a disruption budget*

  > To ensure that your workloads remain available during maintenance, you can

  > configure a PodDisruptionBudget.

  > If availability is important for any applications that run or could run on the node(s)

  > that you are draining, configure a PodDisruptionBudgets

  > first and then continue following this guide.

  > It is recommended to set `AlwaysAllow` Unhealthy Pod Eviction Policy

  > to your PodDisruptionBudgets to support eviction of misbehaving applications during a node drain.

  > The default behavior is to wait for the application pods to become healthy

  > before the drain can proceed.

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpts explain that a PDB limits Pods down during voluntary disruptions and mention configuring a PDB before draining. They do not show a minAvailable: 2 manifest field or Pod selector, and the quoted text does not explicitly show the drain eviction behavior claimed. Add the PDB example/selector and drain-respect excerpts.

---

### `fr-pod-multi-container`

**Question** (fr, concept): Qu'est-ce qu'un Pod et pourquoi peut-il contenir plusieurs conteneurs ?

**Reference answer:** Un Pod est la plus petite unité déployable ; il regroupe un ou plusieurs conteneurs qui partagent le réseau et le stockage, pour des conteneurs étroitement liés.

**Relevant documentation:**

- `concepts/workloads/pods/pod-overview.md`, section: *Aperçu du Pod > Comprendre les Pods*

  > Un *Pod* est l'unité d'exécution de base d'une application Kubernetes--l'unité la plus petite et la plus simple dans le modèle d'objets de Kubernetes--que vous créez ou déployez. Un Pod représente des process en cours d'exécution dans votre cluster.

  > Un Pod encapsule un conteneur applicatif (ou, dans certains cas, plusieurs conteneurs), des ressources de stockage, une identité réseau (adresse IP) unique, ainsi que des options qui contrôlent comment le ou les conteneurs doivent s'exécuter. Un Pod représente une unité de déploiement : *une instance unique d'une application dans Kubernetes*, qui peut consister soit en un unique container soit en un petit nombre de conteneurs qui sont …

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt supports that a Pod is the smallest deployable unit, can contain multiple containers, and encapsulates storage resources and a network identity. It does not explicitly say the containers share the network and storage or that they are tightly coupled. Add the relevant sharing explanation or narrow the answer to the facts shown.

---

### `fr-rollback`

**Question** (fr, task): Comment revenir à la version précédente d'un déploiement ?

**Reference answer:** `kubectl rollout undo deployment/<nom>` (option `--to-revision`).

**Relevant documentation:**

- `concepts/workloads/controllers/deployment.md`, section: *Déploiements > Annulation d'un déploiement*

  > Parfois, vous souhaiterez peut-être annuler un déploiement; par exemple, lorsque le déploiement n'est pas stable, comme en cas d'échecs à répétition (CrashLoopBackOff).

  > Par défaut, tout l'historique des déploiements d'un déploiement est conservé dans le système afin que vous puissiez le restaurer à tout moment (vous pouvez le modifier en modifiant la limite de l'historique des révisions).

  > La révision d'un déploiement est créée lorsque le déploiement d'un déploiement est déclenché.

  > Cela signifie qu'une nouvelle révision est créée si et seulement si le template de pod de déploiement (`.spec.template`) est modifié, par exemple si vous mettez à jour les labels ou les images de conteneur du …

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt describes rollback use and Deployment revision history, but does not show kubectl rollout undo or the --to-revision option. Add the command example excerpt or remove the command-level claims.

---

### `fr-scale`

**Question** (fr, command): Comment changer le nombre de réplicas d'un déploiement ?

**Reference answer:** `kubectl scale deployment/<nom> --replicas=<n>`.

**Relevant documentation:**

- `concepts/workloads/controllers/deployment.md`, section: *Déploiements > Mise à l'échelle d'un déploiement*

  > Vous pouvez mettre à l'échelle un déploiement à l'aide de la commande suivante:

  > ```shell

  > kubectl scale deployment.v1.apps/nginx-deployment --replicas=10

  > ```

  > La sortie est similaire à ceci:

  > ```text

  > deployment.apps/nginx-deployment scaled

  > ```

  > En supposant que l'horizontal Pod autoscaling est activé dans votre cluster, vous pouvez configurer une mise à l'échelle automatique pour votre déploiement et choisir le nombre minimum et maximum de pods que vous souhaitez exécuter en fonction de l'utilisation du processeur de vos pods existants.

  > ```shell

  > kubectl autoscale deployment.v1.apps/nginx-deployment --min=10 --max=15 --cpu-percent=80

  > ```

  > La sortie est similaire à …

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt shows kubectl scale deployment.v1.apps/<name> --replicas=<n>. It does not show the shortened deployment/<name> resource form used in the answer. Use the exact documented syntax or add an excerpt demonstrating the shorthand.

---

### `fr-service-types`

**Question** (fr, concept): Quels types de Service permettent d'exposer une application en dehors du cluster ?

**Reference answer:** NodePort, LoadBalancer et ExternalName ; ClusterIP (par défaut) reste interne au cluster.

**Relevant documentation:**

- `concepts/services-networking/service.md`, section: *Service > Services de publication (ServiceTypes)*

  > Pour certaines parties de votre application (par exemple, les frontaux), vous souhaiterez peut-être exposer un service sur une adresse IP externe, qui est en dehors de votre cluster.

  > Les «ServiceTypes» de Kubernetes vous permettent de spécifier le type de service que vous souhaitez.

  > La valeur par défaut est «ClusterIP».

  > Les valeurs de `Type` et leurs comportements sont:

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpt says ClusterIP is the default and introduces Service type behaviors, but it is cut off before defining the types. It does not support the NodePort, LoadBalancer, or ExternalName claims. Add the complete ServiceTypes definitions or narrow the answer to the supported default statement.

---

### `fr-labels-selectors`

**Question** (fr, concept): À quoi servent les labels et les sélecteurs dans Kubernetes ?

**Reference answer:** Les labels sont des paires clé/valeur attachées aux objets pour les organiser ; les sélecteurs permettent de choisir un ensemble d'objets par leurs labels.

**Relevant documentation:**

- `concepts/overview/working-with-objects/labels.md`, section: *Labels et sélecteurs > Motivation*

  > Les labels permettent aux utilisateurs de mapper leurs propres structures organisationnelles sur les objets système de manière lâchement couplée, sans nécessiter aux clients de stocker ces mappings.

  > Les déploiements de services et les pipelines de traitement par lots sont souvent des entités multidimensionnelles (par exemple, plusieurs partitions ou déploiements, plusieurs pistes de version, plusieurs niveaux, plusieurs micro-services par niveau). La gestion nécessite souvent des opérations transversales, ce qui rompt l'encapsulation des représentations strictement hiérarchiques, en particulier les hiérarchies rigides déterminées par l'infrastructure plutôt que par les …

- `concepts/overview/working-with-objects/labels.md`, section: *Labels et sélecteurs > Sélecteurs de labels*

  > Contrairement aux noms et UIDs, les labels ne garantissent pas l'unicité. En général, nous nous attendons à ce que de nombreux objets portent les mêmes label(s).

  > Via un _sélecteur de label_, le client/utilisateur peut identifier un ensemble d'objets.

  > Le sélecteur de label est le principe de regroupement central dans Kubernetes.

  > L'API prend actuellement en charge deux types de sélecteurs : _basés sur l'égalité_ et _basés sur un ensemble_.

  > Un sélecteur de label peut être composé de plusieurs _exigences_ séparées par des virgules.

  > Dans le cas de plusieurs exigences, toutes doivent être satisfaites, donc le séparateur de virgule

  > agit comme un opérateur logique _ET_ (`&&`).

  > La signification …

**Decision** (tick one):

- [ ] ✅ Correct as written

- [x] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

The excerpts support labels as organizational mappings and selectors as a way to identify sets of objects. They do not include the definition of labels as key/value pairs attached to objects. Add the labels-definition excerpt or revise that clause.

---

### `oos-capital`

**Question** (en, out-of-scope): What is the capital of France?

**Decision** (tick one):

- [x] ✅ Correct as written

- [ ] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

Confirmed: this is a geography question about France, not a Kubernetes question.

---

### `oos-python`

**Question** (en, out-of-scope): Write a Python function that reverses a string.

**Decision** (tick one):

- [x] ✅ Correct as written

- [ ] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

Confirmed: this is a general Python programming task, not a Kubernetes question.

---

### `oos-docker-swarm`

**Question** (en, out-of-scope): How do I create an overlay network in Docker Swarm?

*Drafting note:* Adjacent domain: containers, but not Kubernetes.

**Decision** (tick one):

- [x] ✅ Correct as written

- [ ] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

Confirmed: this asks about Docker Swarm networking, not Kubernetes.

---

### `oos-meteo`

**Question** (fr, out-of-scope): Quel temps fera-t-il à Paris demain ?

**Decision** (tick one):

- [x] ✅ Correct as written

- [ ] ✏️ Needs changes (say what under Notes)

- [ ] ❌ Reject

**Notes:**

Confirmed: this is a weather question about Paris, not a Kubernetes question.

---