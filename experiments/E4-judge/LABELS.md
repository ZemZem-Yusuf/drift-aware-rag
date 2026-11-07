<!-- answers: experiments/E4-judge/results/20261107T152454Z-answers.json -->
# Answer labelling (E4)

For each answer below, read the question, the reference answer, the system's answer and the
sources the model was given. Then tick **one box per line**:

- **Supported by the sources**: *yes* only if **every** statement in the answer is backed by
  the sources shown. Anything from outside knowledge, a wrong detail or a contradiction: *no*.
  Judge against the sources, not against what you know about Kubernetes.
- **Correct answer to the question**: *yes* if it answers the question and agrees with the
  reference answer on what matters. Wrong, missing the main point, or answering something
  else: *no*. For an out-of-scope question, an answer is never correct (it should have refused).
- **Refusal justified** (only for refusals): *yes* if the sources really don't contain the
  answer; *no* if they do and the model should have answered.

Supported and correct are separate questions: an answer can faithfully repeat the wrong sources
(supported, not correct), or be right from outside knowledge (correct, not supported).
Write anything worth remembering under **Notes** (optional).

When done, run: `uv run driftrag-label apply --labeller "Your Name"`

---

### `restart-deployment`

**Question** (en, command): How do I trigger a restart of all the pods in a Deployment?

**Reference answer:** Use `kubectl rollout restart deployment/<name>` (documented example: `kubectl rollout restart deployment/nginx`).

**System answer:**

> To trigger a restart of all Pods in a Deployment, you need to update the Deployment's Pod template (`PodTemplateSpec`) [1][2]. This causes the old Pods to be terminated and replaced by new ones [3][4][5]. Pods are replaced by new, near-identical Pods, rather than being rescheduled [5].
>
> For example, you can patch a Deployment to update its Pod template using a command like:
> ```shell
> kubectl patch deployment patch-demo --patch-file patch-file.yaml
> ```
> where `patch-file.yaml` contains the desired changes to `spec.template.spec.containers` [3].

**Sources the model was given:**

**[1]** `concepts/workloads/controllers/deployment.md`, *Deployments > Updating a Deployment* **(cited)**

> * Running `get pods` should now show only the new Pods:
>
>   ```shell
>   kubectl get pods
>   ```
>
>   The output is similar to this:
>   ```
>   NAME                                READY     STATUS    RESTARTS   AGE
>   nginx-deployment-1564180365-khku8   1/1       Running   0          14s
>   nginx-deployment-1564180365-nacti   1/1       Running   0          14s
>   nginx-deployment-1564180365-z9gth   1/1       Running   0          14s
>   ```
>
>   Next time you want to update these Pods, you only need to update the Deployment's Pod template again.
>
>   Deployment ensures that only a certain number of Pods are down while they are being updated. By default,
>   it ensures that at least 75% of the desired number of Pods are up (25% max unavailable).
>
>   Deployment also ensures that only a certain number of Pods are created above the desired number of Pods.
>   By default, it ensures that at most 125% of the desired number of Pods are up (25% max surge).

**[2]** `concepts/workloads/controllers/deployment.md`, *Deployments > Use Case* **(cited)**

> The following are typical use cases for Deployments:
>
> * Create a Deployment to rollout a ReplicaSet. The ReplicaSet creates Pods in the background. Check the status of the rollout to see if it succeeds or not.
> * Declare the new state of the Pods by updating the PodTemplateSpec of the Deployment. A new ReplicaSet is created and the Deployment manages moving the Pods from the old ReplicaSet to the new one at a controlled rate. Each new ReplicaSet updates the revision of the Deployment.
> * Rollback to an earlier Deployment revision if the current state of the Deployment is not stable. Each rollback updates the revision of the Deployment.
> * Scale up the Deployment to facilitate more load.
> * Pause the rollout of a Deployment to apply multiple fixes to its PodTemplateSpec and then resume it to start a new rollout.
> * Use the status of the Deployment as an indicator that a rollout has stuck.
> * Clean up older ReplicaSets that you don't need anymore.

**[3]** `tasks/manage-kubernetes-objects/update-api-object-kubectl-patch.md`, *Update API Objects in Place Using kubectl patch > Use a strategic merge patch to update a Deployment* **(cited)**

> Here's the configuration file for a Deployment that has two replicas. Each replica
> is a Pod that has one container:
>
> Create the Deployment:
>
> ```shell
> kubectl apply -f https://k8s.io/examples/application/deployment-patch.yaml
> ```
>
> View the Pods associated with your Deployment:
>
> ```shell
> kubectl get pods
> ```
>
> The output shows that the Deployment has two Pods. The `1/1` indicates that
> each Pod has one container:
>
> ```
> NAME                        READY     STATUS    RESTARTS   AGE
> patch-demo-28633765-670qr   1/1       Running   0          23s
> patch-demo-28633765-j5qs3   1/1       Running   0          23s
> ```
>
> Make a note of the names of the running Pods. Later, you will see that these Pods
> get terminated and replaced by new ones.
>
> At this point, each Pod has one Container that runs the nginx image. Now suppose
> you want each Pod to have two containers: one that runs nginx and one that runs redis.
>
> Create a file named `patch-file.yaml` that has this content:
>
> ```yaml
> spec:
>   template:
>     spec:
>       containers:
>       - name: patch-demo-ctr-2
>         image: redis
> ```
>
> Patch your Deployment:
>
> ```shell
> kubectl patch deployment patch-demo --patch-file patch-file.yaml
> ```

**[4]** `concepts/workloads/controllers/deployment.md`, *Deployments > Updating a Deployment* **(cited)**

> For example, if you look at the above Deployment closely, you will see that it first creates a new Pod,
>   then deletes an old Pod, and creates another new one. It does not kill old Pods until a sufficient number of
>   new Pods have come up, and does not create new Pods until a sufficient number of old Pods have been killed.
>   It makes sure that at least 3 Pods are available and that at max 4 Pods in total are available. In case of
>   a Deployment with 4 replicas, the number of Pods would be between 3 and 5.

**[5]** `concepts/workloads/pods/pod-lifecycle.md`, *Pod Lifecycle > Pod lifetime > Pods and fault recovery {#pod-fault-recovery}* **(cited)**

> If one of the containers in the Pod fails, then Kubernetes may try to restart that
> specific container.
> Read How Pods handle problems with containers to learn more.
>
> Pods can however fail in a way that the cluster cannot recover from, and in that case
> Kubernetes does not attempt to heal the Pod further; instead, Kubernetes deletes the
> Pod and relies on other components to provide automatic healing.
>
> If a Pod is scheduled to a node and that
> node then fails, the Pod is treated as unhealthy and Kubernetes eventually deletes the Pod.
> A Pod won't survive an eviction due to
> a lack of resources or Node maintenance.
>
> Kubernetes uses a higher-level abstraction, called a
> controller, that handles the work of
> managing the relatively disposable Pod instances.
>
> A given Pod (as defined by a UID) is never "rescheduled" to a different node; instead,
> that Pod can be replaced by a new, near-identical Pod. If you make a replacement Pod, it can
> even have same name (as in `.metadata.name`) that the old Pod had, but the replacement
> would have a different `.metadata.uid` from the old Pod.

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `resource-limits`

**Question** (en, task): How do I cap the CPU and memory a container is allowed to use?

**Reference answer:** Set `resources.limits.cpu` and `resources.limits.memory` on the container. CPU use above the limit is throttled; a container that exceeds its memory limit can be OOM-killed. `resources.requests` are what the scheduler uses to pick a node.

**System answer:**

> CPU and memory limits are enforced by the kubelet and container runtime, ultimately by the kernel [2]. On Linux nodes, the Linux kernel enforces limits with cgroups [2]. CPU limits are enforced by CPU throttling, restricting access to the CPU corresponding to the container's limit, so containers cannot use more CPU than specified [2]. Similarly, memory limits are enforced by the kernel [2]. You can specify a container's CPU limit using `resource: limits.cpu` and its memory limit using `resource: limits.memory` [5].

**Sources the model was given:**

**[1]** `tasks/configure-pod-container/assign-cpu-resource.md`, *Assign CPU Resources to Containers and Pods > Specify a CPU request and a CPU limit*

> ```shell
> kubectl top pod cpu-demo --namespace=cpu-example
> ```
>
> This example output shows that the Pod is using 974 milliCPU, which is
> slightly less than the limit of 1 CPU specified in the Pod configuration.
>
> ```
> NAME                        CPU(cores)   MEMORY(bytes)
> cpu-demo                    974m         <something>
> ```
>
> Recall that by setting `-cpu "2"`, you configured the Container to attempt to use 2 CPUs, but the Container is only being allowed to use about 1 CPU. The container's CPU use is being throttled, because the container is attempting to use more CPU resources than its limit.
>
> Another possible explanation for the CPU use being below 1.0 is that the Node might not have
> enough CPU resources available. Recall that the prerequisites for this exercise require your cluster to have at least 1 CPU available for use. If your Container runs on a Node that has only 1 CPU, the Container cannot use more than 1 CPU regardless of the CPU limit specified for the Container.

**[2]** `concepts/configuration/manage-resources-containers.md`, *Resource Management for Pods and Containers > Requests and limits* **(cited)**

> If the node where a Pod is running has enough of a resource available, it's possible (and
> allowed) for a container to use more resource than its `request` for that resource specifies.
>
> For example, if you set a `memory` request of 256 MiB for a container, and that container is in
> a Pod scheduled to a Node with 8GiB of memory and no other Pods, then the container can try to use
> more RAM.
>
> Limits are a different story. Both `cpu` and `memory` limits are applied by the kubelet (and
> container runtime),
> and are ultimately enforced by the kernel. On Linux nodes, the Linux kernel
> enforces limits with
> cgroups.
> The behavior of `cpu` and `memory` limit enforcement is slightly different.
>
> `cpu` limits are enforced by CPU throttling. When a container approaches
> its `cpu` limit, the kernel will restrict access to the CPU corresponding to the
> container's limit. Thus, a `cpu` limit is a hard limit the kernel enforces.
> Containers may not use more CPU than is specified in their `cpu` limit.

**[3]** `tasks/configure-pod-container/assign-pod-level-resources.md`, *Assign Pod-level CPU and memory resources > Create a pod with CPU requests and limits at pod-level*

> Use `kubectl top` to fetch the metrics for the Pod:
>
> ```shell
> kubectl top pod cpu-demo --namespace=pod-resources-example
> ```
>
> This example output shows that the Pod is using 974 milliCPU, which is
> slightly less than the limit of 1 CPU specified in the Pod configuration.
>
> ```
> NAME                        CPU(cores)   MEMORY(bytes)
> cpu-demo                    974m         <something>
> ```
>
> Recall that by setting `-cpu "2"`, you configured the Container to attempt to use 2
> CPUs, but the Container is only being allowed to use about 1 CPU. The container's
> CPU use is being throttled, because the container is attempting to use more CPU
> resources than the Pod CPU limit.

**[4]** `concepts/security/linux-kernel-security-constraints.md`, *Linux kernel security constraints for Pods and containers > Kernel-level security features and privileged containers {#kernel-security-features-privileged-containers} > Privileged containers {#privileged-containers}*

> Any container in a Pod can enable *Privileged mode* if you set the
> `privileged: true` field in the
> `securityContext`
> field for the container. Privileged containers override or undo many other hardening settings such as the applied seccomp profile, AppArmor profile, or
> SELinux constraints. Privileged containers are given all Linux capabilities,
> including capabilities that they don't require. For example, a root user in a
> privileged container might be able to use the `CAP_SYS_ADMIN` and
> `CAP_NET_ADMIN` capabilities on the node, bypassing the runtime seccomp
> configuration and other restrictions.
>
> In most cases, you should avoid using privileged containers, and instead grant
> the specific capabilities required by your container using the `capabilities`
> field in the `securityContext` field. Only use privileged mode if you have a
> capability that you can't grant with the securityContext. This is useful for
> containers that want to use operating system administrative capabilities such
> as manipulating the network stack or accessing hardware devices.

**[5]** `concepts/workloads/pods/downward-api.md`, *Downward API > Available fields > Information available via `resourceFieldRef` {#downwardapi-resourceFieldRef}* **(cited)**

> These container-level fields allow you to provide information about
> requests and limits
> for resources such as CPU and memory.
>
> Container CPU and memory resources can be resized while the container is running.
> If this happens, a downward API volume will be updated,
> but environment variables will not be updated unless the container restarts.
> See Resize CPU and Memory Resources assigned to Containers
> for more details.
>
> `resource: limits.cpu`
> : A container's CPU limit
>
> `resource: requests.cpu`
> : A container's CPU request
>
> `resource: limits.memory`
> : A container's memory limit
>
> `resource: requests.memory`
> : A container's memory request
>
> `resource: limits.hugepages-*`
> : A container's hugepages limit
>
> `resource: requests.hugepages-*`
> : A container's hugepages request
>
> `resource: limits.ephemeral-storage`
> : A container's ephemeral-storage limit
>
> `resource: requests.ephemeral-storage`
> : A container's ephemeral-storage request

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `probes-difference`

**Question** (en, concept): What's the difference between a liveness probe and a readiness probe?

**Reference answer:** A failing liveness probe makes the kubelet restart the container; a failing readiness probe removes the Pod from Service endpoints so it gets no traffic, without restarting it.

**System answer:**

> The kubelet uses liveness probes to know when to restart a container, for example, to catch a deadlock where an application is running but unable to make progress [1][2]. If a container repeatedly fails its liveness probe, the kubelet restarts it [2].
>
> The kubelet uses readiness probes to know when a container is ready to start accepting traffic [1]. This signal controls which Pods are used as backends for Services, and a Pod is removed from Service load balancers when it is not ready [1]. If a readiness probe is specified, Kubernetes ensures the application's processes will not receive network traffic until their readiness checks pass [4].
>
> Liveness is a necessary, but not sufficient, condition for readiness; a process can be alive but not ready, particularly during initialization and termination [4]. Liveness probes do not wait for readiness probes to succeed [2]. While liveness and readiness probes can be identical, specifying both ensures that only healthy servers receive network traffic [4]. A readiness probe can also check for strict dependencies on back-end services, while a liveness probe might only check if the app itself is healthy [3].

**Sources the model was given:**

**[1]** `tasks/configure-pod-container/configure-liveness-readiness-startup-probes.md`, *Configure Liveness, Readiness and Startup Probes* **(cited)**

> This page shows how to configure liveness, readiness and startup probes for containers.
>
> For more information about probes, see Liveness, Readiness and Startup Probes
>
> The kubelet uses
> liveness probes to know when to restart a container. For example, liveness
> probes could catch a deadlock, where an application is running, but unable to
> make progress. Restarting a container in such a state can help to make the
> application more available despite bugs.
>
> A common pattern for liveness probes is to use the same low-cost HTTP endpoint
> as for readiness probes, but with a higher failureThreshold. This ensures that the pod
> is observed as not-ready for some period of time before it is hard killed.
>
> The kubelet uses readiness probes to know when a container is ready to start
> accepting traffic. One use of this signal is to control which Pods are used as
> backends for Services. A Pod is considered ready when its `Ready` condition
> is true. When a Pod is not ready, it is removed from Service load balancers.
> A Pod's `Ready` condition is false when its Node's `Ready` condition is not true,
> when one of the Pod's `readinessGates` is false, or when at least one of its containers
> is not ready.

**[2]** `concepts/configuration/liveness-readiness-startup-probes.md`, *Liveness, Readiness, and Startup Probes > Liveness probe* **(cited)**

> Liveness probes determine when to restart a container. For example, liveness probes could catch a deadlock when an application is running but unable to make progress.
>
> If a container fails its liveness probe repeatedly, the kubelet restarts the container.
>
> Liveness probes do not wait for readiness probes to succeed. If you want to wait before executing a liveness probe, you can either define `initialDelaySeconds` or use a
> startup probe.

**[3]** `concepts/workloads/pods/pod-lifecycle.md`, *Pod Lifecycle > Container probes > Types of probe > When should you use a readiness probe?* **(cited)**

> If you'd like to start sending traffic to a Pod only when a probe succeeds,
> specify a readiness probe. In this case, the readiness probe might be the same
> as the liveness probe, but the existence of the readiness probe in the spec means
> that the Pod will start without receiving any traffic and only start receiving
> traffic after the probe starts succeeding.
>
> If you want your container to be able to take itself down for maintenance, you
> can specify a readiness probe that checks an endpoint specific to readiness that
> is different from the liveness probe.
>
> If your app has a strict dependency on back-end services, you can implement both
> a liveness and a readiness probe. The liveness probe passes when the app itself
> is healthy, but the readiness probe additionally checks that each required
> back-end service is available. This helps you avoid directing traffic to Pods
> that can only respond with error messages.

**[4]** `tutorials/stateful-application/zookeeper.md`, *Running ZooKeeper, A Distributed System Coordinator > Managing the ZooKeeper process > Testing for readiness* **(cited)**

> Readiness is not the same as liveness. If a process is alive, it is scheduled
> and healthy. If a process is ready, it is able to process input. Liveness is
> a necessary, but not sufficient, condition for readiness. There are cases,
> particularly during initialization and termination, when a process can be
> alive but not ready.
>
> If you specify a readiness probe, Kubernetes will ensure that your application's
> processes will not receive network traffic until their readiness checks pass.
>
> For a ZooKeeper server, liveness implies readiness.  Therefore, the readiness
> probe from the `zookeeper.yaml` manifest is identical to the liveness probe.
>
> ```yaml
>   readinessProbe:
>     exec:
>       command:
>       - sh
>       - -c
>       - "zookeeper-ready 2181"
>     initialDelaySeconds: 15
>     timeoutSeconds: 5
> ```
>
> Even though the liveness and readiness probes are identical, it is important
> to specify both. This ensures that only healthy servers in the ZooKeeper
> ensemble receive network traffic.

**[5]** `tasks/configure-pod-container/configure-liveness-readiness-startup-probes.md`, *Configure Liveness, Readiness and Startup Probes*

> The kubelet uses startup probes to know when a container application has started.
> If such a probe is configured, liveness and readiness probes do not start until
> it succeeds, making sure those probes don't interfere with the application startup.
> This can be used to adopt liveness checks on slow starting containers, avoiding them
> getting killed by the kubelet before they are up and running.
>
> Liveness probes can be a powerful way to recover from application failures, but
> they should be used with caution. Liveness probes must be configured carefully
> to ensure that they truly indicate unrecoverable application failure, for example a deadlock.
>
> Incorrect implementation of liveness probes can lead to cascading failures. This results in
> restarting of container under high load; failed client requests as your application became less
> scalable; and increased workload on remaining pods due to some failed pods.
> Understand the difference between readiness and liveness probes and when to apply them for your app.
>
> ##

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `configmap-env`

**Question** (en, task): How can I turn every key of a ConfigMap into environment variables in my container?

**Reference answer:** Use `envFrom` in the container spec to define all of the ConfigMap's data as container environment variables.

**System answer:**

> To turn every key of a ConfigMap into environment variables in a container, use the `envFrom` field in the Pod specification [2][3][5]. The `envFrom` field instructs Kubernetes to create environment variables from the sources nested within it [2]. The inner `configMapRef` refers to a ConfigMap by its name and selects all its key-value pairs [2][3]. The contents of the target ConfigMap's `Data` field will represent the key-value pairs as environment variables [3]. The key from the ConfigMap becomes the environment variable name in the Pod [5].
>
> For example, you can create a ConfigMap like this [1]:
> ```yaml
> apiVersion: v1
> kind: ConfigMap
> metadata:
>   name: myconfigmap
> data:
>   username: k8s-admin
>   access_level: "1"
> ```
> Then, create the ConfigMap object [1]:
> ```shell
> kubectl apply -f myconfigmap.yaml
> ```
> A Pod can consume the content of the ConfigMap as environment variables [2]:
> ```shell
> kubectl apply -f env-configmap.yaml
> ```
> You can then retrieve the Pod's logs to confirm the output [2]:
> ```shell
> kubectl logs pod/ env-configmap
> ```
> The output will be similar to [2]:
> ```console
> ...
> username: "k8s-admin"
> access_level: "1"
> ...
> ```

**Sources the model was given:**

**[1]** `concepts/configuration/configmap.md`, *ConfigMaps > Using ConfigMaps > Using Configmaps as environment variables* **(cited)**

> To use a Configmap in an environment variable
> in a Pod:
>
> 1. For each container in your Pod specification, add an environment variable
>    for each Configmap key that you want to use to the
>    `env[].valueFrom.configMapKeyRef` field.
> 1. Modify your image and/or command line so that the program looks for values
>    in the specified environment variables.
>
> This is an example of defining a ConfigMap as a pod environment variable:
>
> The following ConfigMap (myconfigmap.yaml) stores two properties: username and access_level:
>
> ```yaml
> apiVersion: v1
> kind: ConfigMap
> metadata:
>   name: myconfigmap
> data:
>   username: k8s-admin
>   access_level: "1"
> ```
>
> The following command will create the ConfigMap object:
>
> ```shell
> kubectl apply -f myconfigmap.yaml
> ```
>
> The following Pod consumes the content of the ConfigMap as environment variables:

**[2]** `concepts/configuration/configmap.md`, *ConfigMaps > Using ConfigMaps > Using Configmaps as environment variables* **(cited)**

> The following Pod consumes the content of the ConfigMap as environment variables:
>
> The `envFrom` field instructs Kubernetes to create environment variables from the sources nested within it.
> The inner `configMapRef` refers to a ConfigMap by its name and selects all its key-value pairs.
> Add the Pod to your cluster, then retrieve its logs to see the output from the printenv command.
> This should confirm that the two key-value pairs from the ConfigMap have been set as environment variables:
>
> ```shell
> kubectl apply -f env-configmap.yaml
> ```
> ```shell
> kubectl logs pod/ env-configmap
> ```
> The output is similar to this:
> ```console
> ...
> username: "k8s-admin"
> access_level: "1"
> ...
> ```
>
> Sometimes a Pod won't require access to all the values in a ConfigMap.
> For example, you could have another Pod which only uses the username value from the ConfigMap.
> For this use case, you can use the `env.valueFrom` syntax instead, which lets you select individual keys in
> a ConfigMap. The name of the environment variable can also be different from the key within the ConfigMap.
> For example:

**[3]** `reference/kubernetes-api/workload-resources/pod-v1.md`, *Pod > Container {#Container} > Environment variables* **(cited)**

> *Atomic: will be replaced during a merge*
>
>   List of sources to populate environment variables in the container. The keys defined within a source must be a C_IDENTIFIER. All invalid keys will be reported as an event when the container is starting. When a key exists in multiple sources, the value associated with the last source will take precedence. Values defined by an Env with a duplicate key will take precedence. Cannot be updated.
>
>   <a name="EnvFromSource"></a>
>   *EnvFromSource represents the source of a set of ConfigMaps or Secrets*
>
>   - **envFrom.configMapRef** (ConfigMapEnvSource)
>
>     The ConfigMap to select from
>
>     <a name="ConfigMapEnvSource"></a>
>     *ConfigMapEnvSource selects a ConfigMap to populate the environment variables with.
>
>     The contents of the target ConfigMap's Data field will represent the key-value pairs as environment variables.*
>
>     - **envFrom.configMapRef.name** (string)

**[4]** `concepts/configuration/configmap.md`, *ConfigMaps > ConfigMaps and Pods*

> You can write a Pod `spec` that refers to a ConfigMap and configures the container(s)
> in that Pod based on the data in the ConfigMap. The Pod and the ConfigMap must be in
> the same namespace.
>
> The `spec` of a static Pod cannot refer to a ConfigMap
> or any other API objects.
>
> Here's an example ConfigMap that has some keys with single values,
> and other keys where the value looks like a fragment of a configuration
> format.
>
> ```yaml
> apiVersion: v1
> kind: ConfigMap
> metadata:
>   name: game-demo
> data:
>   # property-like keys; each key maps to a simple value
>   player_initial_lives: "3"
>   ui_properties_file_name: "user-interface.properties"
>
>   # file-like keys
>   game.properties: |
>     enemy.types=aliens,monsters
>     player.maximum-lives=5
>   user-interface.properties: |
>     color.good=purple
>     color.bad=yellow
>     allow.textmode=true
> ```
>
> There are four different ways that you can use a ConfigMap to configure
> a container inside a Pod:
>
> 1. Inside a container command and args
> 1. Environment variables for a container
> 1. Add a file in read-only volume, for the application to read
> 1. Write code to run inside the Pod that uses the Kubernetes API to read a ConfigMap

**[5]** `tasks/configure-pod-container/configure-pod-configmap.md`, *Configure a Pod to Use a ConfigMap > Configure all key-value pairs in a ConfigMap as container environment variables* **(cited)**

> * Create a ConfigMap containing multiple key-value pairs.
>
>   Create the ConfigMap:
>
>   ```shell
>   kubectl create -f https://kubernetes.io/examples/configmap/configmap-multikeys.yaml
>   ```
>
> * Use `envFrom` to define all of the ConfigMap's data as container environment variables. The
>   key from the ConfigMap becomes the environment variable name in the Pod.
>
>   Create the Pod:
>
>   ```shell
>   kubectl create -f https://kubernetes.io/examples/pods/pod-configmap-envFrom.yaml
>   ```
>   Now, the Pod's output includes environment variables `SPECIAL_LEVEL=very` and
>   `SPECIAL_TYPE=charm`.
>
>   Once you're happy to move on, delete that Pod:
>   ```shell
>   kubectl delete pod dapi-test-pod --now
>   ```

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `secret-encryption`

**Question** (en, concept): Are Kubernetes Secrets encrypted by default?

**Reference answer:** No. By default, Secrets are stored unencrypted in the API server's underlying data store (etcd). Enable encryption at rest and restrict access with least-privilege RBAC.

**System answer:**

> Encryption at rest for Kubernetes Secrets is not enabled by default; it needs to be configured [1][2][4]. You can enable and configure at-rest encryption for Secrets [2][4]. When encryption at rest is correctly configured, resources are encrypted on write [1].

**Sources the model was given:**

**[1]** `tasks/administer-cluster/kms-provider.md`, *Using a KMS provider for data encryption > Verifying that the data is encrypted* **(cited)**

> When encryption at rest is correctly configured, resources are encrypted on write.
> After restarting your `kube-apiserver`, any newly created or updated Secret or other resource types
> configured in `EncryptionConfiguration` should be encrypted when stored. To verify,
> you can use the `etcdctl` command line program to retrieve the contents of your secret data.
>
> 1. Create a new secret called `secret1` in the `default` namespace:
>
>    ```shell
>    kubectl create secret generic secret1 -n default --from-literal=mykey=mydata
>    ```
>
> 1. Using the `etcdctl` command line, read that secret out of etcd:
>
>    ```shell
>    ETCDCTL_API=3 etcdctl get /kubernetes.io/secrets/default/secret1 [...] | hexdump -C
>    ```
>
>    where `[...]` contains the additional arguments for connecting to the etcd server.
>
> 1. Verify the stored secret is prefixed with `k8s:enc:kms:v1:` for KMS v1 or prefixed with `k8s:enc:kms:v2:` for KMS v2, which indicates that the `kms` provider has encrypted the resulting data.
>
> 1. Verify that the secret is correctly decrypted when retrieved via the API:
>
>    ```shell
>    kubectl describe secret secret1 -n default
>    ```
>
>    The Secret should contain `mykey: mydata`

**[2]** `tasks/administer-cluster/encrypt-data.md`, *Encrypting Confidential Data at Rest* **(cited)**

> All of the APIs in Kubernetes that let you write persistent API resource data support
> at-rest encryption. For example, you can enable at-rest encryption for
> Secrets.
> This at-rest encryption is additional to any system-level encryption for the
> etcd cluster or for the filesystem(s) on hosts where you are running the
> kube-apiserver.
>
> This page shows how to enable and configure encryption of API data at rest.
>
> This task covers encryption for resource data stored using the
> Kubernetes API. For example, you can
> encrypt Secret objects, including the key-value data they contain.
>
> If you want to encrypt data in filesystems that are mounted into containers, you instead need
> to either:
>
> - use a storage integration that provides encrypted
>   volumes
> - encrypt the data within your own application
>
> ##
>
> *
>
> * This task assumes that you are running the Kubernetes API server as a
>   static pod on each control
>   plane node.
>
> * Your cluster's control plane **must** use etcd v3.x (major version 3, any minor version).
>
> * To encrypt a custom resource, your cluster must be running Kubernetes v1.26 or newer.
>
> * To use a wildcard to match resources, your cluster must be running Kubernetes v1.27 or newer.

**[3]** `concepts/configuration/secret.md`, *Secrets > Types of Secret {#secret-types} > TLS Secrets*

> The `kubernetes.io/tls` Secret type is for storing
> a certificate and its associated key that are typically used for TLS.
>
> One common use for TLS Secrets is to configure encryption in transit for
> an Ingress, but you can also use it
> with other resources or directly in your workload.
> When using this type of Secret, the `tls.key` and the `tls.crt` key must be provided
> in the `data` (or `stringData`) field of the Secret configuration, although the API
> server doesn't actually validate the values for each key.
>
> As an alternative to using `stringData`, you can use the `data` field to provide
> the base64 encoded certificate and private key. For details, see
> Constraints on Secret names and data.
>
> The following YAML contains an example config for a TLS Secret:
>
> The TLS Secret type is provided only for convenience.
> You can create an `Opaque` type for credentials used for TLS authentication.
> However, using the defined and public Secret type (`kubernetes.io/tls`)
> helps ensure the consistency of Secret format in your project. The API server
> verifies if the required keys are set for a Secret of this type.
>
> To create a TLS Secret using `kubectl`, use the `tls` subcommand:

**[4]** `tasks/administer-cluster/decrypt-data.md`, *Decrypt Confidential Data that is Already Encrypted at Rest* **(cited)**

> All of the APIs in Kubernetes that let you write persistent API resource data support
> at-rest encryption. For example, you can enable at-rest encryption for
> Secrets.
> This at-rest encryption is additional to any system-level encryption for the
> etcd cluster or for the filesystem(s) on hosts where you are running the
> kube-apiserver.
>
> This page shows how to switch from encryption of API data at rest, so that API data
> are stored unencrypted. You might want to do this to improve performance; usually,
> though, if it was a good idea to encrypt some data, it's also a good idea to leave them
> encrypted.
>
> This task covers encryption for resource data stored using the
> Kubernetes API. For example, you can
> encrypt Secret objects, including the key-value data they contain.
>
> If you wanted to manage encryption for data in filesystems that are mounted into containers, you instead
> need to either:
>
> - use a storage integration that provides encrypted
>   volumes
> - encrypt the data within your own application
>
> ##
>
> *
>
> * This task assumes that you are running the Kubernetes API server as a
>   static pod on each control
>   plane node.

**[5]** `concepts/configuration/secret.md`, *Secrets > Information security for Secrets*

> Although ConfigMap and Secret work similarly, Kubernetes applies some additional
> protection for Secret objects.
>
> Secrets often hold values that span a spectrum of importance, many of which can
> cause escalations within Kubernetes (e.g. service account tokens) and to
> external systems. Even if an individual app can reason about the power of the
> Secrets it expects to interact with, other apps within the same namespace can
> render those assumptions invalid.
>
> A Secret is only sent to a node if a Pod on that node requires it.
> For mounting Secrets into Pods, the kubelet stores a copy of the data into a `tmpfs`
> so that the confidential data is not written to durable storage.
> Once the Pod that depends on the Secret is deleted, the kubelet deletes its local copy
> of the confidential data from the Secret.
>
> There may be several containers in a Pod. By default, containers you define
> only have access to the default ServiceAccount and its related Secret.
> You must explicitly define environment variables or map a volume into a
> container in order to provide access to any other Secret.

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `scale-deployment`

**Question** (en, command): How do I change the number of replicas of a Deployment from the command line?

**Reference answer:** `kubectl scale deployment/<name> --replicas=<n>`.

**System answer:**

> You can change the number of replicas of a Deployment using the `kubectl scale` command [1]. For example, to scale a Deployment named `kubernetes-bootcamp` to 4 replicas, you would use: `kubectl scale deployments/kubernetes-bootcamp --replicas=4` [1].

**Sources the model was given:**

**[1]** `tutorials/kubernetes-basics/scale/scale-intro.md`, *Running Multiple Instances of Your App > Scaling overview > Scaling a Deployment* **(cited)**

> Two important columns of this output are:
>
> * _DESIRED_ displays the desired number of replicas of the application, which you
> define when you create the Deployment. This is the desired state.
> * _CURRENT_ displays how many replicas are currently running.
>
> Next, let’s scale the Deployment to 4 replicas. We’ll use the `kubectl scale` command,
> followed by the Deployment type, name and desired number of instances:
>
> ```shell
> kubectl scale deployments/kubernetes-bootcamp --replicas=4
> ```
>
> To list your Deployments once again, use `get deployments`:
>
> ```shell
> kubectl get deployments
> ```
>
> The change was applied, and we have 4 instances of the application available. Next,
> let’s check if the number of Pods changed:
>
> ```shell
> kubectl get pods -o wide
> ```
>
> There are 4 Pods now, with different IP addresses. The change was registered in
> the Deployment events log. To check that, use the `describe` subcommand:
>
> ```shell
> kubectl describe deployments/kubernetes-bootcamp
> ```
>
> You can also view in the output of this command that there are 4 replicas now.

**[2]** `concepts/workloads/controllers/deployment.md`, *Deployments > Updating a Deployment > Rollover (aka multiple updates in-flight)*

> Each time a new Deployment is observed by the Deployment controller, a ReplicaSet is created to bring up
> the desired Pods. If the Deployment is updated, the existing ReplicaSet that controls Pods whose labels
> match `.spec.selector` but whose template does not match `.spec.template` are scaled down. Eventually, the new
> ReplicaSet is scaled to `.spec.replicas` and all old ReplicaSets is scaled to 0.
>
> If you update a Deployment while an existing rollout is in progress, the Deployment creates a new ReplicaSet
> as per the update and start scaling that up, and rolls over the ReplicaSet that it was scaling up previously
> -- it will add it to its list of old ReplicaSets and start scaling it down.
>
> For example, suppose you create a Deployment to create 5 replicas of `nginx:1.14.2`,
> but then update the Deployment to create 5 replicas of `nginx:1.16.1`, when only 3
> replicas of `nginx:1.14.2` had been created. In that case, the Deployment immediately starts
> killing the 3 `nginx:1.14.2` Pods that it had created, and starts creating
> `nginx:1.16.1` Pods. It does not wait for the 5 replicas of `nginx:1.14.2` to be created
> before changing course.

**[3]** `concepts/workloads/controllers/deployment.md`, *Deployments > Scaling a Deployment > Proportional scaling*

> The output is similar to this:
>   ```
>   deployment.apps/nginx-deployment image updated
>   ```
>
> * The image update starts a new rollout with ReplicaSet nginx-deployment-1989198191, but it's blocked due to the
> `maxUnavailable` requirement that you mentioned above. Check out the rollout status:
>   ```shell
>   kubectl get rs
>   ```
>   The output is similar to this:
>   ```
>   NAME                          DESIRED   CURRENT   READY     AGE
>   nginx-deployment-1989198191   5         5         0         9s
>   nginx-deployment-618515232    8         8         8         1m
>   ```
>
> * Then a new scaling request for the Deployment comes along. The autoscaler increments the Deployment replicas
> to 15. The Deployment controller needs to decide where to add these new 5 replicas. If you weren't using
> proportional scaling, all 5 of them would be added in the new ReplicaSet. With proportional scaling, you
> spread the additional replicas across all ReplicaSets. Bigger proportions go to the ReplicaSets with the
> most replicas and lower proportions go to ReplicaSets with less replicas. Any leftovers are added to the
> ReplicaSet with the most replicas. ReplicaSets with zero replicas are not scaled up.

**[4]** `tasks/run-application/horizontal-pod-autoscale.md`, *Horizontal Pod Autoscaling > Configurable scaling behavior > Scaling policies*

> Since by default the policy which allows the highest amount of change is selected, the second policy will
> only be used when the number of pod replicas is more than 40. With 40 or less replicas, the first policy will be applied.
> For instance if there are 80 replicas and the target has to be scaled down to 10 replicas
> then during the first step 8 replicas will be reduced. In the next iteration when the number
> of replicas is 72, 10% of the pods is 7.2 but the number is rounded up to 8. On each loop of
> the autoscaler controller the number of pods to be change is re-calculated based on the number
> of current replicas. When the number of replicas falls below 40 the first policy _(Pods)_ is applied
> and 4 replicas will be reduced at a time.
>
> The policy selection can be changed by specifying the `selectPolicy` field for a scaling
> direction. By setting the value to `Min` which would select the policy which allows the
> smallest change in the replica count. Setting the value to `Disabled` completely disables
> scaling in that direction.

**[5]** `concepts/workloads/controllers/deployment.md`, *Deployments > Creating a Deployment*

> 2. Run `kubectl get deployments` to check if the Deployment was created.
>
>    If the Deployment is still being created, the output is similar to the following:
>    ```
>    NAME               READY   UP-TO-DATE   AVAILABLE   AGE
>    nginx-deployment   0/3     0            0           1s
>    ```
>    When you inspect the Deployments in your cluster, the following fields are displayed:
>    * `NAME` lists the names of the Deployments in the namespace.
>    * `READY` displays how many replicas of the application are available to your users. It follows the pattern ready/desired.
>    * `UP-TO-DATE` displays the number of replicas that have been updated to achieve the desired state.
>    * `AVAILABLE` displays how many replicas of the application are available to your users.
>    * `AGE` displays the amount of time that the application has been running.
>
>    Notice how the number of desired replicas is 3 according to `.spec.replicas` field.
>
> 3. To see the Deployment rollout status, run `kubectl rollout status deployment/nginx-deployment`.

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `rollback-deployment`

**Question** (en, task): I deployed a broken version of my app. How do I go back to the previous version?

**Reference answer:** `kubectl rollout undo deployment/<name>` (optionally `--to-revision=<n>`); `kubectl rollout history` lists revisions.

**System answer:**

> To roll back your Deployment to the previous version, use the `kubectl rollout undo` command [1][4].
>
> For example:
> ```shell
> kubectl rollout undo deployment/nginx-deployment
> ```
> This command will revert the Deployment to the previous revision [1][4]. You can also specify a particular revision to roll back to using `--to-revision` [1].

**Sources the model was given:**

**[1]** `concepts/workloads/controllers/deployment.md`, *Deployments > Rolling Back a Deployment > Rolling Back to a Previous Revision* **(cited)**

> Follow the steps given below to rollback the Deployment from the current version to the previous version, which is version 2.
>
> 1. Now you've decided to undo the current rollout and rollback to the previous revision:
>    ```shell
>    kubectl rollout undo deployment/nginx-deployment
>    ```
>
>    The output is similar to this:
>    ```
>    deployment.apps/nginx-deployment rolled back
>    ```
>    Alternatively, you can rollback to a specific revision by specifying it with `--to-revision`:
>
>    ```shell
>    kubectl rollout undo deployment/nginx-deployment --to-revision=2
>    ```
>
>    The output is similar to this:
>    ```
>    deployment.apps/nginx-deployment rolled back
>    ```
>
>    For more details about rollout related commands, read `kubectl rollout`.
>
>    The Deployment is now rolled back to a previous stable revision. As you can see, a `DeploymentRollback` event
>    for rolling back to revision 2 is generated from Deployment controller.
>
> 2. Check if the rollback was successful and the Deployment is running as expected, run:
>    ```shell
>    kubectl get deployment nginx-deployment
>    ```

**[2]** `concepts/workloads/controllers/deployment.md`, *Deployments > Rolling Back a Deployment*

> Sometimes, you may want to rollback a Deployment; for example, when the Deployment is not stable, such as crash looping.
> By default, all of the Deployment's rollout history is kept in the system so that you can rollback anytime you want
> (you can change that by modifying revision history limit).
>
> A Deployment's revision is created when a Deployment's rollout is triggered. This means that the
> new revision is created if and only if the Deployment's Pod template (`.spec.template`) is changed,
> for example if you update the labels or container images of the template. Other updates, such as scaling the Deployment,
> do not create a Deployment revision, so that you can facilitate simultaneous manual- or auto-scaling.
> This means that when you roll back to an earlier revision, only the Deployment's Pod template part is
> rolled back.
>
> * Suppose that you made a typo while updating the Deployment, by putting the image name as `nginx:1.161` instead of `nginx:1.16.1`:
>
>   ```shell
>   kubectl set image deployment/nginx-deployment nginx=nginx:1.161
>   ```
>
>   The output is similar to this:
>   ```
>   deployment.apps/nginx-deployment image updated
>   ```

**[3]** `tasks/extend-kubernetes/custom-resources/custom-resource-definition-versioning.md`, *Versions in CustomResourceDefinitions > Overview*

> Removing an old version:
>
> 1. Ensure all clients are fully migrated to the new version. The kube-apiserver
>    logs can be reviewed to help identify any clients that are still accessing via
>    the old version.
> 1. Set `served` to `false` for the old version in the `spec.versions` list. If
>    any clients are still unexpectedly using the old version they may begin reporting
>    errors attempting to access the custom resource objects at the old version.
>    If this occurs, switch back to using `served:true` on the old version, migrate the
>    remaining clients to the new version and repeat this step.
> 1. Ensure the upgrade of existing objects to the new stored version step has been completed.
>    1. Verify that the `storage` is set to `true` for the new version in the `spec.versions` list in the CustomResourceDefinition.
>    1. Verify that the old version is no longer listed in the CustomResourceDefinition `status.storedVersions`.
> 1. Remove the old version from the CustomResourceDefinition `spec.versions` list.
> 1. Drop conversion support for the old version in conversion webhooks.

**[4]** `tutorials/kubernetes-basics/update/update-intro.md`, *Performing a Rolling Update > Rolling updates overview > Roll back an update* **(cited)**

> Let’s perform another update, and try to deploy an image tagged with `v10`:
>
> ```shell
> kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=gcr.io/google-samples/kubernetes-bootcamp:v10
> ```
>
> Use `get deployments` to see the status of the deployment:
>
> ```shell
> kubectl get deployments
> ```
>
> Notice that the output doesn't list the desired number of available Pods. Run the
> `get pods` subcommand to list all Pods:
>
> ```shell
> kubectl get pods
> ```
>
> Notice that some of the Pods have a status of `ImagePullBackOff`.
>
> To get more insight into the problem, run the `describe pods` subcommand:
>
> ```shell
> kubectl describe pods
> ```
>
> In the `Events` section of the output for the affected Pods, notice that the `v10`
> image version did not exist in the repository.
>
> To roll back the deployment to your last working version, use the `rollout undo`
> subcommand:
>
> ```shell
> kubectl rollout undo deployments/kubernetes-bootcamp
> ```
>
> The `rollout undo` command reverts the deployment to the previous known state
> (`v2` of the image). Updates are versioned and you can revert to any previously
> known state of a Deployment.
>
> Use the `get pods` subcommand to list the Pods again:

**[5]** `tutorials/kubernetes-basics/update/update-intro.md`, *Performing a Rolling Update > Rolling updates overview > Update the version of the app*

> To list your Deployments, run the `get deployments` subcommand:
>
> ```shell
> kubectl get deployments
> ```
>
> To list the running Pods, run the `get pods` subcommand:
>
> ```shell
> kubectl get pods
> ```
>
> To view the current image version of the app, run the `describe pods` subcommand
> and look for the `Image` field:
>
> ```shell
> kubectl describe pods
> ```
>
> To update the image of the application to version 2, use the `set image` subcommand,
> followed by the deployment name and the new image version:
>
> ```shell
> kubectl set image deployments/kubernetes-bootcamp kubernetes-bootcamp=docker.io/jocatalin/kubernetes-bootcamp:v2
> ```
>
> The command notified the Deployment to use a different image for your app and initiated
> a rolling update. Check the status of the new Pods, and view the old one terminating
> with the `get pods` subcommand:
>
> ```shell
> kubectl get pods
> ```

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `service-types`

**Question** (en, concept): When should I use a NodePort Service instead of ClusterIP or LoadBalancer?

**Reference answer:** ClusterIP (the default) is only reachable inside the cluster. NodePort exposes the Service on a static port on each node; it lets you set up your own load-balancing solution, configure environments not fully supported by Kubernetes, or expose nodes' IPs directly. LoadBalancer uses an external load balancer.

**System answer:**

> You should use a `NodePort` Service when you need to expose a Service from outside the cluster by connecting to any node using its IP address and an assigned port [3][4]. This type exposes the Service on each Node's IP at a static port [1].
>
> `NodePort` gives you the flexibility to set up your own load balancing solution, configure environments not fully supported by Kubernetes, or directly expose one or more nodes' IP addresses [3].
>
> In contrast:
> *   A `ClusterIP` Service exposes the Service on a cluster-internal IP, making it only reachable from within the cluster [1][4]. This is the default type if not specified [1].
> *   A `LoadBalancer` Service exposes the Service externally using an external load balancer, typically provisioned by a cloud provider that supports external load balancers [1][2][4]. Kubernetes does not directly offer a load balancing component for this type; you must provide one or integrate with a cloud provider [1]. A `LoadBalancer` Service typically starts by making changes equivalent to a `NodePort` Service [2][5].

**Sources the model was given:**

**[1]** `concepts/services-networking/service.md`, *Service > Service type  {#publishing-services-service-types}* **(cited)**

> For some parts of your application (for example, frontends) you may want to expose a
> Service onto an external IP address, one that's accessible from outside of your
> cluster.
>
> Kubernetes Service types allow you to specify what kind of Service you want.
>
> The available `type` values and their behaviors are:
>
> `ClusterIP`
> : Exposes the Service on a cluster-internal IP. Choosing this value
>   makes the Service only reachable from within the cluster. This is the
>   default that is used if you don't explicitly specify a `type` for a Service.
>   You can expose the Service to the public internet using an
>   Ingress or a
>   Gateway.
>
> `NodePort`
> : Exposes the Service on each Node's IP at a static port (the `NodePort`).
>   To make the node port available, Kubernetes sets up a cluster IP address,
>   the same as if you had requested a Service of `type: ClusterIP`.
>
> `LoadBalancer`
> : Exposes the Service externally using an external load balancer. Kubernetes
>   does not directly offer a load balancing component; you must provide one, or
>   you can integrate your Kubernetes cluster with a cloud provider.

**[2]** `concepts/services-networking/service.md`, *Service > Service type  {#publishing-services-service-types} > `type: LoadBalancer` {#loadbalancer}* **(cited)**

> On cloud providers which support external load balancers, setting the `type`
> field to `LoadBalancer` provisions a load balancer for your Service.
> The actual creation of the load balancer happens asynchronously, and
> information about the provisioned balancer is published in the Service's
> `.status.loadBalancer` field.
> For example:
>
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
>
> Traffic from the external load balancer is directed at the backend Pods. The cloud
> provider decides how it is load balanced.
>
> To implement a Service of `type: LoadBalancer`, Kubernetes typically starts off
> by making the changes that are equivalent to you requesting a Service of
> `type: NodePort`. The cloud-controller-manager component then configures the external
> load balancer to forward traffic to that assigned node port.
>
> You can configure a load balanced Service to
> omit assigning a node port, provided that the
> cloud provider implementation supports this.

**[3]** `concepts/services-networking/service.md`, *Service > Service type  {#publishing-services-service-types} > `type: NodePort` {#type-nodeport}* **(cited)**

> If you set the `type` field to `NodePort`, the Kubernetes control plane
> allocates a port from a range specified by `--service-node-port-range` flag (default: 30000-32767).
> Each node proxies that port (the same port number on every Node) into your Service.
> Your Service reports the allocated port in its `.spec.ports[*].nodePort` field.
>
> Using a NodePort gives you the freedom to set up your own load balancing solution,
> to configure environments that are not fully supported by Kubernetes, or even
> to expose one or more nodes' IP addresses directly.
>
> For a node port Service, Kubernetes additionally allocates a port (TCP, UDP or
> SCTP to match the protocol of the Service). Every node in the cluster configures
> itself to listen on that assigned port and to forward traffic to one of the ready
> endpoints associated with that Service. You'll be able to contact the `type: NodePort`
> Service, from outside the cluster, by connecting to any node using the appropriate
> protocol (for example: TCP), and the appropriate port (as assigned to that Service).

**[4]** `tutorials/kubernetes-basics/expose/expose-intro.md`, *Using a Service to Expose Your App > Overview of Kubernetes Services* **(cited)**

> * _ClusterIP_ (default) - Exposes the Service on an internal IP in the cluster. This
> type makes the Service only reachable from within the cluster.
>
> * _NodePort_ - Exposes the Service on the same port of each selected Node in the cluster using NAT.
> Makes a Service accessible from outside the cluster using `NodeIP:NodePort`. Superset of ClusterIP.
>
> * _LoadBalancer_ - Creates an external load balancer in the current cloud (if supported)
> and assigns a fixed, external IP to the Service. Superset of NodePort.
>
> * _ExternalName_ - Maps the Service to the contents of the `externalName` field
> (e.g. `foo.bar.example.com`), by returning a `CNAME` record with its value.
> No proxying of any kind is set up. This type requires v1.7 or higher of `kube-dns`,
> or CoreDNS version 0.0.8 or higher.
>
> More information about the different types of Services can be found in the
> Using Source IP tutorial. Also see
> Connecting Applications with Services.

**[5]** `reference/kubernetes-api/service-resources/service-v1.md`, *Service > ServiceSpec {#ServiceSpec}* **(cited)**

> - **type** (string)
>
>   type determines how the Service is exposed. Defaults to ClusterIP. Valid options are ExternalName, ClusterIP, NodePort, and LoadBalancer. "ClusterIP" allocates a cluster-internal IP address for load-balancing to endpoints. Endpoints are determined by the selector or if that is not specified, by manual construction of an Endpoints object or EndpointSlice objects. If clusterIP is "None", no virtual IP is allocated and the endpoints are published as a set of endpoints rather than a virtual IP. "NodePort" builds on ClusterIP and allocates a port on every node which routes to the same endpoints as the clusterIP. "LoadBalancer" builds on NodePort and creates an external load-balancer (if supported in the current cloud) which routes to the same endpoints as the clusterIP. "ExternalName" aliases this service to the specified externalName. Several other fields do not apply to ExternalName services. More info: https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types
>
> - **ipFamilies** ([]string)
>
>   *Atomic: will be replaced during a merge*

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `pod-pending`

**Question** (en, troubleshooting): My pod has been stuck in Pending for a long time. What can cause that?

**Reference answer:** The Pod can't be scheduled: usually not enough CPU or memory on any node, or a hostPort conflict. `kubectl describe pod` shows the scheduler's events explaining why.

**System answer:**

> If a Pod is stuck in `Pending`, it means it cannot be scheduled onto a node [3]. This is generally due to insufficient resources preventing scheduling [3].
>
> Possible causes include:
> *   Not having enough resources, such as CPU or Memory, in your cluster [3]. In this case, you may need to delete Pods, adjust resource requests, or add new nodes [3].
> *   Using `hostPort`, which limits the number of places a Pod can be scheduled [3]. If `hostPort` is required, you can only schedule as many Pods as there are nodes in your cluster; otherwise, try using a Service object [3].
>
> You can look at the output of the `kubectl describe ...` command for messages from the scheduler about why it cannot schedule your Pod [3].

**Sources the model was given:**

**[1]** `concepts/workloads/pods/disruptions.md`, *Disruptions > Pod disruption conditions {#pod-disruption-conditions}*

> `TerminationByKubelet`
> : Pod has been terminated by the kubelet, because of either node pressure eviction,
>   the graceful node shutdown,
>   or preemption for system critical pods.
>
> In all other disruption scenarios, like eviction due to exceeding
> Pod container limits,
> Pods don't receive the `DisruptionTarget` condition because the disruptions were
> probably caused by the Pod and would reoccur on retry.
>
> A Pod disruption might be interrupted. The control plane might re-attempt to
> continue the disruption of the same Pod, but it is not guaranteed. As a result,
> the `DisruptionTarget` condition might be added to a Pod, but that Pod might then not actually be
> deleted. In such a situation, after some time, the
> Pod disruption condition will be cleared.
>
> Along with cleaning up the pods, the Pod garbage collector (PodGC) will also mark them as failed if they are in a non-terminal
> phase (see also Pod garbage collection).
>
> When using a Job (or CronJob), you may want to use these Pod disruption conditions as part of your Job's
> Pod failure policy.

**[2]** `concepts/scheduling-eviction/pod-priority-preemption.md`, *Pod Priority and Preemption > Troubleshooting > Pods are preempted unnecessarily*

> Preemption removes existing Pods from a cluster under resource pressure to make
> room for higher priority pending Pods. If you give high priorities to
> certain Pods by mistake, these unintentionally high priority Pods may cause
> preemption in your cluster. Pod priority is specified by setting the
> `priorityClassName` field in the Pod's specification. The integer value for
> priority is then resolved and populated to the `priority` field of `podSpec`.
>
> To address the problem, you can change the `priorityClassName` for those Pods
> to use lower priority classes, or leave that field empty. An empty
> `priorityClassName` is resolved to zero by default.
>
> When a Pod is preempted, there will be events recorded for the preempted Pod.
> Preemption should happen only when a cluster does not have enough resources for
> a Pod. In such cases, preemption happens only when the priority of the pending
> Pod (preemptor) is higher than the victim Pods. Preemption must not happen when
> there is no pending Pod, or when the pending Pods have equal or lower priority
> than the victims. If preemption happens in such scenarios, please file an issue.

**[3]** `tasks/debug/debug-application/debug-pods.md`, *Debug Pods > Diagnosing the problem > Debugging Pods > My pod stays pending* **(cited)**

> If a Pod is stuck in `Pending` it means that it can not be scheduled onto a node.
> Generally this is because there are insufficient resources of one type or another
> that prevent scheduling. Look at the output of the `kubectl describe ...` command above.
> There should be messages from the scheduler about why it can not schedule your pod.
> Reasons include:
>
> * **You don't have enough resources**: You may have exhausted the supply of CPU
>   or Memory in your cluster, in this case you need to delete Pods, adjust resource
>   requests, or add new nodes to your cluster. See Compute Resources document
>   for more information.
>
> * **You are using `hostPort`**: When you bind a Pod to a `hostPort` there are a
>   limited number of places that pod can be scheduled. In most cases, `hostPort`
>   is unnecessary, try using a Service object to expose your Pod.  If you do require
>   `hostPort` then you can only schedule as many Pods as there are nodes in your Kubernetes cluster.

**[4]** `concepts/scheduling-eviction/pod-priority-preemption.md`, *Pod Priority and Preemption > Preemption > Limitations of preemption > Inter-Pod affinity on lower-priority Pods*

> A Node is considered for preemption only when the answer to this question is
> yes: "If all the Pods with lower priority than the pending Pod are removed from
> the Node, can the pending Pod be scheduled on the Node?"
>
> Preemption does not necessarily remove all lower-priority
> Pods. If the pending Pod can be scheduled by removing fewer than all
> lower-priority Pods, then only a portion of the lower-priority Pods are removed.
> Even so, the answer to the preceding question must be yes. If the answer is no,
> the Node is not considered for preemption.
>
> If a pending Pod has inter-pod affinity
> to one or more of the lower-priority Pods on the Node, the inter-Pod affinity
> rule cannot be satisfied in the absence of those lower-priority Pods. In this case,
> the scheduler does not preempt any Pods on the Node. Instead, it looks for another
> Node. The scheduler might find a suitable Node or it might not. There is no
> guarantee that the pending Pod can be scheduled.
>
> Our recommended solution for this problem is to create inter-Pod affinity only
> towards equal or higher priority Pods.

**[5]** `tasks/debug/debug-application/debug-pods.md`, *Debug Pods > Diagnosing the problem > Debugging Pods > My pod stays waiting*

> If a Pod is stuck in the `Waiting` state, then it has been scheduled to a worker node,
> but it can't run on that machine. Again, the information from `kubectl describe ...`
> should be informative. The most common cause of `Waiting` pods is a failure to pull the image.
> There are three things to check:
>
> * Make sure that you have the name of the image correct.
> * Have you pushed the image to the registry?
> * Try to manually pull the image to see if the image can be pulled. For example,
>   if you use Docker on your PC, run `docker pull <image>`.

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `crashloop`

**Question** (en, troubleshooting): My container keeps crashing and restarting in a loop. How do I find out why?

**Reference answer:** Read the logs of the previous (crashed) container instance with `kubectl logs <pod> --previous`, and inspect the Pod with `kubectl describe pod`. The kubelet restarts the failing container with an exponential backoff delay (CrashLoopBackOff).

**System answer:**

> Your container is likely in a `CrashLoopBackOff` state, which indicates that an exponential backoff delay mechanism is in effect for a container that is failing and restarting repeatedly [1]. This can be caused by application errors, configuration errors (such as incorrect environment variables or missing files), resource constraints (where the container lacks enough memory or CPU), or failing health checks, liveness probes, or startup probes [4].
>
> To investigate the root cause, you can use `kubectl describe pod` to fetch details about the Pod [2]. This command provides status information about the container(s) and Pod, including the restart count and events, which can be useful for detecting crash loops [2].

**Sources the model was given:**

**[1]** `concepts/workloads/pods/pod-lifecycle.md`, *Pod Lifecycle > How Pods handle problems with containers {#container-restarts}* **(cited)**

> Kubernetes manages container failures within Pods using a `restartPolicy` defined in the Pod `spec`. This policy determines how Kubernetes reacts to containers exiting due to errors or other reasons, which falls in the following sequence:
>
> 1. **Initial crash**: Kubernetes attempts an immediate restart based on the Pod `restartPolicy`.
> 1. **Repeated crashes**: After the initial crash Kubernetes applies an exponential
>    backoff delay for subsequent restarts, described in `restartPolicy`.
>    This prevents rapid, repeated restart attempts from overloading the system.
> 1. **CrashLoopBackOff state**: This indicates that the backoff delay mechanism is currently
>    in effect for a given container that is in a crash loop, failing and restarting repeatedly.
> 1. **Backoff reset**: If a container runs successfully for a certain duration
>    (e.g., 10 minutes), Kubernetes resets the backoff delay, treating any new crash
>    as the first one.
>
> In practice, a `CrashLoopBackOff` is a condition or event that might be seen as output
> from the `kubectl` command, while describing or listing Pods, when a container in the Pod
> fails to start properly and then continually tries and fails in a loop.

**[2]** `tasks/debug/debug-application/debug-running-pod.md`, *Debug Running Pods > Using `kubectl describe pod` to fetch details about pods* **(cited)**

> Here you can see configuration information about the container(s) and Pod (labels, resource requirements, etc.), as well as status information about the container(s) and Pod (state, readiness, restart count, events, etc.).
>
> The container state is one of Waiting, Running, or Terminated. Depending on the state, additional information will be provided -- here you can see that for a container in Running state, the system tells you when the container started.
>
> Ready tells you whether the container passed its last readiness probe. (In this case, the container does not have a readiness probe configured; the container is assumed to be ready if no readiness probe is configured.)
>
> Restart Count tells you how many times the container has been restarted; this information can be useful for detecting crash loops in containers that are configured with a restart policy of 'always.'
>
> Currently the only Condition associated with a Pod is the binary Ready condition, which indicates that the pod is able to service requests and should be added to the load balancing pools of all matching services.

**[3]** `reference/kubernetes-api/workload-resources/pod-v1.md`, *Pod > Container {#Container} > Lifecycle*

> - **restartPolicy** (string)
>
>   RestartPolicy defines the restart behavior of individual containers in a pod. This field may only be set for init containers, and the only allowed value is "Always". For non-init containers or when this field is not specified, the restart behavior is defined by the Pod's restart policy and the container type. Setting the RestartPolicy as "Always" for the init container will have the following effect: this init container will be continually restarted on exit until all regular containers have terminated. Once all regular containers have completed, all init containers with restartPolicy "Always" will be shut down. This lifecycle differs from normal init containers and is often referred to as a "sidecar" container. Although this init container still starts in the init container sequence, it does not wait for the container to complete before proceeding to the next init container. Instead, the next init container starts immediately after this init container is started, or after any startupProbe has successfully completed.

**[4]** `concepts/workloads/pods/pod-lifecycle.md`, *Pod Lifecycle > How Pods handle problems with containers {#container-restarts}* **(cited)**

> In other words, when a container enters the crash loop, Kubernetes applies the
> exponential backoff delay mentioned in the Container restart policy.
> This mechanism prevents a faulty container from overwhelming the system with continuous
> failed start attempts.
>
> The `CrashLoopBackOff` can be caused by issues like the following:
>
> * Application errors that cause the container to exit.
> * Configuration errors, such as incorrect environment variables or missing
>   configuration files.
> * Resource constraints, where the container might not have enough memory or CPU
>   to start properly.
> * Health checks failing if the application doesn't start serving within the
>   expected time.
> * Container liveness probes or startup probes returning a `Failure` result
>   as mentioned in the probes section.
>
> To investigate the root cause of a `CrashLoopBackOff` issue, a user can:

**[5]** `concepts/workloads/pods/init-containers.md`, *Init Containers > Detailed behavior > Pod restart reasons*

> A Pod can restart, causing re-execution of init containers, for the following
> reasons:
>
> * The Pod infrastructure container is restarted. This is uncommon and would
>   have to be done by someone with root access to nodes.
> * All containers in a Pod are terminated while `restartPolicy` is set to Always,
>   forcing a restart, and the init container completion record has been lost due
>   to garbage collection.
>
> The Pod will not be restarted when the init container image is changed, or the
> init container completion record has been lost due to garbage collection. This
> applies for Kubernetes v1.20 and later. If you are using an earlier version of
> Kubernetes, consult the documentation for the version you are using.
>
> ##
>
> Learn more about the following:
> * Creating a Pod that has an init container.
> * Debug init containers.
> * Overview of kubelet and kubectl.
> * Types of probes: liveness, readiness, startup probe.
> * Sidecar containers.

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `pvc-request-storage`

**Question** (en, concept): How does a pod ask for persistent storage that survives restarts?

**Reference answer:** Create a PersistentVolumeClaim (requested storage, access mode, optional storageClassName) and use it as a volume in the Pod spec; the claim is bound to a matching PersistentVolume.

**System answer:**

> A Pod can specify a set of shared storage volumes, which allow persistent data in the Pod to survive if one of its containers needs to be restarted [4].

**Sources the model was given:**

**[1]** `concepts/configuration/manage-resources-containers.md`, *Resource Management for Pods and Containers > Local ephemeral storage*

> Nodes have local ephemeral storage, backed by
> locally-attached writeable devices or, sometimes, by RAM.
> "Ephemeral" means that there is no long-term guarantee about durability.
>
> Pods use ephemeral local storage for scratch space, caching, and for logs.
> The kubelet can provide scratch space to Pods using local ephemeral storage to
> mount `emptyDir`
>  volumes into containers.
>
> The kubelet also uses this kind of storage to hold
> node-level container logs,
> container images, and the writable layers of running containers.
>
> If a node fails, the data in its ephemeral storage can be lost.
> Your applications cannot expect any performance SLAs (disk IOPS for example)
> from local ephemeral storage.
>
> To make the resource quota work on ephemeral-storage, two things need to be done:
>
> * An admin sets the resource quota for ephemeral-storage in a namespace.
> * A user needs to specify limits for the ephemeral-storage resource in the Pod spec.
>
> If the user doesn't specify the ephemeral-storage resource limit in the Pod spec,
> the resource quota is not enforced on ephemeral-storage.
>
> Kubernetes lets you track, reserve and limit the amount
> of ephemeral local storage a Pod can consume.

**[2]** `concepts/workloads/pods/pod-lifecycle.md`, *Pod Lifecycle > Pod lifetime*

> Whilst a Pod is running, the kubelet is able to restart containers to handle some
> kind of faults. Within a Pod, Kubernetes tracks different container
> states and determines what action to take to make the Pod
> healthy again.
>
> In the Kubernetes API, Pods have both a specification and an actual status. The
> status for a Pod object consists of a set of Pod conditions.
> You can also inject custom readiness information into the
> condition data for a Pod, if that is useful to your application.
>
> Pods are only scheduled once in their lifetime;
> assigning a Pod to a specific node is called _binding_, and the process of selecting
> which node to use is called _scheduling_.
> Once a Pod has been scheduled and is bound to a node, Kubernetes tries
> to run that Pod on the node. The Pod runs on that node until it stops, or until the Pod
> is terminated; if Kubernetes isn't able to start the Pod on the selected
> node (for example, if the node crashes before the Pod starts), then that particular Pod
> never starts.

**[3]** `concepts/scheduling-eviction/node-pressure-eviction.md`, *Node-pressure Eviction > Node conditions {#node-conditions} > Pod selection for kubelet eviction*

> `Guaranteed` pods are guaranteed only when requests and limits are specified for
> all the containers and they are equal. These pods will never be evicted because
> of another pod's resource consumption. If a system daemon (such as `kubelet`
> and `journald`) is consuming more resources than were reserved via
> `system-reserved` or `kube-reserved` allocations, and the node only has
> `Guaranteed` or `Burstable` pods using less resources than requests left on it,
> then the kubelet must choose to evict one of these pods to preserve node stability
> and to limit the impact of resource starvation on other pods. In this case, it
> will choose to evict pods of lowest Priority first.
>
> If you are running a static pod
> and want to avoid having it evicted under resource pressure, set the
> `priority` field for that Pod directly. Static pods do not support the
> `priorityClassName` field.
>
> When the kubelet evicts pods in response to inode or process ID starvation, it uses
> the Pods' relative priority to determine the eviction order, because inodes and PIDs have no
> requests.
>
> The kubelet sorts pods differently based on whether the node has a dedicated
> `imagefs` or `containerfs` filesystem:

**[4]** `concepts/workloads/pods/_index.md`, *Pods > Resource sharing and communication > Storage in Pods {#pod-storage}* **(cited)**

> A Pod can specify a set of shared storage
> volumes. All containers
> in the Pod can access the shared volumes, allowing those containers to
> share data. Volumes also allow persistent data in a Pod to survive
> in case one of the containers within needs to be restarted. See
> Storage for more information on how
> Kubernetes implements shared storage and makes it available to Pods.

**[5]** `concepts/architecture/self-healing.md`, *Kubernetes Self-Healing > Self-Healing capabilities {#self-healing-capabilities}*

> - **Container-level restarts:** If a container inside a Pod fails, Kubernetes restarts it based on the `restartPolicy`.
>
> - **Replica replacement:** If a Pod in a Deployment or StatefulSet fails, Kubernetes creates a replacement Pod to maintain the specified number of replicas.
>   If a Pod fails that is part of a DaemonSet fails, the control plane
>   creates a replacement Pod to run on the same node.
>
> - **Persistent storage recovery:** If a node is running a Pod with a PersistentVolume (PV) attached, and the node fails, Kubernetes can reattach the volume to a new Pod on a different node.
>
> - **Load balancing for Services:** If a Pod behind a Service fails, Kubernetes automatically removes it from the Service's endpoints to route traffic only to healthy Pods.
>
> Here are some of the key components that provide Kubernetes self-healing:
>
> - **kubelet:** Ensures that containers are running, and restarts those that fail.
>
> - **ReplicaSet, StatefulSet and DaemonSet controller:** Maintains the desired number of Pod replicas.
>
> - **PersistentVolume controller:** Manages volume attachment and detachment for stateful workloads.

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `namespaces-when`

**Question** (en, concept): When does it make sense to split a cluster into multiple namespaces?

**Reference answer:** When many users spread across multiple teams or projects share a cluster: namespaces scope names and let you divide cluster resources with resource quotas. They aren't needed to separate slightly different versions of the same software.

**System answer:**

> It makes sense to split a cluster into multiple namespaces in environments with many users spread across multiple teams or projects [1]. Namespaces help different projects, teams, or customers share a Kubernetes cluster [2].
>
> Reasons to use multiple namespaces include:
> *   To divide cluster resources between multiple users, often via resource quota [1].
> *   To provide a scope for names, where resource names need to be unique within a namespace but not across them [1][2].
> *   To attach authorization and policy to a subsection of the cluster [2].
> *   To allow each user community to work in isolation, with its own resources, policies, and constraints [2].
> *   To delegate management authority to trusted users [2].
> *   To limit community resource consumption [2].
>
> For clusters with a few to tens of users, creating or thinking about namespaces may not be necessary [1]. It is also not necessary to use multiple namespaces to separate slightly different resources, such as different versions of the same software; labels can be used for this purpose within the same namespace [1].

**Sources the model was given:**

**[1]** `concepts/overview/working-with-objects/namespaces.md`, *Namespaces > When to Use Multiple Namespaces* **(cited)**

> Namespaces are intended for use in environments with many users spread across multiple
> teams, or projects.  For clusters with a few to tens of users, you should not
> need to create or think about namespaces at all.  Start using namespaces when you
> need the features they provide.
>
> Namespaces provide a scope for names.  Names of resources need to be unique within a namespace,
> but not across namespaces. Namespaces cannot be nested inside one another and each Kubernetes
> resource can only be in one namespace.
>
> Namespaces are a way to divide cluster resources between multiple users (via resource quota).
>
> It is not necessary to use multiple namespaces to separate slightly different
> resources, such as different versions of the same software: use
> labels to distinguish
> resources within the same namespace.
>
> For a production cluster, consider _not_ using the `default` namespace. Instead, make other namespaces and use those.

**[2]** `tasks/administer-cluster/namespaces.md`, *Share a Cluster with Namespaces > Understanding the motivation for using namespaces* **(cited)**

> A single cluster should be able to satisfy the needs of multiple users or groups of users
> (henceforth in this document a _user community_).
>
> Kubernetes _namespaces_ help different projects, teams, or customers to share a Kubernetes cluster.
>
> It does this by providing the following:
>
> 1. A scope for names.
> 1. A mechanism to attach authorization and policy to a subsection of the cluster.
>
> Use of multiple namespaces is optional.
>
> Each user community wants to be able to work in isolation from other communities.
> Each user community has its own:
>
> 1. resources (pods, services, replication controllers, etc.)
> 1. policies (who can or cannot perform actions in their community)
> 1. constraints (this community is allowed this much quota, etc.)
>
> A cluster operator may create a Namespace for each unique user community.
>
> The Namespace provides a unique scope for:
>
> 1. named resources (to avoid basic naming collisions)
> 1. delegated management authority to trusted users
> 1. ability to limit community resource consumption
>
> Use cases include:

**[3]** `tasks/administer-cluster/namespaces.md`, *Share a Cluster with Namespaces > Viewing namespaces*

> List the current namespaces in a cluster using:
>
> ```shell
> kubectl get namespaces
> ```
> ```console
> NAME              STATUS   AGE
> default           Active   11d
> kube-node-lease   Active   11d
> kube-public       Active   11d
> kube-system       Active   11d
> ```
>
> Kubernetes starts with four initial namespaces:
>
> * `default` The default namespace for objects with no other namespace
> * `kube-node-lease` This namespace holds Lease objects associated with each node. Node leases allow the kubelet to send heartbeats so that the control plane can detect node failure.
> * `kube-public` This namespace is created automatically and is readable by all users
>   (including those not authenticated). This namespace is mostly reserved for cluster usage,
>   in case that some resources should be visible and readable publicly throughout the whole cluster.
>   The public aspect of this namespace is only a convention, not a requirement.
> * `kube-system` The namespace for objects created by the Kubernetes system
>
> You can also get the summary of a specific namespace using:
>
> ```shell
> kubectl get namespaces <name>
> ```
>
> Or you can get detailed information with:

**[4]** `concepts/overview/working-with-objects/namespaces.md`, *Namespaces > Initial namespaces*

> Kubernetes starts with four initial namespaces:
>
> `default`
> : Kubernetes includes this namespace so that you can start using your new cluster without first creating a namespace.
>
> `kube-node-lease`
> : This namespace holds Lease objects associated with each node. Node leases allow the kubelet to send heartbeats so that the control plane can detect node failure.
>
> `kube-public`
> : This namespace is readable by *all* clients (including those not authenticated). This namespace is mostly reserved for cluster usage, in case that some resources should be visible and readable publicly throughout the whole cluster. The public aspect of this namespace is only a convention, not a requirement.
>
> `kube-system`
> : The namespace for objects created by the Kubernetes system.

**[5]** `reference/kubectl/_index.md`, *Command line tool (kubectl) > In-cluster authentication and namespace overrides*

> By default `kubectl` will first determine if it is running within a pod, and thus in a cluster.
> It starts by checking for the `KUBERNETES_SERVICE_HOST` and `KUBERNETES_SERVICE_PORT` environment
> variables and the existence of a service account token file at `/var/run/secrets/kubernetes.io/serviceaccount/token`.
> If all three are found in-cluster authentication is assumed.
>
> To maintain backwards compatibility, if the `POD_NAMESPACE` environment variable is set
> during in-cluster authentication it will override the default namespace from the
> service account token. Any manifests or tools relying on namespace defaulting will be affected by this.
>
> **`POD_NAMESPACE` environment variable**
>
> If the `POD_NAMESPACE` environment variable is set, cli operations on namespaced resources
> will default to the variable value. For example, if the variable is set to `seattle`,
> `kubectl get pods` would return pods in the `seattle` namespace. This is because pods are
> a namespaced resource, and no namespace was provided in the command. Review the output
> of `kubectl api-resources` to determine if a resource is namespaced.
>
> Explicit use of `--namespace <value>` overrides this behavior.

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `taint-dedicated-node`

**Question** (en, concept): How can I keep ordinary pods from being scheduled on a particular node?

**Reference answer:** Taint the node, e.g. `kubectl taint nodes <node> key1=value1:NoSchedule`. Pods without a matching toleration won't be scheduled there. A toleration allows scheduling on the node but doesn't guarantee it.

**System answer:**

> You can mark a Node as unschedulable, which prevents the scheduler from placing new pods onto that Node [1]. This action does not affect existing Pods on the Node [1].
>
> To mark a Node unschedulable, run:
> ```shell
> kubectl cordon $NODENAME
> ```
> [1]

**Sources the model was given:**

**[1]** `concepts/architecture/nodes.md`, *Nodes > Management > Manual Node administration* **(cited)**

> You can create and modify Node objects using
> kubectl.
>
> When you want to create Node objects manually, set the kubelet flag `--register-node=false`.
>
> You can modify Node objects regardless of the setting of `--register-node`.
> For example, you can set labels on an existing Node or mark it unschedulable.
>
> You can set optional node role(s) for nodes by adding one or more `node-role.kubernetes.io/<role>: <role>` labels to the node where characters of `<role>`
> are limited by the syntax rules for labels.
>
> Kubernetes ignores the label value for node roles; by convention, you can set it to the same string you used for the node role in the label key.
>
> You can use labels on Nodes in conjunction with node selectors on Pods to control
> scheduling. For example, you can constrain a Pod to only be eligible to run on
> a subset of the available nodes.
>
> Marking a node as unschedulable prevents the scheduler from placing new pods onto
> that Node but does not affect existing Pods on the Node. This is useful as a
> preparatory step before a node reboot or other maintenance.
>
> To mark a Node unschedulable, run:
>
> ```shell
> kubectl cordon $NODENAME
> ```
>
> See Safely Drain a Node
> for more details.

**[2]** `concepts/scheduling-eviction/pod-priority-preemption.md`, *Pod Priority and Preemption > Preemption > Limitations of preemption > Inter-Pod affinity on lower-priority Pods*

> A Node is considered for preemption only when the answer to this question is
> yes: "If all the Pods with lower priority than the pending Pod are removed from
> the Node, can the pending Pod be scheduled on the Node?"
>
> Preemption does not necessarily remove all lower-priority
> Pods. If the pending Pod can be scheduled by removing fewer than all
> lower-priority Pods, then only a portion of the lower-priority Pods are removed.
> Even so, the answer to the preceding question must be yes. If the answer is no,
> the Node is not considered for preemption.
>
> If a pending Pod has inter-pod affinity
> to one or more of the lower-priority Pods on the Node, the inter-Pod affinity
> rule cannot be satisfied in the absence of those lower-priority Pods. In this case,
> the scheduler does not preempt any Pods on the Node. Instead, it looks for another
> Node. The scheduler might find a suitable Node or it might not. There is no
> guarantee that the pending Pod can be scheduled.
>
> Our recommended solution for this problem is to create inter-Pod affinity only
> towards equal or higher priority Pods.

**[3]** `concepts/scheduling-eviction/pod-priority-preemption.md`, *Pod Priority and Preemption > Preemption > User exposed information*

> When Pod P preempts one or more Pods on Node N, `nominatedNodeName` field of Pod
> P's status is set to the name of Node N. This field helps the scheduler track
> resources reserved for Pod P and also gives users information about preemptions
> in their clusters.
>
> Please note that Pod P is not necessarily scheduled to the "nominated Node".
> The scheduler always tries the "nominated Node" before iterating over any other nodes.
> After victim Pods are preempted, they get their graceful termination period. If
> another node becomes available while scheduler is waiting for the victim Pods to
> terminate, scheduler may use the other node to schedule Pod P. As a result
> `nominatedNodeName` and `nodeName` of Pod spec are not always the same. Also, if
> the scheduler preempts Pods on Node N, but then a higher priority Pod than Pod P
> arrives, the scheduler may give Node N to the new higher priority Pod. In such a
> case, scheduler clears `nominatedNodeName` of Pod P. By doing this, scheduler
> makes Pod P eligible to preempt Pods on another Node.

**[4]** `concepts/scheduling-eviction/pod-priority-preemption.md`, *Pod Priority and Preemption > Preemption > Limitations of preemption > Cross node preemption*

> Suppose a Node N is being considered for preemption so that a pending Pod P can
> be scheduled on N. P might become feasible on N only if a Pod on another Node is
> preempted. Here's an example:
>
> *   Pod P is being considered for Node N.
> *   Pod Q is running on another Node in the same Zone as Node N.
> *   Pod P has Zone-wide anti-affinity with Pod Q (`topologyKey:
>     topology.kubernetes.io/zone`).
> *   There are no other cases of anti-affinity between Pod P and other Pods in
>     the Zone.
> *   In order to schedule Pod P on Node N, Pod Q can be preempted, but scheduler
>     does not perform cross-node preemption. So, Pod P will be deemed
>     unschedulable on Node N.
>
> If Pod Q were removed from its Node, the Pod anti-affinity violation would be
> gone, and Pod P could possibly be scheduled on Node N.
>
> We may consider adding cross Node preemption in future versions if there is
> enough demand and if we find an algorithm with reasonable performance.

**[5]** `concepts/containers/runtime-class.md`, *Runtime Class > Scheduling*

> By specifying the `scheduling` field for a RuntimeClass, you can set constraints to
> ensure that Pods running with this RuntimeClass are scheduled to nodes that support it.
> If `scheduling` is not set, this RuntimeClass is assumed to be supported by all nodes.
>
> To ensure pods land on nodes supporting a specific RuntimeClass, that set of nodes should have a
> common label which is then selected by the `runtimeclass.scheduling.nodeSelector` field. The
> RuntimeClass's nodeSelector is merged with the pod's nodeSelector in admission, effectively taking
> the intersection of the set of nodes selected by each. If there is a conflict, the pod will be
> rejected.
>
> If the supported nodes are tainted to prevent other RuntimeClass pods from running on the node, you
> can add `tolerations` to the RuntimeClass. As with the `nodeSelector`, the tolerations are merged
> with the pod's tolerations in admission, effectively taking the union of the set of nodes tolerated
> by each.
>
> To learn more about configuring the node selector and tolerations, see
> Assigning Pods to Nodes.

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `node-selector-ssd`

**Question** (en, task): How do I make a pod run only on nodes that have an SSD?

**Reference answer:** Attach a label to the nodes that have an SSD (labels can be attached manually, e.g. `disktype=ssd`) and add a matching `nodeSelector`, or a node affinity rule of type `requiredDuringSchedulingIgnoredDuringExecution`, to the Pod spec. A `preferredDuringSchedulingIgnoredDuringExecution` rule is only a preference: if no matching node is available, the Pod is still scheduled.

**System answer:**

> You can constrain a Pod to run on particular nodes [4]. The recommended approaches use label selectors [4]. To ensure a Pod ends up on a node with an SSD attached to it, you can use the `nodeSelector` field matching against node labels [4]. Labels on Nodes can be used with node selectors on Pods to control scheduling [1].

**Sources the model was given:**

**[1]** `concepts/architecture/nodes.md`, *Nodes > Management > Manual Node administration* **(cited)**

> You can create and modify Node objects using
> kubectl.
>
> When you want to create Node objects manually, set the kubelet flag `--register-node=false`.
>
> You can modify Node objects regardless of the setting of `--register-node`.
> For example, you can set labels on an existing Node or mark it unschedulable.
>
> You can set optional node role(s) for nodes by adding one or more `node-role.kubernetes.io/<role>: <role>` labels to the node where characters of `<role>`
> are limited by the syntax rules for labels.
>
> Kubernetes ignores the label value for node roles; by convention, you can set it to the same string you used for the node role in the label key.
>
> You can use labels on Nodes in conjunction with node selectors on Pods to control
> scheduling. For example, you can constrain a Pod to only be eligible to run on
> a subset of the available nodes.
>
> Marking a node as unschedulable prevents the scheduler from placing new pods onto
> that Node but does not affect existing Pods on the Node. This is useful as a
> preparatory step before a node reboot or other maintenance.
>
> To mark a Node unschedulable, run:
>
> ```shell
> kubectl cordon $NODENAME
> ```
>
> See Safely Drain a Node
> for more details.

**[2]** `concepts/workloads/pods/pod-lifecycle.md`, *Pod Lifecycle > Pod lifetime*

> Whilst a Pod is running, the kubelet is able to restart containers to handle some
> kind of faults. Within a Pod, Kubernetes tracks different container
> states and determines what action to take to make the Pod
> healthy again.
>
> In the Kubernetes API, Pods have both a specification and an actual status. The
> status for a Pod object consists of a set of Pod conditions.
> You can also inject custom readiness information into the
> condition data for a Pod, if that is useful to your application.
>
> Pods are only scheduled once in their lifetime;
> assigning a Pod to a specific node is called _binding_, and the process of selecting
> which node to use is called _scheduling_.
> Once a Pod has been scheduled and is bound to a node, Kubernetes tries
> to run that Pod on the node. The Pod runs on that node until it stops, or until the Pod
> is terminated; if Kubernetes isn't able to start the Pod on the selected
> node (for example, if the node crashes before the Pod starts), then that particular Pod
> never starts.

**[3]** `tasks/debug/debug-application/debug-running-pod.md`, *Debug Running Pods > Debugging via a shell on the node {#node-shell-session}*

> If none of these approaches work, you can find the Node on which the Pod is
> running and create a Pod running on the Node. To create
> an interactive shell on a Node using `kubectl debug`, run:
>
> ```shell
> kubectl debug node/mynode -it --image=ubuntu
> ```
>
> ```
> Creating debugging pod node-debugger-mynode-pdx84 with container debugger on node mynode.
> If you don't see a command prompt, try pressing enter.
> root@ek8s:/#
> ```
>
> When creating a debugging session on a node, keep in mind that:
>
> * `kubectl debug` automatically generates the name of the new Pod based on
>   the name of the Node.
> * The root filesystem of the Node will be mounted at `/host`.
> * The container runs in the host IPC, Network, and PID namespaces, although
>   the pod isn't privileged, so reading some process information may fail,
>   and `chroot /host` may fail.
> * If you need a privileged pod, create it manually or use the `--profile=sysadmin` flag.
>
> Don't forget to clean up the debugging Pod when you're finished with it:
>
> ```shell
> kubectl delete pod node-debugger-mynode-pdx84
> ```

**[4]** `concepts/scheduling-eviction/assign-pod-node.md`, *Assigning Pods to Nodes* **(cited)**

> You can constrain a Pod so that it is
> _restricted_ to run on particular node(s),
> or to _prefer_ to run on particular nodes.
> There are several ways to do this and the recommended approaches all use
> label selectors to facilitate the selection.
> Often, you do not need to set any such constraints; the
> scheduler will automatically do a reasonable placement
> (for example, spreading your Pods across nodes so as not place Pods on a node with insufficient free resources).
> However, there are some circumstances where you may want to control which node
> the Pod deploys to, for example, to ensure that a Pod ends up on a node with an SSD attached to it,
> or to co-locate Pods from two different services that communicate a lot into the same availability zone.
>
> You can use any of the following methods to choose where Kubernetes schedules
> specific Pods:
>
> - nodeSelector field matching against node labels
> - Affinity and anti-affinity
> - nodeName field
> - Pod topology spread constraints

**[5]** `concepts/workloads/pods/_index.md`, *Pods > Working with Pods*

> You'll rarely create individual Pods directly in Kubernetes—even singleton Pods. This
> is because Pods are designed as relatively ephemeral, disposable entities. When
> a Pod gets created (directly by you, or indirectly by a
> controller), the new Pod is
> scheduled to run on a  in your cluster.
> The Pod remains on that node until the Pod finishes execution, the Pod object is deleted,
> the Pod is *evicted* for lack of resources, or the node fails.
>
> Restarting a container in a Pod should not be confused with restarting a Pod. A Pod
> is not a process, but an environment for running container(s). A Pod persists until
> it is deleted.
>
> The name of a Pod must be a valid
> DNS subdomain
> value, but this can produce unexpected results for the Pod hostname.  For best compatibility,
> the name should follow the more restrictive rules for a
> DNS label.

**Labels** (tick one box per line):
- Supported by the sources: [ ] yes [ ] no
- Correct answer to the question: [ ] yes [ ] no

**Notes:**


---

### `hpa-cpu`

**Question** (en, concept): How can Kubernetes add more pods automatically when CPU usage goes up?

**Reference answer:** A HorizontalPodAutoscaler: a control loop that runs intermittently, compares observed metrics such as average CPU utilization with the target you set, and adjusts the number of replicas.

**System answer:** *refused*

> I couldn't find the answer in the documentation.

**Sources the model was given:**

**[1]** `tasks/configure-pod-container/assign-pod-level-resources.md`, *Assign Pod-level CPU and memory resources > Create a pod with CPU requests and limits at pod-level*

> Use `kubectl top` to fetch the metrics for the Pod:
>
> ```shell
> kubectl top pod cpu-demo --namespace=pod-resources-example
> ```
>
> This example output shows that the Pod is using 974 milliCPU, which is
> slightly less than the limit of 1 CPU specified in the Pod configuration.
>
> ```
> NAME                        CPU(cores)   MEMORY(bytes)
> cpu-demo                    974m         <something>
> ```
>
> Recall that by setting `-cpu "2"`, you configured the Container to attempt to use 2
> CPUs, but the Container is only being allowed to use about 1 CPU. The container's
> CPU use is being throttled, because the container is attempting to use more CPU
> resources than the Pod CPU limit.

**[2]** `tasks/administer-cluster/manage-resources/cpu-constraint-namespace.md`, *Configure Minimum and Maximum CPU Constraints for a Namespace > Create a LimitRange and a Pod*

> Here's a manifest for an example LimitRange:
>
> Create the LimitRange:
>
> ```shell
> kubectl apply -f https://k8s.io/examples/admin/resource/cpu-constraints.yaml --namespace=constraints-cpu-example
> ```
>
> View detailed information about the LimitRange:
>
> ```shell
> kubectl get limitrange cpu-min-max-demo-lr --output=yaml --namespace=constraints-cpu-example
> ```
>
> The output shows the minimum and maximum CPU constraints as expected. But
> notice that even though you didn't specify default values in the configuration
> file for the LimitRange, they were created automatically.
>
> ```yaml
> limits:
> - default:
>     cpu: 800m
>   defaultRequest:
>     cpu: 800m
>   max:
>     cpu: 800m
>   min:
>     cpu: 200m
>   type: Container
> ```
>
> Now whenever you create a Pod in the constraints-cpu-example namespace (or some other client
> of the Kubernetes API creates an equivalent Pod), Kubernetes performs these steps:
>
> * If any container in that Pod does not specify its own CPU request and limit, the control plane
>   assigns the default CPU request and limit to that container.
>
> * Verify that every container in that Pod specifies a CPU request that is greater than or equal to 200 millicpu.

**[3]** `tasks/configure-pod-container/assign-cpu-resource.md`, *Assign CPU Resources to Containers and Pods > Specify a CPU request and a CPU limit*

> ```shell
> kubectl top pod cpu-demo --namespace=cpu-example
> ```
>
> This example output shows that the Pod is using 974 milliCPU, which is
> slightly less than the limit of 1 CPU specified in the Pod configuration.
>
> ```
> NAME                        CPU(cores)   MEMORY(bytes)
> cpu-demo                    974m         <something>
> ```
>
> Recall that by setting `-cpu "2"`, you configured the Container to attempt to use 2 CPUs, but the Container is only being allowed to use about 1 CPU. The container's CPU use is being throttled, because the container is attempting to use more CPU resources than its limit.
>
> Another possible explanation for the CPU use being below 1.0 is that the Node might not have
> enough CPU resources available. Recall that the prerequisites for this exercise require your cluster to have at least 1 CPU available for use. If your Container runs on a Node that has only 1 CPU, the Container cannot use more than 1 CPU regardless of the CPU limit specified for the Container.

**[4]** `tasks/configure-pod-container/assign-cpu-resource.md`, *Assign CPU Resources to Containers and Pods > Specify a CPU request that is too big for your Nodes*

> CPU requests and limits are associated with Containers, but it is useful to think
> of a Pod as having a CPU request and limit. The CPU request for a Pod is the sum
> of the CPU requests for all the Containers in the Pod. Likewise, the CPU limit for
> a Pod is the sum of the CPU limits for all the Containers in the Pod.
>
> Pod scheduling is based on requests. A Pod is scheduled to run on a Node only if
> the Node has enough CPU resources available to satisfy the Pod CPU request.
>
> In this exercise, you create a Pod that has a CPU request so big that it exceeds
> the capacity of any Node in your cluster. Here is the configuration file for a Pod
> that has one Container. The Container requests 100 CPU, which is likely to exceed the
> capacity of any Node in your cluster.
>
> Create the Pod:
>
> ```shell
> kubectl apply -f https://k8s.io/examples/pods/resource/cpu-request-limit-2.yaml --namespace=cpu-example
> ```
>
> View the Pod status:
>
> ```shell
> kubectl get pod cpu-demo-2 --namespace=cpu-example
> ```
>
> The output shows that the Pod status is Pending. That is, the Pod has not been
> scheduled to run on any Node, and it will remain in the Pending state indefinitely:

**[5]** `tasks/configure-pod-container/assign-memory-resource.md`, *Assign Memory Resources to Containers and Pods > Clean up > For app developers*

> * Assign CPU Resources to Containers and Pods
>
> * Assign Pod-level CPU and memory resources
>
> * Configure Quality of Service for Pods
>
> * Resize CPU and Memory Resources assigned to Containers

**Labels** (tick one box per line):
- Refusal justified (the answer isn't in the sources): [ ] yes [ ] no

**Notes:**


---
